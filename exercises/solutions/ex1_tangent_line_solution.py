"""
Solution to Exercise 1 — a tangent line sliding along a curve.
    manim -pql exercises/solutions/ex1_tangent_line_solution.py TangentLine
"""
from manim import *


def f(x):
    return x ** 3 / 4 - x


def df(x):
    return 3 * x ** 2 / 4 - 1


class TangentLine(Scene):
    def construct(self):
        axes = Axes(x_range=[-3, 3, 1], y_range=[-2.5, 2.5, 1], x_length=10, y_length=6, tips=False)
        graph = axes.plot(f, color=BLUE)
        self.play(Create(axes), Create(graph))

        x = ValueTracker(-2)
        dot = always_redraw(lambda: Dot(axes.c2p(x.get_value(), f(x.get_value())), color=PINK))
        tangent = always_redraw(lambda: axes.get_secant_slope_group(
            x.get_value(), graph, dx=0.001, secant_line_length=4, secant_line_color=YELLOW))
        slope = always_redraw(lambda: VGroup(
            MathTex("f'(x) ="), DecimalNumber(df(x.get_value()), num_decimal_places=2)
        ).arrange(RIGHT).next_to(dot, UR, buff=0.3))

        self.add(tangent, dot, slope)
        self.play(x.animate.set_value(2), run_time=6)
        self.wait()
