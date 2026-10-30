"""
15 · Code — Big-O: a race between growth rates
Six cost curves grow together as n increases. Constant and logarithmic
stay flat, n² climbs, 2ⁿ leaves the screen almost immediately.

Manim ideas: one ValueTracker drives many always_redraw plots, labels that
ride on the tip of each curve, clipping a curve to the visible range.

Render:
    manim -pqm scenes/15_big_o_race.py BigORace
"""
from manim import *

GREY_M = "#8A93A6"
Y_MAX = 400

CURVES = [
    ("O(1)", lambda n: 1 + 0 * n, "#3DDC97"),
    ("O(log n)", lambda n: np.log2(np.maximum(n, 1)), "#4F9DFF"),
    ("O(n)", lambda n: n, "#FFD166"),
    ("O(n log n)", lambda n: n * np.log2(np.maximum(n, 1)), "#FF8A3D"),
    ("O(n²)", lambda n: n ** 2, "#FF5C8A"),
    ("O(2ⁿ)", lambda n: 2.0 ** n, "#B57BFF"),
]


class BigORace(Scene):
    def construct(self):
        title = Text("Big-O — how the cost grows with n", font_size=38).to_edge(UP, buff=0.3)
        self.play(Write(title))

        axes = Axes(x_range=[0, 20, 5], y_range=[0, Y_MAX, 100], x_length=6.6, y_length=5.4, tips=False,
                    axis_config={"color": GREY_M, "include_numbers": True, "font_size": 22})
        axes.to_edge(LEFT, buff=0.8).shift(DOWN * 0.4)
        labels = VGroup(Text("input size n", font_size=22).next_to(axes.x_axis, DOWN, buff=0.45),
                        Text("operations", font_size=22).next_to(axes.y_axis, UP, buff=0.15))
        self.play(Create(axes), FadeIn(labels))

        n = ValueTracker(0.5)

        def visible_end(f):
            # largest x <= n whose value stays on screen
            xs = np.linspace(0.5, n.get_value(), 400)
            ok = xs[f(xs) <= Y_MAX]
            return ok[-1] if len(ok) else 0.5

        plots, tags = VGroup(), VGroup()
        for name, f, color in CURVES:
            plots.add(always_redraw(lambda f=f, color=color: axes.plot(
                f, x_range=[0.5, max(visible_end(f), 0.51), 0.05], color=color, stroke_width=4)))
            tags.add(always_redraw(lambda f=f, color=color, name=name: Text(name, font_size=22, color=color).next_to(
                axes.c2p(visible_end(f), min(f(visible_end(f)), Y_MAX)), RIGHT, buff=0.1)))

        counter = always_redraw(lambda: Text(f"n = {n.get_value():.0f}", font="Monospace", font_size=30)
                                .to_corner(UR).shift(DOWN * 1.0 + LEFT * 0.5))
        self.add(plots, tags, counter)
        self.play(n.animate.set_value(20), run_time=9, rate_func=linear)
        self.wait()

        table = VGroup(
            Text("n = 1 000 000", font="Monospace", font_size=22, weight=BOLD),
            *[Text(t, font="Monospace", font_size=19, color=c) for t, c in (
                ("log n     ≈ 20", "#4F9DFF"),
                ("n         = 10⁶", "#FFD166"),
                ("n log n   ≈ 2·10⁷", "#FF8A3D"),
                ("n²        = 10¹²   (hours)", "#FF5C8A"),
                ("2ⁿ        → never", "#B57BFF"))],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        box = SurroundingRectangle(table, color=GREY_M, buff=0.25, corner_radius=0.12)
        VGroup(table, box).to_edge(RIGHT, buff=0.25).shift(DOWN * 0.6)
        self.play(FadeIn(box), LaggedStart(*[FadeIn(t, shift=LEFT * 0.2) for t in table], lag_ratio=0.2))
        self.wait(2)
