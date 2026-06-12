# esemede.github.io — CV interactivo de Sebastián Moreno

CV bilingüe (ES/EN) en HTML/CSS/JS puro: roadmap de experiencia animado por
scroll, parallax de cordillera, una pelota de tenis que recorre la página y
descarga del CV en PDF (con código QR) a cambio de un correo.

## Desarrollo local

```bash
python3 -m http.server 8000
# abrir http://localhost:8000
```

Sin build, sin dependencias: editar y recargar.

## Regenerar los PDFs

Los PDFs de `assets/cv/` se generan con un script reproducible (requiere
[uv](https://docs.astral.sh/uv/)):

```bash
uv run --with reportlab --with "qrcode[pil]" scripts/build_pdf.py
```

El contenido del PDF vive en `scripts/build_pdf.py` (`DATA`); si cambias el CV
en `i18n.js`, actualiza también ahí y regenera.

## Configurar Formspree (captura de email)

La descarga del PDF se desbloquea cuando el visitante deja su correo. El envío
usa [Formspree](https://formspree.io) (plan gratis: 50 envíos/mes):

1. Crear cuenta en formspree.io con `domoedse@gmail.com`.
2. Crear un nuevo form ("New form") y copiar su ID (la parte final de
   `https://formspree.io/f/XXXXXXXX`).
3. Reemplazar el valor de la constante `FORMSPREE_ID` en `app.js`.
4. Commit y push.

Mientras el ID sea el placeholder, el formulario mostrará el mensaje de error
al enviar (el resto del sitio funciona normal).

## Estructura

```
index.html        # única página
styles.css        # design tokens + estilos
app.js            # idioma, parallax, pelota, reveals, gate de email
i18n.js           # diccionario ES/EN
assets/           # SVGs, favicon, PDFs en assets/cv/
scripts/build_pdf.py
docs/superpowers/ # spec y plan de este proyecto
```
