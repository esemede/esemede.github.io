# CV Web Interactivo (esemede.github.io) — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publicar en https://esemede.github.io un CV bilingüe (ES/EN) en HTML/CSS/JS puro con roadmap de experiencia animado por scroll, parallax de cordillera, pelota de tenis rebotando, y descarga de PDF (con QR) desbloqueada al dejar un email vía Formspree.

**Architecture:** Sitio estático de una página: `index.html` (estructura semántica con atributos `data-i18n`), `styles.css` (design tokens, secciones alternadas verde/marfil), `app.js` (toggle idioma, reveals, parallax, pelota ligada a scroll, gate de email) e `i18n.js` (diccionario ES/EN como objeto global). PDFs pre-generados por `scripts/build_pdf.py` (reportlab + qrcode vía `uv run`). Deploy: repo `esemede/esemede.github.io`, rama `main`.

**Tech Stack:** HTML5, CSS3 (custom properties, grid), JS vanilla (IntersectionObserver, rAF), Google Fonts (Fraunces + Inter), Formspree, Python (reportlab, qrcode) vía `uv`.

**Nota de ejecución:** El sitio es creativo-visual; al implementar HTML/CSS invocar el skill `frontend-design:frontend-design`. No hay framework de tests para el front: cada task cierra con verificación manual servida en `http://localhost:8000` (`python3 -m http.server`). La paleta y contenidos de este plan son vinculantes.

**Design tokens (vinculantes):**

```css
:root {
  --green-deep: #0b3d2e;   /* fondo secciones oscuras */
  --green-ink:  #122e26;   /* variante más oscura (hero base) */
  --green-mid:  #1e5c46;   /* capas de montaña / bordes */
  --emerald:    #2e8b6a;   /* acentos, hovers */
  --ball:       #cce531;   /* pelota de tenis, acento puntual */
  --ivory:      #f5f1e8;   /* fondo secciones claras */
  --ivory-card: #fffdf7;   /* tarjetas sobre marfil */
  --ink:        #1c2420;   /* texto sobre claro */
  --ink-soft:   #4a5550;   /* texto secundario */
  --font-display: "Fraunces", serif;
  --font-body: "Inter", sans-serif;
}
```

---

### Task 1: Scaffold del repo y esqueleto navegable

**Files:**
- Create: `index.html`, `styles.css`, `app.js`, `i18n.js` (vacío por ahora), `.nojekyll`, `README.md`

- [ ] **Step 1: Crear `.nojekyll`** (vacío, evita procesamiento Jekyll de GitHub Pages).

- [ ] **Step 2: Crear `index.html` esqueleto** con: `<html lang="es">`, meta viewport, `<title>Sebastián Moreno — Líder Técnico · Backend & Cloud</title>`, meta description, preconnect + link a Google Fonts (Fraunces 600/700 ital, Inter 400/500/700), link `styles.css`, scripts `i18n.js` y `app.js` con `defer`. Body con las 9 secciones vacías en orden y sus ids: `header.site-nav`, `section#hero`, `section#resumen`, `section#roadmap`, `section#skills`, `section#logros`, `section#educacion`, `section#vida`, `section#descarga`, `footer#contacto`. Clases de fondo alternado: `hero`/`skills`/`logros`/`descarga` con clase `sec-dark`; `resumen`/`roadmap`/`educacion`/`vida` con `sec-light`.

- [ ] **Step 3: Crear `styles.css`** solo con los design tokens del header del plan, reset mínimo, `body { font-family: var(--font-body); }`, `.sec-dark { background: var(--green-deep); color: var(--ivory); }`, `.sec-light { background: var(--ivory); color: var(--ink); }`.

- [ ] **Step 4: Crear `README.md`** con: descripción del sitio, instrucción para servir local (`python3 -m http.server 8000`), cómo regenerar PDFs (`uv run --with reportlab --with "qrcode[pil]" scripts/build_pdf.py`), y sección "Configurar Formspree": crear cuenta gratis en formspree.io con domoedse@gmail.com, crear form, copiar el ID en la constante `FORMSPREE_ID` de `app.js`.

