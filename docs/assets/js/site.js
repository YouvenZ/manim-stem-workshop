(() => {
  const D = window.DISCIPLINES, EX = window.EXAMPLES, REPO = window.REPO_URL;
  const $ = (s, el = document) => el.querySelector(s);
  const $$ = (s, el = document) => [...el.querySelectorAll(s)];

  /* ---------------- repo links ---------------- */
  $("#repo-link").href = REPO;
  $$(".repo-url").forEach(el => (el.textContent = REPO));

  /* ---------------- hero canvas: a "NumberPlane" with curves being drawn ---------------- */
  const cv = $("#hero-canvas"), ctx = cv.getContext("2d");
  const colors = Object.values(D).map(d => d.color);
  let W, H, DPR, t0 = performance.now();
  const resize = () => {
    DPR = Math.min(window.devicePixelRatio || 1, 2);
    W = cv.clientWidth; H = cv.clientHeight;
    cv.width = W * DPR; cv.height = H * DPR;
    ctx.setTransform(DPR, 0, 0, DPR, 0, 0);
  };
  resize(); addEventListener("resize", resize);

  // Parametric curves (x, y in [-1, 1]) — Lissajous, rose, sine, spiral, heart-ish cardioid.
  const shapes = [
    s => [Math.sin(3 * s + 0.5), Math.sin(2 * s)],
    s => [Math.cos(4 * s) * Math.cos(s), Math.cos(4 * s) * Math.sin(s)],
    s => [s / Math.PI - 1, 0.45 * Math.sin(3 * s)],
    s => [(s / 6.3) * Math.cos(3 * s) * 0.9, (s / 6.3) * Math.sin(3 * s) * 0.9],
    s => [0.5 * (2 * Math.cos(s) - Math.cos(2 * s)) / 1.5, 0.5 * (2 * Math.sin(s) - Math.sin(2 * s)) / 1.5],
    s => [Math.sin(5 * s), Math.cos(4 * s)],
  ];
  const spawn = (i) => ({
    f: shapes[Math.floor(Math.random() * shapes.length)],
    color: colors[i % colors.length],
    cx: 0.1 + Math.random() * 0.8, cy: 0.15 + Math.random() * 0.7,
    r: 70 + Math.random() * 110, born: performance.now() + Math.random() * 3000,
    life: 7000 + Math.random() * 4000, rot: Math.random() * Math.PI,
  });
  let curves = Array.from({ length: 7 }, (_, i) => spawn(i));
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

  function frame(now) {
    ctx.clearRect(0, 0, W, H);
    // grid
    const step = 60, off = ((now - t0) / 80) % step;
    ctx.lineWidth = 1;
    for (let x = -step + off; x < W + step; x += step) {
      ctx.strokeStyle = "rgba(79,157,255,0.07)"; ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
    }
    for (let y = 0; y < H; y += step) {
      ctx.strokeStyle = "rgba(79,157,255,0.07)"; ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
    }
    // curves: drawn progressively (like Manim's Create), then faded out
    curves.forEach((c, i) => {
      const age = now - c.born;
      if (age < 0) return;
      if (age > c.life) { curves[i] = spawn(i); curves[i].born = now; return; }
      const p = Math.min(age / (c.life * 0.45), 1);
      const fade = age > c.life * 0.75 ? 1 - (age - c.life * 0.75) / (c.life * 0.25) : 1;
      const N = 240, end = Math.floor(N * easeInOut(p));
      ctx.save();
      ctx.translate(c.cx * W, c.cy * H); ctx.rotate(c.rot + age / 20000);
      ctx.strokeStyle = c.color; ctx.globalAlpha = 0.55 * fade; ctx.lineWidth = 2.5;
      ctx.shadowColor = c.color; ctx.shadowBlur = 14;
      ctx.beginPath();
      for (let k = 0; k <= end; k++) {
        const [x, y] = c.f((k / N) * 2 * Math.PI);
        k ? ctx.lineTo(x * c.r, y * c.r) : ctx.moveTo(x * c.r, y * c.r);
      }
      ctx.stroke();
      if (end > 0 && p < 1) {           // the "pen" dot
        const [x, y] = c.f((end / N) * 2 * Math.PI);
        ctx.fillStyle = "#fff"; ctx.globalAlpha = fade;
        ctx.beginPath(); ctx.arc(x * c.r, y * c.r, 3, 0, 7); ctx.fill();
      }
      ctx.restore();
    });
    if (!reduced) requestAnimationFrame(frame);
  }
  const easeInOut = x => (x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2);
  requestAnimationFrame(frame);

  /* ---------------- chips + filters ---------------- */
  const chip = (key, extra = "") =>
    `<button class="chip ${extra}" data-d="${key}"><span>${key === "all" ? "All" : D[key].icon + " " + D[key].label}</span></button>`;
  $("#hero-chips").innerHTML = Object.keys(D).map(k => chip(k)).join("");
  $("#filters").innerHTML = chip("all", "all active") + Object.keys(D).map(k => chip(k)).join("");

  function applyFilter(key) {
    $$("#filters .chip").forEach(c => c.classList.toggle("active", c.dataset.d === key));
    $$(".card").forEach(card => card.classList.toggle("hidden", key !== "all" && card.dataset.d !== key));
  }
  $$("#filters .chip").forEach(c => c.addEventListener("click", () => applyFilter(c.dataset.d)));
  $$("#hero-chips .chip").forEach(c => c.addEventListener("click", () => {
    applyFilter(c.dataset.d); $("#gallery").scrollIntoView();
  }));

  /* ---------------- gallery cards ---------------- */
  $("#grid").innerHTML = EX.map((e, i) => {
    const d = D[e.discipline];
    return `
    <article class="card reveal-up" data-d="${e.discipline}" data-i="${i}" style="--accent:${d.color}" tabindex="0">
      <div class="media">
        <img src="posters/${e.slug}.jpg" alt="${e.title}" loading="lazy">
        <video muted loop playsinline preload="none" src="videos/${e.slug}.mp4"></video>
        <span class="num">${e.slug.slice(0, 2)}</span>
        <span class="play">▶</span>
      </div>
      <div class="body">
        <span class="tag">${d.icon} ${d.label}</span><span class="level">${e.level}</span>
        <h3>${e.title}</h3>
        <p>${e.summary}</p>
        <div class="pills">${e.concepts.map(c => `<span class="pill">${c}</span>`).join("")}</div>
      </div>
    </article>`;
  }).join("");

  $$(".card").forEach(card => {
    const v = $("video", card);
    card.addEventListener("mouseenter", () => { v.currentTime = 0; v.play().catch(() => {}); });
    card.addEventListener("mouseleave", () => v.pause());
    card.addEventListener("click", () => openModal(+card.dataset.i));
    card.addEventListener("keydown", ev => { if (ev.key === "Enter") openModal(+card.dataset.i); });
  });

  /* ---------------- modal ---------------- */
  const modal = $("#modal"), mv = $("#m-video");
  let currentCode = "";
  async function openModal(i) {
    const e = EX[i], d = D[e.discipline];
    $(".modal-box").style.setProperty("--accent", d.color);
    $("#m-tag").textContent = `${d.icon} ${d.label} · ${e.level}`;
    $("#m-tag").style.color = d.color;
    $("#m-title").textContent = e.title;
    $("#m-summary").textContent = e.summary;
    $("#m-class").textContent = e.classroom;
    $("#m-pills").innerHTML = e.concepts.map(c => `<span class="pill">${c}</span>`).join("");
    $("#m-cmd").textContent = `manim -pqm scenes/${e.slug}.py ${e.cls}`;
    $("#m-file").textContent = `scenes/${e.slug}.py`;
    $("#m-gh").href = `${REPO}/blob/main/scenes/${e.slug}.py`;
    mv.src = `videos/${e.slug}.mp4`; mv.poster = `posters/${e.slug}.jpg`;
    setRate(1);
    modal.classList.add("open"); modal.setAttribute("aria-hidden", "false");
    document.body.style.overflow = "hidden";
    mv.play().catch(() => {});

    const codeEl = $("#m-code");
    codeEl.textContent = "Loading…"; codeEl.removeAttribute("data-highlighted");
    try {
      const r = await fetch(`code/${e.slug}.py`);
      if (!r.ok) throw new Error(r.status);
      currentCode = await r.text();
      codeEl.textContent = currentCode;
      if (window.hljs) hljs.highlightElement(codeEl);
    } catch {
      currentCode = "";
      codeEl.textContent = "# Could not load the source here (open the site through a web server,\n# e.g.  python -m http.server -d docs). The code is on GitHub ↗";
    }
  }
  function closeModal() {
    modal.classList.remove("open"); modal.setAttribute("aria-hidden", "true");
    mv.pause(); document.body.style.overflow = "";
  }
  $("#m-close").addEventListener("click", closeModal);
  modal.addEventListener("click", e => { if (e.target === modal) closeModal(); });
  addEventListener("keydown", e => { if (e.key === "Escape") closeModal(); });

  function setRate(r) {
    mv.playbackRate = r;
    $$("#m-speed button").forEach(b => b.classList.toggle("active", +b.dataset.rate === r));
  }
  $$("#m-speed button").forEach(b => b.addEventListener("click", () => setRate(+b.dataset.rate)));

  /* ---------------- copy helpers ---------------- */
  const toast = msg => { const t = $("#toast"); t.textContent = msg; t.classList.add("show"); setTimeout(() => t.classList.remove("show"), 1400); };
  const copy = txt => navigator.clipboard.writeText(txt).then(() => toast("Copied!"));
  $("#m-copy").addEventListener("click", () => currentCode && copy(currentCode));
  $$(".shell .copy").forEach(btn => btn.addEventListener("click", () => {
    const lines = $("pre", btn.parentElement).innerText.split("\n")
      .map(l => l.replace(/^\$ /, "").replace(/\s+#.*$/, "")).filter(l => l.trim() && !l.trim().startsWith("#"));
    copy(lines.join("\n"));
  }));

  /* ---------------- tabs ---------------- */
  $$(".tabs").forEach(tabs => {
    const panes = $$("[data-pane]", tabs.parentElement);
    $$("button", tabs).forEach(b => b.addEventListener("click", () => {
      $$("button", tabs).forEach(x => x.classList.toggle("active", x === b));
      panes.forEach(p => (p.hidden = p.dataset.pane !== b.dataset.tab));
    }));
  });

  /* ---------------- reveal on scroll ---------------- */
  const io = new IntersectionObserver(entries => entries.forEach(en => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  }), { threshold: 0.12 });
  $$(".reveal-up").forEach(el => io.observe(el));
})();
