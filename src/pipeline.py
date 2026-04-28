"""End-to-end pipeline: math concept -> Gemma -> Manim code -> rendered mp4.

CLI: python -m src.pipeline "<concept>" [model]

On render failure the pipeline asks Gemma to repair its own code, feeding
back manim's stderr. Up to MAX_RETRIES additional attempts after the first.
"""

from __future__ import annotations

import re
import sys
import time
from pathlib import Path

from src.gemma_client import DEFAULT_MODEL, ask_gemma
from src.manim_runner import ManimRenderError, render

PROMPT_PATH = Path("prompts/manim_generator.txt")
SESSIONS_DIR = Path("videos/sessions")
CODE_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)
MAX_RETRIES = 2
ERROR_TAIL_CHARS = 3000

REPAIR_TEMPLATE = """The previous Manim scene failed to render. Manim's error output (tail):

{error}
{hint_block}
Your previous code was:

```python
{code}
```

Fix the bug and produce a corrected version. Output ONLY a single ```python fenced code block with the full corrected scene, no commentary before or after."""


# Common Manim error patterns → human-readable repair hints. Gemma follows
# these much more reliably than raw stderr, which is often a deep traceback.
# ORDER MATTERS: more specific patterns first; the first match wins. Shape
# `(1,2) into (1,3)` is a different bug from a generic broadcast and would be
# misdiagnosed if the generic broadcast hint matched it first.
HINTS: list[tuple[str, str]] = [
    (
        "from shape (1,2) into shape (1,3)",
        "You used a 2D numpy array as a Manim point. Manim requires 3D "
        "points: `np.array([x, y, 0])`. If you compute many points, define "
        "a helper `def vec(x, y): return np.array([x, y, 0])` and use it "
        "everywhere, including for endpoints of `Line(...)`, `Polygon(...)`, "
        "and any `coords_to_point` results that you then mutate.",
    ),
    (
        "No module named 'matplotlib'",
        "Do not import matplotlib. The pipeline only renders Manim Community "
        "Edition scenes — `import matplotlib` is wrong here. Stay inside "
        "`from manim import *` and use `Scene` (or `ThreeDScene` for 3D) "
        "with manim's API: `axes.plot(callable, x_range=...)`, `Surface(...)`, "
        "`VGroup(...)`, etc.",
    ),
    (
        "could not broadcast input array",
        "You almost certainly passed pre-evaluated arrays to `ax.plot(...)`. "
        "Manim's `ax.plot` takes a CALLABLE: `ax.plot(np.sin, x_range=[-PI, PI])`. "
        "Never `ax.plot(x_values, np.sin(x_values))`.",
    ),
    (
        "got an unexpected keyword argument 'x_range'",
        "`Surface` and other parametric mobjects use `u_range=[u0, u1]` and "
        "`v_range=[v0, v1]`, NEVER `x_range`/`y_range`. The callable takes "
        "(u, v) and returns a 3D point — usually `axes.c2p(u, v, f(u, v))`.",
    ),
    (
        "got an unexpected keyword argument 'y_range'",
        "`Surface` uses `u_range` and `v_range`, never `x_range`/`y_range`.",
    ),
    (
        "Animation only works on Mobjects",
        "You passed a Python list (or something non-Mobject) to an animation. "
        "Wrap with `VGroup(*items)` or unpack: `FadeOut(*items)` — NEVER `FadeOut([a, b, c])`.",
    ),
    (
        "has no attribute 'objects'",
        "`self.objects` does not exist on a Scene. End the scene with `self.wait(...)` — "
        "you do not need to FadeOut everything at the end.",
    ),
    (
        "got an unexpected keyword argument 'point_size'",
        "`Dot` takes `radius=...`, not `point_size=...`.",
    ),
    (
        "got an unexpected keyword argument 'points'",
        "`Triangle` is hardcoded equilateral and rejects custom points. "
        "Use `Polygon(*vertices)` for any non-equilateral triangle or custom polygon.",
    ),
    (
        "no mp4 in",
        "Manim ran but produced no video. Common causes: a `construct()` exception "
        "swallowed silently (look for typos in mobject constructors), or an animation "
        "with a non-Mobject argument that failed before any frame was written.",
    ),
]


