"""
16 · Physics — Newton's first law (inertia)
Two identical pucks are launched at the same speed. On ice (no friction) the
net force is zero, so the velocity never changes. On carpet, friction is
the net force and the puck slows to a stop. The v(t) graph tells the same story.

Manim ideas: one ValueTracker clock for two systems, velocity arrows whose
length follows v, a live v(t) plot drawn with always_redraw.

Render:
    manim -pqm scenes/16_newton_first_law.py NewtonFirstLaw
"""
from manim import *

BLUE_M = "#4F9DFF"
ORANGE_P = "#FF8A3D"
PINK_B = "#FF5C8A"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

V0 = 1.3        # screen units per second
DECEL = 0.45    # friction deceleration on carpet
T_END = 6.0
X0 = -6.0


def x_ice(t):
    return X0 + V0 * t


def v_carpet(t):
    return max(V0 - DECEL * t, 0)


def x_carpet(t):
    ts = min(t, V0 / DECEL)
    return X0 + V0 * ts - 0.5 * DECEL * ts ** 2


class NewtonFirstLaw(Scene):
    def construct(self):
        title = Text("Newton's 1st law — inertia", font_size=40).to_edge(UP, buff=0.3)
        law = Text("ΣF = 0  ⇔  velocity stays constant", font_size=28, color=YELLOW_M).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), FadeIn(law))

        lane_ice = Rectangle(width=9.4, height=1.3, fill_color="#9FD8FF", fill_opacity=0.12, stroke_color=BLUE_M)
        lane_carpet = Rectangle(width=9.4, height=1.3, fill_color="#C27C4A", fill_opacity=0.18, stroke_color=ORANGE_P)
        lanes = VGroup(lane_ice, lane_carpet).arrange(DOWN, buff=1.0).move_to(LEFT * 2.0 + DOWN * 0.5)
        tags = VGroup(Text("ice: no friction", font_size=22, color=BLUE_M).next_to(lane_ice, UP, buff=0.1).align_to(lane_ice, LEFT),
                      Text("carpet: friction", font_size=22, color=ORANGE_P).next_to(lane_carpet, UP, buff=0.1).align_to(lane_carpet, LEFT))
        self.play(FadeIn(lanes), FadeIn(tags))

        clock = ValueTracker(0)
        y_ice, y_carpet = lane_ice.get_y(), lane_carpet.get_y()

        def puck(x, y, color):
            return VGroup(Circle(0.32, color=WHITE, fill_color=color, fill_opacity=0.9),
                          Circle(0.12, color=WHITE, stroke_width=2)).move_to([x, y, 0])

        p_ice = always_redraw(lambda: puck(x_ice(clock.get_value()), y_ice, BLUE_M))
        p_car = always_redraw(lambda: puck(x_carpet(clock.get_value()), y_carpet, ORANGE_P))

        def v_arrow(x, y, v):
            start = np.array([x + 0.35, y, 0])
            if v < 1e-3:
                return VGroup()
            return Arrow(start, start + RIGHT * v * 1.1, buff=0, color=YELLOW_M, stroke_width=5,
                         max_tip_length_to_length_ratio=0.3)

        va_ice = always_redraw(lambda: v_arrow(x_ice(clock.get_value()), y_ice + 0.0, V0))
        va_car = always_redraw(lambda: v_arrow(x_carpet(clock.get_value()), y_carpet, v_carpet(clock.get_value())))
        friction = always_redraw(lambda: VGroup() if v_carpet(clock.get_value()) < 1e-3 else Arrow(
            np.array([x_carpet(clock.get_value()) - 0.35, y_carpet, 0]),
            np.array([x_carpet(clock.get_value()) - 1.25, y_carpet, 0]),
            buff=0, color=PINK_B, stroke_width=5, max_tip_length_to_length_ratio=0.3))
        f_labels = VGroup(Text("v", font_size=24, color=YELLOW_M), Text("f (friction)", font_size=22, color=PINK_B))
        f_labels[0].next_to(lane_ice, DOWN, buff=0.1).align_to(lane_ice, RIGHT)
        f_labels[1].next_to(lane_carpet, DOWN, buff=0.1).align_to(lane_carpet, RIGHT)

        # v(t) graph
        ax = Axes(x_range=[0, T_END, 2], y_range=[0, 1.6, 0.5], x_length=3.4, y_length=2.6, tips=False,
                  axis_config={"color": GREY_M, "font_size": 18})
        ax.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.4)
        ax_lab = VGroup(Text("v", font_size=22).next_to(ax.y_axis, UP, buff=0.1),
                        Text("t", font_size=22).next_to(ax.x_axis, RIGHT, buff=0.1))
        g_ice = always_redraw(lambda: ax.plot(lambda t: V0, x_range=[0, max(clock.get_value(), 0.01)], color=BLUE_M))
        g_car = always_redraw(lambda: ax.plot(v_carpet, x_range=[0, max(clock.get_value(), 0.01), 0.02], color=ORANGE_P))
        self.play(Create(ax), FadeIn(ax_lab), FadeIn(f_labels))

        self.add(g_ice, g_car, p_ice, p_car, va_ice, va_car, friction)
        self.play(clock.animate.set_value(T_END), run_time=T_END, rate_func=linear)

        verdict = VGroup(
            Text("no net force → keeps moving forever", font_size=24, color=BLUE_M),
            Text("friction = net force → it slows down", font_size=24, color=ORANGE_P),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(DOWN, buff=0.25)
        self.play(FadeIn(verdict, shift=UP * 0.2))
        self.wait(2)
