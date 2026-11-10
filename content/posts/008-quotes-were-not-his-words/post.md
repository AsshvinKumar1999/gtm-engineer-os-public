# Post 008: 42% of the quotes I attributed to a GTM genius were not his words

**Status:** caption drafted. Nothing published.
**Best slot:** Monday (build log slot). The hook is a number, so lead with it.

## Storyboard (4 beats)
1. Input: 101 posts, ~240,000 words, and a notes file that quoted them.
2. Process: every quoted line checked against the source text, character by character.
3. Output: 155 broken quotes, split into three named failure types.
4. Proof: the repaired corpus and the test that stops it happening again.

## Caption (paste into LinkedIn)

I attributed 373 quotes to a GTM engineer I study. 155 of them were not his words.

**42% of my quoted material.**

I did not notice. It looked perfect.

Here is what happened. I read 101 posts, wrote notes, and in those notes I put quotes in quotation marks. That is normal. Everyone does it. But I never kept the source text, so I could never check my own work.

So I built the thing I should have built first.

A script that takes every quote in my notes and looks for it in the original posts. Not "does it feel right." Exact match.

155 of 373 failed.

Three failure types, and none of them was random:

→ Silently tightened. I had him saying "Not a vector store." He actually said "not a RAG pipeline." Same idea, different words, in quotes as if he said it that way.

→ Half a sentence. I quoted "The filter step goes away." The real line was "at that price the filter step in go-to-market goes away." I had carved out a quote that never existed on its own.

→ Reconstructed dialogue. I had him saying "Yo Chris, beers Friday?" The source reads "a friend writes 'yo Chris, want to get beers friday?'" Different sentence entirely.

**What this actually cost me.** Nothing visible. Every one of my 155 quotes was close to right. The meaning held. That is exactly why it would have survived review, and why nobody would have caught it, including me.

Then a reader would have pulled the original. Found the difference. And decided the rest of my notes were sloppy.

**The fix is boring and it works.** Keep the source text. Check every quote against it. If it does not match, either fix the quote or stop using quote marks.

I wrote 154 corrections. 137 were the source's own wording, copied exactly. 17 were my own summary lines, so I removed the quote marks and let them be my words.

Then I made it permanent. A test runs the same check and fails the build if a new quote cannot be found in the source.

Now the interesting part.

**If I can break my own notes this badly, every other GTM framework written from someone else's posts has the same problem.** Including the ones you are about to build.

It costs one script and one afternoon. It is the difference between "I read it and understood it" and "I read it and can prove I understood it."

Anyone else doing this? I would like to compare notes.

## Facts and their sources

| Fact | Source |
|---|---|
| 373 quotes checked, 155 failed (42%) | first run of `scripts/verify_quotes.py` |
| 154 corrections: 137 REPLACE + 17 RECAST | the repair log in the repo |
| 101 posts, 240,901 words | `scripts/build_corpus.py` output |
| Final state: 377/377 verify | `python3 scripts/verify_quotes.py` |
| The gate | `tests/test_research_integrity.py` |

## Verification note

The 42% figure is from the **first** run of the audit, before repairs. The current
state is 377/377 exact. Say "155" and "42%" against the first run; never imply the
current state has failures.

Quote wording above is checked: "Not a vector store." → source reads "not a RAG
pipeline"; "The filter step goes away." → source reads "at that price the filter step
in go-to-market goes away"; "Yo Chris, beers Friday?" → source reads "a friend writes
yo chris, want to get beers friday".

## First comment

Link to `scripts/verify_quotes.py` and `scripts/build_corpus.py` on GitHub, with
`?utm_source=linkedin`.

## Substack / Medium

Longer version: the three failure types with before/after examples from the repair
report, why paraphrases in quote marks are worse than wrong numbers (a wrong number
gets checked; a paraphrase reads as authority), and the argument that this applies to
every framework written from someone else's work. See `substack.md` and `medium.md`.
