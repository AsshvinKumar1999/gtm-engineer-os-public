---
name: animated-infographic
description: Build a data-bound animated LinkedIn graphic (particles, flows, counters) as HTML and render it to MP4 + GIF + poster. Use for every LinkedIn post graphic, build-log visual, or workflow explainer.
---

# Animated infographic

LinkedIn's best GTM visuals (Jan Rasmussen, Charlie Hills, Alex Vacca, Nicholas De La Guardia) are diagrams of a workflow. Ours do one thing theirs do not: **every number and every moving particle is bound to a real run.** Theirs say "sample data for illustration". Ours say "counted from the repo".

## The rule that makes it ours
A particle is a unit of real data moving through a real step: one post, one account, one row, one signal. If 412 accounts were scored, 412 particles move. If a number is not in a data file or a run log, it is not on the graphic. Run `agents/skeptic-verifier.md` on the data block before rendering.

## Pick one of two LinkedIn post styles

| Style | Use it for | Template | Canvas |
|---|---|---|---|
| **Build Log** (dark, particles) | Results from a real run: counts, before/after, "N in, M out" | `content/posts/001-hundred-posts/graphic.html` | 1080x1350 (4:5) |
| **Blueprint Play** (light, wired flowchart) | A repeatable play or workflow, step by step, with tools | `content/plays/01-permits-queues/graphic.html` | 1080x1920 (9:16) |

Rotate them. Build Logs prove you ran it; Plays teach how. A Play has no made-up numbers because it is a recipe; if you add numbers, they follow the data rule above.

### Blueprint Play style
Inspired by the GTM plays-library format (Frontal), rebuilt as our own. Never copy another brand's logo, name, footer or play content.
- **Paper:** `#f3f5f8` with a 24px graph-paper grid (`#e4e8ee`). White cards, 1px `#d6dce5` border, soft drop shadow, square corners.
- **Type:** Instrument Serif 104px title, centered. JetBrains Mono for the kicker (`■ PLAY NN`, blue `#2f5bea`), the subtitle, card tags (top-right, uppercase, letter-spaced) and the `FROM` / `WITH` labels. Inter for everything else.
- **Structure:** numbered dark step banners (`#0b1220`, light-blue number square) on the left; cards to their right or below. The first card of a play has a tinted header (`#eaf0fb`). Blue chips (`#eef3ff`) for criteria. Tools are rows of 2-letter mono badges plus a name, never stock logos. Tier rows use a black/grey/light square for rank. Black pills mark a merge point and the final outcome. A stack box lists every tool, and the footer reads `ASSHVIN KUMAR · GTM PLAYS`.
- **Wires:** orthogonal 1.5px `#8e99ab` lines with an open arrowhead, measured from the real card boxes (bottom-center to top-center, horizontal run 14px above the target). Declare them as `[revealStep, fromId, toId]`; never hand-place coordinates.
- **Motion (12 s loop):**
  1. Title rises in.
  2. Each step sweeps in left to right (clip-path) with an 8px rise, 0.8 s apart.
  3. Wires draw themselves (stroke-dashoffset) and arrowheads pop.
  4. Blue square packets flow down every live wire.
  5. Corner brackets walk card to card.
  6. Everything fades back to the empty frame so the loop has no visible jump.
- **Render:** `--height 1920 --seconds 12 --poster-at 6.6 --gif-width 640`.

### Build Log style
- Canvas 1080x1350 (LinkedIn 4:5). Dark graphite `#0d1015`, dot grid, slow dust.
- **Amber `#ffb547` = raw input moving.** **Teal `#3dd6c6` = things built or output.** Grey = not yet touched. Never use color for decoration only.
- Type: Space Grotesk (headline, 60–70px, tight), JetBrains Mono (labels, data, chips).
- Layout top to bottom = time: kicker (BUILD LOG NNN) → 2-line headline → input → process core → outputs → footer with name + proof line.
- Motion: 8–12 s loop. Input drains, core fills/pulses, outputs light up one by one, everything fades back to the start frame so the GIF loops cleanly. Motion must explain flow; nothing moves just to move.
- The last held frame (poster) must read on its own: that is what people see when scrolling with autoplay off.

## Steps
1. **Storyboard in 4 beats** (write them in `content/posts/NNN-slug/post.md`): input, process, output, proof. One sentence each.
2. **Data block**: put the real numbers in the `<script id="data" type="application/json">` block, with a comment naming the source file, run, or commit.
3. **Build** `content/posts/NNN-slug/graphic.html` by copying `content/posts/001-hundred-posts/graphic.html`. Keep the contract: a `#stage` element and `window.renderAt(seconds)` that is deterministic (seeded RNG, no CSS transitions, no `Date.now()`).
4. **Preview live**: open the HTML in a browser (it animates without `?capture=1`).
5. **Render**:
   ```bash
   uv run --with playwright --with imageio-ffmpeg python scripts/render_animation.py content/posts/NNN-slug/graphic.html --seconds 11 --fps 30 --poster-at 9.6
   ```
   Outputs `out/graphic.mp4` (post this; LinkedIn autoplays video muted), `out/graphic.gif` (comments, newsletter, X), `out/poster.png` (thumbnail and carousel cover). First run on a new machine: `uv run --with playwright playwright install chromium-headless-shell`.
6. **Check frames**: read `out/poster.png` and one mid-animation frame (`--seconds 3 --fps 10 --poster-at 2.4 --out <scratch dir>`). Look for overlapping text, chips lighting after the fade, and unreadable labels at phone size.
7. **Caption** through `skills/editorial-gate` and `python scripts/lint_ai_tells.py`.

## Do not
- Do not use "sample data", made-up logos or invented customer quotes.
- Do not put more than about 25 words of body text on the graphic. The caption carries the story.
- Do not use stock icons for tools you do not use.
