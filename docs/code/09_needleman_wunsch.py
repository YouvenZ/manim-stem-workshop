"""
09 · Bioinformatics — Global sequence alignment (Needleman-Wunsch)
The dynamic-programming matrix is filled cell by cell: each value is the
best of "diagonal + match/mismatch", "from above + gap", "from the left + gap".
The traceback path then spells out the optimal alignment.

Manim ideas: grids of Squares + Text built from a NumPy matrix,
colour scales with interpolate_color, Arrows for the recurrence,
highlighting a path with SurroundingRectangle.

Render:
    manim -pqm scenes/09_needleman_wunsch.py NeedlemanWunsch
"""
from manim import *

PINK_B = "#FF5C8A"
YELLOW_M = "#FFD166"
GREEN_B = "#3DDC97"
GREY_M = "#8A93A6"

TOP = "GATTACA"     # columns
SIDE = "GCATGCA"    # rows
MATCH, MISMATCH, GAP = 1, -1, -1


def score_matrix(a, b):
    m, n = len(b), len(a)
    F = np.zeros((m + 1, n + 1), dtype=int)
    F[0, :] = GAP * np.arange(n + 1)
    F[:, 0] = GAP * np.arange(m + 1)
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            s = MATCH if b[i - 1] == a[j - 1] else MISMATCH
            F[i, j] = max(F[i - 1, j - 1] + s, F[i - 1, j] + GAP, F[i, j - 1] + GAP)
    return F


def traceback(F, a, b):
    i, j = len(b), len(a)
    path, top, left = [(i, j)], "", ""
    while i > 0 or j > 0:
        s = MATCH if i > 0 and j > 0 and b[i - 1] == a[j - 1] else MISMATCH
        if i > 0 and j > 0 and F[i, j] == F[i - 1, j - 1] + s:
            top, left, i, j = a[j - 1] + top, b[i - 1] + left, i - 1, j - 1
        elif i > 0 and F[i, j] == F[i - 1, j] + GAP:
            top, left, i = "-" + top, b[i - 1] + left, i - 1
        else:
            top, left, j = a[j - 1] + top, "-" + left, j - 1
        path.append((i, j))
    return path, top, left


class NeedlemanWunsch(Scene):
    def construct(self):
        F = score_matrix(TOP, SIDE)
        path, al_top, al_left = traceback(F, TOP, SIDE)
        m, n = F.shape

        title = Text("Global alignment — Needleman–Wunsch", font_size=38).to_edge(UP, buff=0.25)
        self.play(Write(title))

        size = 0.6
        grid_origin = np.array([-6.0, 2.3, 0])     # centre of the top-left header cell

        def centre(i, j):              # matrix cell (i, j); headers at i = -1 / j = -1
            return grid_origin + np.array([(j + 1) * size, -(i + 1) * size, 0])

        lo, hi = F.min(), F.max()

        def cell_color(v):
            return interpolate_color(ManimColor("#1B2238"), ManimColor("#2E8F8A"), (v - lo) / (hi - lo))

        cells = {}
        for i in range(m):
            for j in range(n):
                sq = Square(size, stroke_color=GREY_M, stroke_width=1,
                            fill_color=cell_color(F[i, j]), fill_opacity=1).move_to(centre(i, j))
                txt = Text(str(F[i, j]), font_size=20).move_to(sq)
                cells[i, j] = VGroup(sq, txt)

        headers = VGroup()
        for j, ch in enumerate("-" + TOP):
            headers.add(Text(ch, font="Monospace", font_size=26, color=YELLOW_M, weight=BOLD).move_to(centre(-1, j)))
        for i, ch in enumerate("-" + SIDE):
            headers.add(Text(ch, font="Monospace", font_size=26, color=PINK_B, weight=BOLD).move_to(centre(i, -1)))

        # Right-hand side: the rules.
        rules = VGroup(
            MathTex(r"F(i,j)=\max\begin{cases}F(i-1,j-1)+s(x_i,y_j)\\ F(i-1,j)+g\\ F(i,j-1)+g\end{cases}",
                    font_size=32),
            Text(f"match +{MATCH}   mismatch {MISMATCH}   gap {GAP}", font_size=22, color=GREY_B),
        ).arrange(DOWN, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 1.2)

        self.play(FadeIn(headers), Write(rules))

        # First row and column: gap penalties.
        border = [cells[0, j] for j in range(n)] + [cells[i, 0] for i in range(1, m)]
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in border], lag_ratio=0.06))

        # Explain one cell in detail.
        self.play(Indicate(headers[1]), Indicate(headers[n + 1]))
        target = Square(size, color=WHITE, stroke_width=4).move_to(centre(1, 1))
        arrows = VGroup(
            Arrow(centre(0, 0), centre(1, 1), buff=0.18, color=GREEN_B, stroke_width=4),
            Arrow(centre(0, 1), centre(1, 1), buff=0.18, color=GREY_B, stroke_width=4),
            Arrow(centre(1, 0), centre(1, 1), buff=0.18, color=GREY_B, stroke_width=4),
        )
        calc = MathTex(r"\max(0{+}1,\;-1{-}1,\;-1{-}1) = 1", font_size=32, color=GREEN_B)
        calc.next_to(rules, DOWN, buff=0.5)
        self.play(Create(target), LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.3), Write(calc))
        self.play(FadeIn(cells[1, 1]))
        self.wait(0.5)
        self.play(FadeOut(target), FadeOut(arrows), FadeOut(calc))

        # Fill the rest, row by row.
        rest = [cells[i, j] for i in range(1, m) for j in range(1, n) if (i, j) != (1, 1)]
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in rest], lag_ratio=0.08), run_time=5)

        # Traceback from the bottom-right corner.
        final = SurroundingRectangle(cells[m - 1, n - 1], color=YELLOW_M, buff=0)
        score = Text(f"optimal score = {F[m - 1, n - 1]}", font_size=26, color=YELLOW_M)
        score.next_to(rules, DOWN, buff=0.5)
        self.play(Create(final), Write(score))
        marks = VGroup(*[Square(size * 0.9, color=YELLOW_M, stroke_width=4).move_to(centre(i, j)) for i, j in path])
        links = VGroup(*[Line(centre(*p), centre(*q), color=YELLOW_M, stroke_width=5)
                         for p, q in zip(path, path[1:])])
        self.play(LaggedStart(*[AnimationGroup(Create(mk), Create(ln)) for mk, ln in zip(marks, links)],
                              lag_ratio=0.5), run_time=3)

        # The resulting alignment.
        def row(s, color):
            return VGroup(*[Text(c, font="Monospace", font_size=36, color=color, weight=BOLD) for c in s])

        r1, r2 = row(al_top, YELLOW_M), row(al_left, PINK_B)
        bars = VGroup()
        for k in range(len(al_top)):
            r1[k].move_to(np.array([1.2 + k * 0.5, -1.6, 0]))
            r2[k].move_to(np.array([1.2 + k * 0.5, -2.6, 0]))
            sym = "|" if al_top[k] == al_left[k] else ("·" if "-" not in (al_top[k], al_left[k]) else " ")
            bars.add(Text(sym, font="Monospace", font_size=30, color=GREEN_B).move_to(np.array([1.2 + k * 0.5, -2.1, 0])))
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in r1], lag_ratio=0.1),
                  LaggedStart(*[FadeIn(c, shift=DOWN * 0.2) for c in r2], lag_ratio=0.1),
                  run_time=2)
        self.play(FadeIn(bars))
        self.wait(2)