- [ ] **Step 5: Verificar** — `python3 -m http.server 8000` y abrir: las franjas alternadas verde/marfil se ven, sin errores de consola.

- [ ] **Step 6: Commit** — `git add -A && git commit -m "feat: scaffold static site skeleton"`.

### Task 2: Diccionario i18n completo (contenido del CV)

**Files:**
- Modify: `i18n.js`

- [ ] **Step 1: Escribir `i18n.js`** definiendo `window.I18N = { es: {...}, en: {...} }`. Contenido vinculante (claves planas; EN es traducción fiel del ES):
  - `nav.*`: resumen/experiencia/skills/educación/contacto + `nav.cta` ("Descargar CV" / "Download CV").
  - `hero.kicker`: "Líder Técnico · Backend & Cloud Developer" / "Tech Lead · Backend & Cloud Developer"; `hero.name`: "Sebastián Moreno"; `hero.tagline`: "Construyo y lidero productos digitales de optimización logística sobre AWS." / "I build and lead logistics-optimization digital products on AWS."; `hero.scroll`: "Desliza para recorrer mi camino" / "Scroll to follow my journey".
  - `resumen.title`: "Resumen" / "Summary"; `resumen.body`: párrafo basado en spec — Ingeniero Mecánico Industrial (USM), 10+ años construyendo software entre energía y consumo masivo; hoy Líder Técnico del optimizador de carga T2 y principal developer de T1 en KOANDINA (Coca-Cola Andina); experto en arquitectura serverless AWS, Python y datos; sello: buenas prácticas, CI/CD, feedback honesto y mejora continua.
  - `roadmap.title`: "Mi roadmap" / "My roadmap"; por cada hito `jobN.period`, `jobN.company`, `jobN.role`, `jobN.b1..bN` con el contenido EXACTO de la spec (7 hitos: KOANDINA T2/T1 con `job1.badge` = "Rol doble" / "Dual role", KOANDINA OTC, KOANDINA IT Senior Dev, SR-Consultores, Phineal con premios, Energio, Inicios).
  - `skills.title` + grupos `skills.cloud/backend/frontend/data/devops/other` con los chips de la spec (los nombres de tecnologías no se traducen).
  - `logros.title`: "Logros" / "Awards"; 4 ítems: Impacto Chile 2021 (ganadores), CAMEXA Energy Challenge México 2020 (ganadores), Blockchain Summit LATAM 2018 (ganador), Actitud Awards 2022 (finalistas).
  - `edu.*`: USM, Ingeniería Mecánica Industrial, 2008–2016; idiomas: Español nativo / Inglés intermedio.
  - `vida.title`: "Más allá del código" / "Beyond the code"; tres ítems: tenis, montaña, familia con una frase cada uno.
  - `descarga.title`: "Llévate mi CV" / "Take my CV with you"; `descarga.hint`: "Déjame tu correo y descarga el PDF (incluye QR a esta página)." / inglés equivalente; `descarga.placeholder`, `descarga.button` ("Desbloquear descarga" / "Unlock download"), `descarga.success`, `descarga.error`, `descarga.dlEs` ("CV en Español (PDF)"), `descarga.dlEn` ("CV in English (PDF)").
  - `footer.*`: email, GitHub, "Hecho a mano con HTML, CSS y JS — verde como la montaña." / equivalente.

- [ ] **Step 2: Verificar** — `node -e "const w={};global.window=w;require('./i18n.js');const es=Object.keys(w.I18N.es),en=Object.keys(w.I18N.en);console.log(es.length===en.length && es.every(k=>en.includes(k)) ? 'OK '+es.length+' claves' : 'MISMATCH')"` → `OK <n> claves`.

- [ ] **Step 3: Commit** — `git commit -am "feat: bilingual ES/EN content dictionary"`.

### Task 3: Markup completo + toggle de idioma

**Files:**
- Modify: `index.html`, `app.js`

