"""
19 · Physics — Air drag on a cyclist at high speed (frottement de l'air à vélo)
A rider pedals with a constant power of 400 W. The pedalling force P/v shrinks
as speed grows, while air drag ½ρC_dA·v² grows with the square of the speed.
Newton's 2nd law  m·dv/dt = P/v − F_drag − F_roll  gives a top speed where
the forces balance (~46 km/h). Tucking in (smaller C_dA) raises it.

Manim ideas: an ODE solved in NumPy, updaters with dt for spinning wheels and
wind streaks, force arrows whose length follows the physics, a force-vs-speed
graph with a moving operating point.

Render:
    manim -pqm scenes/19_cyclist_air_drag.py CyclistAirDrag
"""
from manim import *

GREEN_B = "#3DDC97"
PINK_B = "#FF5C8A"
YELLOW_M = "#FFD166"
BLUE_M = "#4F9DFF"
ORANGE_P = "#FF8A3D"
GREY_M = "#8A93A6"

MASS = 80.0          # rider + bike, kg
POWER = 400.0        # W
RHO = 1.2            # air density, kg/m^3
CDA = 0.30           # drag area C_d * A (upright on the hoods), m^2
CDA_TUCK = 0.22      # aero tuck
F_ROLL = 0.004 * MASS * 9.81
F_MAX = 150.0        # traction limit when starting
T_SIM = 60.0         # simulated seconds


def drag(v, cda=CDA):
    return 0.5 * RHO * cda * v ** 2


def propulsion(v):
    return min(POWER / max(v, 1e-6), F_MAX)


def simulate(dt=0.01):
    ts = np.arange(0, T_SIM + dt, dt)
    vs = np.empty_like(ts)
    v = 0.0
    for i in range(len(ts)):
        vs[i] = v
        v += dt * (propulsion(v) - drag(v) - F_ROLL) / MASS
    return ts, vs


def top_speed(cda):
    # P = (1/2 rho cda) v^3 + F_roll v  ->  positive real root
    roots = np.roots([0.5 * RHO * cda, 0, F_ROLL, -POWER])
    return float(max(r.real for r in roots if abs(r.imag) < 1e-9))


def make_bike():
    wheel_r = 0.55
    wheels = VGroup()
    for x in (-1.0, 1.0):
        rim = Circle(wheel_r, color=WHITE, stroke_width=4)
        spokes = VGroup(*[Line(ORIGIN, wheel_r * np.array([np.cos(a), np.sin(a), 0]), stroke_width=1.5, color=GREY_B)
                          for a in np.linspace(0, 2 * PI, 8, endpoint=False)])
        wheels.add(VGroup(rim, spokes).move_to([x, 0, 0]))
    seat, bars, crank = np.array([-0.35, 0.95, 0]), np.array([0.75, 1.0, 0]), np.array([-0.1, 0.05, 0])
    frame = VGroup(Line([-1, 0, 0], crank), Line(crank, seat), Line(seat, [-1, 0, 0]), Line(seat, bars),
                   Line(crank, bars), Line(bars, [1, 0, 0])).set_stroke(ORANGE_P, 5)
    hip = seat + UP * 0.1
    shoulder = np.array([0.45, 1.55, 0])
    rider = VGroup(
        Line(hip, shoulder, stroke_width=10, color=BLUE_M),              # torso
        Line(shoulder, bars + UP * 0.05, stroke_width=7, color=BLUE_M),  # arm
        Line(hip, crank + UP * 0.25 + RIGHT * 0.2, stroke_width=8, color="#2E5FA8"),  # leg
        Circle(0.2, color=WHITE, fill_color=YELLOW_M, fill_opacity=1).move_to(shoulder + UP * 0.25 + RIGHT * 0.2),
    )
    return VGroup(wheels, frame, rider)


