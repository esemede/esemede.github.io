#!/usr/bin/env python3
"""Genera los CV en PDF (ES/EN) con código QR hacia la página.

Uso:
    uv run --with reportlab --with "qrcode[pil]" scripts/build_pdf.py

El contenido debe mantenerse alineado con i18n.js.
"""
from pathlib import Path

import qrcode
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen.canvas import Canvas

GREEN_DEEP = HexColor("#0b3d2e")
GREEN_INK = HexColor("#122e26")
GREEN_MID = HexColor("#1e5c46")
EMERALD = HexColor("#2e8b6a")
BALL = HexColor("#cce531")
IVORY = HexColor("#f5f1e8")
INK = HexColor("#1c2420")
INK_SOFT = HexColor("#4a5550")

SITE_URL = "https://esemede.github.io"
OUT_DIR = Path(__file__).resolve().parent.parent / "assets" / "cv"

W, H = A4  # 595 x 842 pt
MARGIN = 40
HEADER_H = 110
LEFT_W = 330  # columna principal
RIGHT_X = MARGIN + LEFT_W + 18

DATA = {
    "es": {
        "name": "Sebastián Moreno",
        "title": "Líder Técnico · Frontend, Backend & Cloud Developer",
        "qr_caption": "Versión interactiva",
        "summary_title": "Resumen",
        "summary": (
            "Ingeniero Mecánico Industrial (UTFSM) con más de 10 años construyendo software "
            "entre la energía y el consumo masivo. Hoy, Líder Técnico del optimizador de carga T2 "
            "y principal developer de T1 en KOANDINA (Coca-Cola Andina): soluciones de optimización "
            "logística sobre arquitectura serverless en AWS. Experto en Python, datos SQL, CI/CD y "
            "patrones de diseño. Integro IA aplicada en mis productos: MCPs, RAG y fine-tuning."
        ),
        "exp_title": "Experiencia",
        "jobs": [
            ("Ago 2025 — Actualidad", "KOANDINA · Coca-Cola Andina",
             "Líder Técnico T2 · Principal Developer T1", [
                 "Liderazgo técnico de T2, optimizador de carga de camiones de Centros de Distribución a clientes.",
                 "Principal developer de T1: optimización de carga entre CDs con bolsa de productos y flota.",
                 "Arquitectura serverless AWS y dirección técnica en la célula del Optimizador.",
             ]),
            ("Ago 2024 — Ago 2025", "KOANDINA · célula OTC", "Senior Developer", [
                 "Backend serverless en AWS orquestado con Step Functions (sin frontend).",
                 "API con FastAPI para consumir la data de la base de datos.",
             ]),
            ("Oct 2023 — Ago 2024", "KOANDINA · Coca-Cola Andina", "IT Senior Developer", [
                 "Desarrollo del optimizador de carga regional como parte del equipo interno.",
             ]),
            ("Sep 2022 — Sep 2023", "SR-Consultores", "Consultor Fullstack Developer", [
                 "Optimizador regional de pallets para Coca-Cola Andina (Python, React).",
                 "Serverless AWS: Lambdas, API Gateway, RDS, DynamoDB, Cognito, CloudFormation.",
             ]),
            ("Dic 2018 — Ago 2022", "Phineal", "Ingeniero de Desarrollos", [
                 "Telemetría certificada con blockchain de datos energéticos en plantas solares.",
                 "Plataformas en tiempo real (MERN/PERN); data engineering con Pandas y PySpark.",
                 "Impacto Chile 2021 y CAMEXA Energy Challenge 2020 (ganadores).",
             ]),
            ("May 2018 — Dic 2018", "Energio", "Ingeniero de Desarrollos", [
                 "Smart contract energético en NEO; medidores IoT vía MQTT.",
                 "Ganador desafío de energía, Blockchain Summit LATAM 2018.",
             ]),
            ("2010 — 2015", "Inicios — CODELCO · Arauco · iParty", "Ingeniería mecánica y primeros scripts", [
                 "Memorista y practicante en CODELCO; macros VBA y scripts PHP integrados a un ERP.",
             ]),
        ],
        "skills_title": "Skills",
        "skills": [
            ("Cloud", "AWS (Lambda, Step Functions, API Gateway, RDS, DynamoDB, Cognito) · GCP"),
            ("Backend", "Python · FastAPI · Node.js"),
            ("Frontend", "React · HTML/CSS · JS"),
            ("IA aplicada", "MCP · RAG · Fine-Tuning · LLM APIs · AI Agents"),
            ("Datos", "SQL · PostgreSQL · MySQL · DynamoDB · Pandas · PySpark"),
            ("DevOps", "CI/CD · Git · Bash · Linux"),
            ("Blockchain & IoT", "Smart Contracts · EVM · MQTT · ESP32"),
        ],
        "edu_title": "Educación",
        "edu": ["Ingeniería Mecánica Industrial", "U. Técnica Federico Santa María", "2008 — 2016"],
        "lang_title": "Idiomas",
        "langs": ["Español — Nativo", "Inglés — Intermedio"],
        "awards_title": "Logros",
        "awards": [
            "Impacto Chile 2021 — Ganadores",
            "CAMEXA Energy Challenge 2020 — Ganadores",
            "Blockchain Summit LATAM 2018 — Ganador",
            "Actitud Awards 2022 — Finalistas",
        ],
        "contact": "domoedse@gmail.com · github.com/esemede",
        "filename": "CV-Sebastian-Moreno-ES.pdf",
    },
    "en": {
        "name": "Sebastián Moreno",
        "title": "Tech Lead · Frontend, Backend & Cloud Developer",
        "qr_caption": "Interactive version",
        "summary_title": "Summary",
        "summary": (
            "Industrial Mechanical Engineer (UTFSM) with 10+ years building software across the "
            "energy and consumer-goods industries. Currently Tech Lead of the T2 load optimizer and "
            "principal developer of T1 at KOANDINA (Coca-Cola Andina): logistics-optimization "
            "solutions on AWS serverless architecture. Expert in Python, SQL data, CI/CD and design "
            "patterns. I integrate applied AI into my products: MCPs, RAG and fine-tuning."
        ),
        "exp_title": "Experience",
        "jobs": [
            ("Aug 2025 — Present", "KOANDINA · Coca-Cola Andina",
             "Tech Lead T2 · Principal Developer T1", [
                 "Technical lead of T2, the truck-load optimizer from Distribution Centers to customers.",
                 "Principal developer of T1: load optimization between DCs using a product pool and fleet.",
                 "AWS serverless architecture and technical direction within the Optimizer cell.",
             ]),
            ("Aug 2024 — Aug 2025", "KOANDINA · OTC cell", "Senior Developer", [
                 "Serverless AWS backend orchestrated with Step Functions (no frontend).",
                 "FastAPI API to serve data from the database.",
             ]),
            ("Oct 2023 — Aug 2024", "KOANDINA · Coca-Cola Andina", "IT Senior Developer", [
                 "Development of the regional load optimizer as part of the in-house team.",
             ]),
            ("Sep 2022 — Sep 2023", "SR-Consultores", "Fullstack Developer Consultant", [
                 "Regional pallet optimizer for Coca-Cola Andina (Python, React).",
                 "Serverless AWS: Lambdas, API Gateway, RDS, DynamoDB, Cognito, CloudFormation.",
             ]),
            ("Dec 2018 — Aug 2022", "Phineal", "Development Engineer", [
                 "Blockchain-certified telemetry of energy data in solar plants.",
                 "Real-time platforms (MERN/PERN); data engineering with Pandas and PySpark.",
                 "Impacto Chile 2021 and CAMEXA Energy Challenge 2020 (winners).",
             ]),
            ("May 2018 — Dec 2018", "Energio", "Development Engineer", [
                 "Energy smart contract on NEO; IoT meters over MQTT.",
                 "Winner, energy challenge, Blockchain Summit LATAM 2018.",
             ]),
            ("2010 — 2015", "Early days — CODELCO · Arauco · iParty", "Mechanical engineering & first scripts", [
                 "Thesis student and intern at CODELCO; VBA macros and PHP scripts integrated with an ERP.",
             ]),
        ],
        "skills_title": "Skills",
        "skills": [
            ("Cloud", "AWS (Lambda, Step Functions, API Gateway, RDS, DynamoDB, Cognito) · GCP"),
            ("Backend", "Python · FastAPI · Node.js"),
            ("Frontend", "React · HTML/CSS · JS"),
            ("Applied AI", "MCP · RAG · Fine-Tuning · LLM APIs · AI Agents"),
            ("Data", "SQL · PostgreSQL · MySQL · DynamoDB · Pandas · PySpark"),
            ("DevOps", "CI/CD · Git · Bash · Linux"),
            ("Blockchain & IoT", "Smart Contracts · EVM · MQTT · ESP32"),
        ],
        "edu_title": "Education",
        "edu": ["Industrial Mechanical Engineering", "U. Técnica Federico Santa María", "2008 — 2016"],
        "lang_title": "Languages",
        "langs": ["Spanish — Native", "English — Intermediate"],
        "awards_title": "Awards",
        "awards": [
            "Impacto Chile 2021 — Winners",
            "CAMEXA Energy Challenge 2020 — Winners",
            "Blockchain Summit LATAM 2018 — Winner",
            "Actitud Awards 2022 — Finalists",
        ],
        "contact": "domoedse@gmail.com · github.com/esemede",
        "filename": "CV-Sebastian-Moreno-EN.pdf",
    },
}


