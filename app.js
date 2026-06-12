/* ---------- Idioma ---------- */
let lang = localStorage.getItem("cv-lang") || "es";

function applyLang() {
  document.documentElement.lang = lang;
  const dict = window.I18N[lang];
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const v = dict[el.dataset.i18n];
    if (v !== undefined) el.innerHTML = v;
  });
  document.querySelectorAll("[data-i18n-attr]").forEach((el) => {
    const [attr, key] = el.dataset.i18nAttr.split(":");
    if (dict[key] !== undefined) el.setAttribute(attr, dict[key]);
  });
  document.getElementById("lang-toggle").textContent = lang === "es" ? "EN" : "ES";
}

document.getElementById("lang-toggle").addEventListener("click", () => {
  lang = lang === "es" ? "en" : "es";
  localStorage.setItem("cv-lang", lang);
  applyLang();
});
applyLang();

/* ---------- Tema claro/oscuro ---------- */
const isDark = () => document.documentElement.dataset.theme === "dark";

document.getElementById("theme-toggle").addEventListener("click", () => {
  const next = isDark() ? "light" : "dark";
  document.documentElement.dataset.theme = next;
  localStorage.setItem("cv-theme", next);
});

/* ---------- Animaciones ---------- */
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;

/* Reveals */
const io = new IntersectionObserver(
  (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
  { threshold: 0.15 }
);
document.querySelectorAll(".milestone, .reveal").forEach((el) => {
  if (reduced) el.classList.add("in");
  else io.observe(el);
});

/* Scroll-spy del nav */
const navLinks = [...document.querySelectorAll(".nav-links a")];
const spy = new IntersectionObserver(
  (entries) => entries.forEach((e) => {
    if (!e.isIntersecting) return;
    const id = "#" + e.target.id;
    navLinks.forEach((a) => a.classList.toggle(
      "active",
      a.getAttribute("href") === id ||
        (id === "#vida" && a.getAttribute("href") === "#educacion") ||
        (id === "#logros" && a.getAttribute("href") === "#skills")
    ));
  }),
  { rootMargin: "-40% 0px -55% 0px" }
);
["resumen", "roadmap", "skills", "logros", "educacion", "vida", "contacto"]
  .forEach((id) => spy.observe(document.getElementById(id)));

/* Parallax del hero */
const mBack = document.querySelector(".m-back");
const mMid = document.querySelector(".m-mid");
const mFront = document.querySelector(".m-front");

/* Pelota de tenis ligada al scroll del roadmap */
const road = document.querySelector("#roadmap .road");
const court = document.querySelector(".court");
const ball = document.querySelector(".ball");
const stones = [...document.querySelectorAll(".milestone")];
const isMobile = matchMedia("(max-width: 720px)");

function updateBall() {
  if (!road || !stones.length) return;
  const r = road.getBoundingClientRect();
  const anchor = innerHeight * 0.45; // punto de lectura en el viewport
  const total = r.height - 160;
  const p = Math.min(1, Math.max(0, (anchor - r.top) / total));

  // la cancha se desplaza más lento que el scroll (parallax de fondo)
  if (court) court.style.transform = `translateY(${(p - 0.5) * 130}px)`;

  const nSeg = stones.length - 1;
  const segF = p * nSeg;
  const seg = Math.min(nSeg - 1, Math.floor(segF));
  const segP = segF - seg; // 0..1 dentro del segmento

  // nodos: la pelota viaja de hito en hito por la línea del camino
  const nodeY = (s) => s.offsetTop + 35;
  const lineX = isMobile.matches ? 16 : road.offsetWidth / 2;
  const y = nodeY(stones[seg]) + (nodeY(stones[seg + 1]) - nodeY(stones[seg])) * segP;

  // arco lateral hacia el lado de la tarjeta destino + bote vertical
  const target = stones[seg + 1];
  const sideSign = isMobile.matches ? 1 : (target.classList.contains("side-l") ? -1 : 1);
  const sway = Math.sin(segP * Math.PI) * (isMobile.matches ? 0 : Math.min(140, road.offsetWidth * 0.16)) * sideSign;
  const hop = -Math.abs(Math.sin(segP * Math.PI)) * 70;

  const landing = segP > 0.93 || segP < 0.07;
  const squash = landing ? " scale(1.22, 0.78)" : "";
  ball.style.transform =
    `translate(${lineX - 17 + sway}px, ${y + hop}px) rotate(${p * 1080}deg)${squash}`;

  const activeIdx = Math.round(segF);
  stones.forEach((s, i) => s.classList.toggle("active", i === activeIdx));
}

let ticking = false;
function onScroll() {
  if (ticking) return;
  ticking = true;
  requestAnimationFrame(() => {
    const y = scrollY;
    if (mBack) {
      mBack.style.transform = `translateY(${y * 0.12}px)`;
      mMid.style.transform = `translateY(${y * 0.26}px)`;
      mFront.style.transform = `translateY(${y * 0.42}px)`;
    }
    updateBall();
    ticking = false;
  });
}

if (!reduced) {
  addEventListener("scroll", onScroll, { passive: true });
  addEventListener("resize", onScroll, { passive: true });
  onScroll();
}

/* ---------- Redes de nodos (canvas) ---------- */
/* Partículas que derivan, se enlazan entre sí y reaccionan al cursor.
   `bands()` limita dónde viven (p. ej., fuera de la cancha del roadmap). */
function startNet(canvas, opts) {
  const ctx = canvas.getContext("2d");
  const dpr = Math.min(devicePixelRatio || 1, 2);
  const section = canvas.parentElement;
  let W = 0, H = 0, parts = [], running = false, raf = 0;
  const mouse = { x: -1e4, y: -1e4 };
  const LINK = opts.link || 120;

  function resize() {
    W = section.offsetWidth;
    H = section.offsetHeight;
    canvas.width = W * dpr;
    canvas.height = H * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    parts = [];
    if (W < 720) return; // en móvil no hay red: ahorro de batería
    for (const [x0, x1] of opts.bands(W)) {
      if (x1 - x0 < 70) continue;
      const n = Math.min(opts.max, Math.round(((x1 - x0) * H) / 16000));
      for (let i = 0; i < n; i++) {
        parts.push({
          x: x0 + Math.random() * (x1 - x0), y: Math.random() * H,
          vx: (Math.random() - 0.5) * 0.45, vy: (Math.random() - 0.5) * 0.45,
          x0, x1, r: 1.3 + Math.random() * 1.2,
        });
      }
    }
  }

  function step() {
    if (!running) return;
    ctx.clearRect(0, 0, W, H);
    for (const p of parts) {
      p.x += p.vx; p.y += p.vy;
      if (p.x < p.x0 || p.x > p.x1) p.vx *= -1;
      if (p.y < 0 || p.y > H) p.vy *= -1;
      const dxm = p.x - mouse.x, dym = p.y - mouse.y;
      const dm = Math.hypot(dxm, dym);
      if (dm < 150 && dm > 0.1) { // el cursor empuja suavemente los nodos
        p.x += (dxm / dm) * 0.6;
        p.y += (dym / dm) * 0.6;
      }
    }
    ctx.lineWidth = 1;
    for (let i = 0; i < parts.length; i++) {
      const a = parts[i];
      for (let j = i + 1; j < parts.length; j++) {
        const b = parts[j];
        if (a.x0 !== b.x0) continue; // no se enlaza a través de la cancha
        const d = Math.hypot(a.x - b.x, a.y - b.y);
        if (d < LINK) {
          ctx.strokeStyle = opts.line(1 - d / LINK);
          ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke();
        }
      }
      const dm = Math.hypot(a.x - mouse.x, a.y - mouse.y);
      if (dm < 160) {
        ctx.strokeStyle = opts.line(0.9 * (1 - dm / 160));
        ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke();
      }
      ctx.fillStyle = typeof opts.dot === "function" ? opts.dot() : opts.dot;
      ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 7); ctx.fill();
    }
    raf = requestAnimationFrame(step);
  }

  section.addEventListener("mousemove", (e) => {
    const r = canvas.getBoundingClientRect();
    mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top;
  });
  section.addEventListener("mouseleave", () => { mouse.x = mouse.y = -1e4; });

  new IntersectionObserver((es) => es.forEach((e) => {
    if (e.isIntersecting && !running) { running = true; step(); }
    else if (!e.isIntersecting) { running = false; cancelAnimationFrame(raf); }
  })).observe(section);

  new ResizeObserver(resize).observe(section);
  resize();
}

