#!/usr/bin/env python3
"""Play 01, gift edition: for each target company, find THEIR buyers.

Same two public signals as run.py (SEC Form D + public ATS boards), but the
scoring is inverted. run.py asks "did this company raise AND hire a GTM role".
This asks "did this company raise AND hire the kind of role that company
sells into" - because a gift to a hiring manager is their buyer list, not
their peer list.

For each target company we reuse the cached SEC parse, re-score the job
boards against that company's buyer signature, and write one sheet.

Usage:
  SEC_USER_AGENT="Your Name you@example.com" python3 gift.py \
      --end 2026-11-08 --days 30 --out out/30d-2026-11-09
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run import (  # noqa: E402
    ATS_WORKERS,
    FUND_RE,
    SEC,
    one_per_company,
    find_board,
)

# --------------------------------------------------------------------------
# Buyer signatures: what role means "this company needs what we sell".
# Each pattern is matched against the job TITLE only.
# --------------------------------------------------------------------------
BUYER_PROFILES = {
    "Baseten": {
        "regex": r"machine learning|\bml\b|\bai engineer|inference|data scientist|\bmlops\b|"
                 r"deep learning|model serving|generative ai|\bai\b",
        "why": "Baseten sells inference. A company that just raised and is hiring ML/AI "
               "engineers is buying inference capacity.",
        "sell": "inference",
    },
    "Bluejay": {
        "regex": r"voice|conversational|speech|audio|\bnlp\b|natural language|"
                 r"\bai engineer|machine learning|agent",
        "why": "Bluejay sells evals and observability for voice and text agents. "
               "A company hiring voice/AI/agent engineers is shipping agents that need evals.",
        "sell": "agent evals",
    },
    "FlowGen Labs": {
        "regex": r"\bsap\b|s/4hana|erp|salesforce|systems? analyst|systems? engineer|"
                 r"requirements? engineer|technical program manager",
        "why": "FlowGen Labs sells GTM engineering for companies mid-migration. A job post "
               "naming SAP, ERP or systems work shows a migration in progress.",
        "sell": "migration GTM",
    },
    "Nectar": {
        "regex": r"community|social|brand|marketing|growth|content|creative",
        "why": "Nectar sells community-led growth for consumer brands. A company that just "
               "raised and is hiring community, social or brand roles is spending on growth.",
        "sell": "community growth",
    },
    "Wispr Flow": {
        "regex": r"account executive|\bsales\b|sales development|\bsdr\b|\bbdr\b|"
                 r"business development|sales manager|sales operations|revenue operations",
        "why": "Wispr Flow sells dictation and meeting notes into sales teams. A company "
               "hiring a sales team is buying seats.",
        "sell": "dictation seats",
    },
}


def load_tech(out: Path, days: int, end: dt.date) -> list[dict]:
    """Reuse the cached SEC parse from run.py if the window matches."""
    cache = out / f"sec-cache-{end - dt.timedelta(days=days-1)}-{end}.json"
    if cache.exists():
        saved = json.loads(cache.read_text())
        print(f"[1] Loaded SEC results from {cache.name}", flush=True)
        _, _, tech = saved["filings"], saved["operating"], saved["tech"]
        return one_per_company(tech)
    sys.exit(f"No SEC cache at {cache}. Run run.py first for the same window.")


def load_boards(cache_file: Path, tech: list[dict], ua: str) -> dict:
    """Probe public ATS boards once, cache the result, reuse across profiles."""
    if cache_file.exists():
        print(f"[2] Loaded board cache from {cache_file.name}", flush=True)
        return json.loads(cache_file.read_text())
    print(f"[2] Probing public ATS boards for {len(tech)} companies "
          f"(one pass, cached for every profile)", flush=True)
    with ThreadPoolExecutor(ATS_WORKERS) as pool:
        boards = list(pool.map(lambda a: find_board(a["company"], ua), tech))
    out = {}
    for a, b in zip(tech, boards):
        if b:
            out[a["company"]] = {"ats": b["ats"], "verified": b["verified"],
                                 "jobs": b["jobs"], "slug": b["slug"]}
    cache_file.write_text(json.dumps(out))
    print(f"    boards found: {len(out)}", flush=True)
    return out


def score_profile(tech: list[dict], boards: dict, profile: dict) -> list[dict]:
    """Companies that raised AND are hiring this profile's buyer signature."""
    pat = re.compile(profile["regex"], re.I)
    hits = []
    for a in tech:
        b = boards.get(a["company"])
        if not b:
            continue
        matched = [j for j in b["jobs"] if pat.search(j[0])]
        if not matched:
            continue
        hits.append({
            "company": a["company"],
            "state": a.get("state", ""),
            "raised": a.get("amount_sold", ""),
            "offering": a.get("offering_total", ""),
            "filed": a.get("filed", ""),
            "filing_url": a.get("filing_url", ""),
            "first_sale": a.get("first_sale", ""),
            "people": a.get("people", ""),
            "ats": b["ats"],
            "board_match": "name-verified" if b["verified"] else "slug-only",
            "roles": [(m[0], m[1], m[2]) for m in matched[:4]],
            "role_count": len(matched),
        })
    hits.sort(key=lambda r: (r["board_match"] != "name-verified",
                             -(int(r["raised"]) if str(r["raised"]).isdigit() else 0)))
    return hits


