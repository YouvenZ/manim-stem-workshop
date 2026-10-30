"""
14 · Code — How a hash table (Python dict) finds things fast
Each key goes through a hash function that turns it into a bucket number.
Two keys landing in the same bucket collide and are chained; a lookup only
scans one short chain instead of the whole table.

Manim ideas: a "machine" box the keys travel through, MathTex-free formulas
with Text, chains that grow to the right, Indicate for the lookup scan.

Render:
    manim -pqm scenes/14_hash_table.py HashTable
"""
from manim import *

PURPLE_C = "#B57BFF"
YELLOW_M = "#FFD166"
PINK_B = "#FF5C8A"
GREEN_B = "#3DDC97"
BLUE_M = "#4F9DFF"
GREY_M = "#8A93A6"

KEYS = ["cat", "dog", "owl", "bee", "ant", "fox", "yak"]
SIZE = 7
LOOKUP = "fox"


def h(key):
    return sum(ord(c) for c in key)


class HashTable(Scene):
    def construct(self):
        title = Text("Hash tables — jump straight to the right bucket", font_size=36).to_edge(UP, buff=0.3)
        rule = Text(f"bucket = sum of character codes % {SIZE}", font="Monospace", font_size=22, color=PURPLE_C)
        rule.next_to(title, DOWN, buff=0.2)
        self.play(Write(title), FadeIn(rule))

        machine = VGroup(RoundedRectangle(width=2.2, height=1.3, corner_radius=0.2, color=PURPLE_C,
                                          fill_color=PURPLE_C, fill_opacity=0.15),
                         Text("hash()", font="Monospace", font_size=30, color=PURPLE_C)).move_to(LEFT * 3.6 + DOWN * 0.2)
        self.play(FadeIn(machine, scale=0.8))

        top_y, step = 2.0, 0.68
        buckets = VGroup()
        for i in range(SIZE):
            box = Rectangle(width=0.8, height=0.58, color=GREY_M, fill_color="#151A28", fill_opacity=1)
            num = Text(str(i), font="Monospace", font_size=22, color=GREY_M).move_to(box)
            buckets.add(VGroup(box, num).move_to(np.array([0.3, top_y - i * step, 0])))
        self.play(LaggedStart(*[FadeIn(b, shift=LEFT * 0.3) for b in buckets], lag_ratio=0.07))

        chains = {i: VGroup() for i in range(SIZE)}
        calc_pos = machine.get_bottom() + DOWN * 0.7
        for k, key in enumerate(KEYS):
            idx = h(key) % SIZE
            item = VGroup(RoundedRectangle(width=1.0, height=0.5, corner_radius=0.1, color=BLUE_M,
                                           fill_color=BLUE_M, fill_opacity=0.25),
                          Text(key, font="Monospace", font_size=22))
            item.move_to(LEFT * 6.2 + DOWN * 0.2)
            calc = Text(f"h('{key}') = {h(key)} % {SIZE} = {idx}", font="Monospace", font_size=22, color=YELLOW_M)
            calc.move_to(calc_pos)
            rt = 0.6 if k < 3 else 0.4
            self.play(FadeIn(item, shift=RIGHT * 0.3), run_time=rt)
            self.play(item.animate.move_to(machine), run_time=rt)
            self.play(FadeIn(calc), buckets[idx][0].animate.set_stroke(YELLOW_M), run_time=rt)

            collide = len(chains[idx]) > 0
            anchor = chains[idx][-1] if collide else buckets[idx]
            target = item.copy().next_to(anchor, RIGHT, buff=0.35)
            link = Arrow(anchor.get_right(), target.get_left(), buff=0.05, color=GREY_M, stroke_width=3,
                         max_tip_length_to_length_ratio=0.4)
            if collide:
                item[0].set_color(PINK_B).set_fill(PINK_B, 0.25)
            self.play(item.animate.move_to(target), GrowArrow(link), run_time=rt)
            if collide:
                note = Text("collision → chain it", font_size=22, color=PINK_B).next_to(item, RIGHT, buff=0.3)
                self.play(FadeIn(note), run_time=0.4)
                self.play(FadeOut(note), run_time=0.3)
            chains[idx].add(item)
            self.play(FadeOut(calc), buckets[idx][0].animate.set_stroke(GREY_M), run_time=0.3)

        # Lookup
        idx = h(LOOKUP) % SIZE
        query = Text(f"table['{LOOKUP}'] ?", font="Monospace", font_size=30, color=GREEN_B).move_to(machine.get_top() + UP * 0.8)
        calc = Text(f"h('{LOOKUP}') % {SIZE} = {idx}", font="Monospace", font_size=22, color=YELLOW_M).move_to(calc_pos)
        self.play(Write(query))
        self.play(FadeIn(calc), Indicate(buckets[idx], color=GREEN_B))
        for item in chains[idx]:
            hit = item[1].text == LOOKUP
            self.play(Indicate(item, color=GREEN_B if hit else GREY_B), run_time=0.6)
            if hit:
                self.play(item[0].animate.set_color(GREEN_B).set_fill(GREEN_B, 0.4))
                break
        summary = Text(f"checked {len(chains[idx])} items instead of {len(KEYS)}  →  O(1) on average",
                       font_size=26, color=GREEN_B).to_edge(DOWN, buff=0.35)
        self.play(Write(summary))
        self.wait(2)
