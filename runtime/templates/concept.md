---
title: <Concept name>
kind: concept
track: [<track slug>]
level: core                # core | prereq | application
status: normal             # normal | contested
confidence: draft          # ⚠ NEVER BY HAND — written by `make check`
checks: []                 # ⚠ NEVER BY HAND — written by `make check`
sources:
  - source: <work / URL / file in raw/books>
    loc: "<chapter, section, claim number — must reach the claim, not just the work>"
    page: <printed page, when the corpus capability is on>
    version: <when the field moves fast; React 18 and React 19 are different claims>
    # derives_from: <another source>   ← set this when the source retells another.
    # A source that derives from another buys no independence. Two textbooks
    # retelling one monograph are one source counted twice.
prereqs: ["[[<page>]]"]
unlocks: ["[[<page>]]"]
# levels_na:
#   everyday: "<why an everyday analogy does not apply here>"
#   ↑ A level may be declared inapplicable WITH A REASON. It may not be silently
#     skipped. Same shape as `checks: [n/a — not formalisable]`.
---

# <Concept name>

> **In one sentence.** <The point, no notation.>

## 1. Everyday level

`origin: analogy`

<An analogy from ordinary experience. It has no source by construction — it is invented, and that is exactly why the next section is mandatory.>

### Where this analogy breaks

<Mandatory whenever the block above exists; `make check` refuses the page without it. An analogy without stated limits is worse than no analogy: it installs itself as fact and gets in the way for years. Say at which point the picture stops working and what precisely it distorts.>

## 2. Working level

<Definition. Statement. How it is actually used. The smallest example on which it becomes clear why this thing exists at all.>

## 3. Academic level

<Exact statement with every condition. A sketch of the argument — not the full text, the skeleton: what it rests on, where the narrow place is.>

### Connections

- [[<other page>]] — <why this thing shows up there>
- <A course where you have already seen this without being told it was the same thing>

## What breaks if you drop a condition

| Drop | What stops working | Counterexample | Check |
|---|---|---|---|
| <condition> | <claim> | <concrete object> | `<!-- check:counterexample <name> -->` |

## Problems

Solutions live in `outputs/solutions/Solutions — <concept>.md`. Do not peek. The file is named differently from the concept on purpose: while the names matched, a bare `[[<concept>]]` link opened the solutions rather than the concept — with two pages of one name Obsidian picks the wrong one.

Each problem carries **approach exercises** and a **hint ladder**. The exercises are not parts of the solution; they check that the tool is in your hands. Hints are collapsed — open one at a time, and only when stuck.

### 1. <role: holding the definition>

**Source:** <problem set, page, number — or `author's own`, with why it had to be>

**Statement.** <…>

*Why this one:* <which specific intuition it hits>

**Approach exercises.**

1. <simplest: the definition on a familiar object>
2. <middle: the same move in unfamiliar surroundings>
3. <last step before the problem: the tool on its own, without the problem>

> [!question]- Hint 1 — where to look
> <direction of search, no construction>

> [!question]- Hint 2 — which tool
> <names the move or the object, does not substitute it into the problem>

> [!question]- Hint 3 — nearly the solution
> <the whole construction; the computation is left to do>

**Solution:** [[outputs/solutions/Solutions — <concept>#Problem 1 — <heading verbatim>|walkthrough of problem 1]] — after your own attempt, not before.

### 2. <role: applying the result>

<same structure>

### 3. Break the condition

<Same structure. This role most often needs an author's own problem: problem sets almost never contain the type, and it is the one that repairs the confusion between a condition that is load-bearing and a condition that is decoration.>
