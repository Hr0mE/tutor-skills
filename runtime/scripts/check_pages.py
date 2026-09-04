#!/usr/bin/env python3
"""
check_pages.py — the only thing allowed to write the `confidence` tag.

    check_pages.py                 # check every page, rewrite confidence
    check_pages.py --dry-run       # report only, write nothing
    check_pages.py wiki/concepts/X.md

Why a script and not the author: the scale must measure THE PRESENCE OF CHECKS,
not the confidence of whoever wrote the text. The moment `confidence` can be set
by hand it drifts upward and stops meaning anything.

The core is domain-neutral. Everything specific to a field — what counts as a
source, what a check is, how many independent sources buy `verified` — comes
from the domain layer at `.tutor/config.yaml`, written by /learning-init.

Check markup on a page:

    <!-- check:sympy limit((1+1/n)**n, n, oo) == E -->
    <!-- check:counterexample heine_borel_without_closedness -->
    <!-- check:attested 0 "every open cover has a finite subcover" -->

`check:<runner> <argument>`. Note what is NOT in the markup: the check's TYPE.
The type is declared by the runner in the domain layer, never by the page.
If pages could name their own type, an author could write `check:formal` over a
quotation from Braudel — the exact hole that machine-written `confidence` exists
to close.
"""
from __future__ import annotations

import argparse
import importlib.util
import io
import re
import subprocess
import sys
import traceback
from contextlib import redirect_stdout
from dataclasses import dataclass, field
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _tutor import cfg, load_config, project_root  # noqa: E402

FM_RE = re.compile(r"\A---\n(.*?)\n---\n(.*)\Z", re.S)
CHECK_RE = re.compile(r"<!--\s*check:([A-Za-z0-9_-]+)\s+(.+?)\s*-->")

# The draft banner is owned by this script, like the tag it represents. Hiding a
# draft behind a frontmatter field means hiding from the learner where the base
# is thin — and the frontmatter is exactly what nobody reads.
BANNER_MARK = "<!-- tutor:draft-banner -->"
BANNER_RE = re.compile(rf"^{re.escape(BANNER_MARK)}\n(?:>.*\n)+\n?", re.M)
DEFAULT_BANNER = ("> [!warning] Draft — read with suspicion\n"
                  "> This page has not earned a trustworthiness tag yet. "
                  "Statements on it may be wrong, unsourced, or both.")

# The five types. Fixed in the core: a domain may declare which of them it can
# attain, never invent a sixth.
TYPES = {
    "formal":      "proof-grade: symbolic identity, type check, proof assistant",
    "behavioral":  "observed on one concrete version/installation, not proved",
    "illustrative": "counterexample or numeric demonstration — refutes, does not prove",
    "attested":    "the cited source really does say this — not that it is true",
    "contested":   "sources genuinely disagree; the disagreement is the content",
}

CORE_REQUIRED = ["title", "kind", "sources"]

TIERS = ["draft", "derived", "sourced", "verified"]
ICONS = {"verified": "🟢", "sourced": "🔵", "derived": "🟡", "draft": "⚪"}


@dataclass
class Report:
    path: Path
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    checks: list[str] = field(default_factory=list)
    n_independent: int = 0
    n_sources: int = 0
    n_passed: int = 0
    n_failed: int = 0
    confidence: str = "draft"
    capped: str = ""


# ───────────────────────────── runners ─────────────────────────────