- [ ] **Step 1: Markup de todas las secciones** en `index.html`. Reglas: todo texto visible lleva `data-i18n="clave"`; placeholder del input usa `data-i18n-attr="placeholder:descarga.placeholder"`. Nav fija con nombre, anclas y botón `#lang-toggle` (texto "EN"/"ES"). Hero: kicker, `h1`, tagline, contenedor `.mountains` con 3 `<svg>` de cordillera (`.m-back/.m-mid/.m-front`, paths poligonales simples generados a mano, `preserveAspectRatio="none"`). Roadmap: `<div class="road">` con `<svg class="road-path">` (path serpenteante vertical) + `<div class="ball" aria-hidden="true">` + lista `<ol>` de 7 `<li class="milestone">` alternando izquierda/derecha, cada una con period/company/role/bullets (job1 incluye `.badge`). Skills: grupos con `.chip`s. Logros: 4 tarjetas. Educación: tarjeta USM + tabla idiomas. Vida: 3 ítems con iconos SVG inline (pelota, montaña, hogar). Descarga: `<form id="gate-form">` con input email requerido + botón, `<div id="gate-result" hidden>` con los dos enlaces a `assets/cv/CV-Sebastian-Moreno-ES.pdf` y `-EN.pdf` (atributo `download`), `<p id="gate-error" hidden>`. Footer: mailto domoedse@gmail.com + github.com/esemede.

- [ ] **Step 2: Toggle de idioma en `app.js`:**

```js
const LANGS = ["es", "en"];
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
```

- [ ] **Step 3: Verificar** — en local: todo el contenido visible en ES, click en toggle cambia TODO a EN (sin claves huérfanas mostrando undefined), recarga conserva idioma.

- [ ] **Step 4: Commit** — `git commit -am "feat: full CV markup with language toggle"`.

### Task 4: Estilos completos (invocar frontend-design)

**Files:**
- Modify: `styles.css`, `index.html` (solo clases/ajustes menores)

- [ ] **Step 1: Invocar skill `frontend-design:frontend-design`** y escribir el CSS completo respetando tokens y estos requisitos vinculantes: tipografía display Fraunces para `h1/h2/company` (pesos 600–700, óptica editorial), Inter para cuerpo; nav fija translúcida con blur sobre verde; hero 100svh con cordillera en 3 capas al pie; separadores entre secciones con silueta de cordillera (SVG inline como `background-image` o `clip-path`, color de la sección siguiente); milestones como tarjetas `--ivory-card` con sombra suave, borde izquierdo `--emerald`, badge `--ball` para el rol doble; chips redondeados con borde `--green-mid` sobre fondo oscuro; pelota `.ball` = círculo 34px `--ball` con costura SVG (curva blanca) y sombra elíptica `.ball-shadow`; estados `:hover`/`:focus-visible` accesibles (contraste AA: nunca `--ball` como color de texto sobre marfil); responsive: roadmap a una columna bajo 720px, nav colapsa a fila simple, hero compacto.

- [ ] **Step 2: Verificar** — local en 1440px, 768px y 375px (responsive mode): sin overflow horizontal, contraste legible en ambos fondos, fuentes cargan.

- [ ] **Step 3: Commit** — `git commit -am "feat: full visual design, alternating green/ivory sections"`.

### Task 5: Animaciones — reveals, parallax y pelota de tenis

**Files:**
- Modify: `app.js`, `styles.css`

- [ ] **Step 1: Reveals con IntersectionObserver** — añadir a `app.js`:

```js
const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
const io = new IntersectionObserver(
  (entries) => entries.forEach((e) => e.isIntersecting && e.target.classList.add("in")),
  { threshold: 0.15 }
);
document.querySelectorAll(".milestone, .reveal").forEach((el) => {
  if (reduced) el.classList.add("in");
  else io.observe(el);
});
```

CSS: `.milestone, .reveal { opacity: 0; transform: translateY(24px); transition: opacity .6s, transform .6s; } .in { opacity: 1; transform: none; }` envuelto en `@media (prefers-reduced-motion: no-preference)`.

- [ ] **Step 2: Parallax del hero** — en `app.js`, un solo listener `scroll` con rAF-throttle que mueve las capas (skip total si `reduced`):

