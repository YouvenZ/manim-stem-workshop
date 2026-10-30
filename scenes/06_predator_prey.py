"""
06 · Biology — Predator-prey dynamics (Lotka-Volterra)
Rabbits (prey) and foxes (predators) over time, and the same trajectory
as a closed orbit in the (prey, predator) plane. Both views share one clock.

Manim ideas: SciPy solve_ivp, two linked Axes, partial curves with
pointwise_become_partial, always_redraw dots and dashed guides.

Render:
    manim -pqm scenes/06_predator_prey.py PredatorPrey
"""
from manim import *
from scipy.integrate import solve_ivp

GREEN_B = "#3DDC97"
PINK_B = "#FF5C8A"
GREY_M = "#8A93A6"

ALPHA, BETA, DELTA, GAMMA = 1.1, 0.4, 0.1, 0.4
T_END = 40


def lotka_volterra(t, z):
    x, y = z
    return [ALPHA * x - BETA * x * y, DELTA * x * y - GAMMA * y]


class PredatorPrey(Scene):
    def construct(self):
        ts = np.linspace(0, T_END, 1200)
        sol = solve_ivp(lotka_volterra, (0, T_END), [10, 5], t_eval=ts, rtol=1e-9, atol=1e-9)
        prey, pred = sol.y
        top = float(np.ceil(max(prey.max(), pred.max()) / 10) * 10)

        title = Text("Predator–prey: Lotka–Volterra", font_size=38).to_edge(UP, buff=0.3)
        eqs = MathTex(
            r"\dot x = \alpha x - \beta xy", r"\qquad", r"\dot y = \delta xy - \gamma y", font_size=36
        ).next_to(title, DOWN, buff=0.25)
        eqs[0].set_color(GREEN_B)
        eqs[2].set_color(PINK_B)

        ax_t = Axes(x_range=[0, T_END, 10], y_range=[0, top, 5], x_length=6.2, y_length=4.2,
                    tips=False, axis_config={"color": GREY_M, "include_numbers": True, "font_size": 20})
        ax_p = Axes(x_range=[0, top, 5], y_range=[0, top / 2, 2], x_length=4.6, y_length=4.2,
                    tips=False, axis_config={"color": GREY_M, "include_numbers": True, "font_size": 20})
        VGroup(ax_t, ax_p).arrange(RIGHT, buff=1.2).to_edge(DOWN, buff=0.6).shift(RIGHT * 0.35)
        lab_t = VGroup(Text("time", font_size=22).next_to(ax_t.x_axis, DOWN, buff=0.35),
                       Text("population", font_size=22).rotate(PI / 2).next_to(ax_t.y_axis, LEFT, buff=0.4))
        lab_p = VGroup(Text("prey x", font_size=22, color=GREEN_B).next_to(ax_p.x_axis, DOWN, buff=0.35),
                       Text("predators y", font_size=22, color=PINK_B).rotate(PI / 2).next_to(ax_p.y_axis, LEFT, buff=0.4))

        def curve(ax, xs, ys, color, width=4):
            return VMobject(color=color, stroke_width=width).set_points_as_corners(
                [ax.c2p(x, y) for x, y in zip(xs, ys)])

        full_prey = curve(ax_t, ts, prey, GREEN_B)
        full_pred = curve(ax_t, ts, pred, PINK_B)
        full_orbit = curve(ax_p, prey, pred, "#FFD166")

        clock = ValueTracker(0.001)

        def partial(full):
            return always_redraw(lambda: full.copy().pointwise_become_partial(full, 0, clock.get_value() / T_END))

        def now(arr):
            return np.interp(clock.get_value(), ts, arr)

        dots = always_redraw(lambda: VGroup(
            Dot(ax_t.c2p(clock.get_value(), now(prey)), color=GREEN_B),
            Dot(ax_t.c2p(clock.get_value(), now(pred)), color=PINK_B),
            Dot(ax_p.c2p(now(prey), now(pred)), color=WHITE),
            DashedLine(ax_p.c2p(now(prey), 0), ax_p.c2p(now(prey), now(pred)), color=GREEN_B, stroke_width=2),
            DashedLine(ax_p.c2p(0, now(pred)), ax_p.c2p(now(prey), now(pred)), color=PINK_B, stroke_width=2),
        ))

        self.play(Write(title))
        self.play(Write(eqs))
        self.play(Create(ax_t), Create(ax_p), FadeIn(lab_t), FadeIn(lab_p))
        self.add(partial(full_prey), partial(full_pred), partial(full_orbit), dots)
        self.play(clock.animate.set_value(T_END), run_time=14, rate_func=linear)

        note = Text("closed orbit → populations cycle forever", font_size=24, color="#FFD166")
        note.next_to(eqs, DOWN, buff=0.3)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
