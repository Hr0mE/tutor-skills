# Phase 1 — what can be known before touching the material

Seven questions. Ask them in one round, each with a recommended answer. Before you
ask, **look**: at the learner's disk, their existing notes, the shape of their
subject's documentation. Half of Q2 and most of Q3 you can answer yourself.

---

## Q1 — Subject, and what "I know this" would feel like

What is being learned, and what is the itch? The reference project's answer was
not a syllabus but a sentence: *"the feeling of «I used to know this but never
understood it» should be gone."* That sentence decided everything downstream —
it is why the base has depth levels at all, and why coverage is not the goal.

Push past "I want to learn X". Ask what they will be able to **do** that they
cannot do now, and what has failed before.

➡️ Recommend: name the itch, not the topic list. If they cannot, offer them the
choice between *coverage* (get through this material) and *repair* (fix specific
holes) — the two build different bases, and repair is usually the honest answer
for someone returning to a subject they once passed.

## Q2 — Corpus or live sources

Is this learned from a corpus of stable works — books, papers, monographs — or
from documentation that moves under you?

| | Corpus | Live |
|---|---|---|
| Examples | mathematics, physics, chemistry, history, law | React, Kubernetes, any SDK |
| Citation reaches | printed page + section | URL + **version** |
| Enables | `--corpus`: OCR index, printed-page offset, `make find`, `attested` checks | executing the thing |
| Staleness | none | months |

Some subjects are both: a physics track on a textbook plus current lab practice.
The capability is a toggle, not an identity — turn it on if any load-bearing
source is a book.

➡️ Recommend: check their disk before asking. A folder of PDFs answers this
question. If corpus is on, turn `sources.require_page` on; if live, turn
`sources.require_version` on — an unversioned citation in a fast-moving field is
a claim about nothing.

## Q3 — The canon: who wins when two sources disagree

The single most consulted part of a learning base, and the one people forget to
decide until it is needed at an awkward moment. For each area of the subject:
**which work arbitrates?**

Ask it area by area, not once. A subject rarely has one authority — in the
reference project a real-analysis text arbitrates compactness in Rⁿ, a functional
analysis text arbitrates metric spaces, and a complex analysis text arbitrates
normal families. Each is wrong outside its area.

Then two follow-ons:

- **Problem sets.** Which one is primary, and which supplies the warm-ups when
  the primary starts above the learner's head? These are usually different books.
- **Popular sources** — videos, blog posts, explainers. They are genuinely useful
  and they are not arbiters. Decide their place explicitly now, or they will
  quietly become the source of record for something.

➡️ Recommend: **name an arbiter per area, and admit popular sources into the
everyday level only, never outweighing the canon.** And say plainly that this
table is provisional: it is the thing phase 2 most often revises. In the
reference project the arbiter for one node had to change outright once the
material was reached — the theorem the plan assumed was in the main source turned
out not to be in it at all, and a different work took over that node. Expect that
and it is a finding; do not expect it and it reads as the method failing.

## Q4 — Depth levels

The core ships three: everyday (an analogy, with its limits stated), working
(definition, use, smallest example), academic (exact statement, sketch of the
argument, connections to other courses).

Ask which of these the subject supports and what they are called here. Some
subjects rename them; some cannot support one of them at all.

**The everyday level is the one that breaks.** An everyday analogy for `useEffect`
exists and helps. An everyday analogy for JSX syntax does not. In history the
everyday level often inverts — the material *is* everyday, and what needs the
analogy is the academic apparatus.

➡️ Recommend: keep all three, and set the expectation that individual pages will
declare one inapplicable with a reason. That is `levels_na`, and it is enforced:
a level can be dropped with a stated reason, never silently.

## Q5 — Where problems come from

Three per concept in the reference project, with fixed roles: holding the
definition · applying the result · **break the condition**.

Ask: does this subject have problem sets? Are they pitched where the learner is?
What is the local shape of a problem — a proof, a computation, an essay, a repo
with a failing test, a document to read against a claim?

The third role transfers further than it looks. In code it becomes *remove the
dependency array, drop the `key`, call the setter during render* — and the break
can be **run and watched**, which no mathematics problem can do. In history it
becomes the counterfactual. Keep it.

➡️ Recommend: take from the sources where the sources have them, write your own
where they do not — with two obligations. The source field says `author's own`
and why it had to be, and its answers are pinned by executable checks in
`checks/`. An author's own problem must not be less checkable than a borrowed one.

## Q6 — Strictness

What has to be true for a page to be trusted? Two dials:

- `min_independent_sources` — how many, **counting only sources that do not
  declare `derives_from`**.
- `min_passed_checks` — how many checks must pass.

Offer three settings rather than asking for numbers:

| | sources | checks | fits |
|---|---|---|---|
| **strict** | 2 | 1 | a subject with real arbiters and something executable |
| **standard** | 2 | 0 | a subject with arbiters and little to execute |
| **light** | 1 | 0 | exploratory reading, or a field with one authority |

➡️ Recommend **strict** wherever anything at all is executable, and warn plainly
about the failure mode of the others: a scale that everything passes measures
nothing. If they pick light, say what they are giving up.

## Q7 — Language and layout

Output language (the core's instructions are English; pages are written in
whatever the learner reads in). Whether terms get their English original on first
appearance — recommend yes for any subject whose live literature is in English,
which is nearly all of them.

Then the layout: default is `wiki/concepts`, `wiki/tracks`, `outputs/solutions`,
`checks/`, `audit/`. Change only on a real reason.

➡️ Recommend: their language for pages, English terms in parentheses on first
appearance, default layout. And the line-break convention — one paragraph, one
line — if they read in Obsidian, because Live Preview shows a source wrap as a
real break mid-sentence.

---

## After the round

1. Run `scaffold.py`.
2. Write `.tutor/config.yaml` with **`phase: 1`**.
3. Fill in the prose half of `CLAUDE.md`.
4. Specialise `templates/concept.md` into the subject's own vocabulary.
5. Hand off to `learning-track` for exactly **one** page, and say why it will
   come out `draft`.

Do not attempt phase 2 in the same breath. The whole design rests on a real page
sitting between the two.
