---
name: learning-init
description: >-
  Interview the learner and assemble the domain layer of a personal-tutor
  knowledge base — the arbiters, what counts as a source, what a check is, how
  many independent sources buy `verified`, and what "done" means in this
  subject. Runs in two phases with a real page written in between, because the
  answers about verification and canon are guesswork until the method has hit
  actual material. Use when (1) starting a new learning project on any subject
  — mathematics, React, physics, chemistry, history, (2) closing phase 2 after
  the first page exists, (3) revising the domain layer of an existing project
  when the method has started to strain. Not for writing pages: that is
  learning-track.
---

# learning-init — assembling the domain layer

The core of this plugin is subject-neutral. It knows *how to teach*: depth
levels on one page, a trustworthiness tag no human may write, a route that
explains its own order, problems with a hint ladder, an audit channel.

It does **not** know your subject. It does not know whether "two independent
sources" means two independent proofs, two primary documents, or documentation
plus a passing test. It does not know whether an everyday analogy is possible
for your material. Those answers are the **domain layer**, and this skill
produces them by interviewing the learner.

## The two phases, and why the split is where it is

**The split is not "few questions then more questions". It is: phase 1 asks what
can be known before touching the material; phase 2 asks what only the material
can tell you.**

A learner asked up front "what counts as an independent source in your field?"
will give a plausible answer and it will be wrong. The real answer arrives the
first time they try to cite something and the rule does not fit. In the reference
project the discovery was that the main problem set starts at problem 18 and has
nothing at all on the axioms it opens with — a fact no interview could have
produced, and one that changed where problems come from.

```
/learning-init  →  phase 1 interview  →  scaffold + config(phase: 1)
                                              ↓
                              learning-track writes ONE page
                                              ↓
/learning-init  →  phase 2 interview  →  config(phase: complete)
                                              ↓
                                 make check — recomputes every page
```

**Pages written during phase 1 are capped at `draft`** by `check_pages.py`, whatever
their sources and checks say. Their tag is unearned by construction: the rules it
would be measured against did not exist yet. Closing phase 2 lifts the cap and
recomputes them for real. Say this to the learner when the first page comes out
`draft` — otherwise it reads as a failure.

## How to interview

Not a form. A design tree worked in **rounds**: ask everything whose prerequisites
are settled, then wait. The technique that makes this bearable:

**Put a recommended answer under every question.** It turns an interrogation into
a conversation — "go with your recommendations" is a cheap answer, and the learner
can object to exactly the one that is wrong for them. A question with no
recommendation is work you have pushed onto the person you are supposed to be
helping.

**Render every question in exactly this shape:**

```
❓ **Q3 — The canon: who wins when two sources disagree**

<the question, with the evidence you gathered and the options>

➡️ <the recommended answer>
```

The ❓ makes the questions findable when the round is long, and **the
recommendation goes on its own line, never trailing the question text**. Run them
together and the learner has to parse where the asking stops and the advice
starts — on a round of seven that is the difference between answering and
skimming.

**Close the round by saying how cheaply it can be answered.** Spell out the
shortcut in words, because a learner who does not know it exists will either
write seven paragraphs or abandon the round:

> Answer by number, as briefly as you like. **"1–7, go with your recommendations"
> is a complete answer** — take it whole and object only where one is wrong for
> you, e.g. *"1–7 by your recommendations, except Q5: the problems should come
> from …"*.

A recommendation you would not be willing to have accepted wholesale is not
finished. Write each one so that "go with it" is a decision you would defend.

Number them. Keep each question to a decision that changes what gets built.
Find facts yourself — read their existing notes, look at the books on disk, check
what the documentation for their framework actually looks like. **Never ask the
learner for anything you could look up** *within the boundary they set below*.
Outside it the rule inverts: ask, and say why you are asking rather than looking.

Ground every question in their subject. "What is a source in your field?" is
unanswerable; "You named Kolmogorov–Fomin and Zorich — when they state the same
theorem differently, which one wins?" is answerable.

## Open with the orientation. Always.

**Before the first question, every time — not only when you have just installed the plugin.** The learner may arrive by any route: a fresh install, an update, a second session, a project someone else set up. If the orientation lives only in the deployment instructions it fires on exactly one of those paths, and on the others the person meets seven questions with no idea what they are for.

Four parts. Adapt the wording to the subject; keep all four.

1. **What is installed and reachable** — the two skills, the version, and that skills appear only after a session restart.
2. **What this is.** Not a notes folder and not a summariser. A base with two layers: atomic concept pages, each carrying every depth level in one file, and route pages that argue for the order they put those concepts in. Problems come with approach exercises and a collapsed hint ladder; solutions live apart so you cannot peek. How much of it is trustworthy is decided by a script — `make check` owns that tag, and it measures whether checks exist, not how confident anyone felt.
3. **What they can do with it.** Plan a track and see the argument for its order. Write pages and have unsourced claims refused. Get problems that break on purpose, so they can watch what the condition was holding up. File a correction against a specific line and have it answered — applied or argued down, and archived either way.
4. **What happens now.** The questions, then the project gets laid out, then one page. **That page will come out `draft`, and that is correct, not a failure** — half the rules it would be judged against do not exist yet. The second round, the one that can only be asked after real material has pushed back, lifts the cap and re-scores everything.

Then the preflight results, then the round.

