# 02 — First end-to-end pipeline run

**Date:** 2026-04-27
**Model:** `gemma4:e4b-it-q8_0`
**Goal:** prove that text → Gemma (with curated few-shot prompt) → Manim →
mp4 works at all. No retry loop yet.

## Setup

`prompts/manim_generator.txt` contains a system prompt + 10 hard rules + 4
hand-written few-shots taken from `examples/`:

1. `circle.py` (Circle + Create)
2. `eulers_identity.py` (MathTex + Write)
3. `derivative_tangent.py` (Axes + plot(callable) + ValueTracker + always_redraw)
4. `pythagorean_proof.py` (Polygon + VGroup + Transform)

`src/pipeline.py` reads the template, appends the user concept, calls Gemma,
extracts the fenced code, writes scene.py to `videos/sessions/<id>/`, and
renders via `src/manim_runner.py` (subprocess wrapper around `manim`).

## Run 1

**Concept:** "Visualise that the derivative of x squared is 2x, by showing
a tangent line whose slope updates at a moving point on the parabola y = x
squared."

- Generation: 80.3 s, 3105 chars
- Render: 87.9 s
- Total: ~3 min
- mp4: `videos/sessions/1777234075/media/videos/scene/480p15/QuadraticDerivative.mp4`

**Quality of generated code:** zero syntactic errors. All four hallucinations
that broke the baseline disappeared on the first run with few-shots:

- `axes.plot(callable, x_range=...)` ✓ (was the showstopper in baseline)
- `ValueTracker` + `always_redraw` ✓
- `Dot(radius=...)` ✓
- Single `self.play(tracker.animate.set_value(...))` ✓

**Issues observed:**

1. Labels positioned via `.next_to(parabola, UL)` ended up *off-screen*
   because the parabola extended above the visible frame.
2. Slope readout written as `2({x:.2f}) = {2x:+.2f}` — mathematically correct
   but reads like a function call. Cosmetic.

## Run 2 (after prompt rules 11 + 12)

Added two rules to `prompts/manim_generator.txt`:

- **Rule 11:** place labels with `.to_corner(...)` or `.to_edge(...)`, never
  `.next_to(curve, ...)`.
- **Rule 12:** parametric readouts in natural mathematical notation, not
  `2(x) = ...`.

Re-ran the same concept.

- Generation: 72.2 s, 2604 chars
- Render: 20.1 s
- mp4: `videos/sessions/1777238176/media/videos/scene/480p15/DerivativeQuadratic.mp4`

**What changed:**

- Rule 11: ✅ all three labels (`f_label`, `f_prime_label`, `slope_readout`)
  placed with `.to_corner(...)`. Off-screen issue gone.
- Rule 12: ⚠️ partial. Gemma prefixed `"Slope (m) = "` but kept the
  `2(x) = ...` form inside. Probably because rule 12 only modelled
  trigonometric and `f'` notations; for polynomial derivatives Gemma had no
  near-template to copy. Follow-up: either add a 5th few-shot using a
  polynomial derivative, or rewrite rule 12 imperatively.
- Bonus: Gemma rewrote the tangent geometry to a more standard form
  (`delta_y = slope * delta_x`) and animated `-2 → 2 → -2` rather than a
  single sweep, showing the full slope range.

## Conclusion

**Pipeline works end-to-end on day 2.** With the four hand-written few-shots,
Gemma 4 E4B q8 produces compilable Manim CE code that renders cleanly on the
first try. The remaining issues are positioning and stylistic, not structural,
and are addressable by tightening the prompt rather than touching the
pipeline code.

## Next iteration (day 3+)

- Retry loop on render error (catch the runtime error, feed Manim's stderr
  back to Gemma, regenerate).
- 5th few-shot using a polynomial derivative to give rule 12 a concrete
  template.
- Larger sample of concepts (e.g. 5–10 across calculus / geometry /
  combinatorics) to estimate first-pass success rate.
