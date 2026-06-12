# Spec: CV web interactivo — esemede.github.io

**Fecha:** 2026-06-12
**Estado:** Aprobado por el usuario (diseño conversado y validado)

## Objetivo

Página personal de GitHub Pages con el currículum de Sebastián Moreno: diseño
moderno y elegante en verde oscuro, roadmap de experiencia animado con scroll,
parallax de cordillera y una pelota de tenis que rebota por la página. Permite
descargar el CV en PDF (con código QR a la página) a cambio de dejar un correo.

## Decisiones tomadas

| Tema | Decisión |
|---|---|
| Repositorio / URL | `esemede/esemede.github.io` → https://esemede.github.io (cuenta gh `esemede`) |
| Stack | HTML/CSS/JS puro, sin build ni frameworks |
| Idiomas | Bilingüe ES/EN con toggle en la página (persistido en localStorage) |
| Captura de email | Formspree vía fetch/AJAX; form ID con placeholder hasta que el usuario cree la cuenta |
| PDF | Pre-generado (ES y EN) con script reproducible en el repo; QR embebido apuntando a la página |
| Contacto público | Solo email `domoedse@gmail.com` + enlace a GitHub |
| Dirección visual | Híbrido alternado: secciones verde oscuro ↔ marfil; verde oscuro protagonista |

## Contenido (fuente: CV Word existente + información del usuario)

### Identidad
- **Nombre:** Sebastián Moreno
- **Título:** Líder Técnico · Backend & Cloud Developer (AWS)
- **Perfil:** Ingeniero Mecánico Industrial (U. Técnica Federico Santa María,
  2008–2016) con 10+ años construyendo software; hoy lidera productos digitales
  de optimización logística en KOANDINA (Coca-Cola Andina). Experiencia en
  arquitectura serverless AWS/GCP, Python, datos y blockchain.

### Roadmap de experiencia (orden descendente)
1. **Ago 2025 – actualidad · KOANDINA — Líder Técnico T2 + Principal Developer T1** (rol doble, destacado con badge)
   - T2: liderazgo técnico del optimizador de carga de camiones desde Centros de Distribución hacia clientes.
   - T1: principal developer del producto de optimización de carga entre centros de distribución mediante bolsa de productos y flota de camiones.
2. **Ago 2024 – Ago 2025 · KOANDINA, célula OTC — Senior Developer**
   - Backend serverless en AWS con Step Functions (sin frontend).
   - API con FastAPI para consumir la data de la base de datos.
3. **Oct 2023 – Ago 2024 · KOANDINA — IT Senior Developer**
   - Mismo producto del optimizador de carga regional, ahora interno.
4. **Sep 2022 – Sep 2023 · SR-Consultores — Consultor Fullstack Developer** (remoto, Chile)
   - Optimizador regional de armado de pallets para Coca-Cola Andina (Python).
   - Arquitectura serverless AWS: Lambdas, API Gateway, RDS, DynamoDB, CloudWatch, CloudFormation, Cognito.
   - Módulos UI/UX en React.
5. **Dic 2018 – Ago 2022 · Phineal — Ingeniero de Desarrollos** (remoto, Chile)
   - Telemetría certificada con blockchain de datos energéticos en sistemas solares fotovoltaicos; red blockchain GTIME; plataformas MERN/PERN en tiempo real; data engineering con Pandas/PySpark; smart contracts (oráculo EVM↔GTIME).
   - Premios: Ganadores "Impacto Chile" 2021, CAMEXA Energy Challenge México 2020, finalistas "Actitud Awards" 2022.
6. **May 2018 – Dic 2018 · Energio — Ingeniero de Desarrollos** (Santiago)
   - Smart contract energético en NEO; flujos de potencia con medidores IoT vía MQTT. Ganador desafío Blockchain Summit LATAM 2018.
7. **Nodo compacto "Inicios" (2010–2015):** CODELCO (memorista y práctica), Griferías Cobra, Arauco, iParty (programador web PHP).

