# 04 — Day-4 sample of 10 concepts through the pipeline

**Date:** 2026-04-27
**Model:** `gemma4:e4b-it-q8_0`

## Summary

- Total concepts: 10
- Success first try: 3/10 (30%)
- Success after retry: 0/10
- Total success: 3/10 (30%)
- Failed (gave up): 7/10
- Wall time: 2245.7s (37.4 min)

## Per-concept results

| ID | Status | Attempts | Time (s) | Error head |
|----|--------|----------|----------|------------|
| derivative_x2 | fail | 3 | 291.1 | │                                                              |
| riemann_sum | fail | 3 | 166.7 | │                                                              |
| limit_secant | success | 1 | 110.6 |  |
| triangle_angles | success | 1 | 74.0 |  |
| unit_circle_pythagoras | exception | 1 | 372.4 | ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. ( |
| dot_product | exception | 0 | 300.0 | ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. ( |
| compare_powers | fail | 3 | 508.7 | │                                                              |
| handshake_problem | success | 1 | 61.6 |  |
| cobweb_diagram | fail | 3 | 248.3 | │                                              |
| saddle_3d | fail | 3 | 112.3 | │                                                    |

## Concepts

### derivative_x2

> Visualise that the derivative of x squared is 2x, by showing a tangent line whose slope updates at a moving point on the parabola y = x squared.

Session: `videos/sessions/1777300331/`

Status: **fail** (attempts: 3, 291.1s)

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

Session: `videos/sessions/1777300623/`

Status: **fail** (attempts: 3, 166.7s)

```
pipeline gave up after 3 attempts. last error tail:
                                         │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/scene/scene.py:259 in render                                             │
│                                                             
```

### limit_secant

> Visualise the limit definition of the derivative: a secant line between two points on a parabola y = x squared becomes the tangent line as the second point approaches the first.

Session: `videos/sessions/1777300789/`

Status: **success** (attempts: 1, 110.6s)

`videos/sessions/1777300789/attempt_0_media/videos/attempt_0_scene/480p15/LimitDefinitionDerivative.mp4`

### triangle_angles

> Show that the three angles of a triangle sum to 180 degrees by drawing a triangle, copying each of its three angles, and rearranging the copies along a single straight line.

Session: `videos/sessions/1777300900/`

Status: **success** (attempts: 1, 74.0s)

`videos/sessions/1777300900/attempt_0_media/videos/attempt_0_scene/480p15/TriangleAngleSum.mp4`

### unit_circle_pythagoras

> Animate the Pythagorean identity sin squared theta plus cos squared theta equals one on a unit circle. Show the right triangle inscribed in the circle and update the values of sin theta and cos theta as theta moves around the circle.

Session: `videos/sessions/1777300974/`

Status: **exception** (attempts: 1, 372.4s)

```
ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
```

### dot_product

> Visualise the geometric meaning of the dot product of two 2D vectors by drawing both vectors from the origin, projecting one onto the other, and showing that the projection length equals the dot product divided by the second vector's magnitude.

Session: `videos/sessions/1777301346/`

Status: **exception** (attempts: 0, 300.0s)

```
ReadTimeout: HTTPConnectionPool(host='localhost', port=11434): Read timed out. (read timeout=300)
```

### compare_powers

> Plot f(x) = x squared in blue and g(x) = x cubed in red on the same axes from x = -2 to x = 2, with labels, so the difference between quadratic and cubic growth is visible.

Session: `videos/sessions/1777301703/`

Status: **fail** (attempts: 3, 508.7s)

```
pipeline gave up after 3 attempts. last error tail:
                                         │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/scene/scene.py:259 in render                                             │
│                                                             
```

### handshake_problem

> Visualise the handshake problem for 5 people: arrange 5 dots in a circle and draw every pairwise handshake as a connecting line, then display the total count of 10 handshakes as a label.

Session: `videos/sessions/1777338175/`

Status: **success** (attempts: 1, 61.6s)

`videos/sessions/1777338175/attempt_0_media/videos/attempt_0_scene/480p15/HandshakeProblem.mp4`

### cobweb_diagram

> Draw the cobweb diagram for the iterative function f(x) = 0.5 x + 1 starting from x_0 = 0, showing the first 5 iterations converging to the fixed point at x = 2. Plot the line y = f(x) and the line y = x and animate the cobweb steps between them.

Session: `videos/sessions/1777338236/`

Status: **fail** (attempts: 3, 248.3s)

```
pipeline gave up after 3 attempts. last error tail:
t RerunSceneException:                                   │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/videos/sessions/1777338236/attempt_2 │
│ _scene.py:46 in construct                                                    │
│                                             
```

### saddle_3d

> Show a 3D plot of the saddle surface z = x squared minus y squared, with the camera rotating around the surface so the saddle shape is clearly visible from multiple angles.

Session: `videos/sessions/1777338484/`

Status: **fail** (attempts: 3, 112.3s)

```
pipeline gave up after 3 attempts. last error tail:
ke_smooth()                                        │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/mobject.py:1452 in apply_function                                │
│                                                   
```

---

## Verdict and rollback

**Negative result.** Adding the Riemann few-shot pushed the prompt size past
a threshold and Gemma's generation time roughly tripled (188 s vs 60–90 s
in v2). Two concepts (`unit_circle_pythagoras`, `dot_product`) hit the 300 s
`requests` timeout in `gemma_client.ask_gemma` and surfaced as `ReadTimeout`
exceptions instead of clean failures, taking the success count from 6/10 (v2)
to 3/10 here.

**What changed beyond Riemann:** the same v2 hint mapper, the same retry
loop. Only the prompt text grew. So the regression is attributable to prompt
size — not to a logic regression in the pipeline.

**Action taken:**

- Rolled `prompts/manim_generator.txt` back to 5 few-shots (Circle,
  EulersIdentity, DerivativeTangent, PythagoreanProof, Saddle3D). Riemann
  remains in `examples/` as a standalone reference scene.
- Bumped `DEFAULT_TIMEOUT` in `gemma_client.py` from 300 s to 600 s as a
  defensive measure: a clean failure with `ReadTimeout` is still worse for
  the retry loop than a slow success would be.

**Lesson for future prompt edits:** prompt size is a binding constraint at
this model size. Adding a few-shot is not a free lunch — it competes with
generation latency and, indirectly, with success rate. The next time we
extend the prompt, measure first against the v2 baseline (60% success,
24-min wall time) on this exact concept set.
