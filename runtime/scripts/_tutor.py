"""
_tutor.py — shared plumbing for every core script.

The core scripts live in the plugin, not in the project, so they cannot find the
project by walking up from `__file__` the way a vendored script would. Root
resolution order:

  1. $TUTOR_PROJECT_ROOT
  2. nearest ancestor of $PWD containing `.tutor/config.yaml`
  3. $PWD

This is the whole reason the core stays updatable: the project holds a pointer,
not a copy. See docs/INSTALL.md.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import yaml

CONFIG_REL = Path(".tutor") / "config.yaml"


def project_root(explicit: str | os.PathLike | None = None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("TUTOR_PROJECT_ROOT")
    if env:
        return Path(env).resolve()
    here = Path.cwd().resolve()
    for cand in [here, *here.parents]:
        if (cand / CONFIG_REL).exists():
            return cand
    return here


def load_config(root: Path | None = None) -> dict:
    """The domain layer. Hand-editable by design — it is the user's judgement
    about their own field, unlike `confidence`, which is a machine conclusion."""
    root = root or project_root()
    path = root / CONFIG_REL
    if not path.exists():
        print(f"ERROR: no domain layer at {path}.\n"
              f"Run /learning-init first — the core cannot guess what counts as a "
              f"source, a check, or a closed topic in your field.", file=sys.stderr)
        raise SystemExit(2)
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def cfg(config: dict, path: str, default=None):
    """cfg(c, 'confidence.min_independent_sources', 2)"""
    node = config
    for part in path.split("."):
        if not isinstance(node, dict) or part not in node:
            return default
        node = node[part]
    return node
