---
name: monetization-ladder
description: Design a content-to-paid conversion ladder from the "Who Gets This" template — what stays free above the line, what goes below it, and the two price tiers. Use when turning a build log or playbook into a post with a CTA, pricing a Substack or newsletter, or deciding what a free tier should give away versus sell.
---

# Monetization Ladder

The rule underneath the whole thing: **give away the result, sell the wiring.**

A reader who gets the headline number and the method for free is now convinced the
work is real. What they cannot get for free is the *wiring* — the join keys, the exact
endpoints, the gotchas, the thresholds, the cost ledger. That is what the paid tier
sells, and it is the only thing the paid tier needs to sell.

## The shape

Every paid post ends with a block headed **"Who Gets This"**. It has three parts and
no more:

```
Who Gets This
$50/mo (most readers start here): everything below the line in this post,
  and every paid article.
$2,499/yr: [the thing you install]. [How you talk to it.] Current tools: [named list].
  Whatever ships next is included. Plus all courses + weekly [live session].
  (Go annual — $X/yr.)
Below the line in this post:
  [3–5 bullets naming exactly what the reader gets for paying]
```

Three rules make it work:

1. **One mid tier, one annual tier.** No feature matrix. The mid tier is "everything
   below the line." The annual tier is the *software*, and it names the tools
   explicitly so the price is anchored to a list the reader can count.
2. **Name what ships next.** "Whatever ships next is included" turns the price into a
   subscription to a roadmap rather than a purchase of a snapshot.
3. **The CTA is a live working session, not a course purchase.** "Every week I run
   Applied Office Hours — bring what you're building and we'll work it live." The
   weekly session is the retention engine; the tiers are the monetisation.

## Deciding the line

The line falls where the reader's *next action* changes, not where the content gets
more technical.

| | Above the line (free) | Below the line (paid) |
|---|---|---|
| The result | the headline number, the finding | the per-row data |
| The method | the generalizable steps | the exact join keys, endpoints, thresholds |
| The proof | one worked example | the full list, the source files, the dead ends |
| The cost | the headline cost figure | the itemized ledger and how to buy each part |

Test for a proposed below-the-line item: *would the reader still be able to do the
thing without it?* If yes, it belongs above the line.

## The free tier is not a sample

The free part must be a **complete result**, not a teaser. A teaser teaches the reader
that you hold back the interesting bit, and then every paid thing feels like a toll.
Give away the whole finding — the number, the method, and one real artifact they can
open. Charge for scale and wiring.

## Before you ship the block

- Every number in the post body traces to a run file (`scripts/check_claims.py`).
- The tool list in the annual tier is current. Stale names cost more credibility than
  the tier earns.
- The "below the line" bullets describe what you will *actually* deliver, and you
  have it built. A promise you cannot keep is a refund and a bad review.
- The free text gives a reader everything they need to judge whether the paid tier is
  worth it — including the result.
- Read the block as a stranger with no context. If it does not make sense without the
  post above it, rewrite it.

## Where this comes from

Reverse-engineered from the "Who Gets This" block that appears in **31 of the 101**
source posts. See `research/SYNTHESIS.md` §5b and `research/GAP-ANALYSIS.md` §4 for
the extracted template and the evidence.