class CyclistAirDrag(Scene):
    def construct(self):
        ts, vs = simulate()
        clock = ValueTracker(0)

        def v_now():
            return float(np.interp(clock.get_value(), ts, vs))

        title = Text("Air drag on a fast cyclist", font_size=38).to_edge(UP, buff=0.25)
        subtitle = Text("frottement de l'air à grande vitesse", font_size=24, color=GREY_B, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.12)
        self.play(Write(title), FadeIn(subtitle))

        # --- Left: cyclist, wind, forces
        road = Line(LEFT * 7, LEFT * 0.4, color=GREY_M, stroke_width=4).shift(DOWN * 1.35)
        bike = make_bike().scale(0.9).move_to(LEFT * 3.7 + DOWN * 0.25)
        bike.align_to(road, DOWN).shift(UP * 0.02)
        wheels = bike[0]
        for w in wheels:
            w.add_updater(lambda m, dt: m.rotate(-v_now() * dt * 1.2))

        rng = np.random.default_rng(3)
        streaks = VGroup(*[Line(ORIGIN, RIGHT * rng.uniform(0.3, 0.8), color=BLUE_M, stroke_width=2, stroke_opacity=0.6)
                           .move_to([rng.uniform(-7, -0.6), rng.uniform(-1.0, 1.9), 0]) for _ in range(16)])

        def blow(m, dt):
            m.shift(LEFT * v_now() * dt * 0.6)
            if m.get_right()[0] < -7.1:
                m.set_x(-0.7)
        for s in streaks:
            s.add_updater(blow)

        def force_arrows():
            v = v_now()
            centre = bike.get_center() + UP * 0.2
            fp, fd = propulsion(max(v, 0.3)), drag(v)
            k = 0.03                                              # screen units per newton
            prop = Arrow(centre, centre + RIGHT * min(fp, 80) * k, buff=0, color=GREEN_B, stroke_width=6,
                         max_tip_length_to_length_ratio=0.25)
            back = bike.get_left() + UP * 0.5
            dr = Arrow(back, back + LEFT * max(fd * k, 0.01), buff=0, color=PINK_B, stroke_width=6,
                       max_tip_length_to_length_ratio=0.25)
            return VGroup(prop, dr)

        arrows = always_redraw(force_arrows)
        legend = VGroup(Text("pedalling force P/v", font_size=20, color=GREEN_B),
                        Text("air drag ½ρC_dA·v²", font_size=20, color=PINK_B)).arrange(DOWN, aligned_edge=LEFT)
        legend.next_to(road, DOWN, buff=0.25).align_to(road, LEFT).shift(RIGHT * 0.3)
        speed = always_redraw(lambda: Text(f"{v_now() * 3.6:4.1f} km/h", font="Monospace", font_size=34,
                                           color=YELLOW_M).move_to(LEFT * 3.7 + UP * 2.05))
        tclock = always_redraw(lambda: Text(f"t = {clock.get_value():4.1f} s", font="Monospace", font_size=20,
                                            color=GREY_B).next_to(speed, DOWN, buff=0.08))

        self.add(streaks)
        self.play(Create(road), FadeIn(bike), FadeIn(legend))
        self.add(arrows, speed, tclock)

        # --- Right: forces versus speed
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 80, 20], x_length=5.6, y_length=4.0, tips=False,
                  axis_config={"color": GREY_M, "include_numbers": True, "font_size": 18})
        ax.to_edge(RIGHT, buff=0.45).shift(DOWN * 0.5)
        ax_lab = VGroup(Text("speed (km/h)", font_size=20).next_to(ax.x_axis, DOWN, buff=0.35),
                        Text("force (N)", font_size=20).next_to(ax.y_axis, UP, buff=0.1))
        g_drag = ax.plot(lambda k: drag(k / 3.6), x_range=[0, 60], color=PINK_B, stroke_width=4)
        g_prop = ax.plot(lambda k: POWER / (k / 3.6), x_range=[POWER / 80 * 3.6, 60], color=GREEN_B, stroke_width=4)
        g_roll = ax.plot(lambda k: F_ROLL, x_range=[0, 60], color=GREY_B, stroke_width=2)
        self.play(Create(ax), FadeIn(ax_lab))
        self.play(Create(g_prop), Create(g_drag), Create(g_roll))
        op = always_redraw(lambda: Dot(ax.c2p(v_now() * 3.6, min(drag(v_now()), 80)), color=PINK_B, radius=0.08))
        self.add(op)

        law = MathTex(r"m\,\frac{dv}{dt} = \frac{P}{v} - \tfrac12\rho C_dA\,v^2 - F_{\text{roll}}", font_size=30)
        law.next_to(ax, UP, buff=0.3)
        self.play(Write(law))

        self.play(clock.animate.set_value(T_SIM), run_time=10, rate_func=lambda x: 1 - (1 - x) ** 1.6)

        v_top = top_speed(CDA)
        eq_point = ax.c2p(v_top * 3.6, drag(v_top))
        ring = Circle(0.18, color=YELLOW_M, stroke_width=4).move_to(eq_point)
        eq_txt = Text(f"forces balance → top speed ≈ {v_top * 3.6:.0f} km/h", font_size=22, color=YELLOW_M)
        eq_txt.next_to(ax, DOWN, buff=0.75).align_to(ax, LEFT)
        self.play(Create(ring), Write(eq_txt))
        self.wait(1)

        # Doubling the speed
        facts = VGroup(
            Text("2× speed → 4× drag force", font_size=21, color=PINK_B),
            Text("2× speed → 8× power  (P = F·v ∝ v³)", font_size=21, color=PINK_B),
            Text(f"aero tuck (C_dA {CDA} → {CDA_TUCK}): ≈ {top_speed(CDA_TUCK) * 3.6:.0f} km/h, same 400 W",
                 font_size=19, color=GREEN_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        box = SurroundingRectangle(facts, color=GREY_M, buff=0.2, corner_radius=0.12, fill_color="#0B0F19", fill_opacity=0.9)
        VGroup(box, facts).to_corner(DL, buff=0.2)
        for s in streaks:
            s.clear_updaters()
        for w in wheels:
            w.clear_updaters()
        self.play(FadeOut(legend), FadeIn(box), LaggedStart(*[FadeIn(f, shift=RIGHT * 0.2) for f in facts], lag_ratio=0.4))
        self.wait(3)
