# The method

How I build GTM plays. Short version: find a record someone had to publish, pair it with what they are doing now, and prove every number before anyone sees it.

## 1. Start from a situation, not a filter

"Series B SaaS, 50–200 people" is a filter. Lots of companies match it and most of them have no reason to talk to you this week.

"Just reported a raise to the SEC and is hiring the role my product helps" is a situation. It's something that happened in the real world, it has a date, and you can point to it.

Every play starts with the question: **what situation would make this buyer want to hear from me today?**

## 2. Use data people were forced to publish

The best signals come from records a company *had* to file: SEC filings, visa applications, permits, licenses, registries. They're:

- **free**: government and public data, no API key
- **dated**: you know exactly when it happened
- **hard to fake**: nobody writes a Form D for marketing

So the second question is always: **who was compelled to publish this?**

## 3. One signal is noise. Two are a play.

A raise alone doesn't mean they're buying. A job post alone doesn't mean they have budget. When both show up in the same week, you have a real reason to reach out, and you can say exactly what that reason is.

```
Signal A (compelled record) × Signal B (action happening now) = a play
```

## 4. Code counts, models judge, a human approves

- **Code** does the counting, joining and filtering. Numbers come from scripts, never from a model's memory.
- **Models** judge the fuzzy parts: is this a tech company, is this title similar to that one.
- **A skeptic** (`agents/skeptic-verifier.md`) tries to break every claim.
- **A human** checks the top results by hand and approves anything that goes out.

## 5. Free first, paid last

Answer what you can from free sources and plain code. Use a paid tool only for the rows that are left, and run `scripts/cost_guard.py` before any paid batch.

## 6. Never invent anything

- Every number in a post or message comes from a run file you can open.
- Count each company once, and say "filings" when you mean filings.
- If a match is shaky (for example, two companies share a name), leave it out or label it.
- Messages go through `agents/buyer-critic.md` and `scripts/lint_ai_tells.py` before a human reads them.

## 7. Explain it like the reader is five

If a step needs jargon, rewrite the step. Short lines, real examples, one idea at a time.

## 8. Prove the thing before you say it works

A number that happened is not a cause. Before you claim a tactic works:

- Put the control variable on the **outside**. Compare reps inside one lead source, then pool.
- Test every candidate habit the same way, then let the data pick. Never decide the lever in advance.
- Use the right statistics for small counts: Wilson intervals, a gap of ~2× standard error, and at least 20 leads per side.
- **Publish the tie band.** If two things are inside the noise, refuse to rank them.
- Read the maturity window from your own won deals, not from a default.

`scripts/lever_test.py` does the arithmetic. `skills/lever-test/SKILL.md` is the procedure.

## 9. Give away the result, sell the wiring

A reader who gets the finding for free is convinced the work is real. What they cannot
get for free is the wiring: the join keys, the exact URLs, the gotchas, the thresholds,
the cost ledger. That is the paid tier, and it is the only thing it needs to sell.

The free part is a complete result, never a teaser. One mid tier ("everything below
the line on this post") and one annual tier (the software, with the tools named).
See `skills/monetization-ladder/SKILL.md`.

---

**Credit:** Jordan Crawford's writing on public-data GTM got me started. His free starter kit is here: https://github.com/SantaJordan/gtm-engineer-starter. This repo is my own system and my own words.