class Runners:
    """Domain-supplied check runners plus the built-ins.

    Three kinds, which between them cover every domain seen so far:
      python-call : import a module, call entry(argument)      → sympy, unit checks
      python-dir  : scan a directory for functions, run one    → counterexamples
      shell       : run a command, exit 0 means passed         → vitest, pytest, tsc
    """

    def __init__(self, root: Path, config: dict):
        self.root = root
        self.decl = cfg(config, "runners", {}) or {}
        self._dir_cache: dict[str, dict] = {}

    def type_of(self, name: str) -> str | None:
        if name == "attested":
            return "attested"
        return (self.decl.get(name) or {}).get("type")

    def run(self, name: str, arg: str, fm: dict | None = None) -> tuple[bool, str]:
        if name == "attested":
            return self._attested(arg, fm or {})
        d = self.decl.get(name)
        if d is None:
            return False, (f"runner `{name}` is not declared in .tutor/config.yaml — "
                           f"declare it under `runners:` or fix the markup")
        kind = d.get("kind")
        try:
            if kind == "python-call":
                return self._python_call(d, arg)
            if kind == "python-dir":
                return self._python_dir(d, arg)
            if kind == "shell":
                return self._shell(d, arg)
        except Exception:
            return False, traceback.format_exc(limit=2).strip().splitlines()[-1]
        return False, f"runner `{name}` has unknown kind {kind!r}"

    # -- kinds --------------------------------------------------------------

    def _load(self, rel: str):
        path = self.root / rel
        spec = importlib.util.spec_from_file_location(f"tutor_runner_{path.stem}", path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)  # type: ignore[union-attr]
        return mod

    def _python_call(self, d: dict, arg: str) -> tuple[bool, str]:
        mod = self._load(d["module"])
        fn = getattr(mod, d.get("entry", "run"))
        with redirect_stdout(io.StringIO()):
            res = fn(arg)
        if isinstance(res, tuple):
            return bool(res[0]), str(res[1])
        return bool(res), "ok" if res else "returned false"

    def _python_dir(self, d: dict, arg: str) -> tuple[bool, str]:
        directory = d["directory"]
        if directory not in self._dir_cache:
            reg: dict[str, object] = {}
            for py in sorted((self.root / directory).glob("*.py")):
                if py.name.startswith("_"):
                    continue
                try:
                    mod = self._load(f"{directory}/{py.name}")
                except Exception as e:
                    print(f"⚠ could not load {py.name}: {e}", file=sys.stderr)
                    continue
                prefix = d.get("prefix", "test_")
                for nm, obj in vars(mod).items():
                    if nm.startswith(prefix) and callable(obj):
                        reg[nm[len(prefix):]] = obj
            self._dir_cache[directory] = reg
        fn = self._dir_cache[directory].get(arg)
        if fn is None:
            return False, f"no `{d.get('prefix', 'test_')}{arg}` found in {directory}/"
        with redirect_stdout(io.StringIO()):
            fn()
        return True, "ok"

    def _shell(self, d: dict, arg: str) -> tuple[bool, str]:
        cmd = d["command"].replace("{arg}", arg)
        p = subprocess.run(cmd, shell=True, cwd=self.root, capture_output=True,
                           text=True, timeout=d.get("timeout", 300))
        if p.returncode == 0:
            return True, "exit 0"
        tail = (p.stderr or p.stdout or "").strip().splitlines()
        return False, f"exit {p.returncode}: {tail[-1] if tail else 'no output'}"

    # -- built-in: attestation ---------------------------------------------

    def _attested(self, arg: str, fm: dict) -> tuple[bool, str]:
        """`check:attested <source-index> "quoted text"` — verify that the CITED
        source really carries the quoted words, on the cited page.

        This is the check that keeps the scale alive in fields where nothing is
        executable. It does not certify that the claim is TRUE; it certifies that
        the source was not misquoted — the only thing a machine can honestly
        certify about a documentary claim.

        The source index is not decoration. Searching the whole library instead
        would attest that the words exist *somewhere*, which says nothing about
        the citation — and would pass on a book the page never cited.
        """
        m = re.match(r'^(\d+)\s+"(.+)"$', arg.strip())
        if not m:
            return False, 'markup must be: check:attested <source-index> "quoted text"'
        idx, quote = int(m.group(1)), m.group(2)

        srcs = fm.get("sources") or []
        if idx >= len(srcs) or not isinstance(srcs[idx], dict):
            return False, (f"source index {idx} does not exist on this page "
                           f"({len(srcs)} source(s) listed)")
        src = srcs[idx]
        name = str(src.get("source", src.get("book", "")))
        stem = Path(name).stem
        txt = self.root / "raw" / "books" / ".ocr" / f"{stem}.txt"
        if not txt.exists():
            return False, f"no text index for {name} — run `make ocr`"

        needle = re.sub(r"\s+", " ", quote).strip().lower()
        page = src.get("page")
        pages = self._pages_of(txt, stem, page)
        if pages is None:                       # offset unknown: whole book, and say so
            hay = re.sub(r"\s+", " ", txt.read_text(encoding="utf-8", errors="ignore")).lower()
            if needle in hay:
                return True, f"found in {stem}, but the printed-page offset is unknown"
            return False, f"not found anywhere in {stem}"
        for pdf_page, text in pages:
            hay = re.sub(r"\s+", " ", text).lower()
            if needle in hay:
                return True, f"found on p. {page} of {stem} (pdf p. {pdf_page})"
        return False, (f"not found on p. {page} of {stem} — the wording, the page "
                       f"number, or both are wrong")

    def _pages_of(self, txt: Path, stem: str, printed):
        """Pages of the index whose printed number is the cited one (±1).

        The ±1 is not slack in the offset: a statement routinely straddles a page
        break, and the citation names where it starts. Wider than that and the
        check stops testing the page number at all.

        Deliberately narrow otherwise: whitespace normalised, case ignored, no
        fuzzy matching. Fuzzy matching over OCR would manufacture false
        attestations, which is worse than having no check.
        """
        if printed is None:
            return None
        sys.path.insert(0, str(Path(__file__).resolve().parent.parent
                               / "capabilities" / "corpus"))
        try:
            import find_in_book as fib  # type: ignore
        except Exception:
            return None
        to_printed = fib.offset_fn(stem)
        if to_printed is None:
            return None
        out = []
        for pdf_page, text in fib.pages_of(txt):
            got = to_printed(pdf_page)
            if got is not None and abs(got - int(printed)) <= 1:
                out.append((pdf_page, text))
        return out or []


