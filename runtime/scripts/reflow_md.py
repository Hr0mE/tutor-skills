#!/usr/bin/env python3
"""
reflow_md.py — join soft wraps inside paragraphs: one paragraph = one line.

    reflow_md.py --check          # show what would change
    reflow_md.py                  # apply
    reflow_md.py wiki/index.md    # one file

Why. Obsidian opens notes in Live Preview by default, and Live Preview is an
editor: it shows the document itself, so every line break in the source appears
as a real break mid-sentence. The "Strict line breaks" setting does not help — it
only affects reading mode. The only way to get proper paragraphs in Live Preview
is not to wrap in the source at all, and let the editor wrap to the window.

What is NOT touched: frontmatter, code blocks, display formulas `$$…$$`, tables,
headings, horizontal rules and `<!-- check:… -->` comment lines. List items and
blockquotes are joined within themselves, keeping their prefix.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tutor import project_root  # noqa: E402

ROOT = project_root()

SKIP_DIRS = {".agents", ".venv", ".git", ".obsidian", "raw"}
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+")
QUOTE_RE = re.compile(r"^(\s*>+\s?)(.*)$")
HR_RE = re.compile(r"^\s*([-*_])\1{2,}\s*$")
COMMENT_RE = re.compile(r"^\s*<!--.*-->\s*$")
# An Obsidian callout title: `> [!hint]- Hint`. The `-` suffix collapses the
# block by default, and the whole hint ladder depends on that.
CALLOUT_RE = re.compile(r"^\s*>+\s*\[![a-zA-Z]+\][-+]?")


def verbatim(line: str) -> bool:
    """Lines that must stay on their own.

    On formulas specifically: a line that is entirely `$$…$$` is a DISPLAY
    formula and must keep its own line. Pulled into a paragraph it becomes an
    inline formula — that changes the meaning of the layout, not just its look.

    Block-level HTML gets the same treatment, and for the same reason: `<details>`
    and its `<summary>` are structure, not prose. Joining them still renders, but
    it makes the source misread as a paragraph, and `make reflow-check` could then
    never come back clean on any page that uses a collapsible block.
    """
    s = line.strip()
    display_math = len(s) > 4 and s.startswith("$$") and s.endswith("$$")
    html_block = s.startswith("<") and s.endswith(">") and not s.startswith("<!--")
    return (not s
            or s.startswith("#")
            or s.startswith("|")
            or display_math
            or html_block
            or HR_RE.match(line) is not None
            or COMMENT_RE.match(line) is not None)


def reflow(text: str) -> str:
    lines = text.split("\n")
    out: list[str] = []
    buf: list[str] = []
    prefix = ""

    def flush():
        nonlocal buf, prefix
        if buf:
            out.append(prefix + " ".join(part.strip() for part in buf))
            buf, prefix = [], ""

    i = 0
    # frontmatter — verbatim
    if lines and lines[0].strip() == "---":
        out.append(lines[0])
        i = 1
        while i < len(lines) and lines[i].strip() != "---":
            out.append(lines[i])
            i += 1
        if i < len(lines):
            out.append(lines[i])
            i += 1

    in_fence = False
    in_math = False
    while i < len(lines):
        line = lines[i]
        s = line.strip()

        if s.startswith("```") or s.startswith("~~~"):
            flush()
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue

        if s == "$$":
            flush()
            in_math = not in_math
            out.append(line)
            i += 1
            continue
        if in_math:
            out.append(line)
            i += 1
            continue

        if verbatim(line):
            flush()
            out.append(line)
            i += 1
            continue

        m_quote = QUOTE_RE.match(line)
        m_list = LIST_RE.match(line)

        if m_quote and CALLOUT_RE.match(line):
            # A callout title must stay on its own line: glue it to the body and
            # Obsidian stops recognising the block, so the hint unfolds forever.
            flush()
            out.append(line.rstrip())
            i += 1
            continue

        if m_quote:
            body = m_quote.group(2)
            if not buf or not prefix.lstrip().startswith(">"):
                flush()
                prefix = m_quote.group(1)
            if not body.strip():          # a lone `>` separates blockquote paragraphs
                flush()
                out.append(line.rstrip())
            else:
                buf.append(body)
            i += 1
            continue

        if m_list:
            flush()
            prefix = line[:m_list.end()]
            buf.append(line[m_list.end():])
            i += 1
            continue

        # ordinary line: continuation of this paragraph, or the start of a new one
        if not buf:
            prefix = re.match(r"^\s*", line).group(0)
        buf.append(line)
        i += 1

    flush()
    result = "\n".join(out)
    return result if result.endswith("\n") else result + "\n"


def targets(args: list[str]) -> list[Path]:
    if args:
        return [Path(a).resolve() for a in args]
    found = []
    for p in sorted(ROOT.rglob("*.md")):
        if SKIP_DIRS & set(p.relative_to(ROOT).parts):
            continue
        found.append(p)
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--check", action="store_true", help="report only, write nothing")
    a = ap.parse_args()

    changed = 0
    for p in targets(a.paths):
        before = p.read_text(encoding="utf-8")
        after = reflow(before)
        if before == after:
            continue
        changed += 1
        b_lines = len(before.split("\n"))
        a_lines = len(after.split("\n"))
        try:
            shown = p.relative_to(ROOT)
        except ValueError:               # file outside the project — show as given
            shown = p
        print(f"{'≠' if a.check else '✎'} {shown}  {b_lines} → {a_lines} lines")
        if not a.check:
            p.write_text(after, encoding="utf-8")

    print(f"\n{'would change' if a.check else 'changed'}: {changed} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
