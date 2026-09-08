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
| `runtime/scripts/tutor.py` | **The entry point on every platform.** Command dispatcher; the generated Makefile is sugar that forwards to it |
| `runtime/scripts/setup_venv.py` | Builds the project venv and **proves it by importing**. Stdlib only — it installs the dependency the core needs |
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

**1. Answer phase 1.** The plugin is installed and the interview has now been *reached* once — a React deployment on 2026-09-04 got as far as putting the seven questions, and the three defects that surfaced on the way are folded in (§6). What has still never happened is the other half: the questions being answered, a domain layer written, a page produced. That remains the only untested surface, and it needs an interactive session; it cannot be exercised from a script.

> Note for whoever runs it: `/plugin` is not exposed as a slash command in every environment. Where it is missing, `claude plugin marketplace add …` / `claude plugin install …` does the same thing, and newly installed skills only appear after a restart.

**2. The React pilot.** A real project on the subject the whole thing was started for. Expect the domain layer to want fields that do not exist yet; that is the point of a pilot, and each one is a finding to bring back here.

**3. ~~Publish to GitHub.~~ Done, 2026-09-04** — `Hr0mE/tutor-skills`, public, plugin installed from it at commit `12785b9`. A guessed owner (`dmitrylyapin`) had been left in `plugin.json` and `docs/INSTALL.md`; both corrected afterwards. **The account is `Hr0mE`** — do not re-guess it.

**4. Write to Lewis Liu** (`lylewis@outlook.com`), author of the `llm-wiki` skill. Courtesy, not a blocker — `NOTICE` already records the debt and no file of his is redistributed.

**5. Run the corpus capability end-to-end once**, on a subject that actually needs it, so `make ocr` is exercised through the plugin path rather than inherited on trust from math_learning.

Not on the list, deliberately: migrating `math_learning`. It works, it is finished, and taking apart the one thing that already runs in order to prove an architecture teaches nothing. It is the regression test, not a consumer.

## 4a. Releasing

**Bump `version` in `.claude-plugin/plugin.json` and `marketplace.json` on every release that changes behaviour.** The plugin cache is keyed by version and `claude plugin update` compares that field, not the commit — so fixes published under an unchanged version reach nobody, and the only way out is uninstall-and-reinstall. Three commits of fixes shipped under `0.1.0` before this was noticed. Currently `0.3.0` — the scan-boundary gate changed behaviour, so it took a bump.

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

### Found by the first live deployment (React, 2026-09-04)

Three defects, all fixed, all of a kind that only a real machine produces:

- **`make setup` was broken on half its paths.** `A && B || C` in the shell runs C when B fails, so a half-finished `uv` run fell through into the fallback and landed on top of it. Worse, on a Python whose `ensurepip` does not work — pyenv and some distribution builds — `python3 -m venv` fails *after* creating `.venv/bin/python`, leaving a directory that satisfies the Makefile's `test -x` and contains no pip. `make check` then failed with ModuleNotFoundError and the troubleshooting said "run make setup": a loop. Now `setup_venv.py`, which tries each route, verifies by importing, removes the wreckage, and names what to install.
- **The round contradicted itself on strictness.** It recommended `strict` — which requires a passing check on every trusted page — while reporting in the same breath that no test harness existed and the runtime was too old to build one. Every page would have sat at `sourced` forever and the method would have looked broken. Q6 now runs *after* a preflight and recommends strict only where the toolchain has been seen to work, otherwise offering the honest sequence: standard now, harness first, tighten once a check has actually passed.
- **A live subject has two source questions, not one.** Which version is the version of record is separate from corpus-or-live, and it is rarely the version installed. Folded into Q2.

What the deployment did *right*, worth preserving as the pattern: it looked at the disk before asking anything, found an existing project on the subject, and counted hook usage to ground the first question in the learner's own code rather than in a topic list.

### Found by the second live deployment (history, 2026-09-04)

The preflight and the strictness precondition both worked on first contact: the broken `python3 -m venv` was caught before the interview rather than after, and Q6 produced the honest sequence (standard now → build the corpus → tighten once an `attested` check has actually passed) instead of promising a strictness the machine could not deliver.

What it exposed:

