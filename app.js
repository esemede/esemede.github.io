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

/* Parallax del hero */
const mBack = document.querySelector(".m-back");
const mMid = document.querySelector(".m-mid");
const mFront = document.querySelector(".m-front");

/* Pelota de tenis ligada al scroll del roadmap */
const road = document.querySelector("#roadmap .road");
const ball = document.querySelector(".ball");
const stones = [...document.querySelectorAll(".milestone")];
const isMobile = matchMedia("(max-width: 720px)");

function updateBall() {
  if (!road || !stones.length) return;
  const r = road.getBoundingClientRect();
  const anchor = innerHeight * 0.45; // punto de lectura en el viewport
  const total = r.height - 160;
  const p = Math.min(1, Math.max(0, (anchor - r.top) / total));

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
