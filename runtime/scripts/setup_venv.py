#!/usr/bin/env python3
"""
setup_venv.py — build the project's virtualenv and prove it works.

Stdlib only, by necessity: this is what installs the one dependency the core
needs, so it cannot import it.

Why a script and not three lines in the Makefile. The obvious shell one-liner

    command -v uv && uv venv && uv pip install pyyaml || (python3 -m venv .venv && ...)

is wrong twice. `A && B || C` runs C when B fails, so a half-finished uv run
falls through into the fallback and lands on top of it. And on a Python built
without a working ensurepip — common with pyenv and some distribution builds —
`python3 -m venv` fails *after* creating `.venv/bin/python`, leaving a
directory that exists, satisfies the Makefile's `test -x .venv/bin/python`, and
has no pip in it. `make check` then fails with ModuleNotFoundError, the
troubleshooting says "run make setup", and the loop never terminates.

So: try each route in turn, verify the result by importing, and on failure clean
up the wreckage and say what to install.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

IS_WINDOWS = os.name == "nt"
VENV = Path(".venv")
# Windows puts the interpreter in Scripts\python.exe, everyone else in bin/python.
PY = VENV / ("Scripts" if IS_WINDOWS else "bin") / ("python.exe" if IS_WINDOWS else "python")
DEPS = ["pyyaml"]


def run(cmd: list[str], **kw) -> bool:
    return subprocess.run(cmd, capture_output=True, text=True, **kw).returncode == 0


def works() -> bool:
    """The only success criterion that means anything: the venv can import it."""
    return PY.exists() and run([str(PY), "-c", "import yaml"])


def try_uv() -> bool:
    if not shutil.which("uv"):
        return False
    if not run(["uv", "venv", "--quiet"]):
        return False
    env = {**os.environ, "VIRTUAL_ENV": str(VENV.resolve())}
    return run(["uv", "pip", "install", "--quiet", *DEPS], env=env) and works()


def try_venv() -> bool:
    if not run([sys.executable, "-m", "venv", str(VENV)]):
        return False
    if not run([str(PY), "-m", "pip", "--version"]):
        return False
    return run([str(PY), "-m", "pip", "install", "--quiet", *DEPS]) and works()


def main() -> int:
    hint = "python tutor.py check" if IS_WINDOWS else "make check  (or: python3 tutor.py check)"
    if works():
        print(f"✓ .venv already usable. Next: {hint}")
        return 0

    for attempt in (try_uv, try_venv):
        if attempt():
            print(f"✓ .venv ready. Next: {hint}")
            return 0
        # A failed attempt may have left a half-built venv. The next attempt —
        # and, more importantly, `make check` — must not find it.
        if VENV.exists() and not works():
            shutil.rmtree(VENV, ignore_errors=True)

    install = ('  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"'
               if IS_WINDOWS else "  curl -LsSf https://astral.sh/uv/install.sh | sh")
    print("Could not build a virtualenv.\n", file=sys.stderr)
    print("  uv is not installed, and `-m venv` cannot bootstrap pip on this\n"
          f"  interpreter ({sys.executable}, {sys.version.split()[0]}) — a build\n"
          "  without a working ensurepip.\n", file=sys.stderr)
    if IS_WINDOWS:
        print("  On Windows this is often the Microsoft Store stub: a `python3` that\n"
              "  opens the store instead of running. Install real Python from\n"
              "  python.org, or just install uv, which needs neither.\n", file=sys.stderr)
    print("Install uv:\n"
          f"{install}\n\n"
          "Then run `python tutor.py setup` again.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