def fmt_usd(v: str) -> str:
    try:
        return f"${int(v):,}"
    except (TypeError, ValueError):
        return "?"


def write_sheet(target: str, profile: dict, hits: list[dict], out: Path,
                window: str) -> Path:
    """One markdown sheet per target company: the gift, ready to forward."""
    d = out / "gifts"
    d.mkdir(parents=True, exist_ok=True)
    path = d / f"{target}.md"
    lines = [
        f"# Gift sheet for {target}",
        "",
        f"**What they sell:** {profile['sell']}.",
        f"**Why this list:** {profile['why']}",
        "",
        f"**Filing window:** {window}. SEC Form D + public Greenhouse/Lever/Ashby boards. $0 data.",
        f"**Companies that raised and are hiring:** {len(hits)}",
        "",
        "Every company below filed a Form D in the window AND has a live job post "
        "matching the signature. Name-verified boards are confirmed by company name; "
        "slug-only means the board was matched by URL slug.",
        "",
    ]
    if not hits:
        lines += ["_No matches in this window. Widen the window or the signature._", ""]
    for h in hits:
        lines += [
            f"## {h['company']} ({h['state']})",
            f"- Raised: **{fmt_usd(h['raised'])}** sold of {fmt_usd(h['offering'])} offering"
            + (f" · first sale {h['first_sale']}" if h["first_sale"] else ""),
            f"- Filed: {h['filed']} · [Form D]({h['filing_url']})",
            f"- Board: {h['ats']} ({h['board_match']}) · {h['role_count']} matching role(s)",
        ]
        for title, url, loc in h["roles"]:
            loc_part = f" · {loc}" if loc else ""
            lines.append(f"- [{title}]({url}){loc_part}")
        if h["people"]:
            lines.append(f"- People on the filing: {h['people']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description="Play 01 gift edition: buyer lists per target company")
    ap.add_argument("--days", type=int, default=30)
    ap.add_argument("--end", help="last filing date YYYY-MM-DD")
    ap.add_argument("--out", help="output folder (same one run.py wrote)")
    args = ap.parse_args()
    ua = os.environ.get("SEC_USER_AGENT", "")
    if "@" not in ua:
        sys.exit("Set SEC_USER_AGENT='Your Name your@email.com' (SEC requires a contact).")
    end = dt.date.fromisoformat(args.end) if args.end else dt.date.today() - dt.timedelta(days=1)
    out = Path(args.out).resolve()

    tech = load_tech(out, args.days, end)
    print(f"    tech companies (one per company): {len(tech)}", flush=True)
    boards = load_boards(out / f"boards-{end}.json", tech, ua)

    summary = {}
    window = f"{end - dt.timedelta(days=args.days - 1)} to {end}"
    for target, profile in BUYER_PROFILES.items():
        hits = score_profile(tech, boards, profile)
        path = write_sheet(target, profile, hits, out, window)
        verified = sum(1 for h in hits if h["board_match"] == "name-verified")
        summary[target] = {"matches": len(hits), "name_verified": verified,
                           "sheet": str(path.relative_to(out.parent))}
        print(f"[gift] {target}: {len(hits)} match(es), {verified} name-verified -> {path.name}",
              flush=True)

    (out / "gift-summary.json").write_text(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
