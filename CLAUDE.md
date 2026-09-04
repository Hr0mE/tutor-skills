# tutor-skills — repository schema

> Read at the start of **every** session in this repo, together with `README.md`. Update it after any structural change, any decision that closes a question, and any finding that would otherwise be rediscovered the hard way.

## 1. What this is

A Claude Code plugin: a personal tutor you assemble for your own subject — mathematics, React, physics, chemistry, history. Extracted from a completed mathematics track (`~/Проекты/math_learning`), which stays untouched and serves as the reference implementation.

**The invariant being generalised:** the page format with depth levels · the trustworthiness loop with a machine-written tag · the `tracks/` layer that argues for its own ordering. Everything below is in service of those three.

**The architectural rule that shapes everything:** the core knows *how to teach* and lives in the plugin, updating with it. Only the **domain layer** — what a source is, what a check is, what "done" means in this subject — is generated into the learner's project. A project holds a pointer to the runtime, never a copy. Break this and you get several projects on several frozen forks of the method, discovered on the third one when repair is most expensive.

## 2. Where things are

| Path | What it is |
|---|---|
| `.claude-plugin/plugin.json` · `marketplace.json` | Plugin and self-hosted marketplace manifests. The repo is its own marketplace |
| `skills/learning-init/` | The two-phase interviewer. `SKILL.md` + `references/phase-1.md`, `phase-2.md`, `domain-layer.md` |
| `skills/learning-track/` | The orchestrator. `SKILL.md` + five subordinates in `agents/` + six `references/` |
| `runtime/scripts/check_pages.py` | **The centre of the whole thing.** The only writer of `confidence`. 545 lines |
| `runtime/scripts/_tutor.py` | Root resolution and domain-layer loading. Everything imports it |
| `runtime/scripts/scaffold.py` | Lays out a project; generates the Makefile that points at the plugin |
| `runtime/scripts/{lint_wiki,audit_review,new_audit,reflow_md}.py` | Ported from math_learning, de-hardcoded, translated |
| `runtime/capabilities/corpus/` | Optional: OCR, printed-page offsets, full-text search, catalogue |
| `runtime/templates/` | Neutral page skeletons that `learning-init` specialises per subject |
| `docs/INSTALL.md` | The user-facing walkthrough, GitHub → first page → phase 2 → recount |
| `NOTICE` | Intellectual debts: Karpathy's gist, Lewis Liu's `llm-wiki` skill |

`agents/` inside one skill rather than sibling skills — the shape `~/.claude/skills/tdd` already uses, so the routing table does not grow five entries.

### The seam that was cut

`check_math.py` (284 lines, math-specific) became `check_pages.py` (545, neutral) plus a ~40-line domain runner. Frontmatter schema, the analogy rule, check-markup parsing, independence counting and tag write-back went to the core; SymPy went out as an ordinary runner, on equal footing with a future `vitest`.

**The type of a check is declared by the runner, never by the page.** If a page could name its own type, an author could write `check:formal` over a quotation — exactly the hole that machine-written tags exist to close.

## 3. State

Working tree clean; see `git log` for the reasoning behind each change.

**Verified by running, not by reading:**

- The core against **14 real pages** of the compactness track with SymPy externalised: `verified: 14 · derived: 2`, 53 checks passed, 0 failed — identical to the old script's verdict. The count difference against the old run (84 vs 53) is per-page deduplication, confirmed separately, not skipped checks.
- Eight core scenarios: the analogy rule · `derives_from` cutting independence 2→1 and dropping `verified`→`sourced` · phase-1 capping with `(capped from verified)` · a missing level with and without `levels_na` · a failing check · `contested` without a second source and without its section.
- The draft banner appearing and disappearing as the tag changes.
- `attested` against the real OCR corpus: true quote on the cited page passes, invented quote fails, out-of-range source index fails.
- `scaffold`, `make setup`, `lint`, `audit-new`, `audit`, `reflow-check` on fresh projects; `reflow-check` clean on a new scaffold.

**Not verified by running:** the skills themselves have never been loaded by Claude Code — `check_pages` and friends were exercised directly. `make ocr` has never been run end-to-end through the plugin path (hours on a real corpus). `make find` was exercised only on its empty-index error path.

## 4. What is left, in order

**1. Walk phase 1 live.** The plugin is installed (see item 3), but the interview itself has still never run. It is the only untested surface, and the one where four holes were already found by paper analysis alone — a second subject will show the next ones. Requires an interactive session; it cannot be exercised from a script.

