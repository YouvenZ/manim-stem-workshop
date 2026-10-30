"""
Exercise 1 — A tangent line sliding along a curve  (≈ 20 min)

Goal: animate the tangent to f(x) = x^3/4 - x while x moves from -2 to 2,
with a live read-out of the slope f'(x).

Fill in the TODOs, then render with:
    manim -pql exercises/ex1_tangent_line.py TangentLine

Stuck? See exercises/solutions/ex1_tangent_line_solution.py
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

        # TODO 1: create a ValueTracker that starts at x = -2
        x = ...

        # TODO 2: a Dot that always sits on the graph at x.
        #   hint: always_redraw(lambda: Dot(axes.c2p(x.get_value(), f(x.get_value()))))
        dot = ...

        # TODO 3: the tangent line, rebuilt every frame.
        #   hint: axes.get_secant_slope_group(x.get_value(), graph, dx=0.001,
        #                                     secant_line_length=4, secant_line_color=YELLOW)
        tangent = ...

        # TODO 4 (bonus): a DecimalNumber showing df(x) that follows the dot.

        self.add(tangent, dot)

        # TODO 5: animate x from -2 to 2 in 6 seconds
        ...
        self.wait()
