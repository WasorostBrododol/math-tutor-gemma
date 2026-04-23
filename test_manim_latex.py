from manim import *

class FormulaScene(Scene):
    def construct(self):
        formula = MathTex(r"e^{i\pi} + 1 = 0")
        self.play(Write(formula))
        self.wait(2)
