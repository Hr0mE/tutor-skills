# From GitHub to your first page

Written for someone who already has Claude Code and has never installed a plugin. About twenty minutes, most of it spent answering questions about your own subject.

## What you are installing

Two skills and a small runtime. `learning-init` interviews you and builds the **domain layer** — what counts as a source in your field, what a check is, how many independent sources buy the top trustworthiness tag, what "done" means. `learning-track` then plans tracks, writes pages, builds problems, runs checks, and processes your corrections.

The core is subject-neutral. It knows how to teach; it does not know your subject. That gap is what the interview closes.

## 0. Prerequisites

- **Claude Code** — any recent version.
- **Python 3.10+** and **make**. Both are already on macOS and Linux.
- **Obsidian** — optional but recommended; the pages are written for it.
- **Tesseract and Poppler** — only if you are learning from scanned books. `brew install tesseract poppler` or `apt install tesseract-ocr poppler-utils`.

## 1. Install the plugin

In Claude Code:

```
/plugin marketplace add dmitrylyapin/tutor-skills
/plugin install tutor-skills@tutor-skills
```

The first command registers the repository as a marketplace; the second installs the plugin from it. Restart Claude Code if it asks.

To run from a local clone instead — for development, or before the repo is public:

```
/plugin marketplace add /absolute/path/to/tutor-skills
/plugin install tutor-skills@tutor-skills
```

## 2. Check that it took

```
/plugin
```

`tutor-skills` should be listed as installed. Ask Claude "what skills do you have?" and `learning-init` and `learning-track` should appear. If they do not, see **Troubleshooting** at the end.

## 3. Start the interview

Make an empty directory for the subject and open Claude Code in it:

```bash
mkdir ~/projects/react-learning && cd ~/projects/react-learning
claude
```

Then:

```
/learning-init
```

**Do not scaffold anything by hand first.** The skill lays out the tree itself, and does it differently depending on your answers — a subject learned from books gets machinery that a subject learned from live documentation does not need.

## 4. Phase 1 — six questions

You will get one round of numbered questions, each with a recommended answer. Answering "go with your recommendations" is a legitimate reply; object only where the recommendation is wrong for you.

An abridged real exchange:

> **Q1 — Subject, and what "I know this" would feel like.** What is being learned, and what is the itch?
> ➡️ Recommend naming the itch rather than a topic list.
>
> — React. I can write components but I copy patterns without knowing why they work. I want the "I've seen this before but never understood it" feeling gone.
>
> **Q2 — Corpus or live sources.** I see no PDFs on disk, so this looks like a live-documentation subject: citations reach a URL plus a **version**, and nothing is quoted from a book.
> ➡️ Recommend live sources, `require_version: true` — React 18 and React 19 are different claims about `useEffect`.
>
> — Yes.
>
> **Q3 — Depth levels.** All three, or does this subject not support one?
> ➡️ Recommend keeping all three and letting individual pages declare one inapplicable with a reason. An everyday analogy for `useEffect` earns its place; one for JSX syntax does not.
>
> — Agreed.
>
> **Q4 — Where problems come from.** React has no problem sets. What is the local shape of a problem?
> ➡️ Recommend a repository with a failing test. The "break the condition" role gets stronger here than in any book subject: remove the dependency array and you can watch it break.
>
> — Failing tests, yes.
>
> **Q5 — Strictness.** strict (2 independent sources + 1 passing check), standard, or light?
> ➡️ Recommend strict: everything in this subject is executable, so there is no excuse for a scale that everything passes.
>
> — Strict.
>
> **Q6 — Language and layout.** Pages in Russian with English terms on first appearance, default layout?
>
> — Yes.

Then the skill scaffolds, writes `.tutor/config.yaml` at **phase 1**, fills in `CLAUDE.md`, and specialises the page template for your subject.

## 5. What appeared

```
react-learning/
├── CLAUDE.md          ← the prose half of the schema
├── Makefile           ← points at the plugin runtime; does not copy it
├── .tutor/config.yaml ← the domain layer, phase 1
├── wiki/concepts/     ← concept pages
├── wiki/tracks/       ← route pages: the order, and why
├── outputs/solutions/ ← walkthroughs, kept out of sight
├── checks/            ← executable checks
├── audit/             ← your corrections
└── templates/         ← the page template, specialised for your subject
```

Install the one dependency:

```bash
make setup
```

The Makefile **points at the plugin** rather than copying it. That is deliberate: when the method improves, every project you have already started gets the improvement. Nothing here is a frozen fork.

## 6. Write one page — and expect `draft`

```
Use learning-track to write the page on useEffect
```

Then:

