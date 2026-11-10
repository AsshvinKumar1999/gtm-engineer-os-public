"""Render an animated HTML graphic to MP4 + GIF + poster PNG for LinkedIn.

The HTML page must expose `window.renderAt(seconds)` that draws one frame
deterministically (no CSS transitions, no unseeded randomness) and contain a
`#stage` element sized to the output (default 1080x1350, LinkedIn 4:5).

Usage:
  uv run --with playwright --with imageio-ffmpeg python scripts/render_animation.py \
      content/posts/001-hundred-posts/graphic.html --seconds 11 --fps 30
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

GIF_LIMIT_MB = 8.0  # keep GIFs small enough for LinkedIn and fast loading


def capture_frames(html: Path, frames_dir: Path, width: int, height: int,
                   fps: int, seconds: float, query: str = "") -> int:
    from playwright.sync_api import sync_playwright

    total = int(round(seconds * fps))
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": width, "height": height},
                                device_scale_factor=1)
        page.goto(html.as_uri() + "?capture=1" + (f"&{query}" if query else ""))
        page.wait_for_function("typeof window.renderAt === 'function'")
        page.evaluate("document.fonts.ready.then(() => true)")
        stage = page.locator("#stage")
        for i in range(total):
            page.evaluate(f"window.renderAt({i / fps})")
            stage.screenshot(path=str(frames_dir / f"f{i:05d}.png"))
        browser.close()
    return total


def encode(ffmpeg: str, frames_dir: Path, out_dir: Path, fps: int,
           gif_width: int, gif_fps: int) -> tuple[Path, Path]:
    pattern = str(frames_dir / "f%05d.png")
    mp4 = out_dir / "graphic.mp4"
    gif = out_dir / "graphic.gif"
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", pattern, "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-crf", "18", "-movflags", "+faststart", str(mp4)], check=True)
    vf = (f"fps={gif_fps},scale={gif_width}:-1:flags=lanczos,split[a][b];"
          "[a]palettegen=max_colors=128:stats_mode=diff[p];"
          "[b][p]paletteuse=dither=bayer:bayer_scale=4:diff_mode=rectangle")
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-i", pattern, "-vf", vf, "-loop", "0", str(gif)], check=True)
    return mp4, gif


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("html")
    ap.add_argument("--out", help="output dir (default: <html dir>/out)")
    ap.add_argument("--width", type=int, default=1080)
    ap.add_argument("--height", type=int, default=1350)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--poster-at", type=float, default=None,
                    help="second to use for poster.png (default: 80%% through)")
    ap.add_argument("--gif-width", type=int, default=720)
    ap.add_argument("--gif-fps", type=int, default=15)
    ap.add_argument("--query", default="", help="extra URL query for the page, e.g. theme=dark")
    args = ap.parse_args()

    html = Path(args.html).resolve()
    if not html.is_file():
        print(f"error: {html} not found", file=sys.stderr)
        return 2
    out_dir = Path(args.out).resolve() if args.out else html.parent / "out"
    out_dir.mkdir(parents=True, exist_ok=True)

    import imageio_ffmpeg
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

    frames_dir = Path(tempfile.mkdtemp(prefix="frames-"))
    try:
        total = capture_frames(html, frames_dir, args.width, args.height,
                               args.fps, args.seconds, args.query)
        poster_s = args.poster_at if args.poster_at is not None else args.seconds * 0.8
        poster_idx = min(total - 1, int(poster_s * args.fps))
        shutil.copy(frames_dir / f"f{poster_idx:05d}.png", out_dir / "poster.png")
        mp4, gif = encode(ffmpeg, frames_dir, out_dir, args.fps,
                          args.gif_width, args.gif_fps)
    finally:
        shutil.rmtree(frames_dir, ignore_errors=True)

    gif_mb = gif.stat().st_size / 1e6
    print(f"frames: {total}")
    print(f"mp4:    {mp4} ({mp4.stat().st_size / 1e6:.1f} MB)")
    print(f"gif:    {gif} ({gif_mb:.1f} MB)")
    print(f"poster: {out_dir / 'poster.png'}")
    if gif_mb > GIF_LIMIT_MB:
        print(f"warning: GIF over {GIF_LIMIT_MB} MB; lower --gif-width or --gif-fps, "
              "or post the MP4", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
