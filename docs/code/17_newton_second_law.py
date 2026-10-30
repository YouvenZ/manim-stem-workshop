"""
17 · Physics — Newton's second law: F = m a
The same 2 N force pushes a 1 kg cart and a 2 kg cart. The light cart gets
twice the acceleration: its v(t) line is twice as steep and it covers twice
the distance in the same time.

Manim ideas: positions from kinematics x = ½ a t², force/acceleration arrows
attached to moving objects, a live v(t) graph and DecimalNumber read-outs.

Render:
    manim -pqm scenes/17_newton_second_law.py NewtonSecondLaw
"""
from manim import *

BLUE_M = "#4F9DFF"
PINK_B = "#FF5C8A"
GREEN_B = "#3DDC97"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

F = 2.0                 # newtons
MASSES = (1.0, 2.0)     # kg
COLORS = (BLUE_M, PINK_B)
T_END = 3.0             # simulated seconds
SCALE = 0.6             # screen units per metre
X0 = -5.0


class NewtonSecondLaw(Scene):
    def construct(self):
        title = Text("Newton's 2nd law", font_size=40).to_edge(UP, buff=0.3)
        law = MathTex(r"\vec F = m\,\vec a \quad\Longrightarrow\quad a = \frac{F}{m}", font_size=40, color=YELLOW_M)
        law.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(law))

        t = ValueTracker(0)
        tracks, carts, readouts = VGroup(), VGroup(), VGroup()
        ys = (0.0, -2.0)
        for m, color, y in zip(MASSES, COLORS, ys):
            a = F / m
            tracks.add(Line([X0 - 0.5, y - 0.45, 0], [0.8, y - 0.45, 0], color=GREY_M, stroke_width=3))
            width = 0.8 + 0.4 * m

            def cart(m=m, a=a, color=color, y=y, width=width):
                x = X0 + SCALE * 0.5 * a * t.get_value() ** 2
                body = RoundedRectangle(width=width, height=0.6, corner_radius=0.1, color=WHITE,
                                        fill_color=color, fill_opacity=0.85).move_to([x, y, 0])
                label = Text(f"{m:.0f} kg", font_size=22, color="#0B0F19", weight=BOLD).move_to(body)
                wheels = VGroup(*[Circle(0.13, color=WHITE, fill_color=GREY_M, fill_opacity=1)
                                  .move_to(body.get_bottom() + RIGHT * dx * width / 3 + DOWN * 0.13) for dx in (-1, 1)])
                force = Arrow(body.get_left() + LEFT * 1.1, body.get_left(), buff=0, color=GREEN_B, stroke_width=6,
                              max_tip_length_to_length_ratio=0.25)
                f_lab = MathTex("F", font_size=30, color=GREEN_B).next_to(force, UP, buff=0.05)
                acc = Arrow(body.get_top() + UP * 0.15, body.get_top() + UP * 0.15 + RIGHT * a * 0.6, buff=0,
                            color=YELLOW_M, stroke_width=5, max_tip_length_to_length_ratio=0.3)
                a_lab = MathTex("a", font_size=30, color=YELLOW_M).next_to(acc, RIGHT, buff=0.08)
                return VGroup(body, label, wheels, force, f_lab, acc, a_lab)

            carts.add(always_redraw(cart))
            readouts.add(MathTex(rf"a = \frac{{{F:.0f}\,\mathrm{{N}}}}{{{m:.0f}\,\mathrm{{kg}}}} = {a:.0f}\ \mathrm{{m/s^2}}",
                                 font_size=30, color=color).move_to([-2.6, y + 1.2, 0]))

        ax = Axes(x_range=[0, T_END, 1], y_range=[0, 6.5, 2], x_length=3.6, y_length=3.6, tips=False,
                  axis_config={"color": GREY_M, "include_numbers": True, "font_size": 18})
        ax.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.8)
        ax_lab = VGroup(Text("v (m/s)", font_size=20).next_to(ax.y_axis, UP, buff=0.1),
                        Text("t (s)", font_size=20).next_to(ax.x_axis, DOWN, buff=0.35))
        lines = VGroup(*[always_redraw(lambda a=F / m, c=c: ax.plot(lambda s: a * s, x_range=[0, max(t.get_value(), 0.01)],
                                                                    color=c, stroke_width=5))
                         for m, c in zip(MASSES, COLORS)])

        self.play(Create(tracks), FadeIn(carts), Create(ax), FadeIn(ax_lab))
        self.play(LaggedStart(*[Write(r) for r in readouts], lag_ratio=0.4))
        self.add(lines)
        self.play(t.animate.set_value(T_END), run_time=6, rate_func=linear)

        slopes = VGroup(Text("slope = a", font_size=22, color=GREY_B).next_to(ax, UP, buff=0.15))
        verdict = Text("same force, double mass → half the acceleration", font_size=28, color=YELLOW_M).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(slopes), Write(verdict))
        self.wait(2)