```bash
make check
```

It will say something like:

```
⚑ domain layer is at phase 1: every page is capped at `draft` until /learning-init closes phase 2.
⚪ draft     wiki/concepts/useEffect.md  (capped from verified)
```

**This is correct, not a failure.** The page was written against rules that did not exist yet — half the domain layer is still unanswered — so the tag is unearned by construction. It gets recomputed for real in a moment.

Read the page. What matters now is where it chafed: whether the everyday level was useful or padding, whether "what breaks if you drop a condition" had anything to put in it, whether the hint ladder had three distinguishable rungs or two collapsed into one.

## 7. Phase 2 — the questions that could not be asked before

```
/learning-init
```

It notices phase 1 is done, reads the page you wrote, and asks about **that page**:

> Your `useEffect` page cites the React docs twice — once from the reference and once from the learn guide. Under the rules from phase 1 those are two sources, so the page qualified as `verified`. They are not independent: the second retells the first.
>
> **Q1 — What independence means here.**
> ➡️ Recommend: in this subject **execution counts as the second source and a second document does not.** Two articles about `useEffect` are one source counted twice.
>
> — Yes, that is right.
>
> **Q2 — Which check types are attainable.** You produced one behavioral check. `formal` is unreachable here; `attested` is available if you pin quotations to versioned documentation.
> ➡️ Recommend `[behavioral, attested]`.
>
> **Q3 — Where the format bent.** The everyday level worked for `useEffect`. Will it work for a page on JSX syntax?
> ➡️ Recommend the rule: syntax pages declare `levels_na.everyday` with a stated reason. A rule, not a loosened limit — "skip it when it is hard" erodes the format within a year.
>
> **Q4 — What counts as done.** The book-subject version was "derive the result on paper and solve three non-routine problems". The React version?
> ➡️ Recommend: "can write a custom hook with correct cleanup and explain, without looking, why the dependency array is not an optimisation."
>
> **Q5 — Problem supply.** No problem sets exist. Author-written problems allowed, with the source field reading `author's own` and the answers pinned by tests.

Then `phase: complete`, and:

## 8. The recount

```bash
make check
```

```
🔵 sourced   wiki/concepts/useEffect.md
     ⤷ sources: 2, independent: 1
```

The page dropped from its provisional `verified` to `sourced` — the second citation now declares `derives_from` and buys no independence. **This is the moment the scale becomes a measurement.** A tag you can inflate by citing the same documentation twice is not measuring anything.

## 9. The daily loop

| | |
|---|---|
| `make check` | Recompute trustworthiness. **The only way the tag changes** |
| `make lint` | Graph health. Dead links to unwritten track pages are normal — they are the plan |
| `make audit` | Your open corrections, worst first |
| `make audit-new P="page" T="exact quote" S=error C="what is wrong"` | File a correction |
| `make reflow-check` | Find paragraphs that got hard-wrapped |
| `make find Q="query"` | Search the corpus (book subjects only) |

Corrections go through `audit/`, **not through chat**. Something said in a conversation dies with that conversation; a note in `audit/` is anchored to a specific passage of a specific page and gets processed as its own operation, with the resolution — including a rejection and its reasoning — archived permanently.

## Troubleshooting

**The plugin does not appear in `/plugin`.** The marketplace was added but the plugin was not installed — they are two commands. Run `/plugin marketplace list` to confirm the marketplace is registered, then `/plugin install tutor-skills@tutor-skills`.

**Claude does not use the skills.** Name them: "use learning-track to write the page on X". If that works but automatic invocation does not, the skill is installed and only the description matched poorly — no harm done.

**`make check` says "no domain layer at .tutor/config.yaml".** `/learning-init` has not been run, or was run in a different directory. The core refuses to guess what a source or a check means in your subject, and that refusal is deliberate.

**`ModuleNotFoundError: No module named 'yaml'`.** Run `make setup`.

**Every page is `draft` and nothing lifts it.** Look at the first line of `make check` output. If it says the domain layer is at phase 1 or 2, finish `/learning-init`. Otherwise read the `✗` lines: a missing `loc` on a source, a level neither written nor declared inapplicable, or an analogy without its "where this breaks" section will each hold a page at `draft` on their own.

**A page will not reach `verified` and you think it should.** Check `⤷ sources: N, independent: M`. If `M` is lower than `N`, some source declares `derives_from` and is not being counted — which is usually correct. The fix is a genuinely independent source, or an executable check, not a lower threshold.

**You changed a threshold in `.tutor/config.yaml`.** Run `make check` immediately. Pages tagged under the old rules keep their tag until they are recomputed, and a silent demotion is a lie on a delay.
