"""Week-1 baseline: ask Gemma to write Manim code from scratch, no few-shots.

Writes raw responses and best-effort extracted Python to experiments/baseline/.
Both are gitignored — the .md log next to this script is the audit trail.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from src.gemma_client import DEFAULT_MODEL, ask_gemma

PROMPTS: dict[str, str] = {
    "01_circle": (
        "Write a Manim Community Edition scene that draws a unit circle, "
        "then animates a single dot moving once around the circumference. "
        "Use only standard Manim API. "
        "Output ONLY valid Python code wrapped in a ```python fenced block, "
        "with no commentary before or after."
    ),
    "02_derivative": (
        "Write a Manim Community Edition scene that visualizes the derivative of sin(x). "
        "Show the sine curve and its derivative cosine curve on the same axes, "
        "then animate a tangent line at a point that moves along the sine curve. "
        "Use only standard Manim API. "
        "Output ONLY valid Python code wrapped in a ```python fenced block, "
        "with no commentary before or after."
    ),
    "03_pythagorean": (
        "Write a Manim Community Edition scene that gives a visual proof of the Pythagorean "
        "theorem by area rearrangement: draw a square of side a+b containing four right "
        "triangles and a smaller square of side c, then rearrange the four triangles to "
        "reveal two squares of sides a and b. "
        "Use only standard Manim API. "
        "Output ONLY valid Python code wrapped in a ```python fenced block, "
        "with no commentary before or after."
    ),
}

CODE_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)
OUT_DIR = Path("experiments/baseline")


def extract_code(raw: str) -> tuple[str, bool]:
    """Return (code, fenced). If no fence found, return raw stripped and False."""
    match = CODE_FENCE.search(raw)
    if match:
        return match.group(1).strip(), True
    return raw.strip(), False


def main(model: str = DEFAULT_MODEL) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"baseline model: {model}")
    for name, prompt in PROMPTS.items():
        print(f"--- {name} ---")
        t0 = time.perf_counter()
        raw = ask_gemma(prompt, model=model)
        elapsed = time.perf_counter() - t0
        (OUT_DIR / f"{name}.raw.txt").write_text(raw)
        code, fenced = extract_code(raw)
        (OUT_DIR / f"{name}.py").write_text(code)
        print(f"  {len(raw)} chars in {elapsed:.1f}s, fenced={fenced}, code={len(code)} chars")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) >= 2 else DEFAULT_MODEL)
