#!/usr/bin/env python3
"""Lever test: decide whether a habit changes an outcome, and refuse to rank noise.

The repo rule is "code computes numbers; models only judge". This script does the
computing so the judgment rests on real arithmetic.

Implements the method extracted from the *Rep Review* build:
  - Wilson score intervals for rates (correct at small counts)
  - the 95% lever test: gap must exceed ~2x standard error, with >= 20 leads per side
  - the 1.4 x standard-error tie band, so nothing is ranked inside the noise
  - a maturity window read from your own won deals (9 in 10 closed)
  - per-item x count reconciliation against the totals

Usage:
  python3 scripts/lever_test.py counts.csv --metric won --habit contacted_twice
  python3 scripts/lever_test.py counts.csv --metric won --habit contacted_twice \\
      --min-side 20 --tie-se-multiple 1.4
  python3 scripts/lever_test.py counts.csv --maturity-from-won

CSV format (one row per lead):
  lead_id,group,habit_col,won_col[,value_col]
  group is the control variable (e.g. lead_source). habit_col is 1/0. won_col is 1/0.

Exit 0 even when nothing is a lever: the output is the finding, not a pass/fail.
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from pathlib import Path


# --- statistics -------------------------------------------------------------

def wilson_interval(successes: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion.

    Use this instead of the normal approximation: it stays inside [0, 1] and keeps
    sensible coverage at the small counts a GTM dataset actually has.
    """
    if n == 0:
        return (0.0, 1.0)
    p = successes / n
    denom = 1 + z * z / n
    centre = p + z * z / (2 * n)
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    lo = (centre - margin) / denom
    hi = (centre + margin) / denom
    # Clamp: floating point can push a boundary marginally outside [0, 1].
    return (max(0.0, min(1.0, lo)), max(0.0, min(1.0, hi)))


def standard_error(successes: int, n: int) -> float:
    """Standard error of a proportion."""
    if n == 0:
        return 1.0
    p = successes / n
    return math.sqrt(p * (1 - p) / n)


def maturity_window(ages: list[int], fallback: int = 90) -> tuple[int, str]:
    """The age by which 9 in 10 won deals had closed, rounded up to a multiple of 5.

    Read the window from your own data instead of assuming one. Returns
    (window_days, explanation).
    """
    if len(ages) < 20:
        return (fallback, f"only {len(ages)} wins (need 20), falling back to {fallback} days")
    ages = sorted(ages)
    idx = min(int(len(ages) * 0.9), len(ages) - 1)
    p90 = ages[idx]
    window = int(math.ceil(p90 / 5) * 5)
    return (window, f"{p90}d covers 90% of {len(ages)} wins, rounded up to {window}d")


# --- lever test -------------------------------------------------------------

def test_lever(
    a_success: int, a_n: int, b_success: int, b_n: int, min_side: int = 20
) -> dict:
    """Is the difference between two groups a lever, or is it inside the noise?"""
    rate_a = a_success / a_n if a_n else 0.0
    rate_b = b_success / b_n if b_n else 0.0
    gap = rate_a - rate_b

    se_a = standard_error(a_success, a_n)
    se_b = standard_error(b_success, b_n)
    se_gap = math.sqrt(se_a * se_a + se_b * se_b)

    reasons: list[str] = []
    if a_n < min_side or b_n < min_side:
        reasons.append(f"a side has fewer than {min_side} leads ({a_n}, {b_n})")
    if se_gap > 0 and abs(gap) <= 2 * se_gap:
        reasons.append(f"gap {gap:+.3f} is inside 2x SE ({2 * se_gap:.3f})")

    lo_a, hi_a = wilson_interval(a_success, a_n)
    lo_b, hi_b = wilson_interval(b_success, b_n)

    return {
        "rate_a": rate_a, "rate_b": rate_b, "gap": gap,
        "se_gap": se_gap, "gap_over_se": (gap / se_gap) if se_gap else 0.0,
        "ci_a": (lo_a, hi_a), "ci_b": (lo_b, hi_b),
        "is_lever": not reasons,
        "reasons": reasons,
    }


def tie_band(successes: int, n: int, multiple: float = 1.4) -> float:
    """The gap below which two entities are tied: 1.4 x the standard error."""
    se = standard_error(successes, n)
    return multiple * se


# --- loading ----------------------------------------------------------------

