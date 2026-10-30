"""
05 · Biology — The DNA double helix and base pairing
A 2D "fake 3D" helix: each backbone is cut into short segments whose
opacity follows their depth, so the strands appear to wind around each other.
Below, the complementary strand is read off with A-T and G-C pairing.

Manim ideas: building a frame procedurally inside always_redraw,
depth cueing with opacity, LaggedStart over letters.

Render:
    manim -pqm scenes/05_dna_double_helix.py DNAHelix
"""
from manim import *

BASE_COLORS = {"A": "#FF5C8A", "T": "#FFD166", "G": "#3DDC97", "C": "#4F9DFF"}
PAIR = {"A": "T", "T": "A", "G": "C", "C": "G"}
STRAND_1 = "#E8ECF4"
STRAND_2 = "#9AA4B8"

SEQ = "ATGCGTACCGATTAGC"
R = 1.15                # helix radius on screen
X0, X1 = -6.0, 6.0
Y_C = 0.9               # vertical centre of the helix


def build_helix(phase):
    xs = np.linspace(X0 + 0.4, X1 - 0.4, len(SEQ))
    k = 2 * PI / (10 * (xs[1] - xs[0]))       # ~10 base pairs per turn
    back, front = VGroup(), VGroup()

    # Backbones: short segments, opacity from depth (cos of the angle).
    us = np.linspace(X0, X1, 160)
    for offset, color in ((0, STRAND_1), (PI, STRAND_2)):
        ang = k * us + phase + offset
        pts = [np.array([u, Y_C + R * np.sin(a), 0]) for u, a in zip(us, ang)]
        for i in range(len(us) - 1):
            depth = np.cos(ang[i])
            seg = Line(pts[i], pts[i + 1], stroke_width=7 + 3 * depth, color=color,
                       stroke_opacity=0.35 + 0.65 * (depth + 1) / 2)
            (front if depth > 0 else back).add(seg)

    # Rungs: one half per base, coloured by base.
    rungs = VGroup()
    for x, base in zip(xs, SEQ):
        a = k * x + phase
        top = np.array([x, Y_C + R * np.sin(a), 0])
        bottom = np.array([x, Y_C - R * np.sin(a), 0])
        mid = np.array([x, Y_C, 0])
        op = 0.45 + 0.55 * abs(np.sin(a))
        rungs.add(Line(top, mid, color=BASE_COLORS[base], stroke_width=6, stroke_opacity=op),
                  Line(mid, bottom, color=BASE_COLORS[PAIR[base]], stroke_width=6, stroke_opacity=op))
    return VGroup(back, rungs, front)


def strand_row(seq, y, prime_left, prime_right):
    letters = VGroup(*[Text(b, font="Monospace", font_size=34, color=BASE_COLORS[b], weight=BOLD) for b in seq])
    letters.arrange(RIGHT, buff=0.22)
    left = Text(prime_left, font_size=24, color=GREY_B).next_to(letters, LEFT, buff=0.3)
    right = Text(prime_right, font_size=24, color=GREY_B).next_to(letters, RIGHT, buff=0.3)
    row = VGroup(left, letters, right).move_to(UP * y)
    return row, letters


class DNAHelix(Scene):
    def construct(self):
        phase = ValueTracker(0)
        helix = always_redraw(lambda: build_helix(phase.get_value()))

        title = Text("DNA — the double helix", font_size=40).to_edge(UP, buff=0.3)
        self.play(Write(title))
        self.play(FadeIn(helix), phase.animate.set_value(PI), run_time=3, rate_func=linear)

        top_row, top = strand_row(SEQ, -1.6, "5'", "3'")
        bot_row, bot = strand_row("".join(PAIR[b] for b in SEQ), -2.5, "3'", "5'")
        bot_row.align_to(top_row, LEFT)

        self.play(Write(top_row), phase.animate.set_value(2 * PI), run_time=2.5, rate_func=linear)

        rule = VGroup(
            Text("A ─ T", font_size=30, t2c={"A": BASE_COLORS["A"], "T": BASE_COLORS["T"]}),
            Text("G ─ C", font_size=30, t2c={"G": BASE_COLORS["G"], "C": BASE_COLORS["C"]}),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(DR, buff=0.6)
        rule_box = SurroundingRectangle(rule, color=GREY_B, buff=0.2, corner_radius=0.1)
        self.play(FadeIn(rule), Create(rule_box), phase.animate.set_value(2.6 * PI), run_time=1.5, rate_func=linear)

        # Read off the complementary strand, letter by letter.
        self.play(
            FadeIn(bot_row[0]), FadeIn(bot_row[2]),
            LaggedStart(*[TransformFromCopy(t, b) for t, b in zip(top, bot)], lag_ratio=0.12),
            phase.animate.set_value(4.6 * PI),
            run_time=5, rate_func=linear,
        )

        pair_box = SurroundingRectangle(VGroup(top[2], bot[2]), color=WHITE, buff=0.08)
        note = Text("hydrogen bonds: G≡C (3), A=T (2)", font_size=26).next_to(bot_row, DOWN, buff=0.3)
        self.play(Create(pair_box), Write(note), phase.animate.set_value(5.6 * PI), run_time=2, rate_func=linear)
        self.play(pair_box.animate.surround(VGroup(top[1], bot[1]), buff=0.08),
                  phase.animate.set_value(6.4 * PI), run_time=1.5, rate_func=linear)
        self.play(phase.animate.set_value(8 * PI), run_time=3, rate_func=linear)