## Then ask what you may look at. Before looking.

The interview is only good because it is grounded in what is actually on the
machine — books on disk, an existing project in the subject, how the learner's
other bases are laid out. That is also a stranger reading through someone's
work. **They have to be asked, and asked before the reading, not after.**

Put it as a structured multiple-choice question with checkboxes, not as prose —
this is a gate, not a conversation, and it should cost one click.

**Question 1, single choice — how far may I look?**

| Option | Means |
|---|---|
| **This directory only** (recommend) | The folder the base will live in, and nothing above or beside it |
| This directory plus folders I name | They list them; you touch nothing else |
| My whole projects directory | Free run of the parent |
| Nothing — ask me instead | You look at no files at all and ask for everything |

**Question 2, multiple choice — what may I read inside them?**

File and folder names only · contents of documents and notes · source code ·
git history.

**State the trade-off in the question itself.** Narrower means a longer round and
more questions whose answers were sitting on the disk — the method still works,
it just asks more. Left unsaid, a learner who restricts the scan reads the extra
questions as the tool being poor.

Three rules that make the gate real rather than decorative:

- **Ask before enumerating.** Listing a parent directory to build the checkbox
  options is itself the scan being consented to. Offer the choices generically;
  only after they pick "folders I name" do you go and list anything.
- **Default to the narrowest** whenever the question cannot be put — a
  non-interactive run, no answer. Never widen by assumption.
- **Record it in the domain layer** under `privacy.scan`, and honour it in later
  sessions instead of re-asking or, worse, quietly forgetting. `learning-track`
  reads the same field.

And be exact about what this is: **a rule you follow, not a sandbox.** The
tooling in `runtime/` never reads outside the project root — every path is
resolved from it — but the boundary above governs *your* reading, and it holds
because you hold it. Say so rather than implying an enforcement that does not
exist.

Note that Q0 of the round — where the base should live — depends on this answer.
Under "this directory only" you cannot go looking for better-named empty
candidates; ask instead.

## Before phase 1: preflight

Check what the machine can actually do, and report it with the greeting. This part
needs no permission — it asks the machine what tools exist (`uv`, a runtime, a
compiler, Tesseract), not the learner's files what they contain.
This is not ceremony — **the answers to Q6 depend on it**, and finding out later
that the checks cannot run turns the trustworthiness scale into decoration.

- `uv` present, or a `python3` whose `-m venv` can bootstrap pip. Without one of
  the two, `make setup` cannot build the project's environment.
- For a subject whose checks are executable: does its toolchain run *here*? A
  test runner that needs Node 20 on a machine with Node 18 is a blocker for
  `strict`, not a detail to mention in passing.
- Whatever else the subject leans on — a compiler, a typechecker, Tesseract for a
  book corpus.

Report the blockers **before** asking Q6, and let them change the recommendation.

## Phase 1

Read `references/phase-1.md` for the full question set with recommended answers.
Seven areas: subject and goal · corpus or live sources · **the canon** (who
arbitrates each area, which problem sets, where popular sources are admitted) ·
depth levels · where problems come from · strictness · language and layout.

Output of phase 1:

1. `scaffold.py <root> "<Subject>" [--corpus]` — the tree, the Makefile pointing
   at the plugin runtime, the neutral templates.
2. `.tutor/config.yaml` with `phase: 1` — see `references/domain-layer.md`.
3. `CLAUDE.md` — the prose half of the schema, filled in from the interview.
4. `templates/concept.md` — the neutral template **specialised for this subject**:
   level names in the subject's own vocabulary, the problem roles as they read
   here, the "what breaks if you drop a condition" table renamed if the subject
   calls it something else.

Then hand off: "Now write one page — `learning-track` on the concept you would
start with. It will come out `draft`; that is correct."

## Phase 2

Read `references/phase-2.md`. Runs only after at least one real page exists, and
the questions are drawn **from that page**, not from a list. Six areas: independence · attainable check
types · where the format bent · closure criterion · problem supply · **what is
deliberately being left out**, recorded with its reasoning so the same idea is not
re-argued from nothing every few months.

Open phase 2 by reading the page that was written and naming what went wrong in
it. That is the material the whole phase is about.

Output of phase 2:

1. `.tutor/config.yaml` updated, `phase: complete`.
2. `make check` — every page recomputed with the cap lifted. Show the diff in
   tags and say plainly which pages did not earn what they were provisionally
   given.

## Revising an existing domain layer

The domain layer is **hand-editable on purpose** — it is the learner's judgement
about their own field, unlike `confidence`, which is a machine conclusion. When
they edit it or ask you to, the rule is:

**A change to the thresholds is a migration.** Raise `min_independent_sources`
in June and every page tagged `verified` in March is now wearing a tag it does
not deserve. Always run `make check` straight after, always show what dropped,
never let the change land silently.

## The five types of check are fixed

`formal` · `behavioral` · `illustrative` · `attested` · `contested`. A domain
declares which of them it can **attain**; it never invents a sixth. If a subject
seems to need one, that is a finding about the core worth reporting, not a
config value to make up.

The one to reach for in fields with nothing to execute is **`attested`**: it
verifies not that the claim is true but that the source was not misquoted —
the only thing a machine can honestly certify about a documentary claim, and
enough to keep the scale alive in history, law, or medicine.
