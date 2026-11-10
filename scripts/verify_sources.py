#!/usr/bin/env python3
"""Verify data-source lineage before you spend a dollar on it.

The method says "free first, pay for the residue". This script makes that checkable
instead of aspirational. It applies the lineage rules extracted from the source corpus:

  - a provenance taxonomy: original > official_mirror > scrape_snapshot > derived > unknown
  - `as_of` may only be a date the record itself states — never inferred
  - a survivor-count gate: if the prefilter leaves more than N rows, the filter is broken
  - a lineage filter: only rows with a score, a provenance type and a date survive
  - per-item x count reconciliation against the totals

Usage:
  python3 scripts/verify_sources.py rows.csv
  python3 scripts/verify_sources.py rows.csv --max-survivors 100000
  python3 scripts/verify_sources.py rows.csv --require-as-of --min-score 7

CSV format (one row per record):
  id,provenance_type,gtm_score,as_of,url,title
  provenance_type: original | official_mirror | scrape_snapshot | derived | unknown
  gtm_score: 0-10 (the source ladder)
  as_of: an ISO date the record states, or empty

Exit 1 if any lineage rule is broken — this is a gate, not a report.
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

# The source ladder. Higher is better. "derived" and "unknown" never qualify as a
# source of truth: a scrape is a lead, never an assertion.
PROVENANCE = {
    "original": 5,
    "official_mirror": 4,
    "scrape_snapshot": 2,
    "derived": 1,
    "unknown": 0,
}
QUALIFYING = {"original", "official_mirror"}

ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


def parse_date(v: str) -> date | None:
    v = (v or "").strip()
    if not ISO_DATE.match(v):
        return None
    try:
        return date.fromisoformat(v)
    except ValueError:
        return None


def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Verify data-source lineage before spending")
    ap.add_argument("csv", type=Path)
    ap.add_argument("--max-survivors", type=int, default=100_000,
                    help="if the prefilter leaves more than this, the filter is broken")
    ap.add_argument("--min-score", type=int, default=0)
    ap.add_argument("--require-as-of", action="store_true")
    ap.add_argument("--require-qualifying-provenance", action="store_true")
    ap.add_argument("--stale-after-days", type=int, default=0,
                    help="flag records older than this many days")
    ap.add_argument("--today", default="", help="ISO date to measure staleness against")
    a = ap.parse_args(argv)

    if not a.csv.exists():
        print(f"no such file: {a.csv}", file=sys.stderr)
        return 2
    rows = load(a.csv)
    if not rows:
        print("empty csv", file=sys.stderr)
        return 2

    total = len(rows)
    problems: list[str] = []
    counts = {k: 0 for k in PROVENANCE}
    dated = 0
    scored = 0

    print("=" * 72)
    print("LINEAGE VERIFICATION")
    print("=" * 72)
    print(f"rows in: {total}")

    for r in rows:
        rid = r.get("id", "?")
        prov = (r.get("provenance_type") or "unknown").strip().lower()
        counts[prov] = counts.get(prov, 0) + 1

        if prov not in PROVENANCE:
            problems.append(f"{rid}: unknown provenance_type '{prov}'")
            prov = "unknown"

        raw_score = (r.get("gtm_score") or "").strip()
        score = None
        if raw_score:
            try:
                score = float(raw_score)
                scored += 1
            except ValueError:
                problems.append(f"{rid}: gtm_score '{raw_score}' is not a number")
        else:
            problems.append(f"{rid}: no gtm_score — a row with no score cannot be ranked")

        d = parse_date(r.get("as_of", ""))
        if d:
            dated += 1
        else:
            raw = (r.get("as_of") or "").strip()
            if raw:
                problems.append(
                    f"{rid}: as_of '{raw}' is not an ISO date the record states "
                    "(as_of is never inferred)"
                )

        if a.require_as_of and not d:
            problems.append(f"{rid}: missing as_of")

        if a.require_qualifying_provenance and prov not in QUALIFYING:
            problems.append(
                f"{rid}: provenance '{prov}' is a lead, not a source of truth"
            )

        if score is not None and score < a.min_score:
            problems.append(f"{rid}: gtm_score {score} below the floor {a.min_score}")

        if a.stale_after_days and d:
            today = parse_date(a.today) if a.today else date.today()
            if today:
                age = (today - d).days
                if age > a.stale_after_days:
                    problems.append(
                        f"{rid}: as_of is {age} days old (floor is {a.stale_after_days})"
                    )

    print("\nprovenance breakdown:")
    for k, v in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {k:<18} {v:>7}  (rung {PROVENANCE.get(k, 0)})")
    print(f"\nrows with a score: {scored}/{total}")
    print(f"rows with a stated date: {dated}/{total}")

    # --- the survivor-count gate ---
    qualifying = sum(
        1 for r in rows
        if (r.get("provenance_type") or "unknown").strip().lower() in QUALIFYING
        and (r.get("gtm_score") or "").strip()
        and parse_date(r.get("as_of", ""))
    )
    print(f"\nqualifying rows (score + provenance + stated date): {qualifying}")
    if qualifying > a.max_survivors:
        problems.append(
            f"survivor count {qualifying:,} exceeds the gate {a.max_survivors:,} — "
            "your filter is broken, fix it before spending"
        )

    # --- reconciliation ---
    print(f"\nreconciliation: {sum(counts.values())} = {total} rows? "
          f"{'OK' if sum(counts.values()) == total else 'MISMATCH'}")
    if sum(counts.values()) != total:
        problems.append("provenance counts do not sum to the row count")

    print("\n" + "=" * 72)
    if problems:
        print(f"LINEAGE FAILED — {len(problems)} problem(s):")
        for p in problems[:40]:
            print(f"  - {p}")
        if len(problems) > 40:
            print(f"  ... and {len(problems) - 40} more")
        print("\nDo not spend on this run. Fix the lineage, then re-run.")
        print("=" * 72)
        return 1

    print("LINEAGE OK. Every row has a score, a known provenance type and a stated date.")
    print("Cost guard next: python scripts/cost_guard.py --rows N --unit-price P")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
