---
name: cheap-right-answers
description: Research agent pattern that answers per-row questions about companies/people using free sources first and paid tools only for the residue, with confidence bands, two-root adjudication and a self-grading answer key. Use for enrichment, domain resolution, "is this site live", "who runs X", list verification.
---
# Cheap Right Answers

Metric: **right answers per dollar** = (spend + wrong×w + held×cost_to_close) per 1,000 rows. Always print accuracy next to $/row.

## The elevator (exit at the first floor that settles the row)
0. Own data + wire checks: DNS, parking nameservers, MX, cert-transparency heartbeat, garbage-URL test (shell returns same page for a nonexistent path).
1. Free catalog (registries, Overture, Common Crawl, Wikidata, open data). See `data-source-hunter`.
2. Free quotas (Google Knowledge Graph 100k/day, registry APIs) with a quota ledger.
3. Credits you already paid for (Clay, Blitz flat plans).
4. Cheap search (~$0.0005–0.005/query) + page-to-text + small model.
5. Stubborn sites: archived copy (Common Crawl/Wayback) before any paid render.
6. Expensive agent: 3–15 tool calls, stop when 3 sources agree, forced best answer + confidence. Receives the row's PACKET of verdicts already proven ("parked", "wrong state") as constraints.

## Bands
accept ≥ 0.85 · reject ≤ 0.20 · hold in between → next floor or human queue. Free floors may never stamp "not found"; **absence must be earned** (naming-convention guesses + one search).

## Adjudication
- Two independent roots make a truth; aggregators can nominate, never corroborate.
- Identity = name + place + jurisdiction. County/directory pages are listing evidence, not identity.
- Newer page beats grander site. A wrong answer is worse than a blank → `needs_review`.

## Self-test (every job)
- Answer key: 100–200 rows (50% random, 25% suspicious, 25% coverage strata); blind verifier agents 1–5 rows each; two-root agreement to enter the key.
- Grade /10: accuracy 25 · completeness 25 · validity 15 · source quality 15 · efficiency 10 · consistency 5 · error handling 5. Ship gate 8.0.
- Cluster misses by shared cause → one fix per cluster → rerun that slice.
- Cache keys include the query string. Probe every API filter with a deliberately fake filter as a control.

Run `python scripts/cost_guard.py --rows N --unit-price P` before any paid step.
