"""
11 · Code — Binary search: halve the problem at every step
Three pointers (lo, mid, hi) move over a sorted list; every comparison
throws away half of what is left, so 11 items need at most 4 looks.

Manim ideas: cells built with VGroup + arrange, pointer mobjects moved with
.animate.next_to, dimming discarded cells, status text replaced with Transform.

Render:
    manim -pqm scenes/11_binary_search.py BinarySearch
"""
from manim import *

PURPLE_C = "#B57BFF"
YELLOW_M = "#FFD166"
PINK_B = "#FF5C8A"
GREEN_B = "#3DDC97"
BLUE_M = "#4F9DFF"
GREY_M = "#8A93A6"

ARR = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
TARGET = 72


def pointer(name, color, up=True):
    arrow = Arrow(DOWN * 0.7 if up else UP * 0.7, ORIGIN, buff=0, color=color, stroke_width=5,
                  max_tip_length_to_length_ratio=0.35)
    label = Text(name, font="Monospace", font_size=24, color=color, weight=BOLD)
    label.next_to(arrow, DOWN if up else UP, buff=0.08)
    return VGroup(arrow, label)


class BinarySearch(Scene):
    def construct(self):
        title = Text("Binary search — halve it every time", font_size=38).to_edge(UP, buff=0.3)
        goal = Text(f"find {TARGET} in a sorted list", font_size=28, color=YELLOW_M).next_to(title, DOWN, buff=0.2)
        self.play(Write(title), FadeIn(goal))

        cells = VGroup(*[
            VGroup(Square(0.9, stroke_color=GREY_M, fill_color="#151A28", fill_opacity=1),
                   Text(str(v), font_size=30))
            for v in ARR
        ]).arrange(RIGHT, buff=0.08).shift(UP * 0.2)
        for c in cells:
            c[1].move_to(c[0])
        idx = VGroup(*[Text(str(i), font_size=18, color=GREY_M).next_to(c, UP, buff=0.12)
                       for i, c in enumerate(cells)])
        self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in cells], lag_ratio=0.06), FadeIn(idx))

        code = Text("mid = (lo + hi) // 2", font="Monospace", font_size=28, color=PURPLE_C).to_edge(DOWN, buff=0.4)
        status_pos = DOWN * 1.75
        status = VectorizedPoint(status_pos)
        self.play(Write(code))

        lo_p, hi_p = pointer("lo", BLUE_M), pointer("hi", PINK_B)
        mid_p = pointer("mid", YELLOW_M, up=False)
        lo, hi = 0, len(ARR) - 1
        lo_p.next_to(cells[lo], DOWN, buff=0.1)
        hi_p.next_to(cells[hi], DOWN, buff=0.1)
        self.play(GrowFromEdge(lo_p, DOWN), GrowFromEdge(hi_p, DOWN))

        steps = 0
        while lo <= hi:
            mid = (lo + hi) // 2
            steps += 1
            mid_p.next_to(cells[mid], UP, buff=0.45)
            self.play(FadeIn(mid_p, shift=DOWN * 0.3) if steps == 1 else mid_p.animate.next_to(cells[mid], UP, buff=0.45),
                      cells[mid][0].animate.set_fill(YELLOW_M, 0.35))
            v = ARR[mid]
            if v == TARGET:
                msg = Text(f"{v} == {TARGET}  →  found at index {mid} in {steps} steps", font_size=28, color=GREEN_B)
                self.play(Transform(status, msg.move_to(status_pos)), cells[mid][0].animate.set_fill(GREEN_B, 0.6))
                self.play(Circumscribe(cells[mid], color=GREEN_B))
                break
            if v < TARGET:
                msg = Text(f"{v} < {TARGET}  →  lo = mid + 1", font_size=28)
                gone, lo = range(lo, mid + 1), mid + 1
                move = lo_p.animate.next_to(cells[lo], DOWN, buff=0.1)
            else:
                msg = Text(f"{v} > {TARGET}  →  hi = mid - 1", font_size=28)
                gone, hi = range(mid, hi + 1), mid - 1
                move = hi_p.animate.next_to(cells[hi], DOWN, buff=0.1)
            self.play(Transform(status, msg.move_to(status_pos)))
            self.play(move, *[cells[i].animate.set_opacity(0.2) for i in gone])
            self.wait(0.4)

        compare = Text(f"linear search: {ARR.index(TARGET) + 1} looks   ·   binary search: {steps} looks   ·   "
                       "1 000 000 items → ≤ 20 looks", font_size=22, color=GREY_B)
        compare.next_to(code, UP, buff=0.3)
        self.play(FadeIn(compare, shift=UP * 0.2))
        self.wait(2)
