# Medium: I built a script to check every quote in my notes — 42% failed

**Note:** this is the technical version. The story version is in the Substack post.
Same facts, different reader.

I keep notes on other people's work. GTM engineering frameworks, mostly. The notes are
where the distilled rules live, so they matter more than they look.

I had never kept the source text alongside them. That turned out to be the problem.

## The setup

- 101 source PDFs, 240,901 words, extracted to plain text.
- A notes file: 14 batch files plus a synthesis document.
- 373 double-quoted spans across those notes, attributed to the author.

No source text retained. No checker. Just notes.

## The checker

Three requirements:

1. **Exact match, not similarity.** A quote is either in the source or it is not.
   Fuzzy matching would have hidden the interesting cases.
2. **Normalize what extraction breaks.** PDF extraction produces curly quotes where the
   source had straight ones, em-dashes where the source had hyphens, and splits words
   across lines ("go-to- market"). A verifier that does not normalize these reports
   false failures and gets ignored.
3. **Grade, don't just fail.** Four grades — EXACT, NEAR, PARAPHRASE, MISSING — so
   that a transcription drift is distinguishable from a fabrication. That distinction
   is what makes the report actionable.

The cost model matters too: the corpus is 240,901 words. A naive sliding-window
similarity search over that is too slow to run on every edit. The fix was an inverted
index on word positions, then candidate generation from each quote's rarest words, then
scoring only those windows. Runtime went from minutes to under a second.

## The result

**373 quotes checked. 155 failed.** 41.6%.

| Grade | Count |
|---|---|
| EXACT | 217 |
| NEAR | 1 |
| PARAPHRASE | 47 |
| MISSING | 108 |

Three distinct failure modes, in descending order of how likely they are to survive
human review:

### Silently tightened

The note says "Not a vector store." The source says "not a RAG pipeline." Same claim,
paraphrased, presented in quotation marks as if verbatim.

**Why this is the worst one:** the paraphrase is often *better* than the original.
"Vector store" is the term in circulation now; RAG was the term in the source. My
version would have read as more current and less traceable, and the drift would have
been invisible to me because it made the note read better.

### Fragment presented as complete

The note says "The filter step goes away." The source says "At that price the filter
step in go-to-market goes away." The fragment is genuinely in the source. It just was
never said on its own.

### Reconstructed dialogue

The note says "Yo Chris, beers Friday?" The source reads "A friend writes 'yo chris,
want to get beers friday?'"

## The repairs

154 edits, in two kinds only:

- **REPLACE (137)** — the source's own wording, copied character for character.
- **RECAST (17)** — lines that were the note author's own summary, so the quote marks
  came off and the text became an attributed paraphrase.

Invariant across every edit: no number changed, no claim changed, no bullet removed,
line counts identical before and after. This is a fidelity repair, not a rewrite, and
that constraint is what made it safe to automate.

## Turning it into a gate

The script was useful once. The test is what makes it permanent:

```python
assert len(failures) <= MAX_FAILURES
```

A pytest case that reads the corpus, re-extracts every quoted span from the research
tree, and fails the build if the failure count rises above the current baseline. It
also asserts that the corpus has all 101 posts, that no post is suspiciously short
(a silent extraction failure), and that the named frameworks the research added are
still present.

Two design details worth copying:

**Corpus-dependent tests should skip, not fail, when the corpus is absent.** The
corpus is 1.8MB of third-party content and is gitignored — it rebuilds from the source
PDFs in seconds. A test suite that hard-fails on a fresh clone is a test suite people
disable.

**Downstream files may quote the research record; the research record may only quote
the corpus.** The primary notes are checked against source only. Memos that compare
against the notes are checked against corpus *or* notes. Without this, every downstream
document that cites a prior document becomes a false positive.

## The result

- 377/377 quotes in the primary record now verify as exact substrings.
- 15 remaining failures in downstream memos, each either a fragment or a
  multi-line quote the line-based extractor cannot see.
- One NEAR that cannot be fixed: PDF extraction dropped the apostrophes, so no
  character-exact form of that sentence exists in the extracted text. It stays NEAR
  and is documented as such, rather than being silently "fixed" to something the
  source never said.

## Why this generalizes

Any framework distilled from another person's work has this failure mode by default.
The distilled artifact is more portable than the source, so the source gets dropped,
and once it is dropped there is nothing to check the distillation against.

The fix is unglamorous: keep the source text, check every quote mechanically, and
reclassify anything that does not match. If the number of quotes is small enough to
audit by hand, do that. If it is large enough to matter, it is a script.

---

*The full repair log, the verifier, and the test gate are in the repository linked in
the comments.*
