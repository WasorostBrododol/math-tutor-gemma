# 04 — Day-4 sample of 10 concepts through the pipeline

**Date:** 2026-04-27
**Model:** `gemma4:e4b-it-q8_0`

## Summary

- Total concepts: 10
- Success first try: 3/10 (30%)
- Success after retry: 2/10
- Total success: 5/10 (50%)
- Failed (gave up): 5/10
- Wall time: 1837.8s (30.6 min)

## Per-concept results

| ID | Status | Attempts | Time (s) | Error head |
|----|--------|----------|----------|------------|
| derivative_x2 | success | 3 | 205.2 |  |
| riemann_sum | fail | 3 | 250.2 | │                                             |
| limit_secant | fail | 3 | 245.7 | │                                                   |
| triangle_angles | success | 1 | 109.7 |  |
| unit_circle_pythagoras | fail | 3 | 259.4 | manim render failed (exit 0, no mp4 in videos/sessions/1777278645/attempt_2_medi |
| dot_product | success | 1 | 95.0 |  |
| compare_powers | success | 2 | 136.4 |  |
| handshake_problem | success | 1 | 40.9 |  |
| cobweb_diagram | fail | 3 | 258.3 | │                                                             |
| saddle_3d | fail | 3 | 237.0 | │                                           |

## Concepts

### derivative_x2

> Visualise that the derivative of x squared is 2x, by showing a tangent line whose slope updates at a moving point on the parabola y = x squared.

Session: `videos/sessions/1777277834/`

Status: **success** (attempts: 3, 205.2s)

`videos/sessions/1777277834/attempt_2_media/videos/attempt_2_scene/480p15/QuadraticDerivative.mp4`

### riemann_sum

> Show how a Riemann sum approximates the integral of x squared from 0 to 2 by drawing 8 rectangles under the curve.

Session: `videos/sessions/1777278039/`

Status: **fail** (attempts: 3, 250.2s)

```
pipeline gave up after 3 attempts. last error tail:
pt RerunSceneException:                                   │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/videos/sessions/1777278039/attempt_2 │
│ _scene.py:33 in construct                                                    │
│                                            
```

### limit_secant

> Visualise the limit definition of the derivative: a secant line between two points on a parabola y = x squared becomes the tangent line as the second point approaches the first.

Session: `videos/sessions/1777278289/`

Status: **fail** (attempts: 3, 245.7s)

```
pipeline gave up after 3 attempts. last error tail:
.5)                                                 │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/types/vectorized_mobject.py:1128 in set_points_as_corners        │
│                                                  
```

### triangle_angles

> Show that the three angles of a triangle sum to 180 degrees by drawing a triangle, copying each of its three angles, and rearranging the copies along a single straight line.

Session: `videos/sessions/1777278535/`

Status: **success** (attempts: 1, 109.7s)

`videos/sessions/1777278535/attempt_0_media/videos/attempt_0_scene/480p15/AngleSumTheorem.mp4`

### unit_circle_pythagoras

> Animate the Pythagorean identity sin squared theta plus cos squared theta equals one on a unit circle. Show the right triangle inscribed in the circle and update the values of sin theta and cos theta as theta moves around the circle.

Session: `videos/sessions/1777278645/`

Status: **fail** (attempts: 3, 259.4s)

```
pipeline gave up after 3 attempts. last error tail:
manim render failed (exit 0, no mp4 in videos/sessions/1777278645/attempt_2_media/videos/attempt_2_scene/480p15)
```

### dot_product

> Visualise the geometric meaning of the dot product of two 2D vectors by drawing both vectors from the origin, projecting one onto the other, and showing that the projection length equals the dot product divided by the second vector's magnitude.

Session: `videos/sessions/1777278904/`

Status: **success** (attempts: 1, 95.0s)

`videos/sessions/1777278904/attempt_0_media/videos/attempt_0_scene/480p15/DotProductVisualization.mp4`

### compare_powers

> Plot f(x) = x squared in blue and g(x) = x cubed in red on the same axes from x = -2 to x = 2, with labels, so the difference between quadratic and cubic growth is visible.

Session: `videos/sessions/1777278999/`

Status: **success** (attempts: 2, 136.4s)

`videos/sessions/1777278999/attempt_1_media/videos/attempt_1_scene/480p15/GrowthComparison.mp4`

### handshake_problem

> Visualise the handshake problem for 5 people: arrange 5 dots in a circle and draw every pairwise handshake as a connecting line, then display the total count of 10 handshakes as a label.

Session: `videos/sessions/1777279136/`

Status: **success** (attempts: 1, 40.9s)

`videos/sessions/1777279136/attempt_0_media/videos/attempt_0_scene/480p15/HandshakeProblem.mp4`

### cobweb_diagram

> Draw the cobweb diagram for the iterative function f(x) = 0.5 x + 1 starting from x_0 = 0, showing the first 5 iterations converging to the fixed point at x = 2. Plot the line y = f(x) and the line y = x and animate the cobweb steps between them.

Session: `videos/sessions/1777279177/`

Status: **fail** (attempts: 3, 258.3s)

```
pipeline gave up after 3 attempts. last error tail:
                                          │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/scene/scene.py:259 in render                                             │
│                                                            
```

### saddle_3d

> Show a 3D plot of the saddle surface z = x squared minus y squared, with the camera rotating around the surface so the saddle shape is clearly visible from multiple angles.

Session: `videos/sessions/1777279435/`

Status: **fail** (attempts: 3, 237.0s)

```
pipeline gave up after 3 attempts. last error tail:
  stroke_color=stroke_color,                                │
│                                                                              │
│ /Users/bartek/projekty/math-tutor-gemma/venv/lib/python3.12/site-packages/ma │
│ nim/mobject/types/vectorized_mobject.py:2143 in __init__                     │
│                                          
```
