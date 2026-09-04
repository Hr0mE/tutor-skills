# The page format

One concept, one file, every depth level inside it. The levels are not three
audiences — they are one reader moving, and **the movement between them is the
teaching**. Split them across files and the transition, which is the whole
mechanism, disappears.

## 1. Everyday

An analogy from ordinary experience, marked `origin: analogy`. It has no source
by construction: it is invented, which is exactly why the next section is not
optional.

### Where this analogy breaks

Mandatory. `check_pages.py` fails a page that carries the marker without it.

The reason is not bureaucratic. **An analogy with no stated limits is worse than
no analogy at all** — it installs itself in the reader as a fact, and then
obstructs for years, invisibly, because it never announced that it was a
simplification. Name the exact point at which the picture stops working, and what
it distorts rather than merely omits.

**This is also the level most likely to be genuinely inapplicable.** An everyday
analogy for a lifecycle hook exists and earns its place; an everyday analogy for a
syntax rule does not. In documentary subjects it often inverts — the material is
everyday and it is the academic apparatus that needs the analogy. Declare it:
`levels_na: {everyday: "a syntax rule has no everyday counterpart"}`. With a real
reason, never silently.

## 2. Working

Definition. Statement. How it is actually used. The smallest example on which it
becomes visible why the thing exists at all.

The test of this level: someone who reads only it should be able to use the
concept correctly in the ordinary case, and should know that they have not been
told the whole story.

## 3. Academic

Exact statement with every condition. A **sketch** of the argument, not its full
text: the skeleton, what it rests on, and where the narrow place is. The narrow
place is the part worth remembering.

Then **Connections** — where this shows up in other courses. The highest-value
entries are the ones where the learner has already met the thing without being
told it was the same thing. That recognition is most of what a good base buys.

## What breaks if you drop a condition

| Drop | What stops working | Counterexample | Check |
|---|---|---|---|

Not decoration. This table is what repairs the confusion between a hypothesis
that carries load and a hypothesis that is there for tidiness — the confusion
that makes people misapply results for a decade. Every row gets a concrete
counterexample, and every counterexample gets an executable check.

## Length and splitting

400–1200 words of **connected prose**. Collapsed hint blocks do not count: they
are opened one at a time under duress, not read through.

Past the limit, split into `wiki/concepts/<topic>/` with an `index.md` — a short
overview plus one-line summaries — and one file per aspect. One fat file covering
seven aspects is unreadable, unlinkable, and impossible to file feedback against.
Seven focused files and an index give navigation, selective reading, clean
backlinks, and small audit targets.

## Mechanics

- **No line wrapping in the source.** One paragraph, one line, however long. In
  Obsidian's Live Preview — an editor, not a renderer — a wrap in the source shows
  as a real break mid-sentence, and "Strict line breaks" does not help because it
  only affects reading mode. Display formulas, table rows and `<!-- check:… -->`
  keep their own lines. `make reflow-check` finds violations; `make reflow` fixes them.
- **Mermaid for diagrams.** Never ASCII art: it rots and cannot be annotated.
- **KaTeX for formulas**, `$…$` and `$$…$$`.
- **Page names are human-readable.** Ordering lives in the track page, not in
  filename prefixes.
- **Terms get their English original on first appearance** in subjects whose live
  literature is English — otherwise nothing in the field stays readable later.