```js
let ticking = false;
function onScroll() {
  if (ticking || reduced) return;
  ticking = true;
  requestAnimationFrame(() => {
    const y = scrollY;
    document.querySelector(".m-back").style.transform = `translateY(${y * 0.12}px)`;
    document.querySelector(".m-mid").style.transform = `translateY(${y * 0.26}px)`;
    document.querySelector(".m-front").style.transform = `translateY(${y * 0.42}px)`;
    updateBall(y); // Task 5 Step 3
    ticking = false;
  });
}
addEventListener("scroll", onScroll, { passive: true });
```

- [ ] **Step 3: Pelota ligada al scroll** — la pelota recorre verticalmente el roadmap según el progreso de scroll de la sección y rebota horizontalmente entre los lados de los milestones con squash al impacto:

```js
const road = document.getElementById("roadmap");
const ball = document.querySelector(".ball");
const stones = [...document.querySelectorAll(".milestone")];

function updateBall() {
  if (!road || reduced) return;
  const r = road.getBoundingClientRect();
  const total = r.height - innerHeight * 0.6;
  const p = Math.min(1, Math.max(0, (innerHeight * 0.45 - r.top) / total)); // 0..1
  const yPx = p * (road.offsetHeight - 80);
  const seg = Math.min(stones.length - 1, Math.floor(p * stones.length));
  const segP = p * stones.length - seg; // progreso dentro del segmento 0..1
  const fromX = seg % 2 === 0 ? 12 : 88;       // % del ancho: alterna lados
  const toX = seg % 2 === 0 ? 88 : 12;
  const x = fromX + (toX - fromX) * segP;
  const arc = -Math.sin(segP * Math.PI) * 60;   // parábola del bote
  const squash = segP > 0.94 || segP < 0.06 ? "scale(1.18,.82)" : "scale(1)";
  ball.style.transform = `translate(${x}vw, ${yPx + arc}px) ${squash} rotate(${p * 1080}deg)`;
  stones.forEach((s, i) => s.classList.toggle("active", i === seg));
}
```

`.ball` con `position: absolute; top: 0; left: 0; will-change: transform;` dentro de `#roadmap` (que es `position: relative`); `.milestone.active` realza la tarjeta (borde `--ball`, leve scale). Bajo 720px la pelota queda fija al carril izquierdo (`fromX/toX = 6`), solo bote vertical. Si `reduced`: `.ball { display: none }`.

- [ ] **Step 4: Verificar** — scroll completo: capas del hero se desplazan a distinta velocidad, pelota recorre el roadmap rebotando lado a lado con squash en impactos, milestone activo se realza, 60fps aprox (sin jank visible), con reduced-motion activado (emular en devtools) nada se anima y la pelota no aparece.

- [ ] **Step 5: Commit** — `git commit -am "feat: scroll animations - parallax, reveals, bouncing tennis ball"`.

### Task 6: Gate de email con Formspree

**Files:**
- Modify: `app.js`

- [ ] **Step 1: Lógica del gate** en `app.js`:

```js
const FORMSPREE_ID = "TU_FORM_ID"; // ver README: reemplazar al crear el form
const form = document.getElementById("gate-form");
const result = document.getElementById("gate-result");
const errBox = document.getElementById("gate-error");

function unlock() {
  form.hidden = true;
  result.hidden = false;
  localStorage.setItem("cv-unlocked", "1");
}
if (localStorage.getItem("cv-unlocked")) unlock();

form.addEventListener("submit", async (e) => {
  e.preventDefault();
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
```

- [ ] **Step 2: Verificar** — con el placeholder el POST falla: debe aparecer el mensaje de error amable y el botón rehabilitarse. Simular éxito en consola (`localStorage.setItem("cv-unlocked","1"); location.reload()`): aparecen los dos botones de descarga y el formulario queda oculto; persiste tras recargar.

- [ ] **Step 3: Commit** — `git commit -am "feat: email gate via Formspree unlocking PDF downloads"`.

### Task 7: Script de PDFs con QR + assets

**Files:**
- Create: `scripts/build_pdf.py`, `assets/cv/CV-Sebastian-Moreno-ES.pdf`, `assets/cv/CV-Sebastian-Moreno-EN.pdf`