# ─────────────────────────── page checking ───────────────────────────

def compile_patterns(config: dict) -> dict:
    ru_en = lambda ru, en: rf"^#{{2,4}}\s*(?:{ru}|{en})"  # noqa: E731
    return {
        "analogy_marker": re.compile(
            cfg(config, "rules.analogy.marker", r"origin:\s*analogy"), re.I),
        "analogy_breaks": re.compile(
            cfg(config, "rules.analogy.breaks_pattern",
                ru_en(r"Где\s+.*ломается", r"Where\s+.*breaks")), re.M | re.I),
        "contested_section": re.compile(
            cfg(config, "rules.contested.section_pattern",
                ru_en(r"Расхождени|Спор", r"Where\s+sources\s+disagree|Disagreement")),
            re.M | re.I),
    }


def check_page(path: Path, root: Path, config: dict, runners: Runners,
               pats: dict) -> Report:
    rep = Report(path=path)
    raw = path.read_text(encoding="utf-8")
    m = FM_RE.match(raw)
    if not m:
        rep.errors.append("no YAML frontmatter")
        return rep
    try:
        fm = yaml.safe_load(m.group(1)) or {}
    except yaml.YAMLError as e:
        rep.errors.append(f"broken YAML: {e}")
        return rep
    body = m.group(2)

    # ── schema ──
    required = CORE_REQUIRED + list(cfg(config, "schema.extra_required", []) or [])
    for key in required:
        if key not in fm:
            rep.errors.append(f"missing required field `{key}`")
    kinds = set(cfg(config, "schema.kinds", ["concept", "track", "prereq"]))
    if fm.get("kind") not in kinds:
        rep.errors.append(f"kind={fm.get('kind')!r}, allowed {sorted(kinds)}")

    is_concept = fm.get("kind") == "concept"

    # ── sources and independence ──
    check_sources(fm, root, config, rep)

    # ── core rules ──
    if is_concept:
        check_levels(fm, body, config, rep)
        check_analogy(body, pats, rep)
    check_contested(fm, body, pats, rep)

    # ── checks ──
    run_checks(body, fm, config, runners, rep)

    # ── confidence ──
    compute_confidence(fm, config, rep)
    return rep


