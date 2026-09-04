# tutor-skills

A personal tutor you assemble for your own subject — mathematics, React, physics, chemistry, history.

Not a note-taking system and not a summariser. It builds a base with two layers and a rule that the machine, not you, decides how much of it is trustworthy.

**[Installation and first page →](docs/INSTALL.md)**

## What it makes

| Layer | What it is |
|---|---|
| `wiki/concepts/` | Atomic concepts. Every depth level inside **one** page, because the transition between levels is the teaching |
| `wiki/tracks/` | Route pages: the order of concepts and **why** that order |

A reference book read straight through is mush. A course cut into atoms loses the line. The second layer is what resolves that: concepts stay atomic and reusable across subjects, and the track holds the argument through them.

## The three ideas worth stealing even if you never install this

**An analogy without stated limits is worse than no analogy.** Every everyday-level explanation must be followed by a section on where the analogy breaks. Without it the picture installs itself as fact and obstructs for years, invisibly, because it never announced it was a simplification. This is enforced: a page carrying an analogy and no limits section fails the check.

**The trustworthiness tag is written by a script and never by a human.** The scale measures the presence of checks, not the confidence of whoever wrote the text. The moment it can be set by hand it drifts upward and stops meaning anything — and an inflated scale is worse than none, because it is still trusted.

**Independence, not the number two.** Two textbooks retelling one monograph are one source counted twice; so are two articles paraphrasing one documentation page. What independence *means* is a per-subject answer — different proofs, primary testimony against primary testimony, or **execution against documentation** — and the machine counts only sources that do not declare themselves derivative.

## The five types of check

Fixed in the core. A subject declares which it can attain; it never invents a sixth.

| | Buys you |
|---|---|
| `formal` | A guarantee — symbolic identity, type check, dimensional analysis |
| `behavioral` | An observation on one concrete version |
| `illustrative` | A refutation. A counterexample demonstrates; it does not prove |
| `attested` | That the source was **not misquoted** — not that the claim is true |
| `contested` | A page status: the sources disagree, and that disagreement is the content |

`attested` is what keeps the scale alive in subjects where nothing is executable. It is machine-checkable — the quoted words are on the cited page or they are not — and it is the only thing a machine can honestly certify about a documentary claim.

## How a subject gets configured

The core knows how to teach. It does not know your field. `/learning-init` interviews you and writes the **domain layer**: the arbiters, what a source is, what a check is, what "done" means here.

The interview runs in **two phases with a real page written in between**, and the split is the design: phase 1 asks what can be known before touching the material, phase 2 asks what only the material can tell you. Asked up front, "what counts as an independent source in your field?" gets a plausible answer that turns out wrong; asked after one page has been cited, it gets the real one. Pages written during phase 1 are capped at `draft` and recomputed when phase 2 closes.

The core stays in the plugin and updates with it. Only the domain layer is generated into your project — so improving the method reaches every base you have already started, instead of leaving you with several frozen forks of it.

## Problems

Three per concept by default, with fixed roles: holding the definition, applying the result, and **break the condition** — what falls apart when a hypothesis is removed. That third role repairs the deepest confusion in any subject, the one between a condition that carries load and a condition that is decoration.

A statement on its own is not enough, because a stuck learner with nothing to hold onto closes the page. So each problem carries **approach exercises** (short steps that check the tool is in your hands, not parts of the solution) and a **hint ladder** of three collapsed blocks: where to look, which tool, nearly the whole construction. Solutions live in a separate file, and links point at a specific heading rather than the file — otherwise, on the way to your own problem, your eye catches someone else's.

## Feedback

Corrections go into `audit/`, not into chat. What is said in a conversation dies with it; a note in `audit/` is anchored to a passage, processed as its own operation, and archived with its resolution — **including rejections, with the reasoning**. Nothing is deleted.

## Optional: learning from books

For subjects whose sources are stable works, the corpus capability adds a text index, full-text search, and automatic determination of the **printed-page offset** — a PDF's page 91 is the book's page 79, and a citation that ignores that is wrong by twelve pages, which means nobody can check it.

OCR output is for navigation only. Any wording that enters the base as a quotation is checked against the page image, because OCR mangles indices, quantifiers and Greek letters, and a mangled formula wearing a `verified` tag is the worst thing this system can produce.

## Status

**v0.1 — early.** The method was developed on one completed mathematics track and is being generalised; expect the domain layer's schema to move. See [NOTICE](NOTICE) for what this is built on, and [docs/INSTALL.md](docs/INSTALL.md) to start.

Requires Claude Code, Python 3.10+, and `make`. MIT licensed.
