"""Reference scene: 3D saddle surface z = x² - y² with orbiting camera.

Hand-written few-shot example for the MathMentor pipeline. Demonstrates the
Manim Community Edition 3D idioms:

- `ThreeDScene` (NOT `Scene`) — required for camera orientation control.
- `ThreeDAxes` (NOT `Axes`) — three axes with proper 3D positioning.
- `Surface(callable, u_range=[u0, u1], v_range=[v0, v1], resolution=(...))`
  for parametric surfaces. The callable returns a 3D point. The Surface
  class uses `u_range` and `v_range` — NEVER `x_range`/`y_range`.
- `axes.c2p(x, y, z)` to map data coordinates into the axes' display frame.
- `set_camera_orientation(phi, theta)` for the initial viewpoint.
- `begin_ambient_camera_rotation(rate=...)` / `stop_ambient_camera_rotation()`
  for an orbiting camera.
- `self.add_fixed_in_frame_mobjects(label)` so on-screen text stays anchored
  to the screen (does not rotate with the camera).
"""

from manim import *


class Saddle3D(ThreeDScene):
    def construct(self):
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-9, 9, 3],
            x_length=7,
            y_length=7,
            z_length=5,
        )

        def saddle(u: float, v: float):
            return axes.c2p(u, v, u * u - v * v)

        surface = Surface(
            saddle,
            u_range=[-3, 3],
            v_range=[-3, 3],
            resolution=(30, 30),
            fill_opacity=0.6,
            fill_color=BLUE,
            stroke_color=WHITE,
            stroke_width=1,
        )

        label = MathTex("z = x^2 - y^2", font_size=48)

        self.set_camera_orientation(phi=70 * DEGREES, theta=30 * DEGREES)
        self.add_fixed_in_frame_mobjects(label)
        label.to_corner(UL)

        self.play(Create(axes), run_time=1)
        self.play(Create(surface), run_time=2)

        self.begin_ambient_camera_rotation(rate=0.3)
        self.wait(6)
        self.stop_ambient_camera_rotation()

        self.wait(0.5)
