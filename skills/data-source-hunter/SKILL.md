---
name: data-source-hunter
description: Find and rank the public datasets that can build a list or prove a pain for any vertical, starting from "who was compelled to publish this?". Use when a list doesn't exist in ZoomInfo/Apollo, for vertical TAMs, or to replace a paid data vendor.
---
# Data Source Hunter

## Questions, in order
1. Who was legally compelled to publish it? (regulator, filing, disclosure rule)
2. What license/registration must this entity hold?
3. Which side of the transaction is public (buyer filings, purchase records, board minutes)?
4. What reporting requirement is coming (Federal Register "reporting requirements", Unified Agenda)?

## Rank sources by the ladder (best first)
1 gov registry with unique ID · 2 mandated disclosure · 3 certification directory · 4 platform data w/ real-world grounding · 5 association list (10–40% coverage) · 6 scraped aggregator (lead only, never a source of truth).
Value = ground-truth distance × join-key quality × coverage × free bulk access × update cadence.

## Starter shelf (US) — verify each live before relying on it
NPPES/NPI · CMS Part D + Open Payments · CMS ownership files · OSHA · EPA ECHO · FMCSA · MSHA · CFPB · FDIC · NCUA (CEO names) · SAM.gov UEI → USAspending · EDGAR CIK→EIN → DOL Form 5500 (Schedule C = vendors' customers) · IRS BMF · SEC Form D (related persons) · ATF FFL · TTB · FDA establishments · FCC · FAA NASR (airport owners) · IPEDS · FINRA BrokerCheck · state SoS (Colorado, Florida Sunbiz) · county parcel rolls (Florida DOR) · FEMA USA Structures + DOT address points · USAC E-rate 470/471 · Federal Audit Clearinghouse · EIA-860M · CMS cms-hpt.txt · FTC FDD Item 20 · H1B/PERM · WARN notices · Greenhouse/Lever/Ashby JSON · Common Crawl CDX · crt.sh · Wayback CDX · ICANN CZDS · HTTP Archive · Overture/AllThePlaces · Wikidata/GLEIF.

## Non-US (your edge: build these maps)
Research the equivalents per country (company registry, tax/GST registry, licensing boards, tenders portal, securities filings, beneficial ownership). Use the same ladder and publish the map.

## Before trusting any dataset
Open one actual file · confirm the join column exists · look up the publisher · check last-updated · one-state/one-region spot count vs the official portal (build only if ≥85–95% right) · note license (non-commercial = banned for client work).

## The lineage schema (make it checkable)
Every row you keep carries three fields, so a machine can verify it later:
- `provenance_type` — `original` | `official_mirror` | `scrape_snapshot` | `derived` | `unknown`
- `gtm_score` — 0–10, the ladder above as a number
- `as_of` — **only a date the record itself states. Never inferred.** A plausible date is not a date.

Only `original` and `official_mirror` may be asserted as fact. A scrape is a lead.

## The survivor-count gate (cost, before you spend)
Print the row count after every filter, and **measure the filter before you pay**:
- free keyword prefilter → print survivors
- if survivors > 100,000, the filter is broken — fix it, do not spend
- calibrate per catalog, not globally: the same keywords that work on a company registry
  can match a fifth of all academic abstracts on an archive. Make the match title-only there.
- then the lineage filter (`score ≥ floor AND provenance IN (original, official_mirror)
  AND as_of IS NOT NULL`) → print survivors again

Run `python scripts/verify_sources.py rows.csv` to enforce all of this. It exits non-zero
when a row has no score, no known provenance, an inferred date, or when the survivor
count blows past the gate.

Output: `work/sources.md` table: source, rung, join key, coverage, access path, cadence, cost, gotchas, dead-end flag.
