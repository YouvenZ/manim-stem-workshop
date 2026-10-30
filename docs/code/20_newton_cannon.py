"""
20 · Physics — Newton's cannon: from falling to orbiting
A cannon on a very tall mountain fires horizontally, faster each time.
The same inverse-square gravity bends every path: slow balls fall back,
at the circular speed the ball "falls around" the Earth, faster gives an ellipse.

Manim ideas: numerical orbits (velocity Verlet), paths drawn with Create +
MoveAlongPath, a gravity arrow that always points to the centre.

Render:
    manim -pqm scenes/20_newton_cannon.py NewtonCannon
"""
from manim import *

BLUE_M = "#4F9DFF"
GREEN_B = "#3DDC97"
YELLOW_M = "#FFD166"
PINK_B = "#FF5C8A"
ORANGE_P = "#FF8A3D"
PURPLE_C = "#B57BFF"
GREY_M = "#8A93A6"

GM = 4.0
R_EARTH = 1.45
CENTRE = np.array([-2.2, -0.3, 0])
R0 = 1.75                                  # launch radius (mountain top)
V_CIRC = np.sqrt(GM / R0)
SHOTS = [(0.45, PINK_B), (0.7, ORANGE_P), (0.88, YELLOW_M), (1.0, GREEN_B), (1.15, PURPLE_C)]


def trajectory(v0, dt=0.002, t_max=20.0):
    r = np.array([0.0, R0])
    v = np.array([v0, 0.0])
    a = -GM * r / np.linalg.norm(r) ** 3
    pts, t, swept = [r.copy()], 0.0, 0.0
    while t < t_max:
        r_old = r.copy()
        r = r + v * dt + 0.5 * a * dt ** 2
        a_new = -GM * r / np.linalg.norm(r) ** 3
        v = v + 0.5 * (a + a_new) * dt
        a, t = a_new, t + dt
        swept += abs(np.arctan2(r_old[0] * r[1] - r_old[1] * r[0], r_old @ r))
        pts.append(r.copy())
        if np.linalg.norm(r) < R_EARTH or swept >= 2 * PI:
            break
    return np.array(pts), t


class NewtonCannon(Scene):
    def construct(self):
        title = Text("Newton's cannon — why the Moon doesn't fall", font_size=36).to_edge(UP, buff=0.25)
        self.play(Write(title))

        earth = Circle(R_EARTH, color=BLUE_M, fill_color="#123A6B", fill_opacity=1, stroke_width=3).move_to(CENTRE)
        land = VGroup(*[Ellipse(width=w, height=h, color=GREEN_B, fill_color=GREEN_B, fill_opacity=0.5, stroke_width=0)
                        .move_to(CENTRE + np.array(p)) for w, h, p in
                        ((0.9, 0.5, (-0.5, 0.4, 0)), (0.7, 0.9, (0.55, -0.35, 0)), (0.5, 0.3, (-0.4, -0.8, 0)))])
        mountain = Polygon(CENTRE + UP * (R_EARTH - 0.1) + LEFT * 0.35, CENTRE + UP * R0,
                           CENTRE + UP * (R_EARTH - 0.1) + RIGHT * 0.35,
                           color=GREY_B, fill_color=GREY_M, fill_opacity=1, stroke_width=2)
        cannon = Rectangle(width=0.32, height=0.1, color=WHITE, fill_color=GREY_B, fill_opacity=1)
        cannon.move_to(CENTRE + UP * R0 + RIGHT * 0.12)
        self.play(GrowFromCenter(earth), FadeIn(land), FadeIn(mountain), FadeIn(cannon))

        law = MathTex(r"F = \frac{G M m}{r^2}", font_size=44, color=YELLOW_M).to_corner(UR).shift(DOWN * 0.9 + LEFT * 0.4)
        circ = MathTex(r"v_{\text{circ}} = \sqrt{\frac{GM}{r}}", font_size=36, color=GREEN_B).next_to(law, DOWN, buff=0.4)
        self.play(Write(law))

        legend = VGroup()
        for k, (factor, color) in enumerate(SHOTS):
            pts, t_flight = trajectory(factor * V_CIRC)
            path = VMobject(color=color, stroke_width=4).set_points_smoothly([CENTRE + np.array([x, y, 0]) for x, y in pts[::10]])
            ball = Dot(path.get_start(), radius=0.08, color=color)
            pull = always_redraw(lambda ball=ball: Arrow(
                ball.get_center(), ball.get_center() + 0.45 * normalize(CENTRE - ball.get_center()),
                buff=0, color=WHITE, stroke_width=3, max_tip_length_to_length_ratio=0.35))
            tag = Text(f"v = {factor:.2f} × v_circ", font_size=22, color=color)
            legend.add(tag)
            tag.next_to(circ if k == 0 else legend[k - 1], DOWN, buff=0.25 if k else 0.5).align_to(law, LEFT)
            if factor == 1.0:
                self.play(Write(circ))
            self.add(pull)
            self.play(FadeIn(tag), FadeIn(ball), run_time=0.4)
            self.play(Create(path), MoveAlongPath(ball, path), run_time=min(1.2 + 0.45 * t_flight, 6), rate_func=linear)
            self.remove(pull)
            if np.linalg.norm(pts[-1]) < R_EARTH:
                self.play(Flash(ball, color=color, flash_radius=0.25), run_time=0.5)

        moral = Text("an orbit is a fall that keeps missing the ground", font_size=26, color=YELLOW_M).to_edge(DOWN, buff=0.3)
        self.play(Write(moral))
        self.wait(2)
