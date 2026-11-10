#!/usr/bin/env python3
"""Build a persistent, searchable text corpus from the Crawford PDFs.

Why this exists: `processed.json` records that every PDF was "read", but the extracted
text was never kept on disk. Every quote in the notes therefore cannot be checked
against its source, which breaks the repo rule "every quote must be an exact substring
of its source". This script makes the corpus durable and re-verifiable.

Outputs:
  research/corpus/<slug>.txt          one clean .txt per PDF (immutable once written)
  research/corpus/index.json           per-post metadata + hashes
  research/corpus/INDEX.md            human-readable post index

Usage:
  python3 scripts/build_corpus.py "<SOURCE_DIR>" [--force]
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CORPUS = REPO / "research" / "corpus"

NOISE = [
    re.compile(r"^\d+/\d+/\d+, \d+:\d+ [AP]M.*$"),
    re.compile(r"^https?://\S+ \d+/\d+$"),
    re.compile(r"^On the Edge by Blueprint · https?://\S+ \d+ / \d+$"),
    re.compile(r"^On the Edge by Blueprint · \S+$"),
    re.compile(r"^Share this post.*$"),
]

DATE_PATTERNS = [
    re.compile(r"(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+(\d{1,2}),?\s+(20\d\d)"),
    re.compile(r"(20\d\d)-(\d\d)-(\d\d)"),
]


def slugify(name: str) -> str:
    s = name[: -len(".pdf")] if name.lower().endswith(".pdf") else name
    s = re.sub(r"^On the Edge by Blueprint\s*-\s*", "", s)
    s = re.sub(r"^edge\.blueprintgtm\.com_api_v1_post_pdf_postId=", "post-", s)
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:90] or "post"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def clean(text: str) -> str:
    lines = [l for l in text.splitlines() if not any(p.match(l.strip()) for p in NOISE)]
    text = "\n".join(lines)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def find_date(text: str, fallback: str) -> str:
    for pat in DATE_PATTERNS:
        m = pat.search(text[:6000])
        if m:
            if pat.pattern.startswith("(20"):
                y, mo, d = m.groups()
            else:
                mon, d, y = m.groups()
                try:
                    dt = date(int(y), _MONTHS[mon[:3].lower()], int(d))
                except (KeyError, ValueError):
                    continue
                return dt.isoformat()
            try:
                return date(int(y), int(mo), int(d)).isoformat()
            except ValueError:
                continue
    return fallback


_MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Build a persistent corpus from Crawford PDFs")
    ap.add_argument("source", type=Path)
    ap.add_argument("--force", action="store_true", help="re-extract even if a .txt exists")
    a = ap.parse_args(argv)

    if not a.source.is_dir():
        print(f"not a directory: {a.source}", file=sys.stderr)
        return 2

    CORPUS.mkdir(parents=True, exist_ok=True)
    index: dict[str, dict] = {}

    pdfs = sorted(a.source.glob("*.pdf"))
    if not pdfs:
        print(f"no PDFs in {a.source}", file=sys.stderr)
        return 2

    for i, pdf in enumerate(pdfs, 1):
        try:
            from pypdf import PdfReader
        except ImportError:
            print("pypdf not installed: uv pip install pypdf", file=sys.stderr)
            return 3

        slug = slugify(pdf.name)
        target = CORPUS / f"{slug}.txt"
        h = file_hash(pdf)

        if target.exists() and not a.force:
            text = target.read_text(encoding="utf-8", errors="replace")
        else:
            try:
                reader = PdfReader(pdf)
                raw = "\n".join((pg.extract_text() or "") for pg in reader.pages)
            except Exception as exc:
                print(f"FAILED {pdf.name}: {exc}", file=sys.stderr)
                continue
            text = clean(raw)
            target.write_text(
                f"FILE: {pdf.name}\nSOURCE_SHA16: {h}\n\n{text}", encoding="utf-8"
            )

        body = text.split("\n\n", 1)[-1] if "\n\n" in text else text
        words = len(body.split())
        index[slug] = {
            "file": pdf.name,
            "slug": slug,
            "sha16": h,
            "words": words,
            "chars": len(body),
            "title": pdf.stem.replace("On the Edge by Blueprint - ", "")
            .replace("On the Edge by Blueprint - ", ""),
            "is_titled": not pdf.name.startswith("edge.blueprintgtm.com"),
        }

    (CORPUS / "index.json").write_text(json.dumps(index, indent=1), encoding="utf-8")

    # Human-readable index, sorted by word count so the thin posts are visible.
    lines = [
        "# Crawford corpus index",
        "",
        f"{len(index)} posts extracted to `research/corpus/*.txt`.",
        "",
        "Sorted by length — short posts carry less signal and deserve a re-read.",
        "",
        "| # | slug | words | file |",
        "|---|---|---|---|",
    ]
    for n, (slug, meta) in enumerate(
        sorted(index.items(), key=lambda kv: kv[1]["words"]), 1
    ):
        lines.append(f"| {n} | `{slug}` | {meta['words']} | {meta['file']} |")
    (CORPUS / "INDEX.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    total = sum(m["words"] for m in index.values())
    print(f"corpus: {len(index)} posts, {total:,} words -> {CORPUS}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
