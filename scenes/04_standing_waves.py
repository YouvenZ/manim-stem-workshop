"""
04 · Physics — Two travelling waves make a standing wave
y1 moves right, y2 moves left; their sum y1 + y2 = 2A sin(kx) cos(wt)
oscillates in place, with nodes that never move.

Manim ideas: several Axes stacked with VGroup.arrange, a ValueTracker for
time, always_redraw graphs, Dots placed with Axes.c2p.

Render:
    manim -pqm scenes/04_standing_waves.py StandingWaves
"""
from manim import *

ORANGE_P = "#FF8A3D"
BLUE_M = "#4F9DFF"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

K, W, A = 1.0, 2.0, 1.0
X_MAX = 4 * PI


class StandingWaves(Scene):
    def construct(self):
        t = ValueTracker(0)

        def make_axes(y_max, height):
            return Axes(x_range=[0, X_MAX, PI], y_range=[-y_max, y_max, y_max],
                        x_length=10.5, y_length=height, tips=False,
                        axis_config={"color": GREY_M, "stroke_width": 1.5})

        ax1, ax2, ax3 = make_axes(1.2, 1.3), make_axes(1.2, 1.3), make_axes(2.2, 2.3)
        panels = VGroup(ax1, ax2, ax3).arrange(DOWN, buff=0.45).to_edge(DOWN, buff=0.35).shift(RIGHT * 1.0)

        def wave(ax, f, color, width=3.5):
            return always_redraw(lambda: ax.plot(lambda x: f(x, t.get_value()),
                                                 x_range=[0, X_MAX, 0.05], color=color,
                                                 stroke_width=width))

        y1 = lambda x, s: A * np.sin(K * x - W * s)
        y2 = lambda x, s: A * np.sin(K * x + W * s)
        g1 = wave(ax1, y1, ORANGE_P)
        g2 = wave(ax2, y2, BLUE_M)
        g3 = wave(ax3, lambda x, s: y1(x, s) + y2(x, s), YELLOW_M, 5)

        names = VGroup(
            MathTex(r"y_1=\sin(kx-\omega t)", font_size=30, color=ORANGE_P),
            MathTex(r"y_2=\sin(kx+\omega t)", font_size=30, color=BLUE_M),
            MathTex(r"y_1+y_2", font_size=34, color=YELLOW_M),
        )
        for name, ax in zip(names, panels):
            name.next_to(ax, LEFT, buff=0.25)

        title = Text("Superposition → standing wave", font_size=38).to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.play(LaggedStart(*[Create(ax) for ax in panels], lag_ratio=0.2), Write(names))
        self.add(g1, g2)
        self.play(t.animate.set_value(3), run_time=4, rate_func=linear)

        self.add(g3)
        self.play(t.animate.set_value(7), run_time=5, rate_func=linear)

        nodes = VGroup(*[Dot(ax3.c2p(n * PI / K, 0), color=WHITE, radius=0.09) for n in range(5)])
        node_text = Text("nodes: never move", font_size=24).next_to(ax3, UP, buff=0.05).align_to(ax3, RIGHT)
        identity = MathTex(r"y_1+y_2 = 2A\,\sin(kx)\,\cos(\omega t)", font_size=34, color=YELLOW_M)
        identity.next_to(title, DOWN, buff=0.15)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in nodes], lag_ratio=0.15), FadeIn(node_text))
        self.play(Write(identity), t.animate.set_value(9), run_time=2.5, rate_func=linear)
        self.play(t.animate.set_value(13), run_time=5, rate_func=linear)
        self.wait()