- **The orientation fired on one path out of several.** It lived in the README's quick-start block, which is read only when a human pastes the repository URL. A session that arrived by updating an existing install never saw it. Moved into `learning-init` itself, where it runs whatever the route.
- **Releases without a version bump reach nobody.** See §4a.
- **Interpretive subjects need two arbiters, not one.** There is no arbiter of what actually happened; the primary source settles wording, the secondary literature settles interpretation, and their disagreement is page content rather than a defect. Folded into Q3.
- **A locator must survive republication.** Page numbers do not cross editions and translations diverge on substance; where a canonical division exists (book/chapter/section), that is the citation and the page rides along. Folded into Q2.
- **Nobody knew the round could be answered in one line.** The skill now states the "1–7, go with your recommendations" shortcut explicitly, with the corollary for whoever writes the recommendations: one you would not want accepted wholesale is not finished.
- **No question asked where the base should live.** Added as Q0 — the folder name is the base's name in practice.

### Raised by the learner after watching two deployments (2026-09-04)

**The interview read whatever it liked.** Both runs went through the user's disk unasked — one read an unrelated React project and counted hook usage in it, the other walked the projects directory. Nothing in the skill said they should not; the instruction "never ask for anything you could look up" was written unconditional, and it was followed exactly as written.

Fixed by a **consent gate before any reading**: a checkbox question with two axes — how far (this directory · named folders · the parent · nothing) and how deep (names · documents · code · git history) — asked after the orientation, so the learner knows what they are consenting for, and before any enumeration, since listing a parent directory to build the options is itself the scan. The answer lands in `privacy.scan` and binds `learning-track` in every later session, not just the interview.

Three things this must not become: a scan silently widened later because it was convenient; a default that broadens when the question cannot be asked (it narrows); or a claim of enforcement. **It is a rule the agent follows, not a sandbox** — worth saying plainly, and true in the useful direction: everything in `runtime/` resolves paths from the project root and never reads outside it, so the tooling genuinely cannot wander, only the agent can.

Q0 was the first casualty: "look for empty candidates and name them" is a scan, so it now defers to the boundary and asks outright when the boundary is narrow.

### The boundary's first side effect (2026-09-04, same day)

With the scan gate in, the interview started running in English for a learner who had written nothing but Russian all session. Nothing was broken — the language had simply never been an explicit question. Earlier runs inferred it from the pages in the learner's other bases, and cutting off the reading removed the inference without replacing it.

**Language is now the first step, ahead of the greeting**, defaulting to the language the learner is writing in — a signal that sits in the conversation and costs no permission, and which was the better source even when the disk was readable. `Q7` keeps only what remains genuinely open: whether terms carry their original form on first appearance, and the layout.

The general lesson, written into the gate itself: **what the boundary takes away is not lost facts but unasked questions.** Anything earlier versions inferred by reading around — layout habits, what the learner already owns, the language — has to become something asked, not something guessed. Expect more of these as the gate stays in.

### Why 0.4.0 did not take effect, and what that exposed (2026-09-04)

The run after the language fix still spoke English. It was on `0.3.0`: skills load at session start, so a session that *updates* the plugin keeps running the instructions it began with. The fix was correct and simply had not arrived — which is worth remembering whenever a change appears not to work: check which version was actually in the model's context, not which is on disk.

What it exposed is real, though. **Almost everything the agent says happens before `learning-init` is ever invoked** — installing, reporting the preflight, announcing a blocker — and the skill body is not in context until then. A rule that lives only in the body governs none of that. The README covers the quick-start path and `INSTALL.md` covers whoever opens it; a session arriving by update had neither.

The one place in context from the start of a session is a skill's **`description`**, so the language rule now sits there in both skills, terse, in addition to the body. Anything that must hold *before* invocation belongs there or nowhere.

Also softened: a toolchain blocker is an **input to Q6, not a gate before the round**. The run halted to demand a Node decision from someone who had not yet been told what any of this was — putting the least interesting choice first and the orientation last. Only a blocker that stops the scaffold itself (no `uv`, no working `venv`) justifies stopping.

### An inference dressed as an observation (2026-09-04)

The language question shipped an option reading *"your global instructions and your other projects are written in Russian, so this looks like your working language."* The learner asked, reasonably, whether their projects had been read.

They had not. The session's transcript shows eight commands: `pwd` and `ls` in its own empty directory, `~/.claude/plugins`, `~/.claude/skills`, the plugin cache, and version probes. No path under the learner's projects directory was touched. **The boundary held.** The Russian came from two legitimate places — `~/.claude/CLAUDE.md`, which the harness loads into every session and which contains Cyrillic, and the working directory's own path.

