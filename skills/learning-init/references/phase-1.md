# Phase 1 — what can be decided before touching the material

Eight questions. Ask them in one round, each with a recommended answer.

**Everything below is a note to you, not a script to read out.** Terms in `code` are field names you will write into the config; they are not words to say to the learner. Put every question in the plain wording required by `SKILL.md` → *How to talk to the learner*, pitched at the age, background and style just collected.

Before you ask, **look** — within the boundary the learner set — at their disk, their notes, the shape of their subject's documentation. Q0 and half of Q2 you can often answer yourself.

---

## Q0 — Where should the base live?

`scaffold.py` takes the folder as an argument, so wherever the session happens to be open is not automatically the right place. Where the boundary allows it, look for empty candidates and offer them; where it does not, just ask, and do not go looking — this is the first question the boundary touches.

Say it plainly: *"Which folder should I set this up in? You'll be opening it most days, so a name that still means something in six months is worth more than it looks."*

➡️ Recommend a folder named after the subject, and say so if the session is sitting somewhere temporary. Bases get opened by folder name, not by what is written inside them.

## Q1 — What do you want, and how will you know you have it?

**The subject itself is already settled** — either it was named in the sentence that deployed this, or it was asked outright before the survey (`SKILL.md` → *Then, if you do not know the subject, ask what it is*). Do not ask for it again here; open the question with it: *"So: React. What's bugging you about it?"* What is still open is the goal.

Not a topic list. What is annoying them right now: what they keep getting wrong, what they can half-do, what they look up every single time.

Ask in those words: *"What's bugging you about this subject? Not the topics — the thing that keeps tripping you up."*

Two shapes of answer, and they build different bases: **get through the material** (start to end of a course) versus **fix specific holes** (things they half-know). For someone returning to a subject they once passed, the second is almost always the honest one.

➡️ Recommend asking for the annoyance rather than the syllabus. If they cannot name one, offer the two shapes and let them pick. Whatever they say is what the whole base aims at, so push once if the first answer is vague.

## Q2 — Do you learn this from books, or from things that change?

| | Books and papers | Documentation that moves |
|---|---|---|
| Examples | maths, physics, chemistry, history, law | React, Kubernetes, any library |
| A reference points at | the printed page and section | a web page **and a version number** |
| Turns on | `--corpus`: text search across your books, page numbers worked out automatically, quote-checking | running the thing to see what it does |
| Goes stale | never | in months |

Some subjects are both. It is a switch, not an identity: turn it on if any important source is a book.

**There is a second half to this, and it is the half people forget.**

For a subject that moves: **which version counts?** Rarely the one installed. Someone on an old version who will write their next project on the current one should learn the current one, with the differences marked. Otherwise the base teaches something that will not exist next month.

For books: **which edition, and whose translation?** Page numbers do not survive a new edition, and translations differ in meaning, not only in wording. Where a work has its own internal numbering — book, chapter, section, article, paragraph — *that* is the reference and the page is a convenience on top. "Thucydides I.22" can be checked by anyone holding any edition; "Thucydides, page 47" can be checked by nobody.

➡️ Look at their disk before asking; a folder of PDFs answers the first half. For books, turn on `sources.require_page`, ask for edition and translation in every reference, and put the work's own numbering in `loc` where it has one. For things that move, turn on `sources.require_version` and pin the current release unless they are deliberately maintaining something older.

## Q3 — When two sources disagree, who wins?

Every subject has this moment, and settling it in advance saves an argument later. Ask area by area, not once for the whole subject: a book is usually reliable on one part and wrong outside it.

**In subjects that interpret rather than prove — history, literature, much of social science — this splits in two, and merging them is the mistake.** No book settles *what actually happened*. So ask separately:

- **Who settles what a source says?** The original text, in a named edition. It settles wording and nothing else.
- **Who settles how it is explained?** The later scholarship, by area.

Neither settles the fact. Where explanations disagree, **the disagreement goes on the page as content** — `status: contested` — rather than being hidden until someone picks a winner. Say this out loud, or a learner expecting a single authority will read its absence as the base being half-finished.

Two follow-ons:

- **Where do practice problems come from?** Which collection is the main one, and which supplies easier warm-ups when the main one starts above their head? Usually different books.
- **Videos, blog posts, popular books.** Genuinely useful, and not authorities. Decide their place now, or one of them quietly becomes the source of record.

➡️ Recommend naming one source per area, and letting popular sources into the everyday explanations only, never outweighing the main ones. **Say plainly that this list is provisional** — it is what phase 2 rewrites most often. In one real base the source the plan assumed contained a theorem turned out not to contain it at all, and another book took over that topic. Expected, that is a useful finding; unexpected, it reads as the method failing.