> Note for whoever runs it: `/plugin` is not exposed as a slash command in every environment. Where it is missing, `claude plugin marketplace add …` / `claude plugin install …` does the same thing, and newly installed skills only appear after a restart.

**2. The React pilot.** A real project on the subject the whole thing was started for. Expect the domain layer to want fields that do not exist yet; that is the point of a pilot, and each one is a finding to bring back here.

**3. ~~Publish to GitHub.~~ Done, 2026-09-04** — `Hr0mE/tutor-skills`, public, plugin installed from it at commit `12785b9`. A guessed owner (`dmitrylyapin`) had been left in `plugin.json` and `docs/INSTALL.md`; both corrected afterwards. **The account is `Hr0mE`** — do not re-guess it.

**4. Write to Lewis Liu** (`lylewis@outlook.com`), author of the `llm-wiki` skill. Courtesy, not a blocker — `NOTICE` already records the debt and no file of his is redistributed.

**5. Run the corpus capability end-to-end once**, on a subject that actually needs it, so `make ocr` is exercised through the plugin path rather than inherited on trust from math_learning.

Not on the list, deliberately: migrating `math_learning`. It works, it is finished, and taking apart the one thing that already runs in order to prove an architecture teaches nothing. It is the regression test, not a consumer.

## 5. Settled — do not re-litigate

Each of these cost a round of argument. The reasoning matters more than the verdict, so it is recorded rather than the conclusion alone.

| Decision | Why |
|---|---|
| Orchestrator + subordinates, no intermediate "one fat skill" stage | Chosen deliberately over growing into it |
| No domain packs | Packs mix responsibilities; the interviewer plus a checklist produces the same thing without freezing a taxonomy derived from one subject |
| Core static and updatable; only the domain layer generated | `create-react-app eject` on day one otherwise. See §1 |
| Own interviewer, not a dependency on `grilling` | The technique is twenty lines; a dependency puts someone else's repo between a user and their first run. Also `grill-me` carries `disable-model-invocation` and cannot be called from a skill anyway |
| Two phases with a real page between them | Answers about verification and canon are guesswork before the material. The main problem book starting at problem 18 could not have come out of an interview |
| Five check types, fixed | A subject declares which it can attain, never invents a sixth. If one seems genuinely needed, that is a finding about the core |
| Independence, not the number two | Two textbooks off one monograph are one source counted twice. The machine cannot judge independence — it counts sources not declaring `derives_from` |
| Clean-room, not a fork of `llm-wiki` | Its five operations are not the value here; the method rides on any markdown wiki. Removes the licence question as a side effect |
| English throughout; page language is a parameter | Public repo, and models follow English instructions better |
| Claude Code only in v1 | Multi-platform support for zero users; "Claude Code only" beats half-working Gemini |

## 6. Known limits and open questions

- **The interview has been tested against exactly one subject.** Four gaps surfaced from that single comparison (the arbiter table, popular sources, deliberate exclusions, the draft banner). Assume more, and treat each pilot as a test of the question set rather than only of the method.
- **`attested` is deliberately narrow**: whitespace normalised, case ignored, no fuzzy matching, page window ±1. Fuzzy matching over OCR would manufacture false attestations, which is worse than no check. If it starts producing false negatives on real material, widen the page window before touching the matching.
- **`schema_version: 1` will move.** The domain layer has been written by hand twice and generated by an interview zero times.
- Whether a project needs a `learning-doctor` (the domain layer has drifted from reality) is open. Deferred until the problem actually appears.

## 7. Resuming in a new session

1. Read this file and `README.md`.
2. `git -C /home/dmitry/Проекты/tutor-skills log --oneline` — the commit messages carry the reasoning for each change.
3. To exercise the core without touching anything real: scaffold into the scratchpad, write a `.tutor/config.yaml`, run `make check`. `skills/learning-init/references/domain-layer.md` has a full annotated schema and two worked shapes (React, history).
4. To re-run the mathematics regression: scaffold a project, copy `wiki/` and `checks/` from `~/Проекты/math_learning`, symlink `raw/books`, write the config with a `sympy` runner of kind `python-call`, and compare `make check-dry` against `.venv/bin/python scripts/check_math.py --dry-run` run inside math_learning. Expect `verified: 14 · derived: 2`.

**Never run `make check` against `~/Проекты/math_learning` itself** — it rewrites `confidence` and would insert draft banners into finished pages. Always copy first.
