"""Turn a **bold** draft into LinkedIn-ready text and check its length the way LinkedIn counts.

LinkedIn has no bold, so we use Unicode "Mathematical Sans-Serif Bold" letters. Each of those
counts as 2 characters toward LinkedIn's 3,000 limit (it counts UTF-16 code units).

Usage:
  python3 scripts/linkedin_format.py draft.md            # prints the post and its count
  python3 scripts/linkedin_format.py draft.md -o post.txt
Exits 1 if the post is over the limit.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

LIMIT = 3000
TARGET = 2800  # leave room for an @mention and small edits


def to_bold(text: str) -> str:
    out = []
    for ch in text:
        if "A" <= ch <= "Z":
            out.append(chr(0x1D5D4 + ord(ch) - ord("A")))
        elif "a" <= ch <= "z":
            out.append(chr(0x1D5EE + ord(ch) - ord("a")))
        elif "0" <= ch <= "9":
            out.append(chr(0x1D7EC + ord(ch) - ord("0")))
        else:
            out.append(ch)
    return "".join(out)


def render(draft: str) -> str:
    """Replace **bold** spans with Unicode bold."""
    return re.sub(r"\*\*(.+?)\*\*", lambda m: to_bold(m.group(1)), draft, flags=re.S)


def linkedin_length(text: str) -> int:
    """Characters as LinkedIn counts them (UTF-16 code units)."""
    return len(text.encode("utf-16-le")) // 2


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("draft", help="text file with **bold** markers")
    ap.add_argument("-o", "--out", help="write the LinkedIn-ready text here")
    args = ap.parse_args()
    post = render(Path(args.draft).read_text().strip())
    n = linkedin_length(post)
    if args.out:
        Path(args.out).write_text(post + "\n")
    else:
        print(post)
        print()
    status = "OK" if n <= TARGET else ("TIGHT" if n <= LIMIT else "OVER LIMIT")
    print(f"LinkedIn length: {n} / {LIMIT} ({status}; aim for {TARGET} or less)", file=sys.stderr)
    return 1 if n > LIMIT else 0


if __name__ == "__main__":
    sys.exit(main())
