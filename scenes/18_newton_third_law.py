"""
18 · Physics — Newton's third law: action and reaction
Two skaters push off each other. During the push the forces are equal in size
and opposite in direction, whatever their masses. Afterwards the lighter
skater moves faster: momenta are equal and opposite, total momentum stays 0.

Manim ideas: ValueTracker for time with a "push" phase then a glide phase,
paired force arrows, momentum bars that always cancel.

Render:
    manim -pqm scenes/18_newton_third_law.py NewtonThirdLaw
"""
from manim import *

BLUE_M = "#4F9DFF"
ORANGE_P = "#FF8A3D"
GREEN_B = "#3DDC97"
PINK_B = "#FF5C8A"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

M1, M2 = 50.0, 80.0          # kg
IMPULSE = 160.0              # N·s delivered during the push
T_PUSH, T_END = 0.6, 4.0
SCALE = 0.45                 # screen units per metre


def velocities():
    return -IMPULSE / M1, IMPULSE / M2      # skater 1 goes left, skater 2 right


def position(t, v, x0):
    if t < T_PUSH:   # constant force during the push → uniform acceleration
        return x0 + 0.5 * (v / T_PUSH) * t ** 2 * SCALE
    return x0 + (0.5 * v * T_PUSH + v * (t - T_PUSH)) * SCALE


def skater(color, mass, scale):
    body = RoundedRectangle(width=0.7 * scale, height=1.4 * scale, corner_radius=0.25 * scale,
                            color=WHITE, fill_color=color, fill_opacity=0.9)
    head = Circle(0.3 * scale, color=WHITE, fill_color=color, fill_opacity=0.9).next_to(body, UP, buff=0.05)
    blade = Line(LEFT * 0.45 * scale, RIGHT * 0.45 * scale, color=GREY_B, stroke_width=4).next_to(body, DOWN, buff=0.1)
    label = Text(f"{mass:.0f} kg", font_size=20, color="#0B0F19", weight=BOLD).move_to(body)
    return VGroup(body, head, blade, label)


class NewtonThirdLaw(Scene):
    def construct(self):
        title = Text("Newton's 3rd law — action & reaction", font_size=40).to_edge(UP, buff=0.3)
        law = MathTex(r"\vec F_{1\to2} = -\,\vec F_{2\to1}", font_size=42, color=YELLOW_M).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), Write(law))

        ice = Line(LEFT * 7, RIGHT * 7, color="#9FD8FF", stroke_width=3).shift(DOWN * 0.9)
        self.play(Create(ice))

        t = ValueTracker(0)
        v1, v2 = velocities()
        x1_0, x2_0 = -0.55, 0.55
        y = 0.25

        s1 = always_redraw(lambda: skater(BLUE_M, M1, 0.9).move_to([position(t.get_value(), v1, x1_0), y, 0]))
        s2 = always_redraw(lambda: skater(ORANGE_P, M2, 1.1).move_to([position(t.get_value(), v2, x2_0), y + 0.1, 0]))
        self.play(FadeIn(s1), FadeIn(s2))

        def forces():
            if t.get_value() >= T_PUSH:
                return VGroup()
            a = s1.get_left() + DOWN * 0.1
            b = s2.get_right() + DOWN * 0.1
            return VGroup(
                Arrow(a, a + LEFT * 1.6, buff=0, color=GREEN_B, stroke_width=6),
                MathTex(r"F_{2\to1}", font_size=28, color=GREEN_B).next_to(a + LEFT * 0.8, UP, buff=0.15),
                Arrow(b, b + RIGHT * 1.6, buff=0, color=GREEN_B, stroke_width=6),
                MathTex(r"F_{1\to2}", font_size=28, color=GREEN_B).next_to(b + RIGHT * 0.8, UP, buff=0.15),
            )

        force_arrows = always_redraw(forces)
        self.add(force_arrows)
        t.set_value(0.0001)
        self.wait(1.5)                                   # freeze-frame on the push
        same = Text("same size, opposite direction — even though 50 kg ≠ 80 kg", font_size=24, color=GREEN_B)
        same.next_to(ice, DOWN, buff=0.3)
        self.play(FadeIn(same))
        self.wait(1)
        self.play(t.animate.set_value(T_PUSH), run_time=1.2, rate_func=linear)
        self.play(FadeOut(same), t.animate.set_value(T_END), run_time=3.4, rate_func=linear)

        # Momentum bars
        p1, p2 = M1 * v1, M2 * v2
        base = DOWN * 2.4
        bar1 = Rectangle(width=abs(p1) / 80, height=0.4, fill_color=BLUE_M, fill_opacity=0.8, stroke_width=0)
        bar1.next_to(base, LEFT, buff=0)
        bar2 = Rectangle(width=abs(p2) / 80, height=0.4, fill_color=ORANGE_P, fill_opacity=0.8, stroke_width=0)
        bar2.next_to(base, RIGHT, buff=0)
        zero = Line(base + UP * 0.4, base + DOWN * 0.4, color=WHITE)
        vtxt = VGroup(
            MathTex(rf"v_1 = {v1:.1f}\ \mathrm{{m/s}}", font_size=30, color=BLUE_M).next_to(bar1, LEFT, buff=0.3),
            MathTex(rf"v_2 = +{v2:.1f}\ \mathrm{{m/s}}", font_size=30, color=ORANGE_P).next_to(bar2, RIGHT, buff=0.3),
        )
        total = MathTex(r"p_{\text{total}} = m_1v_1 + m_2v_2 = 0", font_size=34, color=YELLOW_M).next_to(zero, DOWN, buff=0.3)
        self.play(GrowFromEdge(bar1, RIGHT), GrowFromEdge(bar2, LEFT), Create(zero), Write(vtxt))
        self.play(Write(total))
        self.wait(2)