def load(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def as_bool(v: str) -> int:
    return 1 if str(v).strip().lower() in ("1", "true", "yes", "y", "t") else 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Test whether a habit changes an outcome")
    ap.add_argument("csv", type=Path)
    ap.add_argument("--metric", default="won", help="column with 1/0 outcome")
    ap.add_argument("--habit", default="", help="column with 1/0 habit")
    ap.add_argument("--group", default="group", help="control variable column")
    ap.add_argument("--age", default="", help="column with lead age in days")
    ap.add_argument("--value", default="", help="column with a numeric value (e.g. deal size)")
    ap.add_argument("--min-side", type=int, default=20)
    ap.add_argument("--tie-se-multiple", type=float, default=1.4)
    ap.add_argument("--maturity-from-won", action="store_true",
                    help="print the maturity window derived from won deals")
    a = ap.parse_args(argv)

    if not a.csv.exists():
        print(f"no such file: {a.csv}", file=sys.stderr)
        return 2
    rows = load(a.csv)
    if not rows:
        print("empty csv", file=sys.stderr)
        return 2

    # --- maturity window ---
    if a.maturity_from_won:
        ages = []
        for r in rows:
            if as_bool(r.get(a.metric, "0")) and a.age and r.get(a.age):
                try:
                    ages.append(int(float(r[a.age])))
                except ValueError:
                    pass
        if not ages:
            print("no won rows with an age column", file=sys.stderr)
            return 2
        window, why = maturity_window(ages)
        print(f"MATURITY WINDOW: {window} days — {why}")
        return 0

    if not a.habit:
        ap.error("--habit is required (or use --maturity-from-won)")

    # --- reconcile: per-item x count must equal the total ---
    total_rows = len(rows)
    total_won = sum(as_bool(r.get(a.metric, "0")) for r in rows)
    print("=" * 72)
    print("LEVER TEST")
    print("=" * 72)
    print(f"rows: {total_rows}   wins: {total_won}")

    groups: dict[str, list[dict]] = {}
    for r in rows:
        groups.setdefault(r.get(a.group, "all") or "all", []).append(r)

    print(f"\ncontrol variable '{a.group}': {len(groups)} strata")

    overall_levers = []
    for gname in sorted(groups):
        grows = groups[gname]
        hab = [r for r in grows if as_bool(r.get(a.habit, "0"))]
        nohab = [r for r in grows if not as_bool(r.get(a.habit, "0"))]
        a_s = sum(as_bool(r.get(a.metric, "0")) for r in hab)
        b_s = sum(as_bool(r.get(a.metric, "0")) for r in nohab)

        print(f"\n--- stratum: {gname}  ({len(grows)} leads, {len(hab)} with habit) ---")
        res = test_lever(a_s, len(hab), b_s, len(nohab), a.min_side)

        lo_a, hi_a = res["ci_a"]
        lo_b, hi_b = res["ci_b"]
        print(f"  with habit:    {a_s}/{len(hab)} = {res['rate_a']:.1%}  "
              f"95% CI [{lo_a:.1%}, {hi_a:.1%}]")
        print(f"  without habit: {b_s}/{len(nohab)} = {res['rate_b']:.1%}  "
              f"95% CI [{lo_b:.1%}, {hi_b:.1%}]")
        print(f"  gap: {res['gap']:+.1%}   gap/SE: {res['gap_over_se']:.2f}")

        # Reconciliation: the parts must sum to the whole.
        if a_s + b_s != sum(as_bool(r.get(a.metric, "0")) for r in grows):
            print("  !! RECONCILIATION FAILED: strata do not sum to the total")
        else:
            print(f"  reconciles: {a_s} + {b_s} = {a_s + b_s} wins in stratum")

        if res["is_lever"]:
            print("  VERDICT: LEVER (gap beats 2x SE and both sides are big enough)")
            overall_levers.append((gname, res))
        else:
            print(f"  VERDICT: NOT A LEVER — {'; '.join(res['reasons'])}")

        if a.value:
            vals = [float(r[a.value]) for r in grows if r.get(a.value)]
            if vals:
                band = tie_band(a_s, len(hab), a.tie_se_multiple)
                print(f"  tie band (1.4 x SE): +/-{band:.3f} on the rate")

    print("\n" + "=" * 72)
    if overall_levers:
        print(f"LEVERS FOUND: {len(overall_levers)}")
        for gname, res in overall_levers:
            print(f"  {gname}: {res['rate_a']:.1%} vs {res['rate_b']:.1%} "
                  f"(gap {res['gap']:+.1%}, {res['gap_over_se']:.2f}x SE)")
        print("\nReminder: the lever can differ by stratum. Report it per stratum,")
        print("and give each person ONE number benchmarked against a peer who")
        print("already hits it.")
    else:
        print("NO LEVER FOUND. Report it as an observation, not a cause.")
        print("Do not put it on a chart as a lever. Check the input before you")
        print("check the hypothesis — if the output looks too clean, the input is wrong.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
