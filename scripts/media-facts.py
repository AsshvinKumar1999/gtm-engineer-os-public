#!/usr/bin/env python3
"""Record the rendered media facts for each post into one traceable file.

File sizes and canvas dimensions quoted in a post must trace to a file, the same way
every other number does. Run this after rendering a graphic.

Usage:
  python3 scripts/media-facts.py [post_dir ...]
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
POSTS = REPO / "content" / "posts"


def probe(post_dir: Path) -> dict | None:
    out = post_dir / "out"
    if not out.is_dir():
        return None
    files = {}
    for f in sorted(out.iterdir()):
        if f.is_file():
            files[f.name] = f.stat().st_size
    html = post_dir / "graphic.html"
    canvas = {}
    if html.exists():
        text = html.read_text(encoding="utf-8", errors="replace")
        m = re.search(r"width=\"(\d+)\"", text)
        h = re.search(r"height=\"(\d+)\"", text)
        if m and h:
            canvas = {"width": int(m.group(1)), "height": int(h.group(1))}
    # Sizes are recorded in bytes AND in MB, because a post quotes the MB figure.
    sizes_mb = {k: round(v / 1_048_576, 2) for k, v in files.items()}
    return {"files": files, "files_mb": sizes_mb, "canvas": canvas}


def main() -> int:
    targets = [Path(a) if a else d for a in sys.argv[1:]] or [
        d for d in sorted(POSTS.iterdir()) if d.is_dir()
    ]
    facts = {"note": "Rendered media facts per post. Regenerate with media-facts.py."}
    for d in targets:
        if not d.is_dir():
            continue
        p = probe(d)
        if p:
            facts[d.name] = p
            mb = {k: round(v / 1_048_576, 2) for k, v in p["files"].items()}
            print(f"{d.name}: canvas={p['canvas']} files(MB)={mb}")
    path = REPO / "content" / "media-facts.json"
    path.write_text(json.dumps(facts, indent=2), encoding="utf-8")
    print(f"\nWrote {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
