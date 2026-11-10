---
name: pain-segment-finder
description: Find a pain-qualified segment (a situation, not a firmographic filter) and build its TAM from public data. Use for "who should we target", "build a list of X", "our ICP is 50-1000 employees in Y", TAM research, or new-vertical exploration.
---
# Pain Segment Finder

## 1. Lock the problem (read the client site silently first)
What they sell · to whom · the ONE problem the product kills. Every later step is judged against it.

## 2. Concentric Circle Test
- **Segment** (not market): its core challenge must BE the solution (Dish Hubs, not restaurants). Size band 100–2,000 companies; >50k = a market, <50 = an account list.
- **Company:** inside a good segment, filter the ones too busy scaling or already solved.
- **Person:** different roles, different cores (CEO = cost; tech = fear of getting blamed). Can't precompute: discover by asking.
Refuse to proceed on a *category* ("healthcare providers"); require a *type* ("ambulatory surgery centers").

## 3. Find the situation (ask in this order)
1. Who was legally compelled to publish proof of this pain? (inspections, citations, filings, licenses, permits)
2. What licenses must this company type hold? (pesticide applicator registry = every landscaper)
3. Which side of the transaction is public?
4. Delta = upside of the product − downside without it. Rank by delta.
5. Target the CHANGE (certifications coming due, retirement, new region), not the permanent state.
Use `data-source-hunter` for the source map.

## 4. TAM research (5 phases)
- P0 validate every API key (kill switch).
- P1 read site. P2 narrow to one company type.
- P3 five parallel subagents, identical JSON output (`source, coverage_est, records, has_websites, cost, quirks, access`): federal registries · state licensing · associations/directories · maps/local APIs · open data.
- P4 score each source: **Coverage 35 · Websites 30 · Data quality 20 · Cost 15** with anchored levels (100 = legally required; 60 = mostly claimed listings; 20 = Kaggle dump). Government wins ties.
- Recommend a 2–3 source combo (high-coverage anchor + website filler), dedupe on phone/ID. Target ~85% of market.

## 5. Disqualify hard
Write gates that make someone *unable* to benefit (no engineer, regulated gift caps, title has never bought). Disqualification beats demographics.

Output: `work/segment.md` (segment definition, gates, sources table with scores, est. size, the proof fields that will feed the message).
