"""Subprocess wrapper around the Manim Community CLI."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

QUALITY_TO_RES = {"l": "480p15", "m": "720p30", "h": "1080p60", "k": "2160p60"}
DEFAULT_TIMEOUT = 300


def render(scene_file: Path, quality: str = "l", media_dir: Path | None = None) -> Path:
    """Render a Manim scene file. Returns the path to the produced mp4.

    Manim sometimes catches exceptions inside `construct()` and exits 0 even
    on failure, so success is decided by whether an mp4 actually appeared.
    """
    cmd = ["manim", f"-q{quality}", str(scene_file)]
    if media_dir is not None:
        cmd += ["--media_dir", str(media_dir)]

    result = subprocess.run(cmd, capture_output=True, text=True, timeout=DEFAULT_TIMEOUT)

    base = media_dir if media_dir is not None else Path("media")
    output_dir = base / "videos" / scene_file.stem / QUALITY_TO_RES[quality]
    mp4s = [
        p for p in sorted(output_dir.glob("*.mp4"))
        if "partial_movie_files" not in p.parts
    ]

    if not mp4s:
        raise RuntimeError(
            f"manim render failed (exit {result.returncode}, no mp4 in {output_dir})\n"
            f"--- stderr (tail) ---\n{result.stderr[-2000:]}\n"
            f"--- stdout (tail) ---\n{result.stdout[-1000:]}"
        )

    return mp4s[-1]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python -m src.manim_runner <scene_file.py> [quality]", file=sys.stderr)
        sys.exit(1)
    quality = sys.argv[2] if len(sys.argv) >= 3 else "l"
    print(render(Path(sys.argv[1]), quality=quality))
