# Trustworthiness

| Tag | Means |
|---|---|
| `verified` | Enough independent sources **and** enough passing checks, per the domain layer |
| `sourced` | Sourced, but short of the bar — usually one independent source, or no check |
| `derived` | Worked out by the agent from material already in the base; no direct source |
| `draft` | Read with suspicion. Schema errors, a failed check, or a `pending` source |

## The tag is written by the machine. Always.

`make check` and nothing else. Not the author, not an agent, not a hurried edit.

The scale measures **the presence of checks**, not the confidence of whoever wrote
the text. As soon as it can be set by hand it drifts upward, and an inflated scale
is worse than none — because it is still trusted.

Corollary worth internalising: **a page that will not reach the tag it "should"
have is a finding, not an obstacle.** Report it. Never weaken a check, loosen a
threshold, or add a source that merely retells one already cited.

## Drafts are shown, not hidden

A page computed as `draft` gets a visible banner at the top, inserted by
`make check` and removed by it when the page earns a better tag. Hand-editing the
banner is pointless — it is regenerated.

The frontmatter tag alone is not enough, because nobody reads frontmatter.
Concealing which pages are thin conceals where the base needs work, and the
learner ends up trusting a page the system already knows is unreliable.

## The five types of check

Fixed in the core. A subject declares which it can **attain**; it never invents a
sixth.

| Type | What it buys |
|---|---|
| `formal` | A guarantee. Symbolic identity, type check, dimensional analysis, proof assistant |
| `behavioral` | An observation on one concrete version. Version-stamp it or it is not a check |
| `illustrative` | A refutation. A counterexample demonstrates; it does not prove |
| `attested` | That the source was **not misquoted** — not that the claim is true |
| `contested` | A page status, not a runner: the sources disagree, and that is the content |

`formal` and `illustrative` are kept apart so that `verified` on a topological
page does not read like `verified` on an algebraic one.

`attested` is what keeps the scale alive where nothing is executable. It is
machine-checkable — the quoted words either are on the cited page or they are not
— and it is the only thing a machine can honestly certify about a documentary
claim. **Restate its limit whenever a page leans on it**, because a learner who
reads attestation as truth-checking will over-trust the tag exactly where the
material is least certain.

`contested` is a first-class status, not a defect to be resolved later. In some
subjects a source conflict is a rare edge case; in others the disagreement between
sources *is* the field, and filing it under "open questions, pending resolution"
mis-describes the whole discipline.

## The runner declares the type. The page never does.

Markup is `<!-- check:<runner> <argument> -->` and carries no type. If pages could
name their own type, an author could write `check:formal` over a quotation and the
scale would become theatre — the exact hole that machine-written tags exist to
close.

## Independence, not the number two

Two textbooks retelling one monograph are one source counted twice. Two articles
paraphrasing one documentation page are one source counted twice. Mechanically
applying "two sources" in a field with derivative literature manufactures
`verified` tags backed by nothing.

The machine cannot judge independence. It counts sources that do **not** declare
`derives_from` — which forces the author to state the derivation graph, and
refuses to count what they admit is derivative. What independence *means* here is
`sources.independence` in the domain layer: different proofs, primary testimony
against primary testimony, or execution against documentation.

## A threshold change is a migration

Raise `min_independent_sources` in June and every page tagged `verified` in March
is wearing a tag it no longer earns. After **any** edit to `confidence.*`, run
`make check` and show what dropped. A silent demotion is a lie on a delay.

## The phase cap

While the domain layer is at phase 1 or 2, every page is capped at `draft`
whatever its sources and checks. Those pages were written against rules that did
not exist yet, so their tag is unearned by construction. Closing phase 2 lifts the
cap and recomputes them for real — and that recomputation is the moment the scale
becomes a measurement rather than a formality.
