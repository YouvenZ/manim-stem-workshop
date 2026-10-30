"""
13 · Code — Breadth-first search on a graph
BFS explores a graph in "waves": first the start node, then all nodes at
distance 1, then distance 2… The FIFO queue at the bottom is what makes it so.

Manim ideas: nodes and edges from dictionaries, a queue as a VGroup that is
re-arranged after every push/pop, colour as state (unseen / queued / done).

Render:
    manim -pqm scenes/13_bfs_graph.py BFSGraph
"""
from collections import deque

from manim import *

PURPLE_C = "#B57BFF"
YELLOW_M = "#FFD166"
GREEN_B = "#3DDC97"
BLUE_M = "#4F9DFF"
GREY_M = "#8A93A6"
BG = "#0B0F19"

POS = {"A": (-5.0, 1.2), "B": (-3.0, 2.4), "C": (-3.0, 0.0), "D": (-0.8, 2.8),
       "E": (-0.8, 1.2), "F": (-0.8, -0.4), "G": (1.6, 2.2), "H": (1.6, 0.0)}
EDGES = [("A", "B"), ("A", "C"), ("B", "D"), ("B", "E"), ("C", "E"), ("C", "F"),
         ("D", "G"), ("E", "G"), ("E", "H"), ("F", "H")]
START = "A"


class BFSGraph(Scene):
    def construct(self):
        title = Text("Breadth-first search — exploring in waves", font_size=38).to_edge(UP, buff=0.25)
        self.play(Write(title))

        adj = {k: [] for k in POS}
        for a, b in EDGES:
            adj[a].append(b)
            adj[b].append(a)

        offset = np.array([0.4, -0.5, 0])
        p = {k: np.array([x, y, 0]) + offset for k, (x, y) in POS.items()}
        edges = {frozenset(e): Line(p[e[0]], p[e[1]], color=GREY_M, stroke_width=3) for e in EDGES}
        nodes = {k: VGroup(Circle(0.36, color=GREY_M, fill_color="#151A28", fill_opacity=1, stroke_width=3),
                           Text(k, font_size=28, weight=BOLD)).move_to(p[k]) for k in POS}
        self.play(*[Create(e) for e in edges.values()],
                  LaggedStart(*[GrowFromCenter(n) for n in nodes.values()], lag_ratio=0.08))

        legend = VGroup(*[
            VGroup(Dot(color=c, radius=0.1), Text(t, font_size=20)).arrange(RIGHT, buff=0.15)
            for c, t in ((GREY_M, "unseen"), (YELLOW_M, "in queue"), (PURPLE_C, "visiting"), (GREEN_B, "done"))
        ]).arrange(DOWN, aligned_edge=LEFT).to_corner(UR).shift(DOWN * 0.9)
        code = Text("queue = deque([start])\nwhile queue:\n    u = queue.popleft()\n    for v in adj[u]:\n"
                    "        if v not in seen:\n            seen.add(v); queue.append(v)",
                    font="Monospace", font_size=16, line_spacing=0.8).next_to(legend, DOWN, buff=0.5).to_edge(RIGHT, buff=0.25)
        self.play(FadeIn(legend), FadeIn(code))

        q_label = Text("queue (FIFO)", font_size=22, color=GREY_M).to_corner(DL).shift(UP * 0.55 + RIGHT * 0.1)
        q_items = VGroup()

        def q_box(k):
            return VGroup(RoundedRectangle(width=0.7, height=0.7, corner_radius=0.1, color=YELLOW_M,
                                           fill_color=YELLOW_M, fill_opacity=0.2),
                          Text(k, font_size=26, weight=BOLD))

        def q_layout():
            target = q_items.copy().arrange(RIGHT, buff=0.12).next_to(q_label, RIGHT, buff=0.4)
            return [m.animate.move_to(t) for m, t in zip(q_items, target)]

        def set_state(k, color):
            return nodes[k][0].animate.set_stroke(color).set_fill(color, 0.35)

        dist = {START: 0}
        dist_labels = VGroup()

        def dist_tag(k):
            t = Text(f"d={dist[k]}", font_size=20, color=YELLOW_M).next_to(nodes[k], DOWN, buff=0.08)
            dist_labels.add(t)
            return FadeIn(t, scale=0.5)

        self.play(FadeIn(q_label))
        first = q_box(START).next_to(q_label, RIGHT, buff=0.4)
        q_items.add(first)
        self.play(set_state(START, YELLOW_M), FadeIn(first, shift=UP * 0.3), dist_tag(START))

        queue, order = deque([START]), []
        while queue:
            u = queue.popleft()
            order.append(u)
            out = q_items[0]
            q_items.remove(out)
            anims = [FadeOut(out, shift=LEFT * 0.4), set_state(u, PURPLE_C)] + q_layout()
            self.play(*anims, run_time=0.6)
            for v in adj[u]:
                e = edges[frozenset((u, v))]
                if v in dist:
                    continue
                dist[v] = dist[u] + 1
                queue.append(v)
                box = q_box(v)
                box.next_to(q_items[-1] if len(q_items) else q_label, RIGHT, buff=0.12 if len(q_items) else 0.4)
                q_items.add(box)
                self.play(e.animate.set_color(YELLOW_M).set_stroke(width=6),
                          set_state(v, YELLOW_M), FadeIn(box, shift=UP * 0.3), dist_tag(v), run_time=0.55)
            self.play(set_state(u, GREEN_B), run_time=0.3)

        visit = Text("visit order: " + " → ".join(order), font="Monospace", font_size=24, color=GREEN_B)
        visit.to_edge(DOWN, buff=0.35).align_to(q_label, LEFT)
        self.play(Write(visit))
        self.play(LaggedStart(*[Indicate(t, color=WHITE) for t in dist_labels], lag_ratio=0.1))
        self.wait(2)
