"""End-to-end pipeline: math concept -> Gemma -> Manim code -> rendered mp4.

CLI: python -m src.pipeline "<concept>" [model]

No retry loop yet — that is day 3. Today's job is to prove the path works
at all when Gemma is given the curated few-shot prompt.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from src.gemma_client import DEFAULT_MODEL, ask_gemma
from src.manim_runner import render

PROMPT_PATH = Path("prompts/manim_generator.txt")
SESSIONS_DIR = Path("videos/sessions")
CODE_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)


def extract_code(raw: str) -> tuple[str, bool]:
    """Return (code, fenced). If no fence found, return raw stripped, fenced=False."""
    match = CODE_FENCE.search(raw)
    if match:
        return match.group(1).strip(), True
    return raw.strip(), False


def ask(concept: str, model: str = DEFAULT_MODEL) -> Path:
    template = PROMPT_PATH.read_text()
    full_prompt = f"{template} {concept}"

    print(f"[gemma] asking {model} ...", file=sys.stderr)
    t0 = time.perf_counter()
    raw = ask_gemma(full_prompt, model=model)
    gen_elapsed = time.perf_counter() - t0
    print(f"[gemma] {len(raw)} chars in {gen_elapsed:.1f}s", file=sys.stderr)

    code, fenced = extract_code(raw)
    if not fenced:
        print("[warn] no ```python fence found in response — using raw text", file=sys.stderr)

    session_id = str(int(time.time()))
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    scene_file = session_dir / "scene.py"
    scene_file.write_text(code)
    (session_dir / "raw.txt").write_text(raw)
    (session_dir / "concept.txt").write_text(concept)
    print(f"[pipeline] session {session_id} -> {scene_file}", file=sys.stderr)

    print("[manim] rendering ...", file=sys.stderr)
    t0 = time.perf_counter()
    mp4 = render(scene_file, media_dir=session_dir / "media")
    render_elapsed = time.perf_counter() - t0
    print(f"[manim] mp4 in {render_elapsed:.1f}s -> {mp4}", file=sys.stderr)

    return mp4


def _cli() -> None:
    if len(sys.argv) < 2:
        print('usage: python -m src.pipeline "<concept>" [model]', file=sys.stderr)
        sys.exit(1)
    concept = sys.argv[1]
    model = sys.argv[2] if len(sys.argv) >= 3 else DEFAULT_MODEL
    mp4 = ask(concept, model=model)
    print(mp4)


if __name__ == "__main__":
    _cli()
