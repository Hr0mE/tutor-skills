# Tracks — the layer that makes this a course

A reference book read straight through is mush. A course cut into atoms loses the
line. The `tracks/` layer is what resolves the contradiction: concepts stay
atomic and reusable, and the track holds the line through them.

Concepts are the bricks. **The track is the building**, and a track page that is
only a table of links has not been written yet.

## Why this order — the load-bearing section

For each step, one thing: **what it makes possible that was impossible before.**
Not "we need this later" but the specific door it opens.

Write it as prose, not as a list of dependencies. Dependencies are visible from
the `prereqs` fields; what is not visible, and what the learner cannot reconstruct
alone, is the reason someone chose *this* path through them rather than another
valid one.

## Find the arc that closes

The best tracks end by showing that several things met separately are one thing.

In the reference project, five theorems from five different courses — a covering
result, an extremum result, a function-space result, an existence theorem for
differential equations, and a complex-analysis result — turned out to be one
machine, presented five times and never once given a common name. The track closed
twice: at the point where the first theorem became a special case of a general
criterion, and again where the same counting formula reappeared with its index
taken to infinity.

That is the payoff, and it decides the order: arrange everything so the closure
lands.

**If there is no such arc, say so.** A track that is honestly a chain of
prerequisites is still worth walking. A fabricated epiphany is not, and the
learner will feel the fabrication precisely at the moment they were supposed to
feel the insight.

## The route table

Concept column and problems column stay **separate**, the second pointing at
`[[<page>#Problems]]`. Reading the theory and working the problems are two
different sittings; the second one should be reachable in one click rather than by
scrolling through material already read.

Carry the sources in the table too — seeing which arbiter backs which step is how
the learner spots the thin places.

## What counts as done

One sentence, from `closure.criterion`, phrased as a test the learner administers
to themselves and gets a yes or no from. Not coverage — coverage is not the goal
and never was. "Understands X" is not a criterion. "Can derive the key result on
paper from nothing, and solve three non-routine problems on it" is.

## Broken links are the plan

A track page links to concepts that do not exist yet. `make lint` reports them and
that is expected — **the dead links are the plan**. Do not create stub pages to
quiet the linter; a stub reads as coverage and hides the actual state of the base.
What to look at in the lint output is orphans and pages missing from
`wiki/index.md`.
