---
name: pvp-writer
description: Turn a segment + proof data into PQS and PVP messages and grade them like the buyer. Use when drafting cold emails, LinkedIn notes, call openers, or reviewing outbound copy.
---
# PVP Writer

Rule zero: **you write the first draft by hand** (one message, like texting a friend). The model expands, grades and lints. Never ask it to write from scratch.

## Inputs
Segment + the exact record fields that prove the pain (e.g., inspection #, date, violation type, penalty) + the asymmetry candidate.

## Produce 4 messages
- 2 **PQS** (pain-qualified, humble: "would you find this useful?")
- 2 **PVP** (complete gift: a number, a name, a date, one decision they can make, no ask)

## Shapes that work
- Predict their future from your aggregate (say what the pattern across your customers was, then admit you don't know their numbers).
- Anti-threat: frame backwards in time as praise. Send to the CEO, not compliance.
- Proof by naming three (their stores, their customers, their competitors).
- Hold the sheet back ("I have it for every store, daily; want it?").
- Run your product on their behalf; hand over the output.
- Champion moved jobs (case-study mining); laid-off leader gets free help.

## Grade each as the buyer (0–10 each, average)
situation recognition · data credibility · insight value · reply effort (lower friction = higher) · would it land. PQS ≥ 7.0, PVP ≥ 8.5, else rewrite or kill.

## Gates (all required)
- **Copy test:** specific, grounded in a record, and not obvious. If a competitor could send it word for word, rewrite it.
- **Forwardable:** a peer in the same role could act on it without context.
- **Worksheet:** every number traces to records (source, count, method). No receipt, no number.
- **Compass:** would you send it to a friend? Does it sound like a person who cares?
- Run `python scripts/lint_ai_tells.py <draft>`; zero hard hits.
- Kill list: "saw you're hiring", "congrats on", "saw you on our site", "hope this finds you well", dashboard screenshots, data theater.

## Final step (mandatory)
Show the top message to one real customer or ex-customer employee. Record their reaction in `work/message-validation.md`. "That would be really valuable to me" = ship.
