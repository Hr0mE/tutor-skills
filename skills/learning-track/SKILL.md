---
name: learning-track
description: >-
  Build and run a personal-tutor knowledge base on any subject — mathematics,
  React, physics, chemistry, history. Plans a track (the order of concepts and
  why that order), writes concept pages carrying every depth level in one file,
  builds problems with approach exercises and a collapsed hint ladder, keeps
  solutions out of sight, runs the checks that write the `confidence` tag, and
  processes the learner's feedback from audit/. Use when (1) planning or
  extending a learning track, (2) writing or revising a concept page, (3)
  building problems for a concept, (4) running verification and recomputing
  confidence, (5) working through audit/ notes. Requires a domain layer at
  .tutor/config.yaml — run learning-init first. Not for general note-taking or
  answering one-off questions. Write and speak in the base's own language, from
  `language` in the domain layer — never default to English because the
  instructions are in it.
---

# learning-track

A reference book read straight through is mush. A course cut into atoms loses the
line. This skill maintains both layers at once and that is the whole point:

| Layer | What it is | Why |
|---|---|---|
| `wiki/concepts/` | Atomic concepts, every depth level inside **one** page | Reused across subjects — a concept earned once is not rewritten for the next track |
| `wiki/tracks/` | Route pages: the order, and **why** that order | This is the course. Concepts are its bricks |

**Every session starts by reading** `CLAUDE.md`, `.tutor/config.yaml`, and
`wiki/index.md`. Without the domain layer, stop and send the learner to
`/learning-init` — the core does not guess what a source or a check means in a
subject it has not been told about.

**`privacy.scan` in that file is binding on you too.** The learner set it once,
before the interview; writing pages is not a reason to widen it. Where you need
something outside the boundary, ask for it by name and say what for — do not go
and look because it would have been convenient. Silently outgrowing a permission
is worse than never having asked for one.

## The subordinates

Dispatch these rather than doing the work inline. The isolation is not tidiness;
each one is isolated for a reason that breaks if you merge it.

| Agent | Owns | Why its own context |
|---|---|---|
| `track-planner` | Order of concepts, the justification, closure criterion | Thinks about the whole arc; page detail is noise to it |
| `concept-writer` | One page: the depth levels, where the analogy breaks, what breaks if a condition is dropped | Writes one atom; other pages are noise |
| `task-smith` | Problems, approach exercises, hint ladder, solutions in a separate file | **Must not see the solutions while writing the statements.** An agent that just wrote the walkthrough cannot write an honest hint ladder to it |
| `verifier` | `checks/`, check types, running `make check` | The only writer of `confidence`, in machine form as well as in rule |
| `auditor` | `audit/` — apply, partly apply, reject with reasons, archive | Reads criticism cold, without the author's attachment to their own page |

Agent definitions are in `agents/`. Give each one the domain layer and the
relevant `references/` file; do not paraphrase the rules to them.

## Operations

### `plan` — a track

Dispatch `track-planner`. It produces `wiki/tracks/<Name>.md` from
`templates/track.md`: the arc in a paragraph, the justification of the order, the
route table, and the closure criterion from `closure.criterion`.

The load-bearing section is **why this order**. A route table with no argument
under it is a reading list. Look for an **arc that closes** — a point where an
earlier result turns out to be a special case of a later one. In the reference
project five theorems from five different courses turned out to be one machine
that nobody had ever named; that closure is what made the track worth walking
rather than a list worth skimming.

Broken links to unwritten pages are **normal** here. They are the plan.

### `write` — one concept page

Dispatch `concept-writer` with the concept name and the track. It works from
`templates/concept.md` **as specialised for this subject** by `learning-init`,
not from the neutral one in the plugin.

Non-negotiable, enforced by `make check`:

- **An analogy without stated limits is forbidden.** A page with `origin:
  analogy` and no "where this analogy breaks" section fails. An analogy without
  limits installs itself as fact and gets in the way for years.
- **A depth level may be declared inapplicable with a reason, never silently
  skipped.** That is `levels_na` in the frontmatter.
- **Every claim carries a citation reaching the section or claim number**, not
  just the work. No source to hand → `sources: [{source: pending}]`, and the page
  stays `draft`.
- **A source that retells another declares `derives_from`** and buys no
  independence.

**Show the first page of a block on its own**, before writing the rest. The
template gets tested against live material, and it is cheaper to find the problem
once than in ten pages.

### `problems` — the ladder of approach

Dispatch `task-smith`. Read `references/problems.md` before you do.

One statement is not enough: a stuck learner with nothing to hold onto closes the
page. Hence two extra layers per problem — **approach exercises** (two or three
short steps that check the tool is in hand, not parts of the solution) and a
**hint ladder** (three collapsed blocks: where to look · which tool · nearly the
whole construction).

Collapsing matters. A visible hint kills the problem.

### `verify` — recompute the tag

Dispatch `verifier`, or just run it:

```bash
make check          # checks pages and rewrites `confidence`
make check-dry      # report only
```

**`make check` is the only way the tag changes.** Never write `confidence` or
`checks` into frontmatter by hand and never let a subordinate do it. The scale
measures the presence of checks, not the confidence of whoever wrote the text;
the moment it can be set by hand it drifts upward and stops meaning anything.

If the domain layer is at phase 1 or 2, every page is capped at `draft`. That is
correct, not a failure — say so when it surprises the learner.

### `audit` — the learner's feedback

```bash
make audit                                    # open notes, worst first
make audit-new P="page" T="exact quote" S=warn K=kind C="what is wrong"
```

Dispatch `auditor`. Every note ends in `audit/resolved/` with a `# Resolution`
section — **including the rejected ones, with the reasoning**. Nothing is deleted.
Feedback that lives in chat dies with the context; that is the entire reason the
directory exists.

### `lint` — the graph

```bash
make lint
```

Dead links to unwritten track pages are expected. Look at orphans and at pages
missing from `wiki/index.md`.

## Conventions that are not negotiable

- **No line wrapping in the source.** One paragraph is one line, however long.
  Obsidian's Live Preview is an editor: a wrap in the source shows as a real break
  mid-sentence. `make reflow-check` finds them, `make reflow` fixes them. Display
  formulas, table rows and `<!-- check:… -->` stay on their own lines.
- **Diagrams: mermaid only.** Never ASCII art.
- **Page length: 400–1200 words of connected prose.** Collapsed hint blocks do not
  count — they are opened one at a time, not read through. Past the limit, split
  into a subfolder with an `index.md`.
- **The solutions file is named differently from the concept.** While the names
  matched, a bare `[[Concept]]` link opened the solutions instead: with two pages
  of one name Obsidian picks the wrong one. The rule holds itself as long as the
  names differ.
- **Links to a solution point at the specific heading**, never at the file:
  `[[outputs/solutions/Solutions — X#Problem 2 — …|walkthrough of problem 2]]`.
  Otherwise, on the way to their own problem, the learner's eye catches someone
  else's.
- **No condescension.** The learner forgot; they did not fail to understand.

## References

- `references/page-format.md` — the depth levels and what makes each one work
- `references/problems.md` — roles, approach exercises, the hint ladder
- `references/tracks.md` — how to justify an order and find the arc
- `references/confidence.md` — the five check types and how the tag is computed
- `references/audit.md` — the feedback file format and how to process it
- `references/corpus.md` — book corpora: OCR, printed-page offsets, `make find`
