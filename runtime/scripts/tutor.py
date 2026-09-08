#!/usr/bin/env python3
"""
tutor.py — the one entry point, on every platform.

    python tutor.py check          # recompute the confidence tags
    python tutor.py lint
    python tutor.py audit-new "page" --text "quote" --severity warn

Why this exists. The interface used to be a Makefile, which is fine on Linux and
macOS and unusable on Windows: there is no `make`, no `test`, no `command -v`, no
`grep`/`awk`, `python3` is frequently a Microsoft Store stub that opens the store
instead of running, and the virtualenv puts its interpreter in `Scripts\\python.exe`
rather than `bin/python`. Every one of those appeared in the generated Makefile.

So the logic lives here, in stdlib Python, and the Makefile is now sugar that
forwards to it. One code path, three platforms, and the quoting is Python's
problem rather than the shell's.

Stdlib only: this has to run before the project's dependency is installed.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent
IS_WINDOWS = os.name == "nt"

# scripts/ relative to the runtime, plus whether the corpus capability owns it
COMMANDS: dict[str, tuple[str, list[str], str]] = {
    "check":       ("scripts/check_pages.py", [], "check pages and rewrite `confidence` (the ONLY way the tag changes)"),
    "check-dry":   ("scripts/check_pages.py", ["--dry-run"], "same, but write nothing"),
    "lint":        ("scripts/lint_wiki.py", ["."], "health-check of the wiki graph"),
    "reflow":      ("scripts/reflow_md.py", [], "one paragraph = one line (Obsidian Live Preview)"),
    "reflow-check": ("scripts/reflow_md.py", ["--check"], "show where paragraphs are still hard-wrapped"),
    "audit":       ("scripts/audit_review.py", [".", "--open"], "open notes from audit/, by severity"),
    "audit-new":   ("scripts/new_audit.py", [], "file a note: audit-new \"page\" --text \"quote\""),
    "find":        ("capabilities/corpus/find_in_book.py", [], "search the corpus (corpus subjects only)"),
    "ocr":         ("capabilities/corpus/ocr_book.py", ["--all", "--dpi", "300"], "extend the corpus text index"),
    "ocr-status":  ("capabilities/corpus/ocr_book.py", ["--status"], "what is already indexed"),
    "catalog":     ("capabilities/corpus/catalog.py", [], "rebuild raw/books/index.md"),
}


def project_root() -> Path:
    env = os.environ.get("TUTOR_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    here = Path.cwd().resolve()
    for cand in [here, *here.parents]:
        if (cand / ".tutor").is_dir() or (cand / "tutor.py").is_file():
            return cand
    return here


def venv_python(root: Path) -> Path | None:
    """The project interpreter, wherever this platform puts it.

    Windows uses .venv\\Scripts\\python.exe; everything else uses .venv/bin/python.
    Getting this wrong is not a cosmetic bug: the old Makefile tested for
    `.venv/bin/python`, never found it on Windows, silently fell back to whatever
    `python3` meant there, and failed on the missing dependency.
    """
    cand = root / ".venv" / ("Scripts" if IS_WINDOWS else "bin") / ("python.exe" if IS_WINDOWS else "python")
    return cand if cand.exists() else None


def usage() -> int:
    print("tutor — commands for this learning base\n")
    width = max(len(c) for c in COMMANDS) + 2
    print(f"  {'setup'.ljust(width)}create .venv and install the one dependency (PyYAML)")
    for name, (_, _, doc) in COMMANDS.items():
        print(f"  {name.ljust(width)}{doc}")
    print("\nRun as:  python tutor.py <command> [extra arguments]")
    if not IS_WINDOWS:
        print("`make <command>` does the same thing where make is available.")
    return 0


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help", "help"):
        return usage()

    cmd, rest = argv[0], argv[1:]
    root = project_root()
    os.environ["TUTOR_PROJECT_ROOT"] = str(root)

    if cmd == "setup":
        # Runs under whatever interpreter invoked us: it is what builds the venv.
        return subprocess.run([sys.executable, str(RUNTIME / "scripts" / "setup_venv.py")],
                              cwd=root).returncode

    if cmd not in COMMANDS:
        print(f"unknown command: {cmd}\n", file=sys.stderr)
        usage()
        return 2

    rel, fixed, _ = COMMANDS[cmd]
    py = venv_python(root)
    if py is None:
        print("No project environment yet. Run:  python tutor.py setup", file=sys.stderr)
        return 1

    return subprocess.run([str(py), str(RUNTIME / rel), *fixed, *rest], cwd=root).returncode


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
