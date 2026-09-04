#!/usr/bin/env python3
"""
catalog.py — generate raw/books/index.md from the corpus manifest.

    catalog.py                # regenerate the catalogue
    catalog.py --rename       # also apply `rename_from` entries
    catalog.py --init         # draft a manifest from what is on disk

The manifest lives in the **project** at `raw/books/manifest.yaml`, never in this
script. Which books matter, and what each one arbitrates, is exactly the kind of
judgement the domain layer exists to hold.

    books:
      - file: Kolmogorov-Fomin_Elements-of-the-theory-of-functions_1976.pdf
        author: "Kolmogorov A. N., Fomin S. V."
        topic: "Functional analysis"
        relevance: canon          # canon | adjacent | future
        note: "Load-bearing source for the compactness track."
        rename_from: "KolmogorovFomin_scan_1976.pdf"   # optional, only with --rename

This script never deletes a file. Renaming happens only under `--rename`, and
only when the target name is free.
"""
from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
from _tutor import project_root  # noqa: E402

BOOKS = project_root() / "raw" / "books"
MANIFEST = BOOKS / "manifest.yaml"

REL_LABEL = {"canon": "🟢 canon", "adjacent": "🟡 adjacent", "future": "⚪ future"}
REL_ORDER = {"canon": 0, "adjacent": 1, "future": 2}


def load_manifest() -> list[dict]:
    if not MANIFEST.exists():
        sys.exit(f"No manifest at {MANIFEST}.\n"
                 f"Run `catalog.py --init` to draft one from the files on disk, then "
                 f"fill in author, topic and relevance by hand — the script cannot "
                 f"know which of your books arbitrates what.")
    data = yaml.safe_load(MANIFEST.read_text(encoding="utf-8")) or {}
    books = data.get("books") or []
    for b in books:
        if "file" not in b:
            sys.exit(f"manifest entry without `file`: {b!r}")
        b.setdefault("relevance", "adjacent")
        if b["relevance"] not in REL_ORDER:
            sys.exit(f"{b['file']}: relevance must be canon | adjacent | future")
    return books


def init_manifest() -> int:
    if MANIFEST.exists():
        sys.exit(f"{MANIFEST} already exists — not overwriting it.")
    found = sorted(f for f in os.listdir(BOOKS)
                   if (BOOKS / f).is_file() and f.lower().endswith((".pdf", ".djvu")))
    if not found:
        sys.exit(f"No PDF or DjVu files in {BOOKS}.")
    lines = ["# Corpus manifest. Hand-edited: relevance and note are judgements, not",
             "# facts a script can derive. `canon` means this work arbitrates",
             "# contradictions in its area.", "", "books:"]
    for f in found:
        lines += [f"  - file: {f!r}", '    author: ""', '    topic: ""',
                  "    relevance: adjacent", '    note: ""']
    MANIFEST.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"* {MANIFEST} — {len(found)} file(s). Fill in author, topic, relevance.")
    return 0


def pages_and_text(name: str):
    """(page count, does it have a usable text layer).

    The text-layer test is imported from ocr_book — the same function that decides
    whether a book goes to OCR. Duplicating the heuristic is how a book ends up
    listed as text-bearing when only its first few leaves are.
    """
    if name.endswith(".djvu"):
        return None, None
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import ocr_book as ob
    full = BOOKS / name
    try:
        pages = ob.page_count(full)
    except Exception:
        pages = None
    try:
        has_text = ob.has_text_layer(full)
    except Exception:
        has_text = None
    return pages, has_text


def slot(name: str, has_text) -> str:
    """State of the book in the search index raw/books/.ocr/."""
    if name.endswith(".djvu"):
        return "— djvu, no converter"
    indexed = (BOOKS / ".ocr" / f"{Path(name).stem}.txt").exists()
    if has_text:
        return "OK text" if indexed else "pending text extraction"
    return "OCR done" if indexed else "scan, needs OCR"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rename", action="store_true",
                    help="apply `rename_from` entries (never overwrites, never deletes)")
    ap.add_argument("--init", action="store_true",
                    help="draft a manifest from the files present")
    a = ap.parse_args()

    BOOKS.mkdir(parents=True, exist_ok=True)
    if a.init:
        return init_manifest()

    books = load_manifest()
    rows = []
    for b in books:
        name, old = b["file"], b.get("rename_from")
        if a.rename and old and (BOOKS / old).exists():
            if (BOOKS / name).exists():
                print(f"!! name already taken, skipped: {name}")
            else:
                os.rename(BOOKS / old, BOOKS / name)
                print(f"-> {name}")
        if not (BOOKS / name).exists():
            print(f"!! missing on disk: {name}")
            continue
        pages, has_text = pages_and_text(name)
        rows.append({**b, "pages": pages, "has_text": has_text})

    listed = {r["file"] for r in rows}
    stray = [f for f in sorted(os.listdir(BOOKS))
             if (BOOKS / f).is_file() and f.lower().endswith((".pdf", ".djvu"))
             and f not in listed]
    if stray:
        print("!! on disk but absent from the manifest:", ", ".join(stray))

    rows.sort(key=lambda r: (REL_ORDER[r["relevance"]], r["file"]))

    out = ["# Corpus catalogue", "",
           "> Index of `raw/books/`. Generated by `make catalog` from "
           "`raw/books/manifest.yaml` — do not edit by hand. `relevance`: "
           "canon (arbitrates its area) - adjacent (may be needed) - future "
           "(groundwork for other tracks). The *layer* column shows the book's "
           "state in the search index; for scans, a quotation must be checked "
           "against the page image, never against the extracted text.", ""]
    for rel in ("canon", "adjacent", "future"):
        sub = [r for r in rows if r["relevance"] == rel]
        if not sub:
            continue
        out += [f"## {REL_LABEL[rel]}", "",
                "| File | Author | Topic | Pp. | Layer | Note |",
                "|---|---|---|---:|---|---|"]
        for r in sub:
            out.append("| `%s` | %s | %s | %s | %s | %s |" % (
                r["file"], r.get("author", ""), r.get("topic", ""),
                r["pages"] or "-", slot(r["file"], r["has_text"]), r.get("note", "")))
        out.append("")

    n_scan = sum(1 for r in rows if r["has_text"] is False)
    n_idx = sum(1 for r in rows
                if (BOOKS / ".ocr" / f"{Path(r['file']).stem}.txt").exists())
    out += ["## Summary", "",
            f"- Sources: **{len(rows)}**",
            f"- Canon: **{sum(1 for r in rows if r['relevance'] == 'canon')}** - "
            f"adjacent: **{sum(1 for r in rows if r['relevance'] == 'adjacent')}** - "
            f"future: **{sum(1 for r in rows if r['relevance'] == 'future')}**",
            f"- Scans without a native text layer: **{n_scan}**",
            f"- In the search index: **{n_idx}** of {len(rows)} "
            f"(search with `make find Q=\"query\"`)",
            f"- Awaiting djvu conversion: "
            f"**{sum(1 for r in rows if r['file'].endswith('.djvu'))}**", ""]

    (BOOKS / "index.md").write_text("\n".join(out), encoding="utf-8")
    print(f"\nindex.md: {len(rows)} source(s), {n_scan} scan(s) needing OCR")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
