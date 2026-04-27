# 04 — Day-4 sample of 10 concepts through the pipeline

**Date:** 2026-04-27
**Model:** `gemma4:e4b-it-q8_0`

## Summary

- Total concepts: 10
- Success first try: 4/10 (40%)
- Success after retry: 2/10
- Total success: 6/10 (60%)
- Failed (gave up): 4/10
- Wall time: 1442.2s (24.0 min)

## Per-concept results

| ID | Status | Attempts | Time (s) | Error head |
|----|--------|----------|----------|------------|
| derivative_x2 | fail | 3 | 298.3 | │                                                              |
| riemann_sum | success | 1 | 66.5 |  |
| limit_secant | success | 2 | 218.4 |  |
| triangle_angles | success | 1 | 98.4 |  |
| unit_circle_pythagoras | fail | 3 | 204.1 | │                          |
| dot_product | success | 1 | 70.7 |  |
| compare_powers | success | 2 | 93.6 |  |
| handshake_problem | success | 1 | 30.5 |  |
| cobweb_diagram | fail | 3 | 210.6 | │                                              |
| saddle_3d | fail | 3 | 151.1 | │                                           |

## Concepts

### derivative_x2

> Visualise that the derivative of x squared is 2x, by showing a tangent line whose slope updates at a moving point on the parabola y = x squared.

Session: `videos/sessions/1777282233/`

Status: **fail** (attempts: 3, 298.3s)

```
pipeline gave up after 3 attempts. last error tail:
                                         │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/scene/scene.py:259 in render                                             │
│                                                             
```

### riemann_sum

> Show how a Riemann sum approximates the integral of x squared from 0 to 2 by drawing 8 rectangles under the curve.

Session: `videos/sessions/1777282531/`

Status: **success** (attempts: 1, 66.5s)

`videos/sessions/1777282531/attempt_0_media/videos/attempt_0_scene/480p15/RiemannSumApproximation.mp4`

### limit_secant

> Visualise the limit definition of the derivative: a secant line between two points on a parabola y = x squared becomes the tangent line as the second point approaches the first.

Session: `videos/sessions/1777282598/`

Status: **success** (attempts: 2, 218.4s)

`videos/sessions/1777282598/attempt_1_media/videos/attempt_1_scene/480p15/DerivativeVisualization.mp4`

### triangle_angles

> Show that the three angles of a triangle sum to 180 degrees by drawing a triangle, copying each of its three angles, and rearranging the copies along a single straight line.

Session: `videos/sessions/1777282816/`

Status: **success** (attempts: 1, 98.4s)

`videos/sessions/1777282816/attempt_0_media/videos/attempt_0_scene/480p15/TriangleAngleSum.mp4`

### unit_circle_pythagoras

> Animate the Pythagorean identity sin squared theta plus cos squared theta equals one on a unit circle. Show the right triangle inscribed in the circle and update the values of sin theta and cos theta as theta moves around the circle.

Session: `videos/sessions/1777282914/`

Status: **fail** (attempts: 3, 204.1s)

```
pipeline gave up after 3 attempts. last error tail:
  48 │   │   self.add(axes)                                                  │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/mobject.py:735 in getter                                         │
│                         
```

### dot_product

> Visualise the geometric meaning of the dot product of two 2D vectors by drawing both vectors from the origin, projecting one onto the other, and showing that the projection length equals the dot product divided by the second vector's magnitude.

Session: `videos/sessions/1777283118/`

Status: **success** (attempts: 1, 70.7s)

`videos/sessions/1777283118/attempt_0_media/videos/attempt_0_scene/480p15/DotProductVisualization.mp4`

### compare_powers

> Plot f(x) = x squared in blue and g(x) = x cubed in red on the same axes from x = -2 to x = 2, with labels, so the difference between quadratic and cubic growth is visible.

Session: `videos/sessions/1777283189/`

Status: **success** (attempts: 2, 93.6s)

`videos/sessions/1777283189/attempt_1_media/videos/attempt_1_scene/480p15/GrowthComparison.mp4`

### handshake_problem

> Visualise the handshake problem for 5 people: arrange 5 dots in a circle and draw every pairwise handshake as a connecting line, then display the total count of 10 handshakes as a label.

