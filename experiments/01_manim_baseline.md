# 01 — Manim baseline (Gemma 4 E4B q8, no few-shots)

**Date:** 2026-04-26
**Model:** `gemma4:e4b-it-q8_0`
**Goal:** measure how well Gemma 4 E4B writes Manim Community code from cold,
without any curated few-shot examples. Output decides whether Week 1 needs
1 reference scene or 5.

## Method

`experiments/run_baseline.py` sends three prompts (easy / medium / hard) via
`src.gemma_client.ask_gemma`, saves raw response and a best-effort extracted
Python file to `experiments/baseline/`. Each `.py` is then rendered with
`manim -ql` and the result logged here. Outputs are NOT fixed up.

## Prompts

| ID | Difficulty | Concept |
|----|------------|---------|
| 01_circle | easy | Unit circle + dot animating around circumference |
| 02_derivative | medium | sin(x) and cos(x) on same axes, moving tangent line |
| 03_pythagorean | hard | Visual proof of Pythagoras by area rearrangement |

## Results

| ID | Gen time | Fenced? | Compiles? | Renders? | Mathematically sensible? |
|----|----------|---------|-----------|----------|--------------------------|
| 01_circle | 46.9 s | yes | yes | yes (mp4 written) | yes |
| 02_derivative | 57.6 s | yes | no | — | n/a |
| 03_pythagorean | 79.2 s | yes | no | — | logic was already pretzeled in code review |

### 01_circle

```
manim -ql experiments/baseline/01_circle.py
```

Renders cleanly to
`experiments/baseline/media/videos/01_circle/480p15/UnitCircleMovement.mp4`.
Uses `Circle`, `Dot`, `MoveAlongPath`, `FadeOut` — all standard Manim CE API,
all used correctly. The dot orbits the circle once over 6 s, then everything
fades out. Boring but correct.

### 02_derivative

```
manim -ql experiments/baseline/02_derivative.py
→ ValueError: could not broadcast input array from shape (500,) into shape (3,)
  at line 30: sin_graph = ax.plot(x_values, sin_func(x_values), color=BLUE)
```

**Primary hallucination:** Gemma calls `ax.plot(x_values, y_values)` as if it
were Matplotlib. Manim CE's `ax.plot` signature is `plot(function, x_range=...)`
where `function` is a *callable* and `x_range` is a 3-element `[start, stop, step]`.
Passing a 500-element ndarray crashes inside the broadcast. This is the single
most damaging Manim API confusion the model has — it appears the very first
time anything more complex than a `Circle` is involved.

**Secondary hallucinations spotted in code review** (not exercised because the
crash hits first):

- Line 44: `Dot(point_size=0.1, ...)` — `Dot` takes `radius`, not `point_size`.
- Line 80: `np.array(dx, 0)` and `np.array(dy, 1)` — `np.array` requires a
  sequence; this raises `TypeError` before computation. Should be `np.array([dx, 0, 0])`.
- Lines 64–92: 100-iteration loop with one `self.play()` per step — even if it
  ran, render time would be brutal. Manim idiom is `always_redraw` /
  `ValueTracker` updaters, which Gemma did not reach for.

### 03_pythagorean

```
manim -ql experiments/baseline/03_pythagorean.py
→ TypeError: Mobject.__init__() got an unexpected keyword argument 'points'
  at line 22: base_triangle = Triangle(points=[...], color=BLUE)
```

**Primary hallucination:** `Triangle` in Manim CE is hardcoded equilateral and
takes no `points` argument. Custom triangles are built with `Polygon(*points)`.
Gemma reached for a Matplotlib/Mathematica-style API.

**Secondary issues** (code review, not exercised):

- The "rearrangement" logic does not actually rearrange — it FadeOuts the inner
  square, then `Transform`s `square_a`/`square_b` into themselves, then FadeOuts
  the triangles. The visual would not communicate the area-equality argument.
- `triangles.animate.move_to(...)` target is computed by adding two `get_center`
  calls together, which produces nonsense coordinates.

## Conclusion

Gemma 4 E4B q8 scores 1/3 compile and 1/3 render: it handles trivial drawing
primitives but reaches for Matplotlib/Mathematica idioms the moment a scene
needs axes, custom polygons, or tangent updaters. The two highest-cost API
hallucinations are `ax.plot(arrays)` instead of `ax.plot(callable)` and
`Triangle(points=...)` for custom triangles — both will reappear constantly
without correction, because they are exactly the patterns most pedagogical
animations demand. Week 1 should ship five hand-written few-shot scenes —
the existing `Circle` and `MathTex` examples plus `Axes + plot(callable) +
ValueTracker` (covers the tangent/derivative pattern), `Polygon + Transform`
(covers custom shapes and area rearrangement), and one combinatorial
visualization — so the prompt explicitly demonstrates the four idioms Gemma
fails on plus the formula path she gets right.
