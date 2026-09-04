#!/usr/bin/env python3
"""
ocr_book.py — OCR a scanned book into a text layer, for NAVIGATION.

    ocr_book.py raw/books/<file>.pdf [--dpi 300] [--jobs N]
    ocr_book.py --all          # every scan in raw/books, in priority order
    ocr_book.py --status       # what is already done

WARNING — the load-bearing rule of this whole capability:
    OCR output is fit ONLY for search and navigation (finding a section, a
    theorem number, a problem number). Tesseract systematically mangles indices,
    quantifiers and Greek letters. Any wording that enters the wiki as a
    quotation must be checked against the page IMAGE. Copying formulas out of
    .ocr/*.txt is forbidden.

Output format: raw/books/.ocr/<slug>.txt with markers
    ===== PDF-PAGE N =====
where N is the 1-based PDF page number, matching pdftoppm's numbering.
The correspondence "PDF page <-> printed page" is determined automatically
and written to raw/books/.ocr/<slug>.meta.json (field `offset`: printed = pdf + offset).

The run is resumable: re-running continues from the last completed page.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from _tutor import project_root  # noqa: E402

ROOT = project_root()
BOOKS = ROOT / "raw" / "books"
OCRDIR = BOOKS / ".ocr"
BATCH_FACTOR = 3   # pages per worker in one batch
# Written as PDF-PAGE; PDF-СТРАНИЦА is accepted too, so an index built by an
# earlier version keeps working instead of silently yielding no pages.
PAGE_RE = re.compile(r"^===== PDF-(?:PAGE|СТРАНИЦА) (\d+) =====$", re.M)

# Priority order: the domain's load-bearing sources are indexed first, so work
# can start without waiting for the whole run. The list comes from the domain
# layer (.tutor/config.yaml, corpus.priority), not from code: the core has no
# idea which of your books matters most.
from _tutor import load_config, cfg  # noqa: E402

PRIORITY = cfg(load_config(ROOT), "corpus.priority", []) or []


def has_text_layer(pdf: Path) -> bool:
    """Does the WHOLE book have a usable text layer.

    Two traps, both hit on a real corpus:
      1. The layer sometimes covers only the first pages (title, contents) and
         the rest is a clean scan. Testing the first 40 pages declared such books
         text-bearing, and three of them slipped past OCR entirely. So we sample
         pages spread across the whole volume.
      2. The layer sometimes has broken digit encoding: letters extract, digits
         vanish. For a book whose theorem and formula numbers get cited, that is
         worse than an honest scan. So we also look at the digit ratio.
    """
    try:
        total = page_count(pdf)
    except Exception:
        return False
    probes = sorted({max(1, round(total * f)) for f in
                     (0.05, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.75, 0.85, 0.95)})
    with_text = 0
    digits = letters = 0
    for n in probes:
        try:
            out = subprocess.run(["pdftotext", "-f", str(n), "-l", str(n), str(pdf), "-"],
                                 capture_output=True, text=True, timeout=60).stdout
        except Exception:
            continue
        if len("".join(out.split())) > 300:
            with_text += 1
        digits += sum(c.isdigit() for c in out)
        letters += sum(c.isalpha() for c in out)

    if with_text < len(probes) * 0.7:
        return False
    # Threshold calibrated on a real corpus: healthy mathematics texts run at a
    # digit ratio of 0.034-0.045, while one edition with broken digit encoding sat
    # at 0.011. A cut at 0.02 separates them with room to spare. A stricter cut
    # would reject sound books and send them to OCR that is strictly worse than
    # their own text layer.
    if letters > 2000 and digits / letters < 0.02:
        print(f"⚠ {pdf.name}: the text layer is losing digits "
              f"({digits}/{letters} = {digits/letters:.3f}) — sending to OCR", flush=True)
        return False
    return True


def page_count(pdf: Path) -> int:
    out = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    for line in out.splitlines():
        if line.startswith("Pages"):
            return int(line.split()[1])
    raise RuntimeError(f"could not determine the page count: {pdf}")


def done_pages(txt: Path) -> int:
    """How many pages are already in the file (the last consecutive one)."""
    if not txt.exists():
        return 0
    nums = [int(m) for m in PAGE_RE.findall(txt.read_text(encoding="utf-8", errors="replace"))]
    return max(nums) if nums else 0


def extract_text_layer(pdf: Path) -> None:
    """For books with a native text layer — extraction without OCR, same format.

    This is what makes .ocr/ a single search index over the whole corpus, scans
    and ordinary PDFs alike. pdftotext separates pages with a form feed (\f), so
    that is where we cut.
    """
    slug = pdf.stem
    txt = OCRDIR / f"{slug}.txt"
    total = page_count(pdf)
    if done_pages(txt) >= total:
        print(f"✓ already done: {slug} ({total} pp.)")
        return
    raw = subprocess.run(["pdftotext", str(pdf), "-"],
                         capture_output=True, text=True).stdout
    pages = raw.split("\f")
    with txt.open("w", encoding="utf-8") as out:
        for i, body in enumerate(pages[:total], start=1):
            out.write(f"\n===== PDF-PAGE {i} =====\n")
            out.write(body.rstrip() + "\n")
    meta = detect_offset(txt)
    meta.update(source=pdf.name, pages=total, mode="native-text-layer",
                warning="Native text layer, not OCR. Formulas must still be checked against the page image.")
    (OCRDIR / f"{slug}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"✓ {slug}: {total} pp. from the text layer | offset: {meta['offset']} "
          f"(confidence {meta['confidence']})", flush=True)


def render_and_ocr(pdf: Path, page: int, dpi: int, lang: str, tmp: Path) -> tuple[int, str]:
    """Render one page and OCR it immediately. Render and OCR run in the same
    worker thread, so the whole pipeline parallelises by page with no narrow
    space than a sequential pdftoppm run."""
    stem = tmp / f"p{page:05d}"
    subprocess.run(["pdftoppm", "-f", str(page), "-l", str(page), "-r", str(dpi),
                    "-gray", "-png", "-singlefile", str(pdf), str(stem)],
                   check=True, capture_output=True)
    png = stem.with_suffix(".png")
    try:
        # OMP_THREAD_LIMIT=1 is mandatory: tesseract's own threading, with N
        # workers on top, thrashes the cores. Measured on a real corpus:
        # 4.2 s/page with the limit against 14.9 s without it.
        env = {**os.environ, "OMP_THREAD_LIMIT": "1"}
        res = subprocess.run(
            ["tesseract", str(png), "-", "-l", lang, "--oem", "1", "--psm", "3",
             "-c", "preserve_interword_spaces=1"],
            capture_output=True, text=True, env=env)
        return page, res.stdout
    finally:
        png.unlink(missing_ok=True)


def detect_offset(txt: Path) -> dict:
    """Determine the offset between the PDF page number and the printed one.

    A folio nearly always sits on a line of its own, or at the edge of a short
    running-head line. Numbers from "fat" lines (formulas, body text) are
    therefore ignored: otherwise formula numbers enter the ballot and produce a
    confident wrong answer. Below the confidence threshold we honestly return
    None — a missing number beats an invented one.
    """
    MIN_CONFIDENCE = 0.30
    raw = txt.read_text(encoding="utf-8", errors="replace")
    parts = PAGE_RE.split(raw)
    strong: Counter = Counter()   # the number occupies the whole line
    weak: Counter = Counter()     # a number at the edge of a short line (running head)
    checked = 0

    for i in range(1, len(parts) - 1, 2):
        pdf_no = int(parts[i])
        lines = [ln.strip() for ln in parts[i + 1].splitlines() if ln.strip()]
        if not lines:
            continue
        checked += 1
        for line in (lines[0], lines[-1]):
            if re.fullmatch(r"\d{1,4}", line):
                printed = int(line)
                if 0 < printed < 3000:
                    strong[printed - pdf_no] += 1
                continue
            if len(line) > 70:            # a long line is body text, not a running head
                continue
            for m in (re.match(r"^(\d{1,4})\b", line), re.search(r"\b(\d{1,4})$", line)):
                if m:
                    printed = int(m.group(1))
                    if 0 < printed < 3000:
                        weak[printed - pdf_no] += 1

    votes = strong if sum(strong.values()) >= max(5, checked * 0.15) else strong + weak
    kind = "folio on its own line" if votes is strong else "number at the edge of a running head"
    if not votes:
        return {"offset": None, "confidence": 0.0, "checked": checked,
                "note": "page numbers not recognised"}
    offset, hits = votes.most_common(1)[0]
    conf = round(hits / max(checked, 1), 3)
    if conf < MIN_CONFIDENCE:
        return {"offset": None, "confidence": conf, "checked": checked,
                "note": f"offset not confidently determined (best candidate {offset}, "
                        f"confidence {conf}) — verify the printed page by eye"}
    return {"offset": offset, "confidence": conf, "checked": checked, "basis": kind,
            "note": "printed = pdf + offset. Verify by eye before citing."}


def detect_offset_ranges(txt: Path, max_shift: int = 40, window: int = 8,
                         min_len: int = 10) -> list[list[int]]:
    """Piecewise numbering offset: [[from_pdf_page, to_pdf_page, offset], ...].

    Needed where a volume is bound from several parts and the printed numbering
    jumps partway through (one work in the reference corpus runs at -5 in part
    one and -4 in part two, where a single offset is simply wrong). For each page
    we take a plausible folio candidate, smooth by windowed mode, and merge equal
    stretches.
    """
    parts = PAGE_RE.split(txt.read_text(encoding="utf-8", errors="replace"))
    seq: list[tuple[int, int]] = []
    for i in range(1, len(parts) - 1, 2):
        n = int(parts[i])
        lines = [ln.strip() for ln in parts[i + 1].splitlines() if ln.strip()]
        if not lines:
            continue
        for line in (lines[0], lines[-1]):
            m = re.match(r"^(\d{1,4})\b", line) or re.search(r"\b(\d{1,4})$", line)
            if not m:
                continue
            shift = int(m.group(1)) - n
            if abs(shift) <= max_shift:
                seq.append((n, shift))
                break
    if not seq:
        return []

    smoothed = []
    for n, _ in seq:
        win = [o for m, o in seq if n - window <= m <= n + window]
        smoothed.append((n, Counter(win).most_common(1)[0][0]))

    ranges: list[list[int]] = []
    for n, off in smoothed:
        if ranges and ranges[-1][2] == off:
            ranges[-1][1] = n
        else:
            ranges.append([n, n, off])
    return [r for r in ranges if r[1] - r[0] + 1 >= min_len]


def ocr_book(pdf: Path, dpi: int, jobs: int, lang: str = "rus") -> None:
    OCRDIR.mkdir(parents=True, exist_ok=True)
    slug = pdf.stem
    txt = OCRDIR / f"{slug}.txt"
    total = page_count(pdf)
    start = done_pages(txt) + 1
    if start > total:
        print(f"✓ already done: {slug} ({total} pp.)")
        return
    print(f"▶ OCR {slug}: pages {start}–{total} (dpi={dpi}, threads={jobs})", flush=True)

    tmp = Path(tempfile.mkdtemp(prefix="ocr_", dir="/tmp"))
    t0 = time.monotonic()
    try:
        with txt.open("a", encoding="utf-8") as out, ThreadPoolExecutor(max_workers=jobs) as ex:
            batch = jobs * BATCH_FACTOR
            for lo in range(start, total + 1, batch):
                hi = min(lo + batch - 1, total)
                results = list(ex.map(
                    lambda n: render_and_ocr(pdf, n, dpi, lang, tmp), range(lo, hi + 1)))
                for n, text in sorted(results):          # write strictly in order
                    out.write(f"\n===== PDF-PAGE {n} =====\n")
                    out.write(text.rstrip() + "\n")
                out.flush()
                done = hi - start + 1
                rate = done / max(time.monotonic() - t0, 1e-9)
                eta = (total - hi) / rate if rate else 0
                print(f"  {slug}: {hi}/{total} ({hi * 100 // total}%) "
                      f"| {rate * 60:.0f} pp/min | ~{eta / 60:.0f} min left", flush=True)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    meta = detect_offset(txt)
    meta.update(source=pdf.name, pages=total, dpi=dpi, lang=lang,
                warning="Navigation only. Read formulas off the page image, never off this text.")
    (OCRDIR / f"{slug}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    off = meta["offset"]
    print(f"✓ {slug}: {total} pp. | printed-page offset: "
          f"{off if off is not None else 'undetermined'} "
          f"(confidence {meta['confidence']})", flush=True)


def scans() -> list[Path]:
    """Every scan in raw/books, in priority order."""
    allpdf = sorted(p for p in BOOKS.glob("*.pdf"))
    found = [p for p in allpdf if not has_text_layer(p)]
    order = {name: i for i, name in enumerate(PRIORITY)}
    return sorted(found, key=lambda p: (order.get(p.name, 99), p.name))


def status() -> None:
    rows = []
    for pdf in sorted(BOOKS.glob("*.pdf")):
        txt = OCRDIR / f"{pdf.stem}.txt"
        if not txt.exists():
            continue
        rows.append((pdf.stem, done_pages(txt), page_count(pdf)))
    if not rows:
        print("OCR has not been run yet.")
        return
    for slug, d, t in rows:
        mark = "✓" if d >= t else "…"
        print(f"{mark} {d:>4}/{t:<4} {slug}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdf", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--dpi", type=int, default=300)
    ap.add_argument("--jobs", type=int, default=max(1, (os.cpu_count() or 4) - 1))
    a = ap.parse_args()

    if a.status:
        status()
        return
    if a.all:
        native = [p for p in sorted(BOOKS.glob("*.pdf")) if has_text_layer(p)]
        print(f"Native text layer, no OCR needed: {len(native)} work(s)")
        for p in native:
            extract_text_layer(p)
        todo = scans()
        print("OCR queue:", *[f"  {i+1}. {p.name}" for i, p in enumerate(todo)], sep="\n")
        for p in todo:
            ocr_book(p, a.dpi, a.jobs)
        return
    if not a.pdf:
        ap.error("give a PDF, or --all, or --status")
    ocr_book(Path(a.pdf).resolve(), a.dpi, a.jobs)


if __name__ == "__main__":
    main()
