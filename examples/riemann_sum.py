"""Reference scene: Riemann sum of x² on [0, 2] with growing rectangle count.

Hand-written few-shot covering the integration / area-under-curve idiom.
Demonstrates:

- `ax.plot(callable, x_range=...)` — same rule as the derivative scene.
- `ax.get_riemann_rectangles(graph, x_range=..., dx=...)` — the canonical
  Manim CE call for Riemann rectangles. Returns a `VGroup` of `Polygon`s.
- `Transform(group_a, group_b)` to morph between two rectangle counts.
- A label that updates with the rectangle count via `Tex` rebuild.
"""

from manim import *
import numpy as np


class RiemannSum(Scene):
    def construct(self):
        axes = Axes(
            x_range=[0, 2.5, 0.5],
            y_range=[0, 4.5, 1],
            x_length=8,
            y_length=5,
            axis_config={"include_numbers": True},
        ).to_edge(DOWN, buff=0.6)

        graph = axes.plot(lambda x: x * x, x_range=[0, 2], color=BLUE, stroke_width=4)
        f_label = MathTex(r"f(x) = x^2", color=BLUE).to_corner(UL)

        self.play(Create(axes), Create(graph), Write(f_label))

        rects_4 = axes.get_riemann_rectangles(
            graph, x_range=[0, 2], dx=0.5, color=GREEN, fill_opacity=0.6,
        )
        count_label = MathTex("n = 4", color=GREEN).to_corner(UR)
        self.play(Create(rects_4), Write(count_label))
        self.wait(0.5)

        rects_8 = axes.get_riemann_rectangles(
            graph, x_range=[0, 2], dx=0.25, color=GREEN, fill_opacity=0.6,
        )
        new_count = MathTex("n = 8", color=GREEN).to_corner(UR)
        self.play(Transform(rects_4, rects_8), Transform(count_label, new_count))
        self.wait(0.5)

        rects_20 = axes.get_riemann_rectangles(
            graph, x_range=[0, 2], dx=0.1, color=GREEN, fill_opacity=0.6,
        )
        new_count = MathTex("n = 20", color=GREEN).to_corner(UR)
        self.play(Transform(rects_4, rects_20), Transform(count_label, new_count))
        self.wait(0.5)

        result = MathTex(r"\int_0^2 x^2\,dx = \tfrac{8}{3}", font_size=48).to_edge(UP)
        self.play(Write(result))
        self.wait(2)