The defect is the sentence, not the behaviour: *"your other projects are written in Russian"* was extrapolated from a path name and stated as fact. **This is worse for trust than an actual violation**, because the learner's only evidence is the claim itself, and the claim says they were read. A gate nobody can verify is worth little; a gate whose agent misreports its own reach is worth less than none.

Hence the rule now standing above the language question: **say where you got it, every time.** Auto-loaded context is named as such, something read is named as read and had to be inside the boundary, and a guess is marked a guess. A claim you cannot attribute is one to drop and ask about instead.

### Windows and macOS (2026-09-09)

A Windows test showed setup taking far longer than it should. The cause was not slowness anywhere in particular — **the interface was a Makefile**, and every line of it assumed a Unix shell:

| Assumed | On Windows |
|---|---|
| `make` | absent |
| `$(shell test -x .venv/bin/python …)` | no `test`, and the interpreter is `.venv\Scripts\python.exe` |
| `$(shell command -v python3)` | no `command -v`; `python3` is often a Store stub that opens the Store |
| `grep`/`awk` in the `help` target | absent |
| `setup_venv.py` hardcoding `bin/python` | wrong path, so the venv "existed" and had nothing in it |

Fixed by moving the logic into `runtime/scripts/tutor.py` — one stdlib dispatcher — and reducing the Makefile to sugar that forwards to it. The project gets a three-line `tutor.py` shim pointing at the runtime, which is a pointer and not a copy, so the architecture rule in §1 still holds. **No Makefile is generated on Windows at all**; `python tutor.py check` is the interface, and the scaffold writes the correct form into the project's own `CLAUDE.md` §0 so agents read it rather than assuming.

macOS needed less but not nothing: `make` there triggers the Xcode command line tools prompt when they are absent — a multi-minute download landing in the middle of setup — so `tutor.py` is preferred there too.

Verified on Linux for both paths, and the Windows branch of the scaffold was exercised by faking `os.name`, which proves the generation and not the execution. **Nobody has run this on a real Windows box yet** — that is the honest state.

Routing was propagated to the places that would otherwise forget: the preflight in `learning-init`, the command note in `learning-track` and `verifier`, `docs/INSTALL.md`, the README's agent block, and the entry in the user's global `~/.claude/CLAUDE.md`.

### Plain language, and who is being taught (2026-09-09)

Two changes that go together.

**The vocabulary was the plugin author's, not the learner's.** About seventy hits across the interview files — *itch*, *arbiter*, *harness*, *canon*, *preflight*, *corpus*, *domain layer*, *strictness*, *closure criterion* — and the live runs rendered those questions nearly verbatim, so the learner got all of it. `phase-1.md` was rewritten from scratch in plain wording and `phase-2.md` given the same pass; both are now zero-jargon. The durable fix is the translation table in `SKILL.md` → *How to talk to the learner*, which also states the target: **a curious fourteen-year-old teaching themselves, addressed with complete respect.** Plain words are not talking down, and the two are easy to confuse in the wrong direction.

The internal vocabulary stays in the instructions, where it is precise and useful. What changed is that it is now explicitly marked as *ours*, with a required translation before anything reaches a learner. `learning-track` and `concept-writer` carry the same rule, or the pages would drift back into specification prose while the interview stayed friendly.

**A short survey now follows the language question**: age band (skippable, defaults to 14–17 wording with adult respect), background *in the subject's own terms* rather than beginner/intermediate/advanced, and one of five tutor voices — mentor, coach, socratic, storyteller, reference — each offered with what it costs. The five were shaped against what public assistants converged on, GPT-5's Cynic/Robot/Listener/Nerd and Claude's Concise/Explanatory/Formal, which is reasonable evidence those are the axes people actually notice.

All three land in the domain layer as `learner.age_band`, `learner.background`, `tutor.style`, and **bind the page writer as well as the interview** — otherwise a warm interview hands over to pages that read like a datasheet. Background is the one that decides where the route starts; getting it wrong costs boredom or drowning, and both end the project.

One interaction worth keeping in view: **storyteller collides with the comparison rule.** That style produces analogies faster than any other, and every analogy still owes a section on where it stops working. Choosing it does not relax the rule, it makes that section the busiest on the page — and the learner is told so when they pick it.

### Standing

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
