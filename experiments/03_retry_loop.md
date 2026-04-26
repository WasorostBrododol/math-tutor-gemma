# 03 — Retry loop on render error (and a 3D few-shot's limits)

**Date:** 2026-04-27
**Model:** `gemma4:e4b-it-q8_0`
**Goal:** add resilience to `src/pipeline.py` — when manim render fails,
feed the error back to Gemma and let it self-repair, up to 2 retries.
Verify on a regression case (must still succeed first try) and on a hard
case (3D, no/new few-shot).

## What changed in the code

`src/manim_runner.py`:

- Default timeout reduced 300 s → 120 s (low-quality renders are seconds; 5+ min
  always means a hang).
- `subprocess.TimeoutExpired` is now caught and converted to `ManimRenderError`
  — surfaced through the same channel as a normal render failure so the retry
  loop can react.
- Render error is a typed `ManimRenderError(message, *, stderr, stdout)` with
  the captured streams as attributes (instead of one giant string), so the
  pipeline can feed exactly stderr to the repair prompt.

`src/pipeline.py`:

- `ask()` now loops up to `MAX_RETRIES = 2` extra attempts after the first
  (3 total). Each attempt writes its own `attempt_<n>_scene.py`,
  `attempt_<n>_raw.txt`, optional `attempt_<n>_error.txt`, and a per-attempt
  `attempt_<n>_media/` subtree.
- A `REPAIR_TEMPLATE` builds the retry prompt: previous code + tail of manim
  stderr, asking for a corrected fenced block.
- AST pre-check: `compile(code, scene_file, "exec")` runs before invoking
  manim. A `SyntaxError` is caught as a separate failure path and triggers
  retry without paying the 30–80 s render cost.

`prompts/manim_generator.txt`:

- Rules 13–16 added:
  - 13: build the minimum the concept asks for; no decorative axes/circles
    /arrows unless requested. (Addresses the "Gemma overreaches" pattern from
    the previous experiment.)
  - 14: 3D scenes need `ThreeDScene` and `ThreeDAxes`; 2D and 3D classes are
    not interchangeable.
  - 15: `Surface(callable, u_range=..., v_range=..., resolution=...)` —
    parametric, NEVER `x_range` / `y_range`.
  - 16: 3D screen-anchored labels via `self.add_fixed_in_frame_mobjects(label)`.
- Fifth few-shot added: `Saddle3D` matching the new `examples/saddle_3d.py`.

`examples/saddle_3d.py`: hand-written 3D reference scene used as the fifth
few-shot (and renders cleanly stand-alone).

## Run 1 — regression

**Concept:** "Visualise the Pythagorean identity sin² x + cos² x = 1 as a single
beautifully written formula."

| Attempt | Result | Notes |
|---------|--------|-------|
| 0 | success | 33.6 s gen, 3.5 s render |

Total: ~37 s. Gemma produced 19-line MathTex + small label, exactly the
"single beautifully written formula" the prompt asked for. Rule 13 (build
the minimum) appears to have helped — earlier runs of similar prompts had
Gemma adding a unit circle, axes, and a `GrowArrow(Line)` (which hangs
manim, see prior 300 s timeout).

## Run 2 — 3D saddle, no few-shot (BEFORE adding rules 14–16 and Saddle3D few-shot)

**Concept:** "Show a 3D plot of the saddle surface z = x² − y², with the
camera rotating around the surface so the saddle shape is clearly visible
from multiple angles."

| Attempt | Result | Cause |
|---------|--------|-------|
| 0 | fail | `SyntaxError: ... rotation_updater.animate.run_time = 15,` (Manim API generally right, but a literal-syntax slip) |
| 1 | fail | `TypeError: Mobject.__init__() got an unexpected keyword argument 'x_range'` (Surface kwargs hallucination — should be `u_range`/`v_range`) |
| 2 | fail | `ModuleNotFoundError: No module named 'matplotlib'` — Gemma capitulated and switched library |

Total: ~340 s, all three attempts failed. Notable: when Gemma had no
3D few-shot, two retries were not enough; the model drifted away from
manim entirely and reached for matplotlib. **Retry mechanically works but
cannot rescue an absent few-shot.**

## Run 3 — 3D saddle, AFTER adding the 5th few-shot and rules 14–16

| Attempt | Result | Cause |
|---------|--------|-------|
| 0 | fail | `AttributeError: 'SaddleSurface3D' object has no attribute 'objects'` — Gemma followed the few-shot's structure but added a `self.play(FadeOut(self.objects))` at the end. `self.mobjects` is the actual attribute. |
| 1 | fail | `TypeError: Animation only works on Mobjects` — after the previous feedback Gemma swapped `self.objects` for a manual list `scene_objects = [axes, surface, label]` and then passed the *list* to `FadeOut(...)`. Animations need a `Mobject`/`VGroup`, not a list. |
| 2 | fail | Same `TypeError`. Gemma cannot interpret manim's "only works on Mobjects" message and loops. |

Total: also ~3 attempts × ~3 min, all failed. **Worth noting:** Gemma got
the *Surface API* right this time (rule 15 + few-shot worked),
got `ThreeDScene` and `ThreeDAxes` right (rule 14 + few-shot), and got the
camera orientation right. The persistent failure was a *new* class of
mistake: improvising scene cleanup with a method/attribute the few-shot
didn't show. The error message Gemma gets back ("Animation only works on
Mobjects") doesn't tell her to wrap in VGroup, and she self-loops.

## Conclusions

1. **Retry loop works as designed.** The mechanics (catch error → repair
   prompt → fresh attempt → typed error class on `manim_runner` side) all
   operate correctly. Run 1's regression case still passes first try, no
   spurious retries triggered. Runs 2 and 3 exercise the retry path.
2. **AST pre-check is cheap insurance.** Worth ~30–80 s per attempt that
   would otherwise have been spent rendering a syntactically broken file.
3. **Few-shots cover *core idioms* but leak on edges.** Saddle3D taught
   Gemma the parametric Surface, the camera, the fixed-in-frame label —
   exactly what the few-shot showed. But it didn't show *how to end the
   scene*, and Gemma improvised wrong. Two implications:
   - Hand-written few-shots need to be a bit more *complete* (cover the
     opening, the body, AND a clean closing).
   - Or the retry repair prompt needs hints. Right now the prompt feeds
     manim's stderr verbatim, which is sometimes too cryptic — e.g.
     "Animation only works on Mobjects" is not actionable to Gemma. A
     small mapping of common manim error strings → human-readable hints
     could close this gap.
4. **2D is solid; 3D needs another iteration.** Day-3 priority was 2D
   reliability — that's met. 3D pipeline is one more revision away.

## Next iteration (day 4)

- Tighten the 3D few-shot to also show a clean closing (`self.wait(...)`,
  no FadeOut). Or add a rule: "Do not call `self.objects`; do not pass
  lists to animations — use `VGroup(*mobjects)` or unpack with `*`."
- Optional: a small post-processor in `pipeline.py` that translates known
  manim error patterns into hints before feeding to Gemma. Low cost, easy
  to extend.
- Larger sample of concepts (5–10 across 2D / 3D) once 3D is reliably
  passing. That's the number that goes into the write-up.
