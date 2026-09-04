# audit/ — the feedback channel

The base is agent-written; it will be wrong sometimes. The sources are
human-written; they will contradict each other. `audit/` is how corrections
survive.

**Feedback given in chat dies with the context.** That is the entire reason this
directory exists, and the reason a correction should be filed rather than
mentioned — even when the agent is right there and could fix it immediately.

## Filing a note

```bash
make audit-new P="page" T="the exact quote from the page" S=warn K=source C="what is wrong"
```

| Flag | Meaning | Default |
|---|---|---|
| `P=` | Page name, part of a name, or a full path | required |
| `T=` | The **exact** quote, verbatim, markup and formulas included | `T=` or `L=` |
| `L=` | Line number, when the quote is awkward to copy | — |
| `S=` | Severity: `info` · `suggest` · `warn` · `error` | `warn` |
| `K=` | Kind, from `audit.kinds` in the domain layer | last entry |
| `C=` | The note itself, in one sentence | can be written in the file |

The script fills in `id`, `created`, `author`, `target`, `target_lines` and three
text anchors. Eleven fields, seven of them mechanical and three requiring escaping
that is close to impossible to type by hand over a formula — hence the command.

## Severity decides the queue, not the volume of irritation

Processed worst first: `error` → `warn` → `suggest` → `info`.

| | When |
|---|---|
| `error` | **The claim is wrong.** A statement, a citation, a page number, a conclusion |
| `warn` | **Looks wrong, check it.** Doubtful, ambiguous, does not match the source |
| `suggest` | **Would be better this way.** Rephrase, reorder, add a step |
| `info` | **A note for later.** Needs no edit now |

## Anchors, not line numbers

Lines drift as pages are edited. Every note carries `anchor_before`,
`anchor_text`, `anchor_after` — an 80-character window either side of the quoted
text. **Locate the target by the anchors**; a note applied to the wrong lines does
more damage than one left unprocessed.

## Processing

```bash
make audit          # the open queue, worst first
```

Four legitimate outcomes: **accept**, **partly accept**, **reject with reasons**,
**defer** (recorded in `CLAUDE.md` as an open question, note left open with a
comment saying what it waits on).

A well-argued rejection is a normal outcome. Accepting a note you believe is wrong
in order to be agreeable corrupts the page and teaches the learner that the
channel does not think.

Every processed note gets a `# Resolution` section, changes status, and moves to
`audit/resolved/`:

```markdown
# Resolution

2026-09-04 · accepted.
Theorem number corrected: 12 on page 79, not 78 — checked against the printed page.
Updated: wiki/concepts/X.md lines 47–48.
```

**Nothing is deleted. Rejected notes are archived too, with their reasoning.** The
record of what was considered and turned down is worth as much as the record of
what changed — without it the same objection returns every few months and gets
re-argued from nothing.

If a correction touches a claim that a check was pinning, re-run `make check`
rather than editing the tag.
