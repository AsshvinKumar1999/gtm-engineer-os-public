# Substack: 42% of the quotes I attributed to a GTM genius were not his words

I read 101 posts by Jordan Crawford — a GTM engineer whose work I rate highly enough
that I reverse-engineered his method into a system I run every week. Along the way I
wrote a notes file with quotes in it, the way you do.

Then I built the thing I should have built first, and the numbers were not what I
expected.

**155 of my 373 quotes were not his words.**

That is 42% of the quoted material in my notes.

## How it happened

I never kept the source text.

When I read the posts, I extracted the text, wrote my notes, and let the extracted text
go. My notes file recorded that I had read them, and pointed at itself as the record.
That is the whole workflow. There was no second copy of the words, so there was nothing
to check against.

So I built a checker. One script. It takes every double-quoted span in my notes and
looks for it in the original posts. Not "does this feel right" — exact match, after
normalizing the typography that PDF extraction mangles.

The first run found 155 failures. I expected maybe five.

## Three ways a quote breaks

They clustered into three types, and understanding them is the useful part.

### 1. Silently tightened

I had him saying:

> Not a vector store. A wiki with a contract.

The source says:

> not a RAG pipeline. A wiki with a contract.

The second sentence is exactly right. The first is a paraphrase I compressed, and I put
it in quotation marks anyway. It reads better. It is more punchy. And it is not what
he wrote.

This is the most dangerous type, because the paraphrase is *more accurate to the
meaning* than the original in some ways. "Vector store" is the phrase people use today.
RAG is what he said. My version would have sounded more current and less traceable.

### 2. Half a sentence

I had him saying:

> The filter step goes away.

The source says:

> At that price the filter step in go-to-market goes away.

I had carved out a fragment and presented it as a complete thought. The fragment is
real. It appears in the source. But nobody said it that way, alone.

### 3. Reconstructed dialogue

I had him saying:

> Yo Chris, beers Friday?

The source reads:

> A friend writes "yo Chris, want to get beers friday?"

Different sentence, different meaning — one is a fragment of an example, the other is a
complete quotation of a message the post recommends writing.

## What it actually cost me

This is the part that should worry anyone who takes notes on other people's work.

**Nothing visible.**

Every one of my 155 quotes was close to right. The meaning held. The advice still made
sense. Nobody reading my notes would have been misled about any substantive point.

That is exactly why it would have survived review. And exactly why it would have been
caught eventually — by one person, one time, comparing one quote against the original
and deciding the rest of my work was sloppy.

A wrong number gets checked. A near-miss quote reads as authority.

## The fix is boring

I wrote 154 corrections:

- **137 replacements** — the source's own wording, copied character for character,
  including the apostrophes and dashes the PDF extraction produced.
- **17 recasts** — lines that were my own summary, not his, so I removed the quote
  marks and let them be my words.

No note was rewritten. No number changed. No conclusion changed. The bullet structure
and line counts are identical before and after.

Then I made it permanent. A test in the repo runs the same check and fails the build if
a new quote cannot be found in the source. It is now a regression gate, not a habit.

## Why this matters beyond my notes

If I can break my own notes this badly, then every framework written from someone
else's posts has the same problem. Including the ones you are about to build.

The GTM engineering community is full of frameworks distilled from newsletters,
podcasts, and courses. Almost none of them keep the source text next to the
distillation. Almost none of them have a script that checks whether the quotes are
real.

That is a small gap with a large consequence. It takes one script and one afternoon.

**The failure mode is not that people lie. It is that people write accurately about
something, quote it approximately, and then lose the ability to prove either.**

## The wider thing I noticed

Doing this for 373 quotes taught me something about how frameworks propagate.

A paraphrase in quotation marks is a small lie with a long half-life. It survives
because it is easier to read than the original. It gets copied into other notes, then
into other frameworks, then into posts and decks, where each generation strips the
attribution until only the claim remains.

The claim is usually still roughly true. But nobody can check it, because the chain
back to the source was severed at the first paraphrase — and the quote marks made it
look like it had not been.

Two rules I keep now:

1. **Keep the source text.** Not the summary. The text.
2. **Check every quote against it, and if it does not match, either fix it or stop
   using quote marks.**

That is it. That is the whole method.

---

*Full details, the 154-item repair log, and the script are in the repo linked below.*
