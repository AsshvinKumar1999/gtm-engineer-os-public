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

Output: `work/sources.md` table: source, rung, join key, coverage, access path, cadence, cost, gotchas, dead-end flag.
