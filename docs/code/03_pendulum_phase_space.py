"""
03 · Physics — A damped pendulum and its phase portrait
The pendulum (left) and its state (theta, omega) in phase space (right) are
driven by the same clock, so students see that one point in phase space
*is* one configuration of the pendulum. Damping makes the orbit spiral in.

Manim ideas: numerical ODE solved in NumPy, ValueTracker as a clock,
always_redraw, TracedPath.

Render:
    manim -pqm scenes/03_pendulum_phase_space.py PendulumPhaseSpace
"""
from manim import *

ORANGE_P = "#FF8A3D"
YELLOW_M = "#FFD166"
GREY_M = "#8A93A6"

G_OVER_L = 9.81      # g / L  with L = 1 m
GAMMA = 0.25         # damping coefficient
T_END = 14.0


def simulate(theta0=2.0, omega0=0.0, dt=1 / 600):
    """RK4 integration of  theta'' = -(g/L) sin(theta) - gamma * theta'."""
    def f(state):
        th, om = state
        return np.array([om, -G_OVER_L * np.sin(th) - GAMMA * om])

    n = int(T_END / dt) + 1
    ts = np.linspace(0, T_END, n)
    out = np.empty((n, 2))
    y = np.array([theta0, omega0])
    for i in range(n):
        out[i] = y
        k1 = f(y)
        k2 = f(y + dt / 2 * k1)
        k3 = f(y + dt / 2 * k2)
        k4 = f(y + dt * k3)
        y = y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return ts, out[:, 0], out[:, 1]


class PendulumPhaseSpace(Scene):
    def construct(self):
        ts, thetas, omegas = simulate()
        clock = ValueTracker(0)

        def theta():
            return np.interp(clock.get_value(), ts, thetas)

        def omega():
            return np.interp(clock.get_value(), ts, omegas)

        title = Text("Damped pendulum & phase space", font_size=38).to_edge(UP)
        ode = MathTex(r"\ddot\theta = -\frac{g}{L}\sin\theta - \gamma\,\dot\theta", font_size=38)
        ode.next_to(title, DOWN, buff=0.25)

        # Left: the pendulum.
        pivot = np.array([-3.6, 0.8, 0])
        length = 2.4
        ceiling = Line(pivot + LEFT * 1.2, pivot + RIGHT * 1.2, color=GREY_M, stroke_width=6)

        def bob_pos():
            th = theta()
            return pivot + length * np.array([np.sin(th), -np.cos(th), 0])

        rod = always_redraw(lambda: Line(pivot, bob_pos(), color=WHITE, stroke_width=4))
        bob = always_redraw(lambda: Dot(bob_pos(), radius=0.2, color=ORANGE_P))
        bob_trail = TracedPath(lambda: bob_pos(), stroke_color=ORANGE_P, stroke_width=2,
                               stroke_opacity=[0, 0.8], dissipating_time=0.6)

        # Right: phase space.
        axes = Axes(
            x_range=[-3, 3, 1], y_range=[-6, 6, 2], x_length=5.4, y_length=5,
            tips=False, axis_config={"color": GREY_M},
        ).shift(RIGHT * 3.4 + DOWN * 0.9)
        labels = axes.get_axis_labels(MathTex(r"\theta"), MathTex(r"\dot\theta"))
        phase_dot = always_redraw(lambda: Dot(axes.c2p(theta(), omega()), color=YELLOW_M, radius=0.09))
        phase_trail = TracedPath(lambda: axes.c2p(theta(), omega()), stroke_color=YELLOW_M, stroke_width=3)

        self.play(Write(title), Write(ode))
        self.play(Create(ceiling), Create(rod), FadeIn(bob), Create(axes), Write(labels))
        self.add(bob_trail, phase_trail, phase_dot)
        self.wait(0.5)

        self.play(clock.animate.set_value(T_END), run_time=T_END, rate_func=linear)

        note = Text("energy is lost → the orbit spirals to rest", font_size=26, color=YELLOW_M)
        note.to_corner(DL, buff=0.5)
        self.play(FadeIn(note, shift=UP * 0.2))
        self.wait(2)
