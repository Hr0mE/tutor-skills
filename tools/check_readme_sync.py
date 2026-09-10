#!/usr/bin/env python3
"""
check_readme_sync.py — keep the translated READMEs in step with the English one.

    python3 tools/check_readme_sync.py

Why. Seven READMEs carry the same landing page by hand. A translation that
quietly falls behind is worse than no translation, because it is still trusted:
nobody reading `README.ja.md` can tell that the English one grew a section last
month. Prose cannot be compared automatically, but *shape* can — and every drift
that has actually happened here showed up in the shape first: a section added on
one side only, an image placed in five files out of six, a switcher that forgot
a language.

What it checks, per file:

  · the same number of H2 sections, images, mermaid blocks and <details> blocks
    as README.md (the source);
  · the language switcher lists every language, links each of the others, and
    marks its own without a link;
  · every relative link resolves to a file that exists;
  · every image path exists.

What it deliberately does NOT check: that the text says the same thing. That is
a human's job, and pretending otherwise would make this script a false comfort.

Exit code 1 on any drift, so it can run in CI.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = "README.md"

# language tag -> the name shown in the switcher line
LANGUAGES = {
    "": "English",
    "ru": "Русский",
    "zh-CN": "简体中文",
    "ko": "한국어",
    "ja": "日本語",
    "fr": "Français",
    "de": "Deutsch",
}


def readme_path(tag: str) -> Path:
    return ROOT / ("README.md" if tag == "" else f"README.{tag}.md")


def shape(text: str) -> dict[str, int]:
    return {
        "h2": len(re.findall(r"^## ", text, re.M)),
        "images": len(re.findall(r"!\[", text)),
        "mermaid": text.count("```mermaid"),
        "details": text.count("<details>"),
    }


def check_switcher(tag: str, text: str) -> list[str]:
    """The switcher sits above the first heading; self is bold, others are links."""
    head = text.split("\n## ", 1)[0]
    problems = []
    for other, name in LANGUAGES.items():
        if other == tag:
            if f"**{name}**" not in head:
                problems.append(f"does not mark itself as {name!r} in bold")
        else:
            target = readme_path(other).name
            if f"[{name}]({target})" not in head:
                problems.append(f"switcher is missing [{name}]({target})")
    return problems


def check_links(path: Path, text: str) -> list[str]:
    problems = []
    for target in re.findall(r"\]\((?!https?:)([^)#]+)", text):
        if not (ROOT / target).exists():
            problems.append(f"link target does not exist: {target}")
    return problems


def main() -> int:
    source_text = readme_path("").read_text(encoding="utf-8")
    expected = shape(source_text)
    failures = 0

    print(f"source: {SOURCE}  " + "  ".join(f"{k}={v}" for k, v in expected.items()))
    print()

    for tag, name in LANGUAGES.items():
        path = readme_path(tag)
        if not path.exists():
            print(f"✗ {path.name}: missing")
            failures += 1
            continue

        text = path.read_text(encoding="utf-8")
        problems = []

        got = shape(text)
        for key, want in expected.items():
            if got[key] != want:
                problems.append(f"{key}: {got[key]}, expected {want}")

        problems += check_switcher(tag, text)
        problems += check_links(path, text)

        if problems:
            failures += 1
            print(f"✗ {path.name} ({name})")
            for p in problems:
                print(f"    {p}")
        else:
            print(f"✓ {path.name} ({name})")

    print()
    if failures:
        print(f"{failures} file(s) out of step with {SOURCE}.")
        print("Shape drift means a section, an image or a language was added on one side only.")
        return 1
    print(f"All {len(LANGUAGES)} READMEs are in step with {SOURCE}.")
    print("Note: this compares shape, never meaning. Wording still has to be read by a human.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
