"""
Exercise 2 — Your own concept  (≈ 30 min)

1. Pick ONE idea from your own course that students find hard because it *changes*
   (a limit, an orbit, enzyme kinetics, a sorting step, a phylogenetic tree…).
2. Storyboard it on paper in 3–6 beats. One beat ≈ one self.play(...).
3. Build it below, beat by beat. Render often with -ql.

    manim -pql exercises/ex2_your_concept.py MyConcept

Tips
 - Start from the closest gallery scene in scenes/ and copy what you need.
 - Keep a consistent colour for each quantity.
 - Add self.wait() after every important change: students need time to look.
"""
from manim import *


class MyConcept(Scene):
    def construct(self):
        title = Text("My concept", font_size=44).to_edge(UP)
        self.play(Write(title))

        # Beat 1: set the stage (axes, a diagram, a sequence...)

        # Beat 2: introduce the key object

        # Beat 3: make it change (Transform, .animate, ValueTracker...)

        # Beat 4: highlight the take-away (Indicate, Circumscribe, a final equation)

        self.wait(2)
