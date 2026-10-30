"""
02 · Mathematics — Fourier series: building a square wave from sines
Each new odd harmonic sin(kx)/k is drawn on its own, then added to the
partial sum S_N. The overshoot near the jumps never goes away (Gibbs).

Manim ideas: Axes.plot, DashedLine, Transform between graphs,
a live counter with Integer, LaggedStart.

Render:
    manim -pqm scenes/02_fourier_series.py FourierSquareWave
"""
from manim import *

BLUE_M = "#4F9DFF"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"


def partial_sum(x, n_max):
    ks = np.arange(1, n_max + 1, 2)
    return 4 / PI * np.sum(np.sin(np.outer(ks, np.atleast_1d(x))) / ks[:, None], axis=0)


class FourierSquareWave(Scene):
    def construct(self):
        title = Text("Fourier series — a square wave from sines", font_size=38).to_edge(UP)
        formula = MathTex(
            r"S_N(x)=\frac{4}{\pi}\sum_{k=1,3,5,\dots}^{N}\frac{\sin(kx)}{k}", font_size=40
        ).next_to(title, DOWN, buff=0.3)

        axes = Axes(
            x_range=[-PI, PI, PI / 2], y_range=[-1.5, 1.5, 0.5],
            x_length=11, y_length=4.3, tips=False,
            axis_config={"color": GREY_M, "stroke_width": 2},
        ).to_edge(DOWN, buff=0.5)
        x_labels = VGroup(*[
            MathTex(t, font_size=28).next_to(axes.c2p(v, 0), DOWN, buff=0.15)
            for t, v in [(r"-\pi", -PI), (r"\pi", PI)]
        ])

        target = VGroup(
            DashedLine(axes.c2p(-PI, -1), axes.c2p(0, -1)),
            DashedLine(axes.c2p(0, -1), axes.c2p(0, 1)),
            DashedLine(axes.c2p(0, 1), axes.c2p(PI, 1)),
        ).set_color(GREY_M)

        self.play(Write(title))
        self.play(Write(formula), Create(axes), FadeIn(x_labels))
        self.play(Create(target))

        n_label = VGroup(MathTex("N =", font_size=44), Integer(1, font_size=44).set_color(YELLOW_M))
        n_label.arrange(RIGHT).to_corner(UR).shift(DOWN * 1.4)
        self.play(FadeIn(n_label))

        def sum_graph(n):
            return axes.plot(lambda x: partial_sum(x, n)[0], x_range=[-PI, PI, 0.01],
                             color=BLUE_M, stroke_width=4)

        current = sum_graph(1)
        self.play(Create(current), run_time=1.5)

        # Slow, explained steps: show the new harmonic, then add it.
        for n in (3, 5, 7):
            harmonic = axes.plot(lambda x, n=n: 4 / PI * np.sin(n * x) / n,
                                 x_range=[-PI, PI, 0.01], color=YELLOW_M, stroke_width=2.5)
            term = MathTex(rf"+\frac{{4}}{{\pi}}\frac{{\sin({n}x)}}{{{n}}}", font_size=34, color=YELLOW_M)
            term.next_to(n_label, DOWN, buff=0.3)
            self.play(Create(harmonic), FadeIn(term, shift=DOWN * 0.2))
            self.play(
                Transform(current, sum_graph(n)),
                FadeOut(harmonic),
                FadeOut(term),
                n_label[1].animate.set_value(n),
            )

        # Then fast: many harmonics.
        for n in (11, 21, 41, 81):
            self.play(Transform(current, sum_graph(n)), n_label[1].animate.set_value(n), run_time=0.8)

        peak_x = PI / 81
        gibbs = Arrow(axes.c2p(0.8, 1.42), axes.c2p(peak_x + 0.05, 1.18), buff=0.05, color=YELLOW_M)
        gibbs_text = Text("Gibbs overshoot ≈ 9%", font_size=26, color=YELLOW_M).next_to(gibbs.get_start(), RIGHT)
        self.play(GrowArrow(gibbs), Write(gibbs_text))
        self.wait(2)