def check_sources(fm: dict, root: Path, config: dict, rep: Report) -> None:
    """Independence, not the number two, is the invariant.

    Two textbooks retelling one monograph are one source counted twice; so are
    two blog posts paraphrasing the same documentation page. A source that
    declares `derives_from` does not add independence. The machine cannot judge
    independence itself — it can only force the author to declare the derivation
    graph, and refuse to count what is declared derivative.
    """
    srcs = fm.get("sources") or []
    if not isinstance(srcs, list):
        rep.errors.append("`sources` must be a list")
        return
    resolver = cfg(config, "sources.resolver", "none")
    require_loc = cfg(config, "sources.require_loc", True)
    independent = 0
    for s in srcs:
        if not isinstance(s, dict):
            rep.errors.append(f"a source must be a mapping with at least `source`: {s!r}")
            continue
        name = str(s.get("source", s.get("book", "")))
        if name == "pending":
            rep.warnings.append("source marked `pending` — the page cannot rise above draft")
            continue
        if resolver == "corpus" and not (root / "raw" / "books" / name).exists():
            rep.errors.append(f"source not present in raw/books: {name}")
            continue
        if resolver == "url" and not re.match(r"^https?://", name):
            rep.errors.append(f"source must be a URL under the `url` resolver: {name}")
            continue
        if require_loc and not s.get("loc"):
            rep.errors.append(f"source {name} has no `loc` — a citation must reach the "
                              f"section / claim number, not just the work")
            continue
        if cfg(config, "sources.require_version", False) and not s.get("version"):
            rep.errors.append(f"source {name} has no `version` — in a fast-moving field "
                              f"an unversioned citation is a claim about nothing")
            continue
        rep.n_sources += 1
        if not s.get("derives_from"):
            independent += 1
    rep.n_independent = independent


def check_levels(fm: dict, body: str, config: dict, rep: Report) -> None:
    """A level may be declared inapplicable WITH A REASON. It may not be silently
    skipped — the exact shape of `checks: [n/a — not formalisable]`."""
    levels = cfg(config, "levels", {}) or {}
    na = fm.get("levels_na") or {}
    for key, spec in levels.items():
        pattern = spec.get("heading_pattern") if isinstance(spec, dict) else None
        if not pattern:
            continue
        if re.search(pattern, body, re.M | re.I):
            continue
        reason = na.get(key)
        if not reason:
            rep.errors.append(
                f"level `{key}` is missing and not declared inapplicable. Either write it, "
                f"or add `levels_na: {{{key}: \"why it does not apply here\"}}`")
        elif len(str(reason).strip()) < 15:
            rep.errors.append(f"level `{key}` declared inapplicable without a real reason")


def check_analogy(body: str, pats: dict, rep: Report) -> None:
    if pats["analogy_marker"].search(body) and not pats["analogy_breaks"].search(body):
        rep.errors.append(
            "an `origin: analogy` block with no “where this analogy breaks” section. "
            "An analogy without stated limits is worse than no analogy: it installs "
            "itself as fact and gets in the way for years.")


def check_contested(fm: dict, body: str, pats: dict, rep: Report) -> None:
    if fm.get("status") != "contested":
        return
    if len(fm.get("sources") or []) < 2:
        rep.errors.append("`status: contested` needs at least two sources — a disagreement "
                          "requires two parties")
    if not pats["contested_section"].search(body):
        rep.errors.append("`status: contested` but no section laying out the disagreement. "
                          "Contested is not a defect to note in passing; it is the content "
                          "of the page.")


def run_checks(body: str, fm: dict, config: dict, runners: Runners,
               rep: Report) -> None:
    attainable = set(cfg(config, "confidence.attainable_types", list(TYPES)) or [])
    seen = set()
    for name, arg in CHECK_RE.findall(body):
        if (name, arg) in seen:      # the same check may be marked up twice
            continue
        seen.add((name, arg))
        typ = runners.type_of(name)
        if typ is None:
            rep.errors.append(f"check runner `{name}` is not declared in .tutor/config.yaml")
            continue
        if typ not in TYPES:
            rep.errors.append(f"runner `{name}` declares type {typ!r}; the five types are "
                              f"{sorted(TYPES)}")
            continue
        if typ not in attainable:
            rep.warnings.append(f"runner `{name}` is type `{typ}`, which this domain declared "
                                f"unattainable — either the domain layer is wrong or the check is")
        ok, msg = runners.run(name, arg, fm)
        rep.checks.append(f"{name}:{arg} — {'passed' if ok else 'FAILED'} ({msg}) [{typ}]")
        rep.n_passed += ok
        rep.n_failed += not ok


