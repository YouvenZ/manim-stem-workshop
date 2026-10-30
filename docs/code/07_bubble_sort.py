"""
07 · Code — Bubble sort, step by step, next to its source code
The highlighted line of Python follows the animation: compare, swap,
and the largest remaining value "bubbles" to the end of each pass.

Manim ideas: code as monospace Text lines (easy to highlight one line),
bars as Rectangles, .animate.set_x for swaps, counters with Integer.

Render:
    manim -pqm scenes/07_bubble_sort.py BubbleSort
"""
from manim import *

PURPLE_C = "#B57BFF"
YELLOW_M = "#FFD166"
PINK_B = "#FF5C8A"
GREEN_B = "#3DDC97"
GREY_M = "#8A93A6"

CODE = [
    "def bubble_sort(a):",
    "    n = len(a)",
    "    for i in range(n - 1):",
    "        for j in range(n - 1 - i):",
    "            if a[j] > a[j + 1]:",
    "                a[j], a[j+1] = a[j+1], a[j]",
    "    return a",
]
VALUES = [5, 2, 8, 1, 9, 3, 6, 4]


def code_block(lines, font_size=19):
    """Monospace lines that keep their indentation (leading spaces have no glyphs)."""
    char_w = Text("M" * 20, font="Monospace", font_size=font_size).width / 20
    group = VGroup()
    for k, line in enumerate(lines):
        indent = len(line) - len(line.lstrip(" "))
        txt = Text(line.strip(), font="Monospace", font_size=font_size,
                   t2c={"def": PINK_B, "for": PINK_B, "in": PINK_B, "if": PINK_B, "return": PINK_B,
                        "range": PURPLE_C, "len": PURPLE_C})
        txt.move_to(ORIGIN, aligned_edge=LEFT).shift(RIGHT * indent * char_w + DOWN * k * 0.42)
        group.add(txt)
    return group


class BubbleSort(Scene):
    def construct(self):
        title = Text("Bubble sort — algorithm meets animation", font_size=38).to_edge(UP, buff=0.3)
        self.play(Write(title))

        code = code_block(CODE).to_edge(RIGHT, buff=0.45).shift(UP * 0.8)
        panel = SurroundingRectangle(code, color=GREY_M, fill_color="#151A28", fill_opacity=1,
                                     buff=0.25, corner_radius=0.15)
        cursor = SurroundingRectangle(code[0], color=YELLOW_M, fill_color=YELLOW_M, fill_opacity=0.15,
                                      buff=0.06, stroke_width=1.5)
        self.play(FadeIn(panel), Write(code))
        self.play(FadeIn(cursor))

        def go_to(line):
            return cursor.animate.become(
                SurroundingRectangle(code[line], color=YELLOW_M, fill_color=YELLOW_M, fill_opacity=0.15,
                                     buff=0.06, stroke_width=1.5))

        # Bars
        base_y, spacing, x0 = -3.2, 0.66, -6.3
        xs = [x0 + i * spacing for i in range(len(VALUES))]

        def make_bar(v, x):
            rect = Rectangle(width=0.52, height=0.5 * v, fill_color=PURPLE_C, fill_opacity=0.9,
                             stroke_color=WHITE, stroke_width=1.5)
            rect.move_to([x, base_y + rect.height / 2, 0])
            label = Text(str(v), font_size=24).next_to(rect, UP, buff=0.1)
            return VGroup(rect, label)

        bars = [make_bar(v, x) for v, x in zip(VALUES, xs)]
        values = list(VALUES)
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1), go_to(1))

        counters = VGroup(
            VGroup(Text("comparisons", font_size=24), Integer(0, font_size=28, color=YELLOW_M)).arrange(RIGHT),
            VGroup(Text("swaps", font_size=24), Integer(0, font_size=28, color=PINK_B)).arrange(RIGHT),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(panel, DOWN, buff=0.4).align_to(panel, LEFT)
        self.play(FadeIn(counters))
        n_cmp = n_swp = 0

        n = len(values)
        for i in range(n - 1):
            self.play(go_to(2), run_time=0.25)
            for j in range(n - 1 - i):
                left, right = bars[j], bars[j + 1]
                n_cmp += 1
                self.play(go_to(4),
                          left[0].animate.set_fill(YELLOW_M), right[0].animate.set_fill(YELLOW_M),
                          counters[0][1].animate.set_value(n_cmp), run_time=0.3)
                if values[j] > values[j + 1]:
                    n_swp += 1
                    self.play(go_to(5),
                              left.animate(path_arc=PI / 2).set_x(xs[j + 1]), right.animate(path_arc=PI / 2).set_x(xs[j]),
                              counters[1][1].animate.set_value(n_swp),
                              run_time=0.45)
                    bars[j], bars[j + 1] = right, left
                    values[j], values[j + 1] = values[j + 1], values[j]
                self.play(bars[j][0].animate.set_fill(PURPLE_C), bars[j + 1][0].animate.set_fill(PURPLE_C),
                          run_time=0.12)
            # The last element of this pass is now in its final place.
            self.play(bars[n - 1 - i][0].animate.set_fill(GREEN_B), run_time=0.25)

        self.play(go_to(6), bars[0][0].animate.set_fill(GREEN_B))
        done = Text("sorted!  worst case O(n²) comparisons", font_size=26, color=GREEN_B)
        done.next_to(VGroup(*bars), UP, buff=0.5).align_to(bars[0], LEFT)
        self.play(Write(done))
        self.wait(2)
