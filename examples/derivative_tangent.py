"""Reference scene: animated tangent to sin(x), illustrating f'(x) = cos(x).

Hand-written few-shot example for the MathMentor pipeline. Demonstrates the
Manim Community Edition idioms Gemma 4 hallucinated past in the week-1
baseline experiment:

- Axes + ax.plot(callable, x_range=...) — pass a *function*, never a
  pre-evaluated array.
- ValueTracker drives the animated parameter.
- always_redraw rebuilds derived mobjects (dot, tangent line, slope readout)
  every frame from the tracker's current value.
- A single self.play(tracker.animate.set_value(...)) replaces any explicit
  per-step loop.
"""

from manim import *
import numpy as np


class DerivativeTangent(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-PI, PI, PI / 2],
            y_range=[-1.5, 1.5, 0.5],
            x_length=10,
            y_length=5,
            axis_config={"include_numbers": False},
        ).to_edge(DOWN, buff=0.8)

        sin_curve = axes.plot(np.sin, x_range=[-PI, PI], color=BLUE, stroke_width=4)
        cos_curve = axes.plot(np.cos, x_range=[-PI, PI], color=RED, stroke_width=2)
        sin_label = MathTex(r"f(x) = \sin(x)", color=BLUE).to_corner(UL)
        cos_label = MathTex(r"f'(x) = \cos(x)", color=RED).next_to(
            sin_label, DOWN, aligned_edge=LEFT
        )

        self.play(Create(axes))
        self.play(Create(sin_curve), Write(sin_label))
        self.play(Create(cos_curve), Write(cos_label))

        tracker = ValueTracker(-PI + 0.1)

        dot_on_sin = always_redraw(
            lambda: Dot(
                axes.coords_to_point(tracker.get_value(), np.sin(tracker.get_value())),
                color=YELLOW,
                radius=0.08,
            )
        )
        dot_on_cos = always_redraw(
            lambda: Dot(
                axes.coords_to_point(tracker.get_value(), np.cos(tracker.get_value())),
                color=YELLOW,
                radius=0.06,
            )
        )

        def build_tangent() -> Line:
            x = tracker.get_value()
            slope = np.cos(x)
            y = np.sin(x)
            half = 1.2
            return Line(
                axes.coords_to_point(x - half, y - slope * half),
                axes.coords_to_point(x + half, y + slope * half),
                color=YELLOW,
                stroke_width=4,
            )

        tangent = always_redraw(build_tangent)

        slope_readout = always_redraw(
            lambda: MathTex(
                rf"\cos({tracker.get_value():.2f}) = {np.cos(tracker.get_value()):+.2f}",
                color=YELLOW,
            ).to_corner(UR)
        )

        self.play(
            FadeIn(dot_on_sin),
            FadeIn(dot_on_cos),
            Create(tangent),
            Write(slope_readout),
        )
        self.wait(0.3)

        self.play(
            tracker.animate.set_value(PI - 0.1),
            run_time=6,
            rate_func=linear,
        )
        self.wait(1)