def wrap(c, text, font, size, max_w):
    words, lines, line = text.split(), [], ""
    for w in words:
        probe = f"{line} {w}".strip()
        if c.stringWidth(probe, font, size) <= max_w:
            line = probe
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def make_qr():
    qr = qrcode.QRCode(border=1, box_size=8)
    qr.add_data(SITE_URL)
    qr.make(fit=True)
    return qr.make_image(fill_color="#122e26", back_color="white").get_image()


def header(c, d, qr_img):
    c.setFillColor(GREEN_DEEP)
    c.rect(0, H - HEADER_H, W, HEADER_H, fill=1, stroke=0)
    # picos de cordillera en la base de la banda
    c.setFillColor(GREEN_MID)
    base = H - HEADER_H
    for x0 in range(0, int(W) + 80, 80):
        p = c.beginPath()
        p.moveTo(x0 - 40, base)
        p.lineTo(x0, base + 14)
        p.lineTo(x0 + 40, base)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    c.setFillColor(IVORY)
    c.setFont("Times-BoldItalic", 30)
    c.drawString(MARGIN, H - 52, d["name"])
    c.setFillColor(BALL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(MARGIN, H - 72, d["title"].upper())

    qr_size = 64
    c.drawImage(ImageReader(qr_img), W - MARGIN - qr_size, H - 24 - qr_size,
                qr_size, qr_size)
    c.setFillColor(IVORY)
    c.setFont("Helvetica", 6.5)
    c.drawCentredString(W - MARGIN - qr_size / 2, H - 30 - qr_size, d["qr_caption"])
    c.drawCentredString(W - MARGIN - qr_size / 2, H - 38 - qr_size, SITE_URL.replace("https://", ""))


def section_title(c, x, y, text, color=GREEN_DEEP):
    c.setFillColor(color)
    c.setFont("Times-Bold", 14)
    c.drawString(x, y, text)
    c.setStrokeColor(BALL)
    c.setLineWidth(2)
    c.line(x, y - 4, x + 28, y - 4)
    return y - 20


def footer(c, d, page):
    c.setFillColor(GREEN_DEEP)
    c.rect(0, 0, W, 26, fill=1, stroke=0)
    c.setFillColor(IVORY)
    c.setFont("Helvetica", 8)
    c.drawString(MARGIN, 9, d["contact"])
    c.drawRightString(W - MARGIN, 9, f"{SITE_URL}  ·  {page}")


def build(lang):
    d = DATA[lang]
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / d["filename"]
    c = Canvas(str(path), pagesize=A4)
    c.setTitle(f"CV {d['name']}")
    c.setAuthor(d["name"])
    qr_img = make_qr()

    # fondo marfil
    c.setFillColor(IVORY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    header(c, d, qr_img)
    page = 1

    # ---- columna derecha ----
    y = H - HEADER_H - 36
    y = section_title(c, RIGHT_X, y, d["skills_title"])
    for group, items in d["skills"]:
        c.setFillColor(EMERALD)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(RIGHT_X, y, group)
        y -= 11
        c.setFillColor(INK_SOFT)
        c.setFont("Helvetica", 8)
        for ln in wrap(c, items, "Helvetica", 8, W - MARGIN - RIGHT_X):
            c.drawString(RIGHT_X, y, ln)
            y -= 10
        y -= 4
    y -= 10
    y = section_title(c, RIGHT_X, y, d["edu_title"])
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(RIGHT_X, y, d["edu"][0]); y -= 11
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 8)
    c.drawString(RIGHT_X, y, d["edu"][1]); y -= 10
    c.drawString(RIGHT_X, y, d["edu"][2]); y -= 24
    y = section_title(c, RIGHT_X, y, d["lang_title"])
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 8)
    for ln in d["langs"]:
        c.drawString(RIGHT_X, y, ln)
        y -= 11
    y -= 13
    y = section_title(c, RIGHT_X, y, d["awards_title"])
    for ln in d["awards"]:
        c.setFillColor(BALL)
        c.circle(RIGHT_X + 2, y + 2.5, 2, fill=1, stroke=0)
        c.setFillColor(INK_SOFT)
        c.setFont("Helvetica", 8)
        for i, sub in enumerate(wrap(c, ln, "Helvetica", 8, W - MARGIN - RIGHT_X - 10)):
            c.drawString(RIGHT_X + 9, y, sub)
            y -= 10
        y -= 2

    # ---- columna izquierda ----
    y = H - HEADER_H - 36
    y = section_title(c, MARGIN, y, d["summary_title"])
    c.setFillColor(INK_SOFT)
    c.setFont("Helvetica", 8.5)
    for ln in wrap(c, d["summary"], "Helvetica", 8.5, LEFT_W):
        c.drawString(MARGIN, y, ln)
        y -= 11
    y -= 14

    y = section_title(c, MARGIN, y, d["exp_title"])
    for period, company, role, bullets in d["jobs"]:
        needed = 34 + 10 * sum(
            len(wrap(c, b, "Helvetica", 8, LEFT_W - 10)) for b in bullets
        )
        if y - needed < 50:
            footer(c, d, page)
            c.showPage()
            page += 1
            c.setFillColor(IVORY)
            c.rect(0, 0, W, H, fill=1, stroke=0)
            y = H - 60
        c.setFillColor(EMERALD)
        c.setFont("Helvetica-Bold", 7.5)
        c.drawString(MARGIN, y, period.upper())
        y -= 12
        c.setFillColor(GREEN_DEEP)
        c.setFont("Times-Bold", 11.5)
        c.drawString(MARGIN, y, company)
        y -= 11
        c.setFillColor(INK)
        c.setFont("Helvetica-Bold", 8.5)
        c.drawString(MARGIN, y, role)
        y -= 12
        c.setFillColor(INK_SOFT)
        c.setFont("Helvetica", 8)
        for b in bullets:
            first = True
            for ln in wrap(c, b, "Helvetica", 8, LEFT_W - 10):
                if first:
                    c.setFillColor(EMERALD)
                    c.drawString(MARGIN, y, "—")
                    c.setFillColor(INK_SOFT)
                    first = False
                c.drawString(MARGIN + 10, y, ln)
                y -= 10
        y -= 9

    footer(c, d, page)
    c.save()
    print(f"OK {path} ({page} página(s))")


if __name__ == "__main__":
    for lang in ("es", "en"):
        build(lang)
