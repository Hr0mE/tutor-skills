# Problems, and the ladder of approach

A statement on its own is not enough. **A stuck learner with nothing to hold onto
closes the page**, and closing the page is the failure mode the whole apparatus
exists to prevent. Hence three layers per problem.

## The roles

Fixed count and fixed roles, from `tasks.*`. The reference set:

1. **Holding the definition** — can they use it, not recite it.
2. **Applying the result** — the standard move, in unfamiliar clothes.
3. **Break the condition** — what falls apart when a hypothesis is removed.

The third role is the one that transfers furthest and is dropped most often
because problem sets rarely contain the type. Do not drop it. In code it is at its
strongest: remove the dependency array, delete the `key`, call the setter during
render — the break can be **executed and watched**, which no proof-based subject
allows. In documentary subjects it becomes the counterfactual.

## Approach exercises

Two or three short steps before the problem. **They are not parts of the
solution** — they verify the tool is in hand:

1. the definition on a familiar object,
2. the same move in unfamiliar surroundings,
3. the tool by itself, without the problem.

The diagnostic value is the point: if the exercises go smoothly the problem will
too; if the learner stalls on exercise 2, they know precisely what to go back and
relearn instead of concluding they are bad at the subject.

## The hint ladder

Three collapsed blocks, strictly increasing, never overlapping:

```markdown
> [!question]- Hint 1 — where to look
> Direction of search. Names no construction.

> [!question]- Hint 2 — which tool
> Names the move or object. Does not substitute it into the problem.

> [!question]- Hint 3 — nearly the solution
> The construction entire. The computation is left to do.
```

The `-` suffix collapses the block by default, and that is not cosmetic: **a
visible hint kills the problem.** The callout title stays on its own line.

Write every statement, exercise and hint **before** any walkthrough. Hints written
by someone who already holds the answer leak it at every rung.

## Where problems come from

From the sources, where the sources have them. Where they do not — and often they
do not, because books are written for readers already past the run-up — write your
own, under two obligations:

- the source field reads `author's own` **and says why it had to be**;
- the answers are pinned by executable checks in `checks/`.

An author's own problem must not be less checkable than a borrowed one. Record
where the corpus turned out thin in `CLAUDE.md`, so the gap stays visible instead
of being rediscovered every time.

Where a subject has computational problems, use them early: after a long gap the
hand needs warming before the argument does.

## Solutions

Separate file, `outputs/solutions/Solutions — <concept>.md`.

**The filename must differ from the concept's.** While they matched, a bare
`[[Concept]]` link from the track, the index and the Connections section opened
the solutions instead of the concept — with two pages of one name Obsidian picks
the wrong one. Keep the names distinct and the rule holds itself; no link needs a
full path.

Link **to the specific heading**, never the file:

```markdown
**Solution:** [[outputs/solutions/Solutions — X#Problem 2 — the compactness argument|walkthrough of problem 2]]
```

Otherwise, on the way to their own problem, the learner's eye catches someone
else's — and that problem is now spent.
