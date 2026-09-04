# The corpus capability

For subjects learned from stable works — mathematics, physics, chemistry, history,
law. Off by default; turned on by `learning-init` when a load-bearing source is a
book. Orthogonal to the subject itself: it is about *citing paper*, not about any
one field.

```bash
make ocr           # extend the text index (resumable, hours on a large corpus)
make ocr-status    # what is already indexed
make find Q="..."  # search the corpus; B=Author narrows to one work
make catalog       # rebuild raw/books/index.md
```

## The printed-page offset

The single most undervalued piece of the machinery. A PDF's page 91 is the book's
printed page 79, and a citation that ignores the offset is wrong by twelve pages
— which means the learner cannot check it, which means the whole citation
discipline quietly stops working.

The indexer determines the offset per book by voting on running-heads, ignoring
numbers from dense lines so that formula numbers do not enter the ballot. The
result lands in `raw/books/.ocr/*.meta.json` — small, hand-verified, and
**versioned even though the text index is not**, because it costs manual checking
to produce and nothing to store.

`make find` reports the printed page, not the PDF page. Cite what it reports.

## OCR is for navigation only

**A quoted statement is always verified against the image of the page.** Never
against the text index.

OCR systematically mangles indices, quantifiers, Greek letters and diacritics. A
mangled formula wearing a `verified` tag is the worst outcome this system can
produce: it is wrong, it looks checked, and the error is invisible precisely
because the tag says it was examined. Copying formulas out of `.ocr/*.txt` is
forbidden. Use the index to find the page; open the page as an image to read it.

The built-in `attested` check runs against the text index and is deliberately
narrow — whitespace normalised, case ignored, **no fuzzy matching**. Fuzzy
matching over OCR would manufacture false attestations, which is worse than
having no check at all.

## What is versioned

The PDFs are not: large, and locally held. The text index is not: fully derived,
and it would duplicate itself in history on every re-index. What *is* versioned:
the catalogue `raw/books/index.md`, and the page-offset metadata.

## Priority

`corpus.priority` in the domain layer lists the works indexed first, so that work
can begin before a long OCR run finishes. The core has no opinion about which
books matter — that is exactly the kind of thing the domain layer is for.