def compute_confidence(fm: dict, config: dict, rep: Report) -> None:
    min_src = cfg(config, "confidence.min_independent_sources", 2)
    min_chk = cfg(config, "confidence.min_passed_checks", 1)

    if rep.errors or rep.n_failed:
        rep.confidence = "draft"
    elif rep.n_sources == 0:
        # No source at all is not a failure — it is an honest `derived`: the agent
        # worked it out from material already in the base.
        rep.confidence = "derived"
    elif rep.n_independent >= min_src and rep.n_passed >= min_chk:
        rep.confidence = "verified"
    else:
        rep.confidence = "sourced"

    # Phase cap. Pages written during phase 1 ran against a domain layer that was
    # knowingly incomplete, so their tag is unearned by construction. Closing
    # phase 2 lifts the cap and this script recomputes them for real.
    phase = str(cfg(config, "phase", "complete"))
    if phase in {"1", "2"} and TIERS.index(rep.confidence) > TIERS.index("draft"):
        rep.capped = rep.confidence
        rep.confidence = "draft"


def apply_banner(body: str, is_draft: bool, banner: str) -> str:
    """Put the draft banner on the page, or take it off.

    Drafts are shown, not hidden — but with a visible banner rather than a
    frontmatter field alone. A tag nobody reads is not a warning, and concealing
    which pages are thin is concealing where the base needs work.

    Owned by this script for the same reason the tag is: anything a human can
    edit by hand drifts out of agreement with the checks.
    """
    body = BANNER_RE.sub("", body)
    if not is_draft:
        return body
    block = f"{BANNER_MARK}\n{banner}\n\n"
    m = re.search(r"^#\s+.*\n+", body, re.M)
    if m:
        return body[:m.end()] + block + body[m.end():]
    return block + body.lstrip("\n")


def write_back(path: Path, rep: Report, config: dict) -> bool:
    raw = path.read_text(encoding="utf-8")
    m = FM_RE.match(raw)
    if not m:
        return False
    fm = yaml.safe_load(m.group(1)) or {}
    new_checks = list(dict.fromkeys(rep.checks)) or ["n/a — not formalisable"]
    banner = cfg(config, "rules.draft_banner", DEFAULT_BANNER)
    body = apply_banner(m.group(2), rep.confidence == "draft", banner)
    unchanged = (fm.get("confidence") == rep.confidence
                 and fm.get("checks") == new_checks
                 and body == m.group(2))
    if unchanged:
        return False
    fm["confidence"] = rep.confidence
    fm["checks"] = new_checks
    dumped = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, width=100)
    path.write_text(f"---\n{dumped}---\n{body}", encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--root", help="project root (default: nearest .tutor/config.yaml)")
    a = ap.parse_args()

    root = project_root(a.root)
    config = load_config(root)
    runners = Runners(root, config)
    pats = compile_patterns(config)
    wiki = root / cfg(config, "layout.wiki", "wiki")

    targets = ([Path(p).resolve() for p in a.paths] if a.paths
               else sorted(p for p in wiki.rglob("*.md")
                           if not p.name.startswith("_") and p.name != "index.md"))
    if not targets:
        print("No pages yet — nothing to check.")
        return 0

    phase = str(cfg(config, "phase", "complete"))
    if phase in {"1", "2"}:
        print(f"⚑ domain layer is at phase {phase}: every page is capped at `draft` "
              f"until /learning-init closes phase 2.\n")

    bad = 0
    tally: dict[str, int] = {}
    for path in targets:
        rep = check_page(path, root, config, runners, pats)
        tally[rep.confidence] = tally.get(rep.confidence, 0) + 1
        try:
            rel = path.relative_to(root)
        except ValueError:
            rel = path
        cap = f"  (capped from {rep.capped})" if rep.capped else ""
        print(f"{ICONS[rep.confidence]} {rep.confidence:<9} {rel}{cap}")
        for e in rep.errors:
            print(f"     ✗ {e}")
            bad += 1
        for w in rep.warnings:
            print(f"     ⚠ {w}")
        for c in rep.checks:
            print(f"     · {c}")
        if rep.n_sources:
            print(f"     ⤷ sources: {rep.n_sources}, independent: {rep.n_independent}")
        if not a.dry_run and write_back(path, rep, config):
            print("     ✎ frontmatter updated")

    print("\nTotals:", " · ".join(f"{k}: {v}" for k, v in sorted(tally.items())))
    if bad:
        print(f"Errors: {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
