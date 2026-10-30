"""
12 · Code — Recursion and the call stack
fact(4) calls fact(3), which calls fact(2)… Each call is a frame pushed on
the stack; when the base case returns, frames pop one by one and the
partial results flow back down.

Manim ideas: a stack of frames built and removed with FadeIn/FadeOut(shift),
Transform to update a frame's text, a highlight cursor over source code.

Render:
    manim -pqm scenes/12_recursion_stack.py RecursionStack
"""
from manim import *

PURPLE_C = "#B57BFF"
YELLOW_M = "#FFD166"
PINK_B = "#FF5C8A"
GREEN_B = "#3DDC97"
GREY_M = "#8A93A6"

CODE = [
    "def fact(n):",
    "    if n == 0:",
    "        return 1",
    "    return n * fact(n - 1)",
]
N = 4


def code_block(lines, font_size=26):
    char_w = Text("M" * 20, font="Monospace", font_size=font_size).width / 20
    group = VGroup()
    for k, line in enumerate(lines):
        indent = len(line) - len(line.lstrip(" "))
        txt = Text(line.strip(), font="Monospace", font_size=font_size,
                   t2c={"def": PINK_B, "if": PINK_B, "return": PINK_B, "fact": PURPLE_C})
        txt.move_to(ORIGIN, aligned_edge=LEFT).shift(RIGHT * indent * char_w + DOWN * k * 0.55)
        group.add(txt)
    return group


class RecursionStack(Scene):
    def construct(self):
        title = Text("Recursion — watching the call stack", font_size=38).to_edge(UP, buff=0.3)
        self.play(Write(title))

        code = code_block(CODE).to_edge(LEFT, buff=0.8).shift(UP * 0.8)
        panel = SurroundingRectangle(code, color=GREY_M, fill_color="#151A28", fill_opacity=1, buff=0.3, corner_radius=0.15)
        self.play(FadeIn(panel), Write(code))

        def cursor_on(line):
            return SurroundingRectangle(code[line], color=YELLOW_M, fill_color=YELLOW_M, fill_opacity=0.15,
                                        buff=0.07, stroke_width=1.5)

        cursor = cursor_on(0)
        call = Text(f"fact({N}) = ?", font="Monospace", font_size=32, color=YELLOW_M).next_to(panel, DOWN, buff=0.6)
        self.play(FadeIn(cursor), Write(call))

        stack_label = Text("call stack", font_size=24, color=GREY_M).move_to(RIGHT * 3.6 + DOWN * 3.5)
        base = Line(RIGHT * 1.6 + DOWN * 3.15, RIGHT * 5.6 + DOWN * 3.15, color=GREY_M, stroke_width=4)
        self.play(Create(base), FadeIn(stack_label))

        def frame(n, text, color):
            box = RoundedRectangle(width=4.0, height=0.8, corner_radius=0.12, stroke_color=color,
                                   fill_color=color, fill_opacity=0.15)
            label = Text(text, font="Monospace", font_size=24).move_to(box)
            return VGroup(box, label).move_to(RIGHT * 3.6 + DOWN * (2.7 - 0.9 * (N - n)))

        frames = {}
        for n in range(N, -1, -1):           # calls going down
            f = frame(n, f"fact({n})   n = {n}", PURPLE_C)
            frames[n] = f
            self.play(FadeIn(f, shift=DOWN * 0.4), cursor.animate.become(cursor_on(1)), run_time=0.6)
            if n > 0:
                pending = Text(f"{n} * fact({n - 1})", font="Monospace", font_size=24).move_to(f)
                self.play(cursor.animate.become(cursor_on(3)), Transform(f[1], pending), run_time=0.6)

        # base case
        self.play(cursor.animate.become(cursor_on(2)),
                  Transform(frames[0][1], Text("returns 1", font="Monospace", font_size=24, color=GREEN_B).move_to(frames[0])),
                  frames[0][0].animate.set_stroke(GREEN_B).set_fill(GREEN_B, 0.2))
        self.wait(0.4)

        value = 1
        for n in range(1, N + 1):            # returns going up the chain
            prev = frames[n - 1]
            ret = Text(str(value), font="Monospace", font_size=28, color=GREEN_B).move_to(prev)
            self.play(FadeOut(prev, shift=UP * 0.4), FadeIn(ret), run_time=0.5)
            new_value = n * value
            done = Text(f"{n} * {value} = {new_value}", font="Monospace", font_size=24, color=GREEN_B).move_to(frames[n])
            self.play(ret.animate.move_to(frames[n][1].get_right() + LEFT * 0.3).set_opacity(0),
                      Transform(frames[n][1], done),
                      frames[n][0].animate.set_stroke(GREEN_B).set_fill(GREEN_B, 0.2),
                      cursor.animate.become(cursor_on(3)), run_time=0.8)
            self.remove(ret)
            value = new_value

        result = Text(f"fact({N}) = {value}", font="Monospace", font_size=36, color=GREEN_B).move_to(call)
        self.play(FadeOut(frames[N], shift=UP * 0.4), Transform(call, result))
        tip = Text("no base case → the stack never stops growing (RecursionError)", font_size=22, color=PINK_B)
        tip.next_to(call, DOWN, buff=0.4).align_to(panel, LEFT)
        self.play(Circumscribe(call, color=GREEN_B), FadeIn(tip))
        self.wait(2)