- [ ] **Step 1: Escribir `scripts/build_pdf.py`** — Python con reportlab (canvas A4) + qrcode. Estructura: constante `DATA = {"es": {...}, "en": {...}}` replicando el contenido de `i18n.js` en forma compacta de CV de 2 páginas (resumen, experiencia con bullets, skills, educación, idiomas, premios); paleta del plan (`HexColor("#0b3d2e")` etc.); layout: banda superior verde con nombre/título en blanco y QR (generado con `qrcode.make("https://esemede.github.io")`, pegado vía `ImageReader`) en la esquina superior derecha con la leyenda "Versión interactiva" / "Interactive version"; cuerpo a dos columnas (izquierda 65%: experiencia; derecha 35%: skills/educación/idiomas/premios) sobre fondo marfil; footer con email y URL. Función `build(lang, path)` llamada para `es` y `en`.

- [ ] **Step 2: Generar** — `uv run --with reportlab --with "qrcode[pil]" scripts/build_pdf.py` → crea ambos PDFs en `assets/cv/`.

- [ ] **Step 3: Verificar** — abrir ambos PDFs (`open assets/cv/*.pdf`): 2 páginas máx, sin texto cortado ni solapado, QR presente; escanear el QR con el teléfono (o decodificar: `uv run --with "qreader" ...` opcional) → apunta a https://esemede.github.io.

- [ ] **Step 4: Commit** — `git add -A && git commit -m "feat: PDF CVs (ES/EN) with QR code + build script"`.

### Task 8: Verificación integral local

- [ ] **Step 1: Recorrido completo** en `http://localhost:8000`: nav ancla a cada sección; toggle ES/EN cambia todo (incluida la sección descarga y placeholders); animaciones según Task 5; gate según Task 6; enlaces de descarga bajan los PDFs correctos; footer mailto y GitHub correctos.
- [ ] **Step 2: Responsive + accesibilidad** — 375px sin overflow; tab-navegación con focus visible; `prefers-reduced-motion` estático.
- [ ] **Step 3: Consola limpia** — cero errores JS en carga y scroll completo.
- [ ] **Step 4: Commit de ajustes** si los hubo — `git commit -am "fix: polish from full local review"`.

### Task 9: Publicación en GitHub Pages

- [ ] **Step 1: Cambiar cuenta gh** — `gh auth switch -u esemede` y confirmar con `gh auth status`.
- [ ] **Step 2: Crear repo y push** — `gh repo create esemede.github.io --public --source . --remote origin --push` (si el remote ya existe: `git push -u origin main`).
- [ ] **Step 3: Verificar Pages** — `gh api repos/esemede/esemede.github.io/pages` debe responder (user pages se habilita solo); esperar build: `curl -sI https://esemede.github.io | head -1` → `HTTP/2 200` (reintentar ~2 min).
- [ ] **Step 4: Smoke test en producción** — abrir https://esemede.github.io: contenido, animaciones y descarga de PDFs funcionan; escanear QR del PDF descargado → vuelve a la página.
- [ ] **Step 5: Restaurar cuenta gh original** — `gh auth switch -u semoreno_ANDINA`.

### Task 10: Pendiente del usuario (documentado, no bloqueante)

- [ ] **Step 1: Confirmar en README** la sección Formspree (creada en Task 1) y dejar nota final al usuario: crear el form en formspree.io, reemplazar `FORMSPREE_ID` en `app.js`, commit + push.

## Self-review

- **Cobertura de spec:** estructura/contenido (T2–T3), visual híbrido (T4), parallax+pelota+reveals+reduced-motion (T5), gate Formspree (T6), PDFs con QR (T7), verificación (T8), deploy (T9), placeholder Formspree documentado (T1/T10). Sin huecos.
- **Placeholders:** solo `FORMSPREE_ID`, intencional y documentado (depende de acción del usuario).
- **Consistencia:** ids/clases (`#roadmap`, `.milestone`, `.ball`, `#gate-form`, `#gate-result`, `#gate-error`, `#lang-toggle`) coinciden entre T3, T5 y T6; rutas de PDFs coinciden entre T3 y T7.
