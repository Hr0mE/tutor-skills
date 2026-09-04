# The domain layer — `.tutor/config.yaml`

Everything the core cannot know about a subject. Written by `learning-init`,
**hand-editable afterwards on purpose**: it is the learner's judgement about
their own field, unlike `confidence`, which is a machine conclusion about a page.

> A change to `confidence.*` is a migration. Run `make check` immediately after
> and show what dropped. Otherwise pages keep wearing tags they no longer earn.

## Full schema

```yaml
schema_version: 1
phase: complete            # 1 | 2 | complete — while 1 or 2, every page is capped at draft
subject: "Real analysis — compactness"
language: ru               # language of the pages; the core's own instructions stay English

layout:
  wiki: wiki               # where check_pages.py looks for pages

schema:
  kinds: [concept, track, prereq, solutions]
  extra_required: [track]  # frontmatter fields this subject additionally demands

# ── what a source is here ───────────────────────────────────────────────
sources:
  resolver: corpus         # corpus | url | none
  require_loc: true        # a citation must reach the claim, not just the work
  require_page: true       # printed page (corpus subjects)
  require_version: false   # set true for anything that moves: React 18 ≠ React 19
  independence: >-
    Two sources are independent when they establish the claim by different means.
    A textbook and its own problem book are one source. Where the literature is
    derivative, execution counts as the second source and a second document
    does not.

# ── what buys a tag ─────────────────────────────────────────────────────
confidence:
  min_independent_sources: 2      # counts only sources WITHOUT `derives_from`
  min_passed_checks: 1
  attainable_types: [formal, illustrative, attested]

# ── how a check actually runs ───────────────────────────────────────────
# The runner declares the TYPE. The page never does — otherwise an author could
# write `check:formal` over a quotation and the scale would be theatre.
runners:
  sympy:
    type: formal
    kind: python-call
    module: checks/_sympy.py     # relative to the project root
    entry: run                   # called as run(argument) -> bool | (bool, message)

  counterexample:
    type: illustrative
    kind: python-dir
    directory: checks            # scanned for functions named prefix + argument
    prefix: test_

  vitest:
    type: behavioral
    kind: shell
    command: "npx vitest run -t {arg}"   # exit 0 = passed
    timeout: 300

  # `attested` is built into the core and needs no declaration. It verifies that
  # a quoted string really occurs in the cited source's text index.
  # Markup:  <!-- check:attested 0 "the exact words" -->

# ── the depth levels of this subject ────────────────────────────────────
# A level absent from a page must be declared inapplicable in that page's
# frontmatter (`levels_na: {everyday: "reason"}`). Never silently skipped.
levels:
  everyday:
    name: "Бытовой уровень"
    heading_pattern: '^#{2,3}\s*1\.'
  working:
    name: "Рабочий уровень"
    heading_pattern: '^#{2,3}\s*2\.'
  academic:
    name: "Академический уровень"
    heading_pattern: '^#{2,3}\s*3\.'

rules:
  analogy:
    marker: 'origin:\s*analogy'
    breaks_pattern: '^#{2,4}\s*Где\s+.*ломается'
  contested:
    section_pattern: '^#{2,4}\s*(Расхождени|Спор)'

# ── problems ────────────────────────────────────────────────────────────
tasks:
  count: 3
  roles:
    - "holding the definition"
    - "applying the result"
    - "break the condition"
  author_allowed: true
  author_obligations: >-
    `source: author's own` plus why it had to be, and answers pinned by
    executable checks in checks/. An author's own problem must not be less
    checkable than a borrowed one.
  sources_thin_on: >-
    No exercise anywhere in the corpus checks the metric axioms; the main problem
    book opens at problem 18. Warm-ups come from elsewhere.

closure:
  criterion: >-
    Derive the key result from scratch on paper, and solve three non-routine
    problems on it.

# ── the canon ───────────────────────────────────────────────────────────
canon:
  arbiters:
    - area: "metric spaces, coverings, Arzelà, Peano"
      source: "Kolmogorov–Fomin"
    - area: "compactness in Rⁿ, Weierstrass, Cantor"
      source: "Zorich, part 1"
  popular_sources: >-
    Admitted into the everyday level only. Never outweigh the canon.

audit:
  kinds: [statement, source, analogy, problem, hint, link, length, typo, other]

corpus:
  enabled: true
  priority:                # indexed first, so work can start before OCR finishes
    - "Kolmogorov-Fomin.pdf"
```

## Minimal config

Everything above has a default except these:

```yaml
schema_version: 1
phase: 1
subject: "React"
sources: {resolver: url, require_version: true}
confidence: {min_independent_sources: 2, min_passed_checks: 1,
             attainable_types: [behavioral, attested]}
runners:
  vitest: {type: behavioral, kind: shell, command: "npx vitest run -t {arg}"}
```

## Two worked shapes

**A live-documentation subject (React).** `resolver: url`, `require_version:
true`, `attainable_types: [behavioral, attested]` — nothing here is provable, but
everything is runnable. Independence: *execution against documentation*, because
two articles about `useEffect` are one source counted twice. The "break the
condition" role gets stronger, not weaker: remove the dependency array and you
can **watch** it break, which no theorem allows.

**A documentary subject (history).** `resolver: corpus`, `require_page: true`,
`attainable_types: [attested]`, and `min_passed_checks: 1` still works — every
claim carries a quotation the machine confirms is really on the cited page.
Independence: primary testimony against other primary testimony. Expect
`status: contested` to be the normal case rather than the exception, and set
`rules.contested.section_pattern` to whatever the pages actually head that
section with.
