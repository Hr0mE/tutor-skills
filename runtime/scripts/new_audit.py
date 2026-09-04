#!/usr/bin/env python3
"""
new_audit.py — file a note in audit/ without filling in the anchors by hand.

    make audit-new P="Metric space" T="the exact quote from the page"
    make audit-new P="Arzela" L=42 S=error K=statement C="what is wrong"

Why a script rather than just a template: of the eleven required fields, seven
are mechanical — id, created, author, target, target_lines and three text
anchors. The anchors must additionally be SINGLE-LINE double-quoted strings with
escaped newlines, because `lint_wiki.py`'s minimal parser understands nothing
else. Typing that by hand over a page carrying formulas is close to impossible.

What is left to the human is exactly what the note is for: severity, kind, and
the text itself.

Field semantics are documented in the skill's references/audit.md.
"""
from __future__ import annotations

import argparse
import re
import secrets
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tutor import project_root  # noqa: E402

ROOT = project_root()
AUDIT = ROOT / "audit"
ANCHOR_WINDOW = 80

SEVERITIES = ("info", "suggest", "warn", "error")
# Kinds are a domain-layer list: what systematically goes wrong differs between
# a mathematics base and a history base. Defaults cover the neutral set.
from _tutor import cfg, load_config  # noqa: E402

KINDS = tuple(cfg(load_config(ROOT), "audit.kinds", None) or (
    "statement", "source", "analogy", "problem", "hint",
    "link", "length", "typo", "other"))


def yaml_quote(s: str) -> str:
    """Quote a string so it survives lint_wiki.py's minimal parser.

    That parser expands \\n and \\" inside double quotes, and strips single
    quotes without processing anything. Hence the rule:

    * contains a newline or a single quote -> double quotes;
    * otherwise -> SINGLE quotes, and this matters in any subject using LaTeX.

    The trap the whole function exists for: LaTeX is full of a backslash followed
    by n (\\ne, \\nu, \\nabla). Inside double quotes the parser would expand
    that pair into a real newline and corrupt the anchor. Inside single quotes it
    does not, so single quotes are the default.
    """
    if "\n" not in s and "\r" not in s and "'" not in s:
        return f"'{s}'"

    escaped = (s.replace('"', '\\"')
                .replace("\r", "")
                .replace("\n", "\\n")
                .replace("\t", " "))
    if _looks_like_escape(s):
        print("⚠ the anchor contains both a newline and a \\n<letter> sequence "
              "(e.g. \\ne). A minimal parser may distort it — locate the passage by "
              "anchor_text rather than by line number.", file=sys.stderr)
    return f'"{escaped}"'


def _looks_like_escape(s: str) -> bool:
    """Is there a backslash followed by n, as in \\ne or \\nu."""
    return re.search(r"\\\\n[A-Za-z]", s) is not None


def find_target(query: str) -> Path:
    """Find a page by a substring of its name. A full path is accepted too."""
    direct = (ROOT / query)
    if direct.is_file():
        return direct

    candidates = [
        p for p in sorted(ROOT.rglob("*.md"))
        if not {".agents", ".venv", ".git", "raw"} & set(p.relative_to(ROOT).parts)
        and query.lower() in p.stem.lower()
    ]
    if not candidates:
        sys.exit(f"Page not found: {query!r}\n"
                 f"Hint: make audit-new P=\"part of the page name\" ...")
    if len(candidates) > 1:
        # The usual ambiguity: a concept page and its solutions file sharing a
        # name. A note is nearly always about the wiki page, so it wins.
        in_wiki = [c for c in candidates if c.relative_to(ROOT).parts[0] == "wiki"]
        if len(in_wiki) == 1:
            others = [c for c in candidates if c not in in_wiki]
            print(f"· several files matched; took the one under wiki/. "
                  f"Others: {', '.join(str(o.relative_to(ROOT)) for o in others)}",
                  file=sys.stderr)
            return in_wiki[0]
        listing = "\n".join(f"  {c.relative_to(ROOT)}" for c in candidates)
        sys.exit(f"{query!r} matches several pages:\n{listing}\n"
                 f"Narrow the query or give the full path.")
    return candidates[0]


