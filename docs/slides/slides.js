// Builds the gallery slides from examples.js, wires the interactive widgets, then starts reveal.js.
(() => {
  const D = window.DISCIPLINES, EX = window.EXAMPLES;
  const esc = s => s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

  // Key excerpt of each scene (full code is on the website and in scenes/).
  const SNIPPETS = {
    "01_pythagoras": `# same square, four triangles: just translate three of them
self.play(
    T4.animate.shift(RIGHT * a + DOWN * b),
    T1.animate.shift(UP * a),
    T3.animate.shift(LEFT * b),
    run_time=2.5,
)
final = MathTex("a^2", "+", "b^2", "=", "c^2")
self.play(TransformFromCopy(VGroup(eq1, eq2), final))`,
    "02_fourier_series": `def sum_graph(n):
    return axes.plot(lambda x: partial_sum(x, n)[0],
                     x_range=[-PI, PI, 0.01], color=BLUE_M)

current = sum_graph(1)
for n in (3, 5, 7, 11, 21, 41, 81):
    self.play(Transform(current, sum_graph(n)),
              n_label[1].animate.set_value(n))`,
    "03_pendulum_phase_space": `ts, thetas, omegas = simulate()          # RK4 in NumPy
clock = ValueTracker(0)
theta = lambda: np.interp(clock.get_value(), ts, thetas)

rod = always_redraw(lambda: Line(pivot, bob_pos()))
phase_dot = always_redraw(
    lambda: Dot(axes.c2p(theta(), omega())))
trail = TracedPath(lambda: axes.c2p(theta(), omega()))
self.play(clock.animate.set_value(T_END),
          run_time=T_END, rate_func=linear)`,
    "04_standing_waves": `t = ValueTracker(0)
y1 = lambda x, s: np.sin(K * x - W * s)
y2 = lambda x, s: np.sin(K * x + W * s)

g3 = always_redraw(lambda: ax3.plot(
    lambda x: y1(x, t.get_value()) + y2(x, t.get_value()),
    color=YELLOW_M))
self.add(g3)
self.play(t.animate.set_value(7), run_time=5, rate_func=linear)`,
    "05_dna_double_helix": `def build_helix(phase):
    for i in range(len(us) - 1):
        depth = np.cos(ang[i])           # -1 (back) .. +1 (front)
        seg = Line(pts[i], pts[i + 1],
                   stroke_width=7 + 3 * depth,
                   stroke_opacity=0.35 + 0.65 * (depth + 1) / 2)
        (front if depth > 0 else back).add(seg)
    return VGroup(back, rungs, front)    # painter's order

helix = always_redraw(lambda: build_helix(phase.get_value()))`,
    "06_predator_prey": `sol = solve_ivp(lotka_volterra, (0, T_END), [10, 5],
                t_eval=ts)
prey, pred = sol.y

def partial(full):          # draw the curve up to "now"
    return always_redraw(lambda: full.copy()
        .pointwise_become_partial(full, 0, clock.get_value() / T_END))

self.add(partial(full_prey), partial(full_pred), partial(full_orbit))`,
    "07_bubble_sort": `for i in range(n - 1):
    for j in range(n - 1 - i):
        self.play(go_to(4), left[0].animate.set_fill(YELLOW_M), ...)
        if values[j] > values[j + 1]:
            self.play(go_to(5),
                left.animate(path_arc=PI / 2).set_x(xs[j + 1]),
                right.animate(path_arc=PI / 2).set_x(xs[j]))
            bars[j], bars[j + 1] = right, left`,
    "08_gradient_descent": `def descend(lr):
    pts = [START]
    for _ in range(STEPS):
        pts.append(pts[-1] - lr * grad(pts[-1]))
    return pts

for lr, color in ((0.08, PURPLE_C), (0.23, ORANGE_P)):
    for a, b in zip(pts, pts[1:]):
        self.play(GrowArrow(Arrow(plane.c2p(*a), plane.c2p(*b))),
                  walker.animate.move_to(plane.c2p(*b)))`,
    "09_needleman_wunsch": `F[i, j] = max(F[i-1, j-1] + s,   # diagonal: (mis)match
              F[i-1, j] + GAP,   # from above: gap
              F[i, j-1] + GAP)   # from the left: gap

cells[i, j] = VGroup(
    Square(size, fill_color=cell_color(F[i, j]), fill_opacity=1),
    Text(str(F[i, j]), font_size=20))
self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in rest],
                      lag_ratio=0.08), run_time=5)`,
    "10_central_dogma": `mrna = strand(mrna_seq, 0.3)          # row of coloured tiles
self.play(
    polymerase.animate.shift(RIGHT * STEP * 14),
    LaggedStart(*[TransformFromCopy(t, m)
                  for t, m in zip(template, mrna)], lag_ratio=0.25),
    run_time=5, rate_func=linear)

for codon in codons:
    self.play(ribosome.animate.move_to(codon.get_center() + UP * 0.35))`,
    "11_binary_search": `while lo <= hi:
    mid = (lo + hi) // 2
    self.play(mid_p.animate.next_to(cells[mid], UP))
    if ARR[mid] < TARGET:
        gone, lo = range(lo, mid + 1), mid + 1
    else:
        gone, hi = range(mid, hi + 1), mid - 1
    self.play(*[cells[i].animate.set_opacity(0.2) for i in gone])`,
    "12_recursion_stack": `for n in range(N, -1, -1):              # calls: push frames
    f = frame(n, f"fact({n})   n = {n}", PURPLE_C)
    self.play(FadeIn(f, shift=DOWN * 0.4))

for n in range(1, N + 1):               # returns: pop frames
    self.play(FadeOut(frames[n - 1], shift=UP * 0.4))
    self.play(Transform(frames[n][1],
              Text(f"{n} * {value} = {n * value}")))`,
    "13_bfs_graph": `queue = deque([START])
while queue:
    u = queue.popleft()
    self.play(FadeOut(q_items[0]), set_state(u, PURPLE_C), *q_layout())
    for v in adj[u]:
        if v not in dist:
            dist[v] = dist[u] + 1
            queue.append(v)
            self.play(set_state(v, YELLOW_M), FadeIn(q_box(v)))`,
    "14_hash_table": `idx = h(key) % SIZE
self.play(item.animate.move_to(machine))          # into hash()
self.play(FadeIn(calc), buckets[idx][0].animate.set_stroke(YELLOW_M))
anchor = chains[idx][-1] if chains[idx] else buckets[idx]
self.play(item.animate.next_to(anchor, RIGHT, buff=0.35),
          GrowArrow(link))                         # chain on collision`,
    "15_big_o_race": `n = ValueTracker(0.5)
for name, f, color in CURVES:
    plots.add(always_redraw(lambda f=f, color=color: axes.plot(
        f, x_range=[0.5, visible_end(f)], color=color)))
self.add(plots, tags, counter)
self.play(n.animate.set_value(20), run_time=9, rate_func=linear)`,
    "16_newton_first_law": `def x_ice(t):    return X0 + V0 * t                 # ΣF = 0
def x_carpet(t):
    ts = min(t, V0 / DECEL)
    return X0 + V0 * ts - 0.5 * DECEL * ts ** 2       # friction

p_ice = always_redraw(lambda: puck(x_ice(clock.get_value()), ...))
p_car = always_redraw(lambda: puck(x_carpet(clock.get_value()), ...))
self.play(clock.animate.set_value(T_END), rate_func=linear)`,
    "17_newton_second_law": `for m in (1.0, 2.0):
    a = F / m                                   # Newton's 2nd law
    def cart(a=a, ...):
        x = X0 + SCALE * 0.5 * a * t.get_value() ** 2
        ...
    carts.add(always_redraw(cart))
lines = [ax.plot(lambda s: a * s, ...) for a in accs]   # v = a t`,
    "18_newton_third_law": `v1, v2 = -IMPULSE / M1, IMPULSE / M2     # same impulse, opposite signs

def forces():                            # only while pushing
    if t.get_value() >= T_PUSH:
        return VGroup()
    return VGroup(Arrow(a, a + LEFT * 1.6),   # F(2→1)
                  Arrow(b, b + RIGHT * 1.6))  # F(1→2): same length
force_arrows = always_redraw(forces)`,
    "19_cyclist_air_drag": `def drag(v):  return 0.5 * RHO * CDA * v ** 2
def propulsion(v):  return min(POWER / v, F_MAX)

for i in range(len(ts)):              # m dv/dt = P/v - drag - roll
    v += dt * (propulsion(v) - drag(v) - F_ROLL) / MASS

wheel.add_updater(lambda m, dt: m.rotate(-v_now() * dt * 1.2))
arrows = always_redraw(force_arrows)  # lengths follow the physics`,
    "20_newton_cannon": `while t < t_max:                          # velocity Verlet
    r = r + v * dt + 0.5 * a * dt ** 2
    a_new = -GM * r / np.linalg.norm(r) ** 3   # inverse square
    v = v + 0.5 * (a + a_new) * dt
    a = a_new

path = VMobject().set_points_smoothly(points)
self.play(Create(path), MoveAlongPath(ball, path))`,
  };

  /* ---------- gallery ---------- */
  const thumbs = document.getElementById("thumbs");
  const stack = document.getElementById("gallery");
  EX.forEach((e, i) => {
    const d = D[e.discipline];
    thumbs.insertAdjacentHTML("beforeend",
      `<div class="thumb" style="--c:${d.color}" data-v="${i + 1}">
         <img src="../posters/${e.slug}.jpg" alt=""><i>${e.slug.slice(0, 2)}</i><span>${e.title}</span></div>`);
    stack.insertAdjacentHTML("beforeend", `
      <section class="ex" data-background-gradient="radial-gradient(ellipse at 85% 10%, ${d.color}22, #0B0F19 60%)">
        <div class="cols wide-left">
          <div>
            <video data-autoplay muted loop playsinline src="../videos/${e.slug}.mp4" poster="../posters/${e.slug}.jpg"></video>
            <div class="inclass"><b>In class:</b> ${e.classroom}</div>
          </div>
          <div>
            <span class="tag" style="color:${d.color}">${d.icon} ${d.label} · ${e.level}</span>
            <h2>${e.title}</h2>
            <p class="summary">${e.summary}</p>
            <pre><code class="language-python" data-trim>${esc(SNIPPETS[e.slug] || "")}</code></pre>
            <div class="cmd">manim -pqm scenes/${e.slug}.py ${e.cls}</div>
          </div>
        </div>
      </section>`);
  });

  /* ---------- widget: rate functions ---------- */
  const sig = x => 1 / (1 + Math.exp(-x));
  const smooth = t => { const s = 10; const e = sig(-s / 2); return Math.min(Math.max((sig(s * (t - 0.5)) - e) / (1 - 2 * e), 0), 1); };
  const RATES = {
    linear: t => t,
    smooth,
    rush_into: t => 2 * smooth(t / 2),
    rush_from: t => 2 * smooth(t / 2 + 0.5) - 1,
    there_and_back: t => smooth(t < 0.5 ? 2 * t : 2 * (1 - t)),
    there_and_back_with_pause: t => (t < 1 / 3 ? smooth(3 * t) : t < 2 / 3 ? 1 : smooth(3 - 3 * t)),
    wiggle: t => Math.sin(4 * Math.PI * t) * (t < 0.5 ? smooth(2 * t) : smooth(2 - 2 * t)) * 0.3,
    double_smooth: t => (t < 0.5 ? 0.5 * smooth(2 * t) : 0.5 * (1 + smooth(2 * t - 1))),
  };
  const rc = document.getElementById("rate-canvas"), rctx = rc.getContext("2d");
  let rateName = "smooth", rateStart = null;
  const rb = document.getElementById("rate-buttons");
  Object.keys(RATES).forEach(name => {
    const b = document.createElement("button");
    b.textContent = name; if (name === rateName) b.classList.add("active");
    b.onclick = () => { rateName = name; rateStart = performance.now();
      [...rb.children].forEach(x => x.classList.toggle("active", x === b)); };
    rb.appendChild(b);
  });
  function drawRate(now) {
    const W = rc.width, H = rc.height, f = RATES[rateName];
    const dur = 2000, t = rateStart === null ? 1 : Math.min((now - rateStart) / dur, 1);
    rctx.clearRect(0, 0, W, H);
    // graph box
    const gx = 40, gy = 30, gw = 360, gh = 300;
    rctx.strokeStyle = "#2A3350"; rctx.lineWidth = 1.5; rctx.strokeRect(gx, gy, gw, gh);
    rctx.fillStyle = "#8A93A6"; rctx.font = "18px JetBrains Mono";
    rctx.fillText("t →", gx + gw - 40, gy + gh + 24); rctx.fillText("progress", gx, gy - 8);
    const isWiggle = rateName === "wiggle";
    const Y = v => gy + gh - (isWiggle ? (v + 0.5) : v) * gh;
    rctx.strokeStyle = "#FFD166"; rctx.lineWidth = 4; rctx.beginPath();
    for (let k = 0; k <= 200 * t; k++) { const u = k / 200; const x = gx + u * gw, y = Y(f(u)); k ? rctx.lineTo(x, y) : rctx.moveTo(x, y); }
    rctx.stroke();
    // track + moving dot
    const tx0 = 470, tx1 = 860, ty = 180;
    rctx.strokeStyle = "#2A3350"; rctx.lineWidth = 3; rctx.beginPath(); rctx.moveTo(tx0, ty); rctx.lineTo(tx1, ty); rctx.stroke();
    const p = f(t), x = isWiggle ? (tx0 + tx1) / 2 + p * (tx1 - tx0) : tx0 + p * (tx1 - tx0);
    rctx.fillStyle = "#4F9DFF"; rctx.shadowColor = "#4F9DFF"; rctx.shadowBlur = 25;
    rctx.beginPath(); rctx.arc(x, ty, 22, 0, 7); rctx.fill(); rctx.shadowBlur = 0;
    rctx.fillStyle = "#E8ECF4"; rctx.font = "22px JetBrains Mono";
    rctx.fillText(`rate_func=${rateName}`, tx0 - 10, 300);
    rctx.fillStyle = "#8A93A6"; rctx.fillText(`t = ${t.toFixed(2)}`, tx0 - 10, 340);
    requestAnimationFrame(drawRate);
  }
  requestAnimationFrame(drawRate);

  /* ---------- widget: ValueTracker tangent ---------- */
  const tc = document.getElementById("tangent-canvas"), tctx = tc.getContext("2d");
  const slider = document.getElementById("tangent-x"), readout = document.getElementById("tangent-readout");
  const fx = x => 0.25 * x ** 3 - x, dfx = x => 0.75 * x ** 2 - 1;
  const TW = tc.width, TH = tc.height, sx = TW / 6.4, sy = TH / 5.2;
  const P = (x, y) => [TW / 2 + x * sx, TH / 2 - y * sy];
  function drawTangent() {
    const x0 = +slider.value;
    tctx.clearRect(0, 0, TW, TH);
    tctx.strokeStyle = "#1C2440"; tctx.lineWidth = 1;
    for (let gx = -3; gx <= 3; gx++) { const [a] = P(gx, 0); tctx.beginPath(); tctx.moveTo(a, 0); tctx.lineTo(a, TH); tctx.stroke(); }
    for (let gy = -2; gy <= 2; gy++) { const [, b] = P(0, gy); tctx.beginPath(); tctx.moveTo(0, b); tctx.lineTo(TW, b); tctx.stroke(); }
    tctx.strokeStyle = "#8A93A6"; tctx.lineWidth = 2;
    let [a, b] = P(-3.2, 0), [c, d] = P(3.2, 0); tctx.beginPath(); tctx.moveTo(a, b); tctx.lineTo(c, d); tctx.stroke();
    [a, b] = P(0, -2.6); [c, d] = P(0, 2.6); tctx.beginPath(); tctx.moveTo(a, b); tctx.lineTo(c, d); tctx.stroke();
    tctx.strokeStyle = "#4F9DFF"; tctx.lineWidth = 5; tctx.beginPath();
    for (let k = 0; k <= 300; k++) { const x = -2.9 + 5.8 * k / 300; const [u, v] = P(x, fx(x)); k ? tctx.lineTo(u, v) : tctx.moveTo(u, v); }
    tctx.stroke();
    const m = dfx(x0), y0 = fx(x0), L = 1.4 / Math.sqrt(1 + m * m);
    [a, b] = P(x0 - L, y0 - m * L); [c, d] = P(x0 + L, y0 + m * L);
    tctx.strokeStyle = "#FFD166"; tctx.lineWidth = 4; tctx.beginPath(); tctx.moveTo(a, b); tctx.lineTo(c, d); tctx.stroke();
    const [px, py] = P(x0, y0);
    tctx.fillStyle = "#FF5C8A"; tctx.beginPath(); tctx.arc(px, py, 11, 0, 7); tctx.fill();
    tctx.fillStyle = "#E8ECF4"; tctx.font = "24px JetBrains Mono"; tctx.fillText("f(x) = x³/4 − x", 20, 36);
    readout.textContent = `x = ${x0.toFixed(2)}   slope f'(x) = ${m.toFixed(2)}`;
  }
  slider.addEventListener("input", drawTangent);
  document.getElementById("tangent-play").onclick = () => {
    const start = performance.now(), from = -2, to = 2, dur = 6000;
    const step = now => { const t = Math.min((now - start) / dur, 1);
      slider.value = from + (to - from) * smooth(t); drawTangent(); if (t < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  drawTangent();

  /* ---------- reveal.js ---------- */
  Reveal.initialize({
    hash: true,
    width: 1280, height: 720, margin: 0.05,
    slideNumber: "c/t",
    transition: "slide", backgroundTransition: "fade",
    autoAnimateDuration: 0.8,
    plugins: [RevealHighlight, RevealNotes, RevealZoom],
  }).then(() => {
    document.querySelectorAll(".thumb").forEach(t =>
      t.addEventListener("click", () => Reveal.slide(Reveal.getIndices(stack.querySelector("section")).h, +t.dataset.v)));
  });
})();
