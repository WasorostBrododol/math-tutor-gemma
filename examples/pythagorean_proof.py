"""Reference scene: Pythagorean theorem visual proof by area rearrangement.

Hand-written few-shot example for the MathMentor pipeline. Demonstrates the
Manim Community Edition idioms Gemma 4 hallucinated past in the week-1
baseline (03_pythagorean):

- Polygon(*vertices) for custom shapes. Manim's Triangle class is hardcoded
  equilateral and does NOT accept a `points=` argument.
- VGroup to manage a configuration as a single unit.
- Transform between two valid arrangements of the same four triangles, to
  visually argue that the central c² area equals a² + b².
"""

from manim import *
import numpy as np


def vec(x: float, y: float) -> np.ndarray:
    return np.array([x, y, 0])


class PythagoreanProof(Scene):
    def construct(self):
        a, b = 1.5, 2.5
        s = a + b
        center_shift = vec(-s / 2, -s / 2)

        outer = Polygon(
            vec(0, 0), vec(s, 0), vec(s, s), vec(0, s),
            color=WHITE, stroke_width=3,
        )
        v1, v2, v3, v4 = vec(b, 0), vec(s, b), vec(a, s), vec(0, a)
        inner_c2 = Polygon(v1, v2, v3, v4, color=RED, fill_opacity=0.5)

        t1 = Polygon(v1, vec(s, 0), v2, color=BLUE, fill_opacity=0.5)
        t2 = Polygon(v2, vec(s, s), v3, color=BLUE, fill_opacity=0.5)
        t3 = Polygon(v3, vec(0, s), v4, color=BLUE, fill_opacity=0.5)
        t4 = Polygon(v4, vec(0, 0), v1, color=BLUE, fill_opacity=0.5)

        c2_label = MathTex("c^2", color=RED).move_to(inner_c2.get_center())

        config1 = VGroup(outer, t1, t2, t3, t4, inner_c2, c2_label)
        config1.shift(center_shift)

        self.play(Create(outer))
        self.play(FadeIn(t1, t2, t3, t4))
        self.play(FadeIn(inner_c2), Write(c2_label))
        self.wait(1)

        t1_target = Polygon(vec(a, 0), vec(s, 0), vec(s, a), color=BLUE, fill_opacity=0.5)
        t2_target = Polygon(vec(a, 0), vec(s, a), vec(a, a), color=BLUE, fill_opacity=0.5)
        t3_target = Polygon(vec(0, a), vec(a, a), vec(a, s), color=BLUE, fill_opacity=0.5)
        t4_target = Polygon(vec(0, a), vec(a, s), vec(0, s), color=BLUE, fill_opacity=0.5)

        sq_a = Polygon(
            vec(0, 0), vec(a, 0), vec(a, a), vec(0, a),
            color=GREEN, fill_opacity=0.5,
        )
        sq_b = Polygon(
            vec(a, a), vec(s, a), vec(s, s), vec(a, s),
            color=ORANGE, fill_opacity=0.5,
        )
        a2_label = MathTex("a^2", color=GREEN).move_to(sq_a.get_center())
        b2_label = MathTex("b^2", color=ORANGE).move_to(sq_b.get_center())

        for m in (t1_target, t2_target, t3_target, t4_target, sq_a, sq_b, a2_label, b2_label):
            m.shift(center_shift)

        self.play(FadeOut(inner_c2), FadeOut(c2_label))
        self.play(
            Transform(t1, t1_target),
            Transform(t2, t2_target),
            Transform(t3, t3_target),
            Transform(t4, t4_target),
            run_time=2.5,
        )
        self.play(FadeIn(sq_a), FadeIn(sq_b), Write(a2_label), Write(b2_label))
        self.wait(0.5)

        equation = MathTex("a^2 + b^2 = c^2", font_size=56).to_edge(UP)
        self.play(Write(equation))
        self.wait(2)
