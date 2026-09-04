# Phase 1 — what can be known before touching the material

Seven questions. Ask them in one round, each with a recommended answer. Before you
ask, **look**: at the learner's disk, their existing notes, the shape of their
subject's documentation. Half of Q2 and most of Q3 you can answer yourself.

---

## Q0 — Where the base goes

`scaffold.py` takes the root as an argument, so the session's own directory is not
automatically the right one. Where the scan boundary allows it, look for empty
candidates and name them; where it does not, ask outright and do not go looking —
this question is the first place the boundary bites.

The only thing this decides is where the learner will open Obsidian and run
`make check` for the next year — which makes the folder name the base's name in
practice.

➡️ Recommend a directory named after the subject, and say plainly if the session
is sitting somewhere provisional. A placeholder name tells them nothing in six
months, and bases get opened by folder name, not by their `CLAUDE.md` title.

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

**For a live subject there is a second half to this question: which version is
the version of record?** It is rarely the one installed. A learner running 18.3
who will write their next project on 19 should learn 19, with the places 18.3
differs marked on the page — otherwise the base teaches something that will not
exist in their next repository. Look at what is actually on their disk before
asking; the gap between installed and current is the whole question.

**A corpus subject has the same second half, in a nastier form: which edition, and
whose translation.** Page numbers do not survive a change of edition, and
translations diverge on substance rather than only on style. Where a body of work
has a canonical internal division — book, chapter, section, article, clause,
paragraph number — that division is the locator that survives republication, and
the page is a convenience on top of it. "Thucydides I.22" is checkable by anyone
holding any edition; "Thucydides, p. 47" is checkable by nobody else.

➡️ Recommend: check their disk before asking. A folder of PDFs answers the first
half. If corpus is on, turn `sources.require_page` on; if live, turn
`sources.require_version` on — an unversioned citation in a fast-moving field is
a claim about nothing — and pin the *current* release as canonical unless they
are maintaining something old on purpose. For a corpus subject, require the
edition and translation in the citation, and where a canonical division exists,
make `loc` carry it — the page then rides along as a convenience rather than
being the only handle.

## Q3 — The canon: who wins when two sources disagree

The single most consulted part of a learning base, and the one people forget to
decide until it is needed at an awkward moment. For each area of the subject:
**which work arbitrates?**

Ask it area by area, not once. A subject rarely has one authority — in the
reference project a real-analysis text arbitrates compactness in Rⁿ, a functional
analysis text arbitrates metric spaces, and a complex analysis text arbitrates
normal families. Each is wrong outside its area.

**In interpretive subjects the question splits in two, and merging them is the
mistake.** History, literary study, much of the social sciences: there is no
arbiter of *what actually happened*, and pretending otherwise puts a
`verified` tag on somebody's reading. Ask separately:

- **Who arbitrates what the source says?** The primary text, in a named edition.
  It settles wording and nothing else.
- **Who arbitrates how it is explained?** The secondary literature, by area — and
  different schools will arbitrate different areas, one being wrong outside its own.

Neither arbitrates the fact. Where the schools disagree, that disagreement is the
content of the page — `status: contested` — not a defect to be resolved before
writing. Say this out loud during the round: a learner who expects a single
authority will read the absence of one as the base being unfinished.

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
analogy is the mechanism behind it: a currency debasement wants a modern parallel,
a battle wants none.

**In any subject about the past, "where this analogy breaks" reads as
anti-anachronism**: not "the picture is imprecise" but "what makes this situation
categorically not ours". The failure mode is specific and durable — a modern
category quietly substituted for a historical one lodges as fact and distorts
everything downstream. Name that when specialising the template, so the section
gets written as a defence rather than as a disclaimer.

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

**A subject may need an obligatory element the core does not ship**, and adding one
is legitimate — `tasks.roles` is a domain field. Where sources are testimony
rather than proof, the usual addition is source criticism pinned to the first
role: who is speaking, to whom, to what end, and what they leave out. Without it
the subject degrades into memorising paraphrases. Add such an element as a
*standing requirement with a reason*, not as an occasional extra.

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

**Ask this one last, and only after the preflight.** `strict` demands a passing
check on every trusted page, so it is a promise about the machine, not about the
learner's ambition. Recommending it where the test runner cannot start — no
harness yet, a runtime too old, a toolchain not installed — produces a base where
every page sits at `sourced` forever and the learner concludes the method is
broken. It is not; the round was.

➡️ Recommend **strict** where the checks demonstrably run — meaning you have seen
the toolchain work, not inferred that it should. Where the subject is executable
in principle but not yet here, say so plainly and offer the honest sequence:
**standard now, build the harness as the first task, tighten to strict once a
check has actually passed.** Record it in `CLAUDE.md` so the tightening is a
scheduled step rather than something forgotten. And warn about the failure mode
of the loose settings: a scale that everything passes measures nothing.

## Q7 — Terminology and layout

The language itself was settled before this round began — by then you were already
conducting the interview in it. What is left is narrower and genuinely open.

**Do terms carry their original form on first appearance?** Not a translation
question: a base written in Russian that never shows *Völkerwanderung*, `useEffect`
or *translatio imperii* leaves the learner unable to search, and everything worth
reading next is under the original spelling. The cost is a page that stutters, so
it is a real trade rather than an obvious yes.

Then the layout: default is `wiki/concepts`, `wiki/tracks`, `outputs/solutions`,
`checks/`, `audit/`. Change only on a real reason.

➡️ Recommend: original form in parentheses at first appearance — for terms, key
names, and anything they will have to type into a search box — and the default
layout. Plus the line-break convention, one paragraph one line, if they read in
Obsidian: Live Preview is an editor and shows a source wrap as a real break
mid-sentence.

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
