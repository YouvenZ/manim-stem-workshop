"""
01 · Mathematics — Pythagoras, a proof without words
The same (a+b)x(a+b) square holds four identical triangles in two ways:
the leftover area is c^2 in the first arrangement and a^2 + b^2 in the second.

Manim ideas: Polygon from coordinates, DrawBorderThenFill, .animate.shift,
MathTex split into coloured parts, TransformFromCopy, Circumscribe.

Render:
    manim -pqm scenes/01_pythagoras.py Pythagoras
"""
from manim import *

BLUE_M = "#4F9DFF"
YELLOW_M = "#FFD166"
PINK_M = "#FF5C8A"
GREEN_M = "#3DDC97"


class Pythagoras(Scene):
    def construct(self):
        a, b = 1.25, 2.15
        s = a + b
        centre = np.array([-3.2, -0.45, 0])
        origin = centre - np.array([s / 2, s / 2, 0])

        def P(x, y):
            return origin + np.array([x, y, 0])

        title = Text("Pythagoras — a proof without words", font_size=40).to_edge(UP)
        self.play(Write(title))

        frame = Square(side_length=s, color=WHITE, stroke_width=3).move_to(centre)
        style = dict(fill_color=BLUE_M, fill_opacity=0.85, stroke_color=WHITE, stroke_width=2)
        # Four copies of the right triangle with legs a and b.
        T1 = Polygon(P(0, 0), P(a, 0), P(0, b), **style)
        T2 = Polygon(P(a, 0), P(s, 0), P(s, a), **style)
        T3 = Polygon(P(s, s), P(s - a, s), P(s, a), **style)
        T4 = Polygon(P(0, s), P(0, s - a), P(s - a, s), **style)
        triangles = VGroup(T1, T2, T3, T4)

        self.play(Create(frame))
        self.play(LaggedStart(*[DrawBorderThenFill(t) for t in triangles], lag_ratio=0.3))

        hyp_dir = normalize(np.array([b, a, 0]))
        labels = VGroup(
            MathTex("a").next_to(Line(P(0, 0), P(a, 0)), DOWN, buff=0.12),
            MathTex("b").next_to(Line(P(0, 0), P(0, b)), LEFT, buff=0.12),
            MathTex("c").move_to(P(a / 2, b / 2) + 0.3 * hyp_dir),
        )
        self.play(Write(labels))

        inner = Polygon(P(a, 0), P(s, a), P(b, s), P(0, b),
                        fill_color=YELLOW_M, fill_opacity=0.55, stroke_width=0)
        c2 = MathTex("c^2", font_size=56).move_to(inner)
        self.play(FadeIn(inner), Write(c2))

        eq1 = MathTex(r"(a+b)^2", "=", "c^2", "+", r"4\cdot\tfrac12 ab").shift(RIGHT * 3 + UP * 1.2)
        eq1.set_color_by_tex("c^2", YELLOW_M)
        self.play(Write(eq1))
        self.wait()

        # Rearrange: pure translations of three triangles.
        self.play(FadeOut(inner), FadeOut(c2), FadeOut(labels))
        self.play(
            T4.animate.shift(RIGHT * a + DOWN * b),
            T1.animate.shift(UP * a),
            T3.animate.shift(LEFT * b),
            run_time=2.5,
        )

        sq_a = Square(side_length=a, fill_color=PINK_M, fill_opacity=0.6, stroke_width=0).move_to(P(a / 2, a / 2))
        sq_b = Square(side_length=b, fill_color=GREEN_M, fill_opacity=0.6, stroke_width=0).move_to(P(a + b / 2, a + b / 2))
        a2 = MathTex("a^2").move_to(sq_a)
        b2 = MathTex("b^2", font_size=56).move_to(sq_b)
        self.play(FadeIn(sq_a), FadeIn(sq_b), Write(a2), Write(b2))

        eq2 = MathTex(r"(a+b)^2", "=", "a^2", "+", "b^2", "+", r"4\cdot\tfrac12 ab").next_to(eq1, DOWN, buff=0.6)
        eq2.set_color_by_tex("a^2", PINK_M).set_color_by_tex("b^2", GREEN_M)
        self.play(Write(eq2))
        self.wait()

        final = MathTex("a^2", "+", "b^2", "=", "c^2", font_size=80).next_to(eq2, DOWN, buff=0.9)
        final[0].set_color(PINK_M)
        final[2].set_color(GREEN_M)
        final[4].set_color(YELLOW_M)
        self.play(TransformFromCopy(VGroup(eq1, eq2), final))
        self.play(Circumscribe(final, color=YELLOW_M))
        self.wait(2)