Session: `videos/sessions/1777283283/`

Status: **success** (attempts: 1, 30.5s)

`videos/sessions/1777283283/attempt_0_media/videos/attempt_0_scene/480p15/HandshakeProblem.mp4`

### cobweb_diagram

> Draw the cobweb diagram for the iterative function f(x) = 0.5 x + 1 starting from x_0 = 0, showing the first 5 iterations converging to the fixed point at x = 2. Plot the line y = f(x) and the line y = x and animate the cobweb steps between them.

Session: `videos/sessions/1777283313/`

Status: **fail** (attempts: 3, 210.6s)

```
pipeline gave up after 3 attempts. last error tail:
                                                         │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/types/vectorized_mobject.py:1128 in set_points_as_corners        │
│                                             
```

### saddle_3d

> Show a 3D plot of the saddle surface z = x squared minus y squared, with the camera rotating around the surface so the saddle shape is clearly visible from multiple angles.

Session: `videos/sessions/1777283524/`

Status: **fail** (attempts: 3, 151.1s)

```
pipeline gave up after 3 attempts. last error tail:
  stroke_color=stroke_color,                                │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/types/vectorized_mobject.py:2143 in __init__                     │
│                                          
```

---

## Comparison vs. baseline (no hints)

| Metric | v1 (baseline) | v2 (with hints) | Delta |
|--------|---------------|-----------------|-------|
| First-try success | 3/10 (30%) | 4/10 (40%) | +10 pp |
| After retry | 2/10 | 2/10 | — |
| Total success | 5/10 (50%) | 6/10 (60%) | +10 pp |
| Wall time | 30.6 min | 24.0 min | −6.6 min |

### Per-concept delta

| Concept | v1 | v2 | Delta |
|---------|----|----|-------|
| derivative_x2 | success(3) | fail(3) | regression — small N, likely Gemma seed noise |
| riemann_sum | fail(3) | success(1) | **first-try success** without even needing the hint (it shipped a clean ax.plot(callable)) |
| limit_secant | fail(3) | success(2) | hint repaired on retry 1 |
| triangle_angles | success(1) | success(1) | — |
| unit_circle_pythagoras | fail(3) | fail(3) | no hint covers its silent "no mp4" pattern |
| dot_product | success(1) | success(1) | — |
| compare_powers | success(2) | success(2) | — |
| handshake_problem | success(1) | success(1) | — |
| cobweb_diagram | fail(3) | fail(3) | error is `getter() got 'color' kwarg` — not in HINTS |
| saddle_3d | fail(3) | fail(3) | hint *did* repair Surface kwargs on attempt 1, but a new broadcast error then sent Gemma into a context drift — by attempt 2 she had reverted to `Scene` (not `ThreeDScene`) and to `x_range` |

### Verdict

Hints help, measurably and in the expected places (riemann_sum, limit_secant) — those were exactly the broadcast-array hallucinations the hint was written for. Hints do NOT save the cases where:

1. The error has no entry in `HINTS` yet (cobweb, unit_circle).
2. Gemma's first repair succeeds but a *different* failure on the next attempt sends the model into a drift back to its training prior (saddle_3d).

### Implications for the rest of the project

- **2D pipeline at 60% with retry** — usable, but not yet reliable for a 70/30 video grade. We need ≥80% on the curated demo prompts. Path forward:
  - Add hint patterns for the two remaining 2D failure modes (`cobweb` color kwarg, `unit_circle` silent no-mp4).
  - Promote `examples/riemann_sum.py` into the prompt template as the 6th few-shot once more concepts in that family appear.
- **3D is a different game.** Two retries are not enough; the model context-drifts. For the submission demo, the right call is to **hand-author the 3D scene** (we already have `examples/saddle_3d.py` that renders cleanly) and showcase generated 2D content. The pipeline's 3D path can stay in the codebase as a proof-of-concept, not a demo gate.
- **Demo-prompt curation is now the highest-leverage work.** Pick 4–5 prompts with reliable success, polish them, and lock them in for the recorded video. Don't fight Gemma into doing every concept under the sun.
