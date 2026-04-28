# Curated demo prompts

Hand-picked prompts for the recorded demo video. Each one was observed to
succeed on the v2 sample (6/10 success rate, with hints, no Riemann
few-shot in the prompt). They cover four distinct math domains so the
recording shows variety, not one trick repeated.

For each: a single-paragraph prompt to paste into the UI / CLI verbatim.
Use `python -m src.pipeline "<prompt>"` for a CLI run, or paste into the
React form at `http://localhost:5173`.

Order is intentional — the demo flow alternates topics so the audience
doesn't fatigue on similar visuals.

## 1. Pythagorean theorem visual proof — geometry
**Why it's reliable:** Pythagoras is a hand-written few-shot in the prompt
template. Gemma has the structure memorised and reliably produces a clean
rearrangement.

> Show a visual proof of the Pythagorean theorem by area rearrangement: a
> square of side a+b containing four right triangles around a smaller
> square of side c, then rearrange the four triangles to expose two
> squares of sides a and b.

## 2. Triangle angle sum — classic geometry
**Why it's reliable:** v1 and v2 both first-try success. Polygon idiom
matches `pythagorean_proof.py` few-shot.

> Show that the three angles of a triangle sum to 180 degrees by drawing
> a triangle, copying each of its three angles, and rearranging the
> copies along a single straight line.

## 3. Handshake problem (combinatorics) — n=5
**Why it's reliable:** v1 and v2 both first-try success in ~40 s. Easy
visual: 5 dots, 10 connecting lines, count label. Demonstrates the
pipeline beyond calculus/geometry.

> Visualise the handshake problem for 5 people: arrange 5 dots in a
> circle and draw every pairwise handshake as a connecting line, then
> display the total count of 10 handshakes as a label.

## 4. Dot product — vector geometry
**Why it's reliable:** v2 first-try success in ~70 s. Polygon + Line
idioms.

> Visualise the geometric meaning of the dot product of two 2D vectors
> by drawing both vectors from the origin, projecting one onto the
> other, and showing that the projection length equals the dot product
> divided by the second vector's magnitude.

## 5. Derivative of x² (calculus) — tangent line
**Why it's reliable:** Mostly first-try; this concept is structurally a
near-twin of the `derivative_tangent.py` few-shot. v1 succeeded after
retry, v2 first-try succeeded a separate run earlier in the day.

> Visualise that the derivative of x squared is 2x, by showing a tangent
> line whose slope updates at a moving point on the parabola y = x squared.

---

## Backups (if a primary fails on the day of recording)

These are also v2-success but a tier behind in either visual punch or
reliability:

- **Limit definition of derivative (secant → tangent):** v2 succeeded on
  retry. Strong calculus narrative, but the secant-to-tangent transition
  is visually subtle in 480p. Promote if a primary slot fails.
- **Riemann sum:** v2 first-try success (no Riemann few-shot in prompt!).
  Visually striking but the prompt-size regression in v3 means we should
  not expect this to be reproducible if anyone touches the prompt.

## Out of scope for this video

- 3D scenes (`saddle_3d`): pipeline cannot produce these reliably. For
  any 3D in the demo, run the hand-written `examples/saddle_3d.py`
  directly with `manim -qh` and cut to the resulting mp4.
- Cobweb diagram, unit-circle Pythagorean identity: not yet reliable.
  Skip in this recording, revisit in a later iteration.

## Recording tips

1. Run the demo in **`-qh`** (1080p60) for the recording, not `-ql`. Edit
   `manim_runner.DEFAULT_TIMEOUT` to 600 s if needed; high-quality renders
   take longer.
2. Pre-render each prompt once before the take to populate manim's cache,
   so the recorded run is as fast as possible.
3. Cap the visible Gemma generation in the UI — it's slow (~30–80 s).
   Either edit the demo to cut over generation, or use a "we generated
   this earlier" voice-over.