## Q4 — Which levels of explanation does this subject support?

Every page carries the same three in order, and moving between them is most of the teaching:

- **Everyday** — a comparison with something ordinary, plus a section saying where the comparison stops working.
- **Working** — the definition, how it is used, the smallest example showing why it exists.
- **Full** — the exact statement with all its conditions, how it works underneath, and where the same thing shows up in other subjects.

**The everyday level is the one that breaks.** A comparison for "what an effect does" helps; a comparison for a piece of syntax does not. In history it inverts — the material is already everyday, and what needs the comparison is the machinery behind it: a currency collapse wants a modern parallel, a battle wants none.

**In any subject about the past, "where the comparison stops working" means one specific thing: what makes that situation categorically not ours.** Quietly swapping a modern idea for an old one lodges as fact and bends everything after it. Say that when adapting the page template, so the section is written as a guard and not as a disclaimer.

➡️ Recommend keeping all three, and setting the expectation now that some pages will mark one as not applicable *with a reason*. That is `levels_na`, and it is enforced: a level can be dropped for a stated reason, never silently.

## Q5 — What does a practice problem look like here?

Three per topic by default, each doing a different job: **use the definition** · **apply the result** · **break it on purpose**, removing one condition to see what falls apart.

Ask whether the subject has problem collections at all, whether they start where the learner is, and what a problem physically *is* here: a proof, a calculation, an essay, a small project with a failing test, a document to read against a claim.

The third job travels further than it looks. In programming it becomes *delete the dependency list, remove the key, change state during a render* — and the breakage can be **run and watched**, which no proof allows. In history it becomes "what if this had not happened". Keep it.

**A subject may need a fourth thing the core does not ship, and adding one is fine.** Where sources are testimony rather than proof, the usual addition is questioning the source itself: who is speaking, to whom, to what end, and what they leave out. Without it the subject decays into memorising retellings. Add it as a standing requirement with a reason, not an occasional extra.

➡️ Recommend taking problems from the books where the books have them and writing your own where they do not, under two conditions: the source line says `author's own` **and why it had to be**, and the answers are pinned by something runnable in `checks/`. A problem you wrote must not be less checkable than one you borrowed.

## Q6 — How strict should the trust mark be?

Every page carries a mark saying how well-supported it is, and **a script decides it, never a person**. Two dials:

- how many sources are needed, counting only ones that **do not simply repeat each other**;
- how many automatic checks must pass.

Offer settings, not numbers:

| | sources | checks | fits |
|---|---|---|---|
| **strict** | 2 | 1 | reliable reference works, and something that can be run or verified |
| **standard** | 2 | 0 | reliable reference works, little that can be run |
| **light** | 1 | 0 | reading around a subject, or a field with a single authority |

**Ask this last, and only after the preflight.** `strict` is a promise about the machine, not about ambition. Recommend it where the checks cannot actually run — no test setup yet, a runtime too old, a tool missing — and every page sits at the middle mark forever while the learner concludes the method is broken. It is not; the round was.

➡️ Recommend **strict** where you have *seen* the checks run, not where you assume they could. Where the subject could be checked but the machine is not ready, say so and offer the honest order: **standard now, get the checking working as the first task, tighten later once a check has actually passed.** Write that into `CLAUDE.md` so tightening is a scheduled step and not a forgotten intention. And name the cost of the loose settings: a mark that everything gets is measuring nothing.

## Q7 — Original spellings, and folder layout

The language was settled before this round; you have been speaking it all along. What is left is narrower.

**Should terms keep their original spelling the first time they appear?** Not a translation question. A base written in Russian that never once shows `useEffect` or *Völkerwanderung* leaves the learner unable to search for anything, because everything worth reading next is under the original spelling. The cost is a page that reads less smoothly — a real trade, not an obvious yes.

Then the folders: by default `wiki/concepts`, `wiki/tracks`, `outputs/solutions`, `checks/`, `audit/`. Change only for a real reason.

➡️ Recommend the original spelling in brackets at first appearance — for terms, names, anything they will type into a search box — and the default folders. Plus the one-line-per-paragraph rule if they read in Obsidian: its editing view shows a line break in the file as a real break mid-sentence.

---

## After the round

1. Run `scaffold.py`.
2. Write `.tutor/config.yaml` with **`phase: 1`**, including what the survey collected: `learner.age_band`, `learner.background`, `tutor.style`.
3. Fill in the prose half of `CLAUDE.md`, **in the learner's language**.
4. Adapt `templates/concept.md` to the subject's own vocabulary — and to the level and style just chosen.
5. Hand off to `learning-track` for exactly **one** page, and say why it will come out marked as a draft.

Do not attempt phase 2 in the same breath. The whole design rests on a real page sitting between the two.