def derive_hint(error: str) -> str | None:
    for needle, hint in HINTS:
        if needle in error:
            return hint
    return None


def extract_code(raw: str) -> tuple[str, bool]:
    """Return (code, fenced). If no fence found, return raw stripped, fenced=False."""
    match = CODE_FENCE.search(raw)
    if match:
        return match.group(1).strip(), True
    return raw.strip(), False


def ask(concept: str, model: str = DEFAULT_MODEL, max_retries: int = MAX_RETRIES) -> Path:
    template = PROMPT_PATH.read_text()
    initial_prompt = f"{template} {concept}"

    session_id = str(int(time.time()))
    session_dir = SESSIONS_DIR / session_id
    session_dir.mkdir(parents=True, exist_ok=True)
    (session_dir / "concept.txt").write_text(concept)
    print(f"[pipeline] session {session_id} -> {session_dir}", file=sys.stderr)

    last_code: str | None = None
    last_error: str | None = None

    for attempt in range(max_retries + 1):
        if attempt == 0:
            prompt = initial_prompt
        else:
            hint = derive_hint(last_error or "")
            if hint:
                print(f"[gemma] retry {attempt}/{max_retries} (hint: {hint[:60]}...)", file=sys.stderr)
                hint_block = f"\nHint for this specific error:\n{hint}\n"
            else:
                print(f"[gemma] retry {attempt}/{max_retries}", file=sys.stderr)
                hint_block = ""
            prompt = REPAIR_TEMPLATE.format(
                error=(last_error or "")[-ERROR_TAIL_CHARS:],
                hint_block=hint_block,
                code=last_code or "",
            )

        print(f"[gemma] asking {model} (attempt {attempt}) ...", file=sys.stderr)
        t0 = time.perf_counter()
        raw = ask_gemma(prompt, model=model)
        gen_elapsed = time.perf_counter() - t0
        print(f"[gemma] {len(raw)} chars in {gen_elapsed:.1f}s", file=sys.stderr)

        code, fenced = extract_code(raw)
        if not fenced:
            print(f"[warn] no ```python fence in attempt {attempt}", file=sys.stderr)

        scene_file = session_dir / f"attempt_{attempt}_scene.py"
        scene_file.write_text(code)
        (session_dir / f"attempt_{attempt}_raw.txt").write_text(raw)

        try:
            compile(code, str(scene_file), "exec")

            print(f"[manim] rendering attempt {attempt} ...", file=sys.stderr)
            t0 = time.perf_counter()
            mp4 = render(scene_file, media_dir=session_dir / f"attempt_{attempt}_media")
            render_elapsed = time.perf_counter() - t0
            print(f"[manim] mp4 in {render_elapsed:.1f}s -> {mp4}", file=sys.stderr)
            print(f"[pipeline] success on attempt {attempt}", file=sys.stderr)
            return mp4
        except SyntaxError as exc:
            last_code = code
            last_error = f"Python SyntaxError before render: {exc.msg} at line {exc.lineno}"
            (session_dir / f"attempt_{attempt}_error.txt").write_text(last_error)
            print(f"[validate] attempt {attempt} failed ({last_error})", file=sys.stderr)
        except ManimRenderError as exc:
            last_code = code
            last_error = exc.stderr or str(exc)
            (session_dir / f"attempt_{attempt}_error.txt").write_text(last_error)
            print(f"[manim] attempt {attempt} failed", file=sys.stderr)

    raise RuntimeError(
        f"pipeline gave up after {max_retries + 1} attempts. last error tail:\n"
        f"{(last_error or '')[-2000:]}"
    )


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