def locate(text: str, quote: str | None, line_no: int | None) -> tuple[str, int, int]:
    """Returns (anchor text, first line, last line), 1-indexed."""
    lines = text.split("\n")

    if quote:
        idx = text.find(quote)
        if idx < 0:
            sys.exit("The quote does not occur on the page verbatim.\n"
                     "Copy the fragment exactly as it stands in the file — formulas "
                     "and markup included — or give a line number with L=.")
        if text.find(quote, idx + 1) >= 0:
            print("⚠ the quote occurs several times; took the first",
                  file=sys.stderr)
        start_line = text.count("\n", 0, idx) + 1
        end_line = start_line + quote.count("\n")
        return quote, start_line, end_line

    if line_no is None:
        sys.exit("Give either T=\"quote\" or L=<line number>.")
    if not (1 <= line_no <= len(lines)):
        sys.exit(f"The file has {len(lines)} lines; {line_no} was requested.")
    picked = lines[line_no - 1].strip()
    if not picked:
        sys.exit(f"Line {line_no} is empty — no anchor can be built from it.")
    return picked, line_no, line_no


def author() -> str:
    try:
        name = subprocess.run(["git", "config", "user.name"], cwd=ROOT,
                              capture_output=True, text=True).stdout.strip()
        if name:
            return name
    except Exception:
        pass
    import os
    return os.environ.get("USER", "unknown")


def slugify(s: str, limit: int = 40) -> str:
    s = re.sub(r"[^\w\s-]", "", s, flags=re.U).strip().lower()
    s = re.sub(r"[\s_]+", "-", s)
    return (s[:limit].rstrip("-") or "note")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("page", help="page name, or a path to it")
    ap.add_argument("--text", "-t", help="the exact quote from the page")
    ap.add_argument("--line", "-l", type=int, help="line number instead of a quote")
    ap.add_argument("--severity", "-s", default="warn", choices=SEVERITIES)
    ap.add_argument("--kind", "-k", default=KINDS[-1], choices=KINDS)
    ap.add_argument("--comment", "-c", default="", help="the note itself")
    a = ap.parse_args()

    target = find_target(a.page)
    body = target.read_text(encoding="utf-8")
    anchor_text, line_from, line_to = locate(body, a.text, a.line)

    idx = body.find(anchor_text)
    before = body[max(0, idx - ANCHOR_WINDOW):idx]
    after = body[idx + len(anchor_text): idx + len(anchor_text) + ANCHOR_WINDOW]

    now = datetime.now().astimezone()
    stamp = now.strftime("%Y%m%d-%H%M%S")
    audit_id = f"{stamp}-{secrets.token_hex(2)}"
    slug = slugify(a.comment or anchor_text)
    path = AUDIT / f"{stamp}-{slug}.md"

    comment = a.comment or "<what is wrong, and what it should be>"
    fm = "\n".join([
        "---",
        f"id: {audit_id}",
        f"target: {target.relative_to(ROOT)}",
        f"target_lines: [{line_from}, {line_to}]",
        f"anchor_before: {yaml_quote(before)}",
        f"anchor_text: {yaml_quote(anchor_text)}",
        f"anchor_after: {yaml_quote(after)}",
        f"severity: {a.severity}",
        f"kind: {a.kind}",
        f"author: {author()}",
        "source: manual",
        f"created: {now.isoformat(timespec='seconds')}",
        "status: open",
        "---",
    ])

    AUDIT.mkdir(parents=True, exist_ok=True)
    path.write_text(f"{fm}\n\n# Comment\n\n{comment}\n", encoding="utf-8")

    print(f"✓ {path.relative_to(ROOT)}")
    print(f"  target:   {target.relative_to(ROOT)}, lines {line_from}–{line_to}")
    print(f"  severity: {a.severity} · kind: {a.kind}")
    if not a.comment:
        print("  ⚠ the note is empty — write it into the file under # Comment")
    return 0


if __name__ == "__main__":
    sys.exit(main())
