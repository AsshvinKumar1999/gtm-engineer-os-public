#!/usr/bin/env python3
"""Verify every quoted line in the research notes against the corpus, with honest grades.

The repo rule: "Never fabricate a scenario, quote, number or source. Every quote must
be an exact substring of its source." Nothing enforced it before — `processed.json`
recorded that the PDFs were read but kept no text, so no quote could be checked.

Grading. A naive substring test reports false failures because PDF extraction breaks
sentences across lines and swaps typography. So each quote is graded:

  EXACT      - matches a corpus passage exactly after whitespace/typography normalization
  NEAR       - same words, small difference (a word swapped, a number rounded, a typo)
  PARAPHRASE - no close match; the note's wording is not the source's wording
  MISSING    - the quote does not appear in the corpus at all

Only PARAPHRASE and MISSING are real integrity failures. NEAR is transcription drift
worth fixing but not a fabrication.

Outputs:
  research/corpus/quote_audit.json
  research/corpus/QUOTE-AUDIT.md

Usage:
  python3 scripts/verify_quotes.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
CORPUS = REPO / "research" / "corpus"
NOTES = REPO / "research"

TRANSLATE = str.maketrans({
    "‘": "'", "’": "'", "“": '"', "”": '"',
    "—": " ", "–": " ", "…": " ", " ": " ",
    "­": "", "ﬁ": "fi", "ﬂ": "fl",
})

QUOTE_RE = re.compile(r'"([^"\n]{10,400})"')
# Markdown emphasis wrapping a quote: *"like this"*. Capture the inner text too.
EMPH_QUOTE_RE = re.compile(r'\*"(?!\s)([^"*\n]{10,400})"\*')


def extract_quotes(text: str) -> list[str]:
    """Every quoted span in the text, including ones wrapped in markdown emphasis.

    The plain regex pairs quotes by position, so a line with three quoted spans can
    match the wrong pair. Emphasis-wrapped quotes are matched first and their
    spans are then consumed, so the remaining plain regex cannot straddle them.
    """
    found: list[str] = []
    consumed: list[tuple[int, int]] = []

    for m in EMPH_QUOTE_RE.finditer(text):
        found.append(m.group(1))
        consumed.append(m.span())

    def overlaps(a: int, b: int) -> bool:
        return any(not (b <= s or a >= e) for s, e in consumed)

    for m in QUOTE_RE.finditer(text):
        if overlaps(m.start(), m.end()):
            continue
        found.append(m.group(1))

    return found


def normalize(s: str) -> str:
    s = s.translate(TRANSLATE)
    s = re.sub(r"[^\w\s%$.,:;()/&+\-']", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def words(s: str) -> list[str]:
    return re.sub(r"[^\w%$.,:;/&+-]+", " ", s).split()


def loose(s: str) -> str:
    """Word sequence only: no punctuation, no hyphenation, no quote marks.

    PDF extraction breaks words across lines ("go-to- market") and the source uses
    nested quote marks the notes flatten. Both are typography, not wording, so a
    quote that matches on its word sequence alone is still a faithful quote.
    """
    s = normalize(s)
    s = s.replace("- ", "-").replace("-", " ")
    s = s.replace("'", "").replace('"', "")
    s = re.sub(r"[^a-z0-9$%.]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def build_index(hay_words: list[str]) -> dict[str, list[int]]:
    """Inverted index: word -> positions. Makes candidate lookup O(1) instead of O(n)."""
    idx: dict[str, list[int]] = {}
    for i, w in enumerate(hay_words):
        idx.setdefault(w, []).append(i)
    return idx


def best_window_score(
    qw: list[str], hay_words: list[str], index: dict[str, list[int]]
) -> tuple[float, str]:
    """Best similarity of the quote to any same-length window in the corpus.

    Candidate windows are generated from the rarest words in the quote, so the cost is
    proportional to how unusual the quote is rather than to the corpus size.
    """
    n = len(qw)
    if not n or not hay_words or n > len(hay_words):
        return 0.0, ""

    # Anchor on the quote's rarest words; skip ultra-common ones.
    common = {"the", "a", "an", "of", "and", "to", "in", "is", "it", "you", "your",
              "i", "we", "that", "for", "on", "not", "with", "this", "s", "t"}
    ranked = sorted(
        ((len(index.get(w, [])), w) for w in set(qw) if w not in common),
        key=lambda t: t[0],
    )
    anchors = [w for _, w in ranked[:3] if _ < 4000] or [qw[0]]
    if not anchors:
        return 0.0, ""

    positions: set[int] = set()
    for w in anchors:
        for pos in index.get(w, [])[:400]:
            positions.add(pos)

    best, best_txt = 0.0, ""
    for pos in positions:
        for start in (pos - n + 1, pos):
            if start < 0 or start + n > len(hay_words):
                continue
            w = hay_words[start:start + n]
            r = SequenceMatcher(None, qw, w).ratio()
            if r > best:
                best, best_txt = r, " ".join(w)
                if best > 0.995:
                    return best, best_txt
    return best, best_txt


def matches_any(q: str, lq: str, hay_norm: str, hay_loose: str) -> bool:
    """Does the quote appear in the haystack?

    Handles the three legitimate shapes: exact substring, substring without
    trailing punctuation, and an ellipsis-joined quote where each fragment must
    appear in order.
    """
    if q in hay_norm or q.rstrip(".,;:") in hay_norm:
        return True
    if lq and (lq in hay_loose or lq.rstrip(".,;:") in hay_loose):
        return True
    # Ellipsis-joined quote: every fragment must appear, in order.
    if "…" in q or "..." in q:
        frags = [normalize(f) for f in re.split(r"…|\.\.\.", q)]
        frags = [f for f in frags if len(f) >= 8]
        if len(frags) >= 2:
            pos = 0
            ok = True
            for f in frags:
                i = hay_norm.find(f, pos)
                if i < 0:
                    ok = False
                    break
                pos = i + len(f)
            if ok:
                return True
    return False


def main(argv: list[str] | None = None) -> int:
    argv = argv or []
    index_path = CORPUS / "index.json"
    if not index_path.exists():
        print("run build_corpus.py first", file=sys.stderr)
        return 2
    index = json.loads(index_path.read_text())

    raw_texts: dict[str, str] = {}
    for slug in index:
        p = CORPUS / f"{slug}.txt"
        if p.exists():
            raw_texts[slug] = p.read_text(encoding="utf-8", errors="replace")

    hay_norm = "\n".join(normalize(t) for t in raw_texts.values())
    hay_loose = loose(" ".join(raw_texts.values()))
    hay_words: list[str] = []
    for t in raw_texts.values():
        hay_words.extend(words(normalize(t)))
    word_index = build_index(hay_words)

    # Secondary sources: our own research record. A deep memo may legitimately quote
    # SYNTHESIS.md (that is what it is comparing against) or a note batch. These are
    # NOT independent sources for a quote attributed to Crawford, so they are only
    # allowed for files that are themselves downstream of the record.
    secondary_paths = [NOTES / "SYNTHESIS.md", *sorted(NOTES.glob("notes-batch*.md"))]
    secondary_norm = "\n".join(
        normalize(p.read_text(encoding="utf-8", errors="replace"))
        for p in secondary_paths if p.exists()
    )
    secondary_loose = loose(
        " ".join(
            p.read_text(encoding="utf-8", errors="replace")
            for p in secondary_paths if p.exists()
        )
    )

    sources = sorted(NOTES.glob("notes-batch*.md")) + [NOTES / "SYNTHESIS.md"]
    # Extra files to audit (e.g. research/deep/*.md, research/GAP-ANALYSIS.md).
    for arg in argv:
        if arg.startswith("--file="):
            extra = Path(arg.split("=", 1)[1])
            if extra.is_dir():
                sources.extend(sorted(extra.glob("*.md")))
            elif extra.exists():
                sources.append(extra)
    # Dedupe while preserving order (SYNTHESIS.md may be added twice).
    seen_src: set[Path] = set()
    unique_sources = []
    for s in sources:
        if s not in seen_src:
            seen_src.add(s)
            unique_sources.append(s)
    sources = unique_sources
    # The primary record must trace to the corpus only. Downstream files (deep
    # memos, gap analysis, skills) may also quote our own research record.
    primary = {NOTES / "SYNTHESIS.md", *NOTES.glob("notes-batch*.md")}
    findings: list[dict] = []

    for src in sources:
        if not src.exists():
            continue
        is_primary = src in primary
        text = src.read_text(encoding="utf-8", errors="replace")
        for lineno, line in enumerate(text.splitlines(), 1):
            for raw in extract_quotes(line):
                raw = raw.strip()
                q = normalize(raw)
                if len(q) < 10:
                    continue
                if matches_any(q, loose(raw), hay_norm, hay_loose):
                    findings.append({"source": src.name, "line": lineno,
                                     "quote": raw, "grade": "EXACT", "score": 1.0})
                    continue
                if not is_primary:
                    if matches_any(q, loose(raw), secondary_norm, secondary_loose):
                        findings.append({"source": src.name, "line": lineno,
                                         "quote": raw, "grade": "EXACT", "score": 1.0})
                        continue
                qw = words(q)
                score, near = best_window_score(qw, hay_words, word_index)
                if score >= 0.97:
                    grade = "NEAR"
                elif score >= 0.72:
                    grade = "PARAPHRASE"
                else:
                    grade = "MISSING"
                findings.append({
                    "source": src.name, "line": lineno, "quote": raw,
                    "grade": grade, "score": round(score, 3), "nearest": near[:300],
                })

    (CORPUS / "quote_audit.json").write_text(json.dumps(findings, indent=1), encoding="utf-8")

    counts = Counter(f["grade"] for f in findings)
    bad = [f for f in findings if f["grade"] in ("PARAPHRASE", "MISSING")]

    lines = [
        "# Quote audit — notes vs. corpus",
        "",
        f"Corpus: {len(raw_texts)} posts. Quotes checked: {len(findings)}.",
        "",
        "| grade | count | meaning |",
        "|---|---|---|",
        f"| EXACT | {counts['EXACT']} | exact substring of the source |",
        f"| NEAR | {counts['NEAR']} | same words, minor drift (typo/rounding) |",
        f"| PARAPHRASE | {counts['PARAPHRASE']} | note's wording is not the source's wording |",
        f"| MISSING | {counts['MISSING']} | quote not found in the corpus |",
        "",
        f"**Integrity failures (PARAPHRASE + MISSING): {len(bad)}.**",
        "",
        "These are quotes the notes present as Crawford's words but that the PDFs do not "
        "contain in that form. Each needs correction, relabelling as a paraphrase, or removal.",
        "",
    ]
    if bad:
        lines += [
            "## Failures",
            "",
            "| source:line | grade | score | quote | nearest corpus text |",
            "|---|---|---|---|---|",
        ]
        for f in bad:
            q = f["quote"].replace("|", "/")[:130]
            n = (f.get("nearest") or "").replace("|", "/")[:130]
            lines.append(
                f"| {f['source']}:{f['line']} | {f['grade']} | {f['score']} | {q} | {n} |"
            )
    (CORPUS / "QUOTE-AUDIT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"quotes checked: {len(findings)}")
    for g in ("EXACT", "NEAR", "PARAPHRASE", "MISSING"):
        print(f"  {g:<11} {counts[g]}")
    print(f"integrity failures: {len(bad)} -> {CORPUS / 'QUOTE-AUDIT.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
