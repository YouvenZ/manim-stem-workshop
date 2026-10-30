"""
00 · Warm-up — your very first Manim scene
Manim ideas: Scene.construct, Mobjects (Circle, Square, Text), play(), Transform.

Render (preview, low quality):
    manim -pql scenes/00_hello_manim.py HelloManim
"""
from manim import *


class HelloManim(Scene):
    def construct(self):
        circle = Circle(radius=1.5, color="#4F9DFF", fill_opacity=0.5)
        square = Square(side_length=3, color="#FF8A3D", fill_opacity=0.5)
        label = Text("Hello, Manim!", font_size=48).next_to(circle, DOWN, buff=0.6)

        self.play(Create(circle), Write(label))       # draw the circle, write the text
        self.wait(0.5)
        self.play(Transform(circle, square))          # morph circle -> square
        self.play(circle.animate.rotate(PI / 4).set_color("#3DDC97"))
        self.play(Indicate(label, color="#FFD166"))
        self.wait()
