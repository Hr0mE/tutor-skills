# Phase 2 — what only the material can tell you

Runs after at least one real page exists. **Open by reading that page and naming
what went wrong in it** — the friction is the agenda. If nothing went wrong, say
so and ask a shorter round; a smooth first page usually means the subject is
tamer than expected, not that the questions are unnecessary.

Six questions.

---

## Q1 — What independence means here

The core requires independent sources. It cannot judge independence — it can only
count sources that do not declare `derives_from`. This question fixes what the
learner should be declaring.

**The number two is a setting. Independence is the invariant.** Two textbooks
retelling one monograph are one source counted twice. So are two blog posts
paraphrasing the same documentation page. Mechanically applying "two sources" in
a field where everything descends from one authority produces `verified` tags
backed by nothing — the exact rot the machine-written tag exists to prevent.

Per-field answers worth offering:

| Field | Independent | Not independent |
|---|---|---|
| Mathematics | proofs by different means | a textbook and its own problem book |
| Fast-moving software | **execution vs documentation** | two articles restating the docs |
| History | primary testimony vs another primary | three textbooks off one monograph |
| Medicine, law | separate trials, separate rulings | a review citing the trial |

➡️ Recommend: write the definition into `sources.independence` as a sentence the
learner will actually re-read while citing, and — in fields where the literature
is derivative — recommend that **execution counts as the second source** and a
second document does not.

## Q2 — Which check types are attainable

The five are fixed: `formal`, `behavioral`, `illustrative`, `attested`,
`contested`. Ask which this subject can really produce, using the page just
written as evidence.

- **`formal`** — symbolic identity, type check, dimensional analysis, proof
  assistant. Physics and chemistry get unit checking almost free; do not skip it,
  it is cheap and catches a lot.
- **`behavioral`** — ran it on one version and watched. The whole of software.
  Always version-stamped; a behavioral check without a version is not a check.
- **`illustrative`** — a counterexample. Refutes, never proves. Marked as such so
  that `verified` on topology does not read like `verified` on algebra.
- **`attested`** — the source really says this. Machine-checkable against the
  corpus index. **This is the one that keeps the scale alive where nothing is
  executable.** It certifies the absence of misquotation, not the truth of the
  claim — say that out loud, because a learner who mistakes it for truth-checking
  will over-trust the tag.
- **`contested`** — a page status, not a runner. Sources genuinely disagree and
  the disagreement is the content of the page.

**`contested` deserves a direct question in the humanities.** In mathematics a
source conflict is a rare edge case to be resolved. In history, historiography
*is* the subject; a status under which disagreement files as "open question,
pending resolution" mis-describes the entire field. Ask whether disagreement here
is a defect or the material.

➡️ Recommend: declare only what was actually produced or clearly could be. An
aspirational `attainable_types` is how the scale dies — every page falls short of
a bar nobody can clear, and the learner starts ignoring the tag.

## Q3 — Where the format bent

Concrete, from the page just written:

- Did the everyday level work, or was it padding? (If padding: which kinds of
  concept in this subject should declare `levels_na.everyday`, and for what
  reason.)
- Did "what breaks if you drop a condition" have anything to put in it?
- Did the page fit 400–1200 words, or does this subject want a different size?
- Did the hint ladder have three distinguishable rungs, or did two collapse into
  one?

➡️ Recommend: record the answers as **rules with reasons**, not as loosened
limits. "Syntax pages declare `levels_na.everyday` because a syntax rule has no
everyday counterpart" is a rule. "Skip the everyday level when it is hard" is
erosion, and in a year the format will be gone.

## Q4 — What counts as done

The reference project's criterion: *derive the key result from scratch on paper,
and solve three non-routine problems on it.* Sharp, testable, and not coverage.

Ask for the local equivalent. It has to be something the learner can put
themselves against and get a yes or no. "Understands hooks" is not one. "Can
write a custom hook with correct cleanup and explain, without looking, why the
dependency array is not an optimisation" is.

➡️ Recommend: one sentence per track, in `closure.criterion`, written as a test
the learner administers to themselves. If they cannot state it, the track is not
yet designed — send it back to `track-planner` rather than settling for coverage.

## Q5 — Problem supply, now that it has been tried

Did the sources actually have problems at the right level for the first concept?
Nearly always partly no — the reference project found its main problem book
started at problem 18 with nothing on the axioms it opens with, because books are
written for people who are already past the run-up.

➡️ Recommend: set `tasks.author_allowed: true` with the two obligations
(`source: author's own` plus a stated reason; answers pinned by checks), and
record in `CLAUDE.md` where the corpus is thin, so the gap is visible rather than
rediscovered each time.

## Q6 — What you are deliberately leaving out

The question nobody thinks to ask, and the one that saves the most time later.

By now the learner has met the material and had ideas about the base: a formal
proof assistant, spaced repetition, a web viewer, a neighbouring topic that keeps
suggesting itself. Some of those they have already decided against, for reasons
that were good at the time.

**Record the rejections with their reasoning.** Not a wishlist — a list of things
considered and turned down, and why. Without it the same idea returns every few
months and gets re-argued from nothing, usually reaching the same answer at the
same cost.

This is the same principle the audit channel runs on: a rejected note is archived
with its reasoning rather than deleted, because the record of what was considered
and refused is worth as much as the record of what changed. Scope decisions
deserve the same treatment.

➡️ Recommend: a short section in `CLAUDE.md` — "deliberately out of scope" — with
one line of reasoning each. The reference project's entry for a proof assistant
reads roughly: *gives a real guarantee, but formalising even one theorem is weeks
of work, and the project would turn into learning the assistant instead of the
subject.* That is the shape: what it would have bought, and what it would have
cost.

---

## Closing phase 2

1. Update `.tutor/config.yaml`, set **`phase: complete`**.
2. Run `make check`.
3. **Show what changed.** Every page was capped at `draft`; now they get their
   real tags. Name the pages that did not earn what they were provisionally
   given, and what they are missing. This is the moment the scale becomes real,
   and it should be visibly a measurement, not a formality.