if (!reduced) {
  const netHero = document.getElementById("net-hero");
  if (netHero) startNet(netHero, {
    max: 70,
    link: 130,
    dot: "rgba(204, 229, 49, 0.55)",
    line: (a) => `rgba(46, 139, 106, ${0.38 * a})`,
    bands: (w) => [[0, w]],
  });

  const netRoad = document.getElementById("net-road");
  if (netRoad) startNet(netRoad, {
    max: 55,
    link: 110,
    dot: () => isDark() ? "rgba(143, 212, 178, 0.55)" : "rgba(46, 139, 106, 0.5)",
    line: (a) => isDark() ? `rgba(143, 212, 178, ${0.22 * a})` : `rgba(30, 92, 70, ${0.2 * a})`,
    bands: (w) => {
      // bandas laterales: el espacio fuera de la cancha de tenis
      const courtW = Math.min(road ? road.offsetWidth : w * 0.92, 920);
      const gap = (w - courtW) / 2 - 24;
      return [[16, gap], [w - gap, w - 16]];
    },
  });
}

/* ---------- Gate de email (Formspree) ---------- */
const FORMSPREE_ID = "xjgdaaag";
const form = document.getElementById("gate-form");
const result = document.getElementById("gate-result");
const errBox = document.getElementById("gate-error");

function unlock() {
  form.hidden = true;
  errBox.hidden = true;
  result.hidden = false;
  localStorage.setItem("cv-unlocked", "1");
}
if (localStorage.getItem("cv-unlocked")) unlock();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  if (!form.reportValidity()) return;
  errBox.hidden = true;
  const btn = form.querySelector("button");
  btn.disabled = true;
  try {
    const res = await fetch(`https://formspree.io/f/${FORMSPREE_ID}`, {
      method: "POST",
      headers: { Accept: "application/json" },
      body: new FormData(form),
    });
    if (!res.ok) throw new Error(res.status);
    unlock();
  } catch {
    errBox.hidden = false;
  } finally {
    btn.disabled = false;
  }
});
