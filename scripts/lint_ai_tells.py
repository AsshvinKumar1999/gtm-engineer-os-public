"""Deterministic lint for LLM writing tells. Exit 1 on any hard hit.

Usage: python scripts/lint_ai_tells.py FILE [FILE...]
"""
from __future__ import annotations
import re
import sys
from pathlib import Path

HARD_PATTERNS = {
    "reversal-cliffhanger": r"\b(wasn't|isn't|is not|was not)\s+(the|a|an|about)\s+\w+\.\s+(it|that|the)\s+\w+\s+(was|is)\b",
    "antithesis-tic": r"\bit'?s not (just )?\w+[,.\s\-—]+\s*(it'?s|it is)\s+\w+",
    "ai-vocab": r"\b(delve|leverage|robust|seamless|holistic|synergy|paradigm|empower|harness|streamline|cutting-edge|best-in-class|game-changer|unlock|elevate|tapestry|notably|moreover|furthermore|utilize|underscore|pivotal|transcend|testament|realm)\b",
    "throat-clearing": r"(?im)^\s*(in today's|as we all know|it's no secret|in this article|let me start by|before we begin|it goes without saying)",
    "recap": r"\b(in summary|to recap|key takeaways|in conclusion|to sum up)\b",
    "filler-transition": r"\b(having said that|with that being said|that being said|speaking of which)\b",
    "despite-challenges": r"\bdespite (its|these|the) (challenges|drawbacks|limitations)\b",
    "magic-adverb": r"\b(quietly|fundamentally|deeply|remarkably|profoundly)\s+(transforms|changes|redefines|reveals|signals|matters)\b",
    "vague-attribution": r"\b(industry reports|observers have|experts argue|studies suggest|some critics argue)\b",
    "imagine-a-world": r"\bimagine a world\b",
    "outbound-cliche": r"\b(i hope this (email|message) finds you|saw you('re| are) hiring|congrats(ulations)? on the (raise|new role)|quick call|circle back)\b",
}
EM_DASH_MAX_PER_SENTENCE = 0.15


def lint_text(text: str) -> list[tuple[str, str]]:
    """Return a list of (rule, matched_text) hard hits."""
    hits = []
    for rule, pattern in HARD_PATTERNS.items():
        for m in re.finditer(pattern, text, flags=re.IGNORECASE):
            hits.append((rule, m.group(0)))
    sentences = max(1, len(re.findall(r"[.!?](\s|$)", text)))
    dashes = text.count("—")
    if dashes / sentences > EM_DASH_MAX_PER_SENTENCE:
        hits.append(("em-dash-overuse", f"{dashes} dashes / {sentences} sentences"))
    return hits


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    total = 0
    for path in argv:
        text = Path(path).read_text(encoding="utf-8")
        hits = lint_text(text)
        total += len(hits)
        for rule, snippet in hits:
            print(f"{path}: [{rule}] {snippet!r}")
    print(f"{total} hard hit(s)")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
