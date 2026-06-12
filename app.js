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
