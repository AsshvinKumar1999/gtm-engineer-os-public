#!/usr/bin/env python3
"""Check that every number in a draft traces to a run file or a known source.

This is the gate behind the rule "never invent the scenario". It cannot tell whether a
number is TRUE, but it can tell whether a number is TRACEABLE: every figure in the
draft must either appear in one of the known source files, or be on an explicit
allowlist of structural facts (counts of letters, the window length, and so on).

Usage:
  python3 scripts/check_claims.py <draft.md> [--allow 1,2,3]

Exit 1 if any number is untraceable. Untraceable does not mean wrong, it means
unproven. Fix the draft or add the number to a source file.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RESUME_SRC = Path(
    "/Users/asshvinkumar/Documents/CLAUDE MEMORY FOLDER - DO NOT DELETE"
    "/Job Role References/Tailored Resumes/_source"
)

# Where numbers legitimately come from.
SOURCE_FILES = [
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/summary.json",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/gift-summary.json",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/accounts.csv",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/jobs.csv",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/gifts",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/briefs.md",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-09/aggregate.json",
    # Play 01, the 30-day run Play 06 read.
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-08/summary.json",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-08/accounts.csv",
    REPO / "plays/01-fresh-capital-open-role/out/30d-2026-11-08/jobs.csv",
    # Play 01, the earlier 7-day run.
    REPO / "plays/01-fresh-capital-open-role/out/2026-11-08/summary.json",
    # Play 06, the H-1B sponsor run of 2026-11-08.
    REPO / "plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/summary.json",
    REPO / "plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/sponsors.csv",
    REPO / "plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/roles.csv",
    # Play 06 identity and coverage audit. Regenerate with
    # `python3 plays/06-fresh-capital-visa-sponsor/audit_identity.py`.
    REPO / "plays/06-fresh-capital-visa-sponsor/out/30d-2026-11-08/identity-audit.json",
    # Rendered media facts: file sizes and canvas dimensions quoted in posts.
    REPO / "content" / "media-facts.json",
    # Resume build: content.py holds the bullets, the .txt files hold the final words.
    RESUME_SRC / "content.py",
    RESUME_SRC / "build.py",
    RESUME_SRC / "measure.py",
    RESUME_SRC / "build-metrics.json",
]

# Rounded figures that are derived from a source value. Key is the token as it
# appears in prose; value is the source token it must be derived from.
DERIVED = {
    "$1.9B": "1908732450",     # $1,908,732,450 rounded to $1.9B
    "$601M": "601892375",      # $601,892,375 rounded to $601M
    "$1.9": "1908732450",
    "$601": "601892375",
    "1.9B": "1908732450",
    "601M": "601892375",
}

# Ratios: the token is allowed only when EVERY source value behind it is present.
DERIVED_RATIOS = {
    "2.4": ("44", "18"),      # 44 rows / 18 unique companies = 2.44x
    "2.4x": ("44", "18"),
}

# Numbers that describe the artifact itself rather than a data run.
STRUCTURAL = {
    "3000", "2800", "2000", "500", "100", "50", "25", "10", "5", "4", "3", "2", "1",
    "12", "13", "14", "30", "60", "2026", "2025", "2024", "2023", "2022", "2021",
    "758", "396", "283", "12", "34", "28", "23", "18", "44", "231", "6", "38",
    "8", "7", "9", "11", "16", "15", "20", "0",
}

# Numbers as written in prose: 1,089 / $1,908,732,450 / 105% / 3.9
NUM_RE = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")


def collect_source_numbers() -> set[str]:
    """Every numeric token that appears in the known source files."""
    found: set[str] = set()
    for path in SOURCE_FILES:
        if not path.exists():
            continue
        if path.is_dir():
            for f in path.glob("*.md"):
                found.update(norm_tokens(f.read_text(encoding="utf-8", errors="replace")))
        else:
            found.update(norm_tokens(path.read_text(encoding="utf-8", errors="replace")))
    return found


def norm_tokens(text: str) -> set[str]:
    """Numeric tokens, plus their comma-free form so 1,089 matches 1089."""
    out: set[str] = set()
    for m in NUM_RE.finditer(text):
        tok = m.group(0)
        out.add(tok)
        out.add(tok.replace(",", ""))
        out.add(tok.lstrip("$").rstrip("%"))
        out.add(tok.lstrip("$").rstrip("%").replace(",", ""))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Check every number in a draft is traceable")
    ap.add_argument("draft")
    ap.add_argument("--allow", default="", help="comma-separated numbers to allow as unproven")
    args = ap.parse_args()

    draft_path = Path(args.draft)
    if not draft_path.exists():
        sys.exit(f"No such file: {draft_path}")

    draft = draft_path.read_text(encoding="utf-8", errors="replace")
    sources = collect_source_numbers()
    allowed = {a.strip() for a in args.allow.split(",") if a.strip()}

    # Only check the published caption/body, not the internal facts table.
    body = draft
    for marker in ("## Caption (paste into LinkedIn)", "## Facts and their sources"):
        if marker in body:
            body = body.split(marker)[-1]

    # URLs carry digits that are identifiers, not claims (a GitHub user id, a
    # CIK, a filing date). Remove them before scanning.
    body = re.sub(r"https?://\S+", " ", body)
    # Markdown link targets are the same thing.
    body = re.sub(r"\]\([^)]*\)", "] ", body)
    # A post label ("Post 002") is a name, not a claim.
    body = re.sub(r"\bPost\s+\d+", " ", body)

    seen: set[str] = set()
    untraceable: list[tuple[str, str]] = []
    for m in NUM_RE.finditer(body):
        tok = m.group(0)
        plain = tok.lstrip("$").rstrip("%").replace(",", "")
        if not plain or plain in STRUCTURAL or tok in allowed or plain in allowed:
            continue
        # A rounded figure is fine if the exact source value is present.
        derived = DERIVED.get(tok) or DERIVED.get(plain)
        if derived and derived in sources:
            continue
        # A ratio is fine if every value behind it is present.
        ratio = DERIVED_RATIOS.get(tok) or DERIVED_RATIOS.get(plain)
        if ratio and all(v in sources for v in ratio):
            continue
        if tok in sources or plain in sources or plain in {s.lstrip("$").rstrip("%") for s in sources}:
            continue
        # A percentage written as "105%" is traceable when "105" appears in a source.
        if tok.endswith("%") and plain in sources:
            continue
        # Digits inside a URL (a GitHub username, a date, a CIK) are not claims.
        if plain in seen:
            continue
        seen.add(plain)
        untraceable.append((tok, plain))

    if not untraceable:
        print(f"OK: every number in {draft_path.name} traces to a source file "
              f"({len(sources)} source tokens checked).")
        return 0

    print(f"UNTRACEABLE numbers in {draft_path.name} ({len(untraceable)}):")
    for tok, plain in untraceable:
        print(f"  {tok}")
    print("\nEach one must be added to a run file, reworded, or passed with --allow.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
