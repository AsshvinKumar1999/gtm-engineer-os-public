#!/usr/bin/env python3
"""Audit the DOL sponsor index and the Play 06 run.

Play 06 matches a company that just raised money to the Department of Labor's H-1B
wage filings. The primary join key is the company's tax ID (EIN), read from the
header of its own SEC filing. The fallback key is the employer name, normalized.

This script measures the three things that decide how honest a claim about that
matching can be:

  1. Index size: how many certified H-1B rows the index is built from, how many
     employers it holds, and how many name keys sit on top of those employers.
  2. Name collisions: how many employer names are carried by two or more
     different tax IDs, and how many employers a name lookup can reach at all.
  3. The coverage ceiling: the newest decision date in the index, compared with
     the end of the Form D window the run covers.

Every number written into a post must come from this file.

Usage:
  python3 audit_identity.py
  python3 audit_identity.py --index data/sponsors.json --run out/30d-2026-11-08
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
SUFFIX_RE = re.compile(r"\b(inc|incorporated|llc|l\.l\.c|corp|corporation|co|company|ltd|limited|pbc|lp|llp)\b\.?", re.I)

# Word length and stop words are the ones run.py uses to compare job titles.
STOP = {"senior", "staff", "lead", "principal", "junior", "associate", "manager", "director", "head",
        "with", "team", "remote", "the", "and", "for", "level", "intern", "global", "group"}


def norm_name(s: str) -> str:
    """The name key Play 06 uses. Must match build_index.py exactly."""
    return re.sub(r"[^a-z0-9]", "", SUFFIX_RE.sub("", (s or "").lower()))


def title_words(s: str) -> set[str]:
    """The title comparison run.py uses to flag a role as similar to a sponsored one."""
    return {w for w in re.findall(r"[a-z]+", (s or "").lower()) if len(w) >= 4 and w not in STOP}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--index", default=str(HERE / "data" / "sponsors.json"))
    ap.add_argument("--run", default=str(HERE / "out" / "30d-2026-11-08"))
    ap.add_argument("--out", default=str(HERE / "out" / "30d-2026-11-08" / "identity-audit.json"))
    args = ap.parse_args()

    idx = json.loads(Path(args.index).read_text())
    by_fein = idx["by_fein"]
    by_name = idx["by_name"]

    # --- 1. index size ---------------------------------------------------
    last_decisions = [r["last_decision"] for r in by_fein.values() if r.get("last_decision")]
    newest_decision = max(last_decisions)

    # --- 2. name collisions ----------------------------------------------
    # Group the employer records by the name they are stored under, so a name
    # carried by two different tax IDs shows up.
    raw_to_feins: dict[str, set[str]] = defaultdict(set)
    for fein, rec in by_fein.items():
        raw_to_feins[rec.get("name", "")].add(fein)
    raw_shared = {k: v for k, v in raw_to_feins.items() if len(v) > 1}

    norm_to_feins: dict[str, set[str]] = defaultdict(set)
    for raw, feins in raw_to_feins.items():
        norm_to_feins[norm_name(raw)] |= feins
    norm_shared = {k: v for k, v in norm_to_feins.items() if len(v) > 1}

    # by_name keeps one record per normalized name (setdefault), so a name
    # carried by two tax IDs can only ever point at one of them.
    shadowed = [k for k in norm_shared if k in by_name and by_name[k].get("fein") in norm_shared[k]]

    # Which tax IDs can a name lookup reach at all?
    fein_to_names: dict[str, set[str]] = defaultdict(set)
    for key, rec in by_name.items():
        fein = rec.get("fein")
        if fein:
            fein_to_names[fein].add(key)
    unreachable = sorted(f for f in by_fein if f not in fein_to_names)

    # A shared name keeps ONE tax ID in by_name (setdefault). The other tax IDs
    # are hidden behind that name, unless a different spelling reaches them.
    hidden, hidden_unreachable = [], []
    for key, feins in norm_shared.items():
        rec = by_name.get(key)
        if not rec or not rec.get("fein"):
            continue
        kept = rec["fein"]
        for f in feins:
            if f == kept:
                continue
            hidden.append(f)
            if f not in fein_to_names:
                hidden_unreachable.append(f)

    collisions = []
    for raw in sorted(raw_shared):
        feins = sorted(raw_shared[raw])
        collisions.append({
            "employer_name": raw,
            "normalized_name": norm_name(raw),
            "tax_ids": feins,
            "certified_h1b_per_tax_id": [by_fein[f]["certified_h1b"] for f in feins],
            "last_decision_per_tax_id": [by_fein[f]["last_decision"] for f in feins],
        })

    # The same, but for names that only collide AFTER normalizing. A DBA
    # suffix or a spelled-out suffix makes two tax IDs share a name key.
    normalized_collisions = []
    for key in sorted(norm_shared):
        feins = sorted(norm_shared[key])
        kept = by_name.get(key, {}).get("fein")
        normalized_collisions.append({
            "normalized_name": key,
            "employer_names": sorted({by_fein[f]["name"] for f in feins}),
            "tax_ids": feins,
            "certified_h1b_per_tax_id": [by_fein[f]["certified_h1b"] for f in feins],
            "last_decision_per_tax_id": [by_fein[f]["last_decision"] for f in feins],
            "name_index_kept_tax_id": kept,
            "tax_ids_hidden": [f for f in feins if f != kept],
        })

    # --- 3. the run ------------------------------------------------------
    run = Path(args.run)
    sponsors = list(csv.DictReader(open(run / "sponsors.csv")))
    roles = list(csv.DictReader(open(run / "roles.csv")))
    play06 = json.loads((run / "summary.json").read_text())

    by_ein = [s for s in sponsors if s["match"] == "EIN"]
    name_only = [s for s in sponsors if s["match"] == "name-only"]
    hiring = Counter(r["company"] for r in roles)
    flagged = [r for r in roles if r["similar_title_sponsored"] == "yes"]
    flagged_by_company = Counter(r["company"] for r in flagged)

    # How many of Modal's flags come from one generic sponsored title?
    modal_generic = 0
    for r in flagged:
        if r["company"] != "Modal Labs, Inc.":
            continue
        hits = [t for t in r["h1b_titles"].split(" | ") if len(title_words(r["title"]) & title_words(t)) >= 2]
        if hits and all("technical" in title_words(t) for t in hits):
            modal_generic += 1

    top_two = flagged_by_company.most_common(2)
    top_two_flags = sum(n for _, n in top_two)

    # --- 4. the coverage ceiling -----------------------------------------
    # The Form D window this run covers ends on the day the Play 01 run closed.
    play01 = json.loads((HERE.parent / "01-fresh-capital-open-role" / "out" / "30d-2026-11-08"
                         / "summary.json").read_text())
    window_end = dt.date.fromisoformat(play01["window"].split(" to ")[1])
    ceiling_date = dt.date.fromisoformat(newest_decision)
    gap_days = (window_end - ceiling_date).days
    employers_after_ceiling = sum(1 for d in last_decisions if d > newest_decision)

    cert_counts = sorted(int(s["h1b_certified"]) for s in sponsors)

    # How many of the sponsors had a job board Play 01 could find at all?
    # A sponsor with no board is not a sponsor that is not hiring.
    play01_accounts = list(csv.DictReader(open(HERE.parent / "01-fresh-capital-open-role" / "out"
                                               / "30d-2026-11-08" / "accounts.csv")))
    p01_board = {a["company"]: a["board_match"] for a in play01_accounts}
    sponsors_with_board = [s for s in sponsors if p01_board.get(s["company"])]
    sponsors_without_board = [s for s in sponsors if not p01_board.get(s["company"])]

    # The earlier, shorter Play 01 run, for comparison.
    play01_short = json.loads((HERE.parent / "01-fresh-capital-open-role" / "out" / "2026-11-08"
                                / "summary.json").read_text())

    # --- 5. what a name-only join would have done -------------------------
    # For every sponsor in the run, look the company up by name only and see
    # whether the name route lands on the same tax ID the EIN route found.
    # Three honest outcomes:
    #   same        - name route lands on the tax ID the run used
    #   different   - name route lands on another tax ID (a wrong answer)
    #   run_no_tax_id - the run matched by name, so there is no tax ID to compare
    #   miss        - the name route finds nothing at all
    name_route_same, name_route_diff, name_route_miss, name_route_no_tax_id = 0, 0, 0, 0
    name_route_details = []
    for s in sponsors:
        rec = by_name.get(norm_name(s["company"]))
        if rec is None:
            name_route_miss += 1
            name_route_details.append({"company": s["company"], "run_match": s["match"],
                                       "name_route_fein": None, "run_ein": s["ein"] or None,
                                       "name_route_outcome": "miss"})
            continue
        got = rec.get("fein", "")
        want = s["ein"]
        if not want:
            name_route_no_tax_id += 1
            outcome = "run_no_tax_id"
        elif got == want:
            name_route_same += 1
            outcome = "same"
        else:
            name_route_diff += 1
            outcome = "different"
        name_route_details.append({"company": s["company"], "run_match": s["match"],
                                   "name_route_fein": got or None, "run_ein": want or None,
                                   "name_route_outcome": outcome,
                                   "name_route_certified": rec["certified_h1b"]})

    # How many sponsors carry a different employer name at the DOL than at the SEC?
    dol_name_differs = [s["company"] for s in sponsors if s["dol_employer_name"] != s["company"]]
    # And how many of those still normalize to the same name key?
    dol_name_differs_after_normalizing = [s["company"] for s in sponsors
                                           if s["dol_employer_name"] != s["company"]
                                           and norm_name(s["dol_employer_name"]) != norm_name(s["company"])]

    # --- 6. the pipeline's own constants ----------------------------------
    # Numbers quoted about how the pipeline behaves come from here, so they
    # are traceable to a file rather than to a sentence someone typed.
    run_src = (HERE / "run.py").read_text()
    delay = float(re.search(r"SEC_DELAY_S\s*=\s*([\d.]+)", run_src).group(1))
    xlsx_bytes = (HERE / "data" / idx["source"]).stat().st_size

    out = {
        "note": "Identity, coverage and run audit for Play 06. Regenerate with audit_identity.py.",
        "index": {
            "source_file": idx["source"],
            "rows_read": idx["rows_read"],
            "certified_h1b": idx["certified_h1b"],
            "employers": idx["employers"],
            "by_fein_entries": len(by_fein),
            "by_name_entries": len(by_name),
            "extra_name_keys_vs_employers": len(by_name) - len(by_fein),
            "employers_reachable_by_more_than_one_name": sum(1 for s in fein_to_names.values() if len(s) > 1),
            "employers_with_no_name_route": len(unreachable),
            "tax_ids_hidden_behind_a_shared_name": len(hidden),
            "hidden_tax_ids_with_no_other_name_route": len(hidden_unreachable),
            "normalized_names_shared_by_two_or_more_tax_ids": len(norm_shared),
            "raw_names_shared_by_two_or_more_tax_ids": len(raw_shared),
            "shared_names_shadowed_in_the_name_index": len(shadowed),
            "collisions": collisions,
            "normalized_collisions": normalized_collisions,
        },
        "coverage": {
            "newest_decision_date_in_index": newest_decision,
            "earliest_decision_date_in_index": min(last_decisions),
            "source_file_bytes": xlsx_bytes,
            "source_file_megabytes": round(xlsx_bytes / 1_000_000),
            "sec_delay_seconds_between_filing_fetches": delay,
            "employers_with_a_filing_after_the_ceiling": employers_after_ceiling,
            "form_d_window": play01["window"],
            "form_d_window_end": window_end.isoformat(),
            "days_between_ceiling_and_window_end": gap_days,
            "months_between_ceiling_and_window_end": round(gap_days / 30.44, 1),
        },
        "run": {
            "run_dir": str(run.relative_to(HERE.parent)) if str(run).startswith(str(HERE.parent)) else str(run),
            "play01_window": play01["window"],
            "play01_form_d_filings": play01["form_d_new"],
            "play01_operating_companies": play01["operating"],
            "play01_tech_companies": play01["tech"],
            "play01_open_roles": play01["open_roles"],
            "tech_companies_checked": play06["tech_companies"],
            "ein_found": play06["ein_found"],
            "sponsors": len(sponsors),
            "matched_by_tax_id": len(by_ein),
            "matched_by_name_only": len(name_only),
            "name_only_companies": [s["company"] for s in name_only],
            "sponsors_hiring_now": len(hiring),
            "open_roles_at_sponsors": len(roles),
            "roles_flagged_similar": len(flagged),
            "flagged_by_company": dict(flagged_by_company),
            "top_two_flagged_companies": [c for c, _ in top_two],
            "top_two_flagged_roles": top_two_flags,
            "top_two_share_of_flags_percent": round(top_two_flags / len(flagged) * 100, 1),
            "modal_flags_from_one_generic_title": modal_generic,
            "modal_roles": hiring.get("Modal Labs, Inc.", 0),
            "modal_flags": flagged_by_company.get("Modal Labs, Inc.", 0),
            "legora_roles": hiring.get("Legora, Inc.", 0),
            "legora_flags": flagged_by_company.get("Legora, Inc.", 0),
            "certified_h1b_per_sponsor": cert_counts,
            "sponsors_with_exactly_one_certified_filing": sum(1 for c in cert_counts if c == 1),
            "sponsors_with_four_or_more_certified_filings": sum(1 for c in cert_counts if c >= 4),
            "roles_per_hiring_company": dict(hiring),
            "sponsors_with_a_job_board_found": len(sponsors_with_board),
            "sponsors_with_no_job_board_found": len(sponsors_without_board),
            "play01_tech_companies_with_a_board": play01["with_board"],
            "name_route_would_land_on_same_tax_id": name_route_same,
            "name_route_would_land_on_a_different_tax_id": name_route_diff,
            "name_route_would_find_nothing": name_route_miss,
            "name_route_found_nothing_for_a_run_with_no_tax_id": name_route_no_tax_id,
            "name_route_total_sponsors_reached": name_route_same + name_route_diff + name_route_no_tax_id,
            # The fallback fires for every company the tax ID route did not settle:
            # those with no EIN in the filing header, plus those whose EIN is not
            # in the index. That is every company except the 23 matched by EIN.
            "name_route_attempts": play06["tech_companies"] - len(by_ein),
            "name_route_hits": len(name_only),
            "name_route_per_sponsor": name_route_details,
            "sponsors_whose_dol_name_differs_from_sec_name": len(dol_name_differs),
            "sponsors_whose_names_differ_after_normalizing": len(dol_name_differs_after_normalizing),
            "play01_short_run": {
                "window": play01_short["window"],
                "form_d_filings": play01_short["form_d_new"],
                "operating_companies": play01_short["operating"],
                "tech_companies": play01_short["tech"],
                "open_roles": play01_short["open_roles"],
                "tier1": play01_short["tier1"],
            },
        },
    }
    out["run"]["tier1_similar_role_open"] = play06["tier1_similar_role_open"]
    out["run"]["tier2_other_roles_open"] = play06["tier2_other_roles_open"]
    out["run"]["tier3_no_open_roles_found"] = play06["tier3_no_open_roles_found"]

    dest = Path(args.out)
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"Wrote {dest}")
    print(json.dumps({"index": {k: v for k, v in out["index"].items() if k != "collisions"},
                      "coverage": out["coverage"], "run": out["run"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