### Otras secciones
- **Skills (chips agrupados):** Cloud (AWS: Lambda, Step Functions, API Gateway, RDS, DynamoDB, Cognito; GCP), Backend (Python, FastAPI, Node.js), Frontend (React), Datos (SQL/NoSQL, Pandas, PySpark), DevOps (CI/CD), Blockchain/IoT (resumen).
- **Logros:** strip de premios (sección verde oscuro).
- **Educación e idiomas:** USM Ingeniería Mecánica Industrial 2008–2016; Español nativo, Inglés intermedio.
- **"Más allá del código":** tenis, montaña, familia (iconos sutiles; conecta con la pelota y la cordillera del diseño).
- **Descarga CV:** sección con formulario de email → desbloquea PDFs.
- **Footer:** email y GitHub.

## Diseño visual

- **Paleta:** verde bosque profundo (base ~#0B3D2E / #122E26), marfil (~#F5F1E8),
  acento esmeralda y amarillo-verde "pelota de tenis" (~#CCE531) usado con
  moderación (la pelota, hovers, detalles).
- **Tipografía:** serif display para nombre/títulos (p. ej. Fraunces o similar
  vía Google Fonts) + sans legible para cuerpo (p. ej. Inter).
- **Layout:** secciones alternadas verde oscuro ↔ marfil con transiciones
  (separadores con silueta de cordillera). Responsive mobile-first.

## Animaciones e interacción

- **Hero parallax:** cordillera en 3 capas SVG que se desplazan a velocidades
  distintas con el scroll (requestAnimationFrame + transform).
- **Roadmap + pelota de tenis:** timeline serpenteante (path SVG). Una pelota
  de tenis ligada al progreso de scroll recorre el path, rebota en cada hito
  (squash & stretch al impacto) y cruza las transiciones de sección.
- **Reveals:** IntersectionObserver para aparición de tarjetas/secciones.
- **Accesibilidad:** `prefers-reduced-motion` desactiva parallax y pelota
  (timeline estático). En móvil, versión simplificada de la pelota.

## PDF con QR

- Script reproducible `scripts/build_pdf.py` (Python) que genera
  `assets/cv/CV-Sebastian-Moreno-ES.pdf` y `...-EN.pdf` con diseño a juego
  (paleta verde/marfil) y un código QR hacia https://esemede.github.io.
- Los PDFs se commitean al repo (descarga estática instantánea).

## Gate de email (Formspree)

1. Visitante ingresa su email en el formulario (validación HTML5 + JS).
2. `fetch` POST a `https://formspree.io/f/<FORM_ID>`.
3. Respuesta 200 → se muestran los botones de descarga (PDF del idioma activo
   primero) y se guarda flag en localStorage para no volver a pedirlo.
4. Error → mensaje amable con reintento.
- `FORM_ID` queda como placeholder constante en `app.js`, documentado en el
  README; el usuario crea el form gratis en formspree.io con domoedse@gmail.com.
- Limitación aceptada: al ser sitio estático, la URL del PDF es descubrible;
  el gate es disuasivo, no de seguridad.

## Estructura del repo

```
index.html        # única página
styles.css
app.js            # parallax, pelota, reveals, gate, toggle idioma
i18n.js           # diccionario ES/EN
assets/           # SVGs (cordillera, pelota), favicon, PDFs en assets/cv/
scripts/build_pdf.py
README.md         # cómo regenerar PDFs y configurar Formspree
docs/superpowers/ # specs y planes
```

Los archivos fuente de Word (`_Sebastian-Moreno-CV.html` y `.fld/`) quedan en
`.gitignore` (no se publican).

## Despliegue

- `git init` en esta carpeta, repo `esemede/esemede.github.io` creado con
  `gh` autenticado como `esemede` (`gh auth switch`), push a `main`.
- GitHub Pages de usuario se activa automáticamente sirviendo `main`.

## Pruebas / verificación

- Servir localmente (`python -m http.server`) y verificar: toggle de idioma,
  animaciones, gate (con Formspree en modo test o placeholder), descarga PDF,
  responsive (viewport móvil), `prefers-reduced-motion`.
- Validar que los PDFs abren y el QR escanea hacia la URL correcta.
- Tras el push, verificar la URL pública.

## Fuera de alcance

- Analytics, dominio propio, blog, modo claro/oscuro conmutables, backend propio.
