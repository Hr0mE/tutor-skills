#!/usr/bin/env python3
"""
find_in_book.py — search the whole corpus, reporting the printed page.

    find_in_book.py "Arzela"
    find_in_book.py "normal famil\\w+" --book Shabat
    find_in_book.py "Peano" --canon --context 2

Searches raw/books/.ocr/*.txt — the single text index of the corpus (OCR for
scans, the native text layer for ordinary PDFs; `make ocr` produces both).

Prints the work, the printed page and the fragment. The printed page is computed
from the offset in <slug>.meta.json, and is exactly what belongs in a source's
`page` field on a wiki page.

WARNING: a hit is a navigation aid, not a ready quotation. Before moving any
wording into the wiki, open the page as an image and check it by eye. OCR mangles
indices, quantifiers and Greek letters.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from _tutor import project_root  # noqa: E402

ROOT = project_root()
OCRDIR = ROOT / "raw" / "books" / ".ocr"
BOOKS_INDEX = ROOT / "raw" / "books" / "index.md"
# Written as PDF-PAGE; PDF-СТРАНИЦА is accepted too, so an index built by an
# earlier version keeps working instead of silently yielding no pages.
PAGE_RE = re.compile(r"^===== PDF-(?:PAGE|СТРАНИЦА) (\d+) =====$", re.M)


def canon_slugs() -> set[str]:
    """Stems of the works the manifest marks as canon.

    Read from raw/books/manifest.yaml rather than parsed back out of the
    generated index.md — the manifest is the source of truth, and a heading
    heuristic over generated prose breaks the moment the wording changes.
    """
    manifest = ROOT / "raw" / "books" / "manifest.yaml"
    if not manifest.exists():
        return set()
    import yaml
    data = yaml.safe_load(manifest.read_text(encoding="utf-8")) or {}
    return {Path(b["file"]).stem for b in (data.get("books") or [])
            if b.get("relevance") == "canon" and b.get("file")}


def pages_of(txt: Path):
    parts = PAGE_RE.split(txt.read_text(encoding="utf-8", errors="replace"))
    for i in range(1, len(parts) - 1, 2):
        yield int(parts[i]), parts[i + 1]


def offset_fn(slug: str):
    """Return a function "PDF page -> printed page", or None.

    One global offset does not fit every book: a volume bound from several parts
    has its numbering jump in the middle (one work in the reference corpus runs
    at -5 in part one and -4 in part two). Piecewise ranges are therefore
    supported. When no offset is known we return None, and the search honestly
    prints the PDF page only.
    """
    meta_p = OCRDIR / f"{slug}.meta.json"
    if not meta_p.exists():
        return None
    try:
        meta = json.loads(meta_p.read_text(encoding="utf-8"))
    except Exception:
        return None
    off = meta.get("offset")
    if off is not None:
        return lambda n: n + off
    ranges = meta.get("offset_ranges") or []
    if not ranges:
        return None

    def by_range(n: int):
        for lo, hi, delta in ranges:
            if lo <= n <= hi:
                return n + delta
        return None
    return by_range


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pattern", help="regular expression (case-insensitive)")
    ap.add_argument("--book", help="restrict to works whose filename contains this substring")
    ap.add_argument("--canon", action="store_true", help="only works marked as canon in the catalogue")
    ap.add_argument("--context", type=int, default=1, help="lines of context around each match")
    ap.add_argument("--max", type=int, default=40, help="maximum number of matches")
    a = ap.parse_args()

    if not OCRDIR.exists():
        print("The text index is empty. Run `make ocr` first.", file=sys.stderr)
        return 1

    rx = re.compile(a.pattern, re.I)
    allowed = canon_slugs() if a.canon else None
    found = 0

    for txt in sorted(OCRDIR.glob("*.txt")):
        slug = txt.stem
        if a.book and a.book.lower() not in slug.lower():
            continue
        if allowed is not None and slug not in allowed:
            continue
        to_printed = offset_fn(slug)
        printed_header = False
        for pdf_page, body in pages_of(txt):
            lines = body.splitlines()
            for i, line in enumerate(lines):
                if not rx.search(line):
                    continue
                if found >= a.max:
                    print(f"\n… truncated at {a.max} matches; narrow the query")
                    return 0
                if not printed_header:
                    print(f"\n━━━ {slug} ━━━")
                    printed_header = True
                lo = max(0, i - a.context)
                hi = min(len(lines), i + a.context + 1)
                snippet = " ".join(" ".join(lines[lo:hi]).split())[:300]
                printed = to_printed(pdf_page) if to_printed else None
                label = f"p. {printed:<4}" if printed is not None else "p.   ?  "
                print(f"  {label} (PDF {pdf_page:<4}) {snippet}")
                found += 1

    if not found:
        print("Nothing found.")
    else:
        print(f"\nMatches: {found}. "
              "Before citing, check the wording against the page image.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
