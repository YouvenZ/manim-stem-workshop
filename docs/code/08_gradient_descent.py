"""
08 · Code / ML — Gradient descent and the learning rate
Two runs on the same bowl f(x, y) = x^2 + 4y^2: a small step size walks
smoothly to the minimum, a large one zig-zags across the valley.
The loss curve (right) is drawn from the very same iterates.

Manim ideas: contour lines as Ellipses, Arrows for update steps,
a loss plot built point by point, MathTex for the update rule.

Render:
    manim -pqm scenes/08_gradient_descent.py GradientDescent
"""
from manim import *

PURPLE_C = "#B57BFF"
ORANGE_P = "#FF8A3D"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

START = np.array([-3.6, 1.7])
STEPS = 14


def f(p):
    return p[0] ** 2 + 4 * p[1] ** 2


def grad(p):
    return np.array([2 * p[0], 8 * p[1]])


def descend(lr):
    pts = [START]
    for _ in range(STEPS):
        pts.append(pts[-1] - lr * grad(pts[-1]))
    return pts


class GradientDescent(Scene):
    def construct(self):
        title = Text("Gradient descent — choosing the learning rate", font_size=36).to_edge(UP, buff=0.3)
        rule = MathTex(r"\mathbf{x}_{t+1} = \mathbf{x}_t - \eta\,\nabla f(\mathbf{x}_t)", font_size=40)
        rule.next_to(title, DOWN, buff=0.25)
        self.play(Write(title))
        self.play(Write(rule))

        plane = Axes(x_range=[-4, 4, 1], y_range=[-2.2, 2.2, 1], x_length=7.2, y_length=4.0,
                     tips=False, axis_config={"color": GREY_M, "stroke_width": 1.5})
        plane.to_edge(LEFT, buff=0.4).shift(DOWN * 0.7)
        unit = plane.x_axis.get_unit_size()
        contours = VGroup(*[
            Ellipse(width=2 * np.sqrt(c) * unit, height=np.sqrt(c) * unit,
                    color=interpolate_color(ManimColor("#2B3A67"), ManimColor("#4F9DFF"), 1 - c / 16),
                    stroke_width=2).move_to(plane.c2p(0, 0))
            for c in (0.5, 1.5, 3, 5, 7.5, 10.5, 14)
        ])
        minimum = Dot(plane.c2p(0, 0), color=WHITE, radius=0.06)
        fx = MathTex(r"f(x,y)=x^2+4y^2", font_size=30).next_to(plane, UP, buff=0.1).align_to(plane, LEFT)

        loss_ax = Axes(x_range=[0, STEPS, 2], y_range=[0, 25, 5], x_length=4.6, y_length=3.6, tips=False,
                       axis_config={"color": GREY_M, "include_numbers": True, "font_size": 20})
        loss_ax.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.7)
        loss_labels = VGroup(Text("iteration", font_size=20).next_to(loss_ax.x_axis, DOWN, buff=0.35),
                             Text("loss f", font_size=20).next_to(loss_ax, UP, buff=0.1).align_to(loss_ax, LEFT))

        self.play(Create(plane), LaggedStart(*[Create(c) for c in contours], lag_ratio=0.1),
                  FadeIn(minimum), Write(fx))
        self.play(Create(loss_ax), FadeIn(loss_labels))

        legend = VGroup()
        for k, (lr, color) in enumerate(((0.08, PURPLE_C), (0.23, ORANGE_P))):
            pts = descend(lr)
            tag = MathTex(rf"\eta = {lr:.2f}", font_size=32, color=color)
            legend.add(tag)
            tag.next_to(loss_ax, UP, buff=0.55 + 0.45 * k).align_to(loss_ax, RIGHT)
            self.play(FadeIn(tag))

            walker = Dot(plane.c2p(*pts[0]), color=color, radius=0.09)
            loss_dots = VGroup(Dot(loss_ax.c2p(0, f(pts[0])), color=color, radius=0.05))
            self.play(FadeIn(walker), FadeIn(loss_dots[0]))
            for t in range(1, len(pts)):
                a, b = plane.c2p(*pts[t - 1]), plane.c2p(*pts[t])
                step = Arrow(a, b, buff=0, color=color, stroke_width=3,
                             max_tip_length_to_length_ratio=0.25, tip_length=0.15)
                new_dot = Dot(loss_ax.c2p(t, f(pts[t])), color=color, radius=0.05)
                seg = Line(loss_dots[-1].get_center(), new_dot.get_center(), color=color, stroke_width=3)
                rt = 0.5 if t < 5 else 0.25
                self.play(GrowArrow(step), walker.animate.move_to(b), Create(seg), FadeIn(new_dot), run_time=rt)
                loss_dots.add(new_dot)

        verdict = Text("too small: slow   ·   too large: oscillates (or diverges!)", font_size=22, color=YELLOW_M)
        verdict.to_edge(DOWN, buff=0.12)
        self.play(Write(verdict))
        self.wait(2)
