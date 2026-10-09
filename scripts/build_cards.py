#!/usr/bin/env python3
"""Dibuja la portada y las tarjetas de proyectos del README. Sin dependencias.

A diferencia de build_stats.py, aqui no hay datos que cambien cada noche: cada tarjeta cuenta un
proyecto con una animacion pequeña de lo que hace (el técnico que escanea el QR del barco, la
boleta que SUNAT acepta, el sismo que cae a su profundidad...). Se corre a mano cuando cambia
un proyecto:

    python scripts/build_cards.py

PALETA Y LETRA. Las de build_stats.py y yoiber.com: fondo #1f1e1d, tres grises, el ambar como
acento y un rojo apagado solo para lo que falla. Fuentes del sistema: un SVG dentro de <img> no
puede cargar fuentes de fuera, y empotrarlas haria cada tarjeta diez veces mas pesada.

ANIMACION. CSS dentro de cada SVG, que GitHub respeta en las imagenes del README. Todas giran en
bucle y se quedan quietas con prefers-reduced-motion. Cada tarjeta, sin animar, sigue contando lo
suyo: el primer fotograma es una imagen completa.
"""
import json
import math
import os
import random
import textwrap
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / "assets" / "cards"

BG, BG2, INK, MID, DIM, LINE, AMB, RED = "#1f1e1d", "#262523", "#f4f4f2", "#93938f", "#6a6a66", "#3a3936", "#ffd166", "#e8775f"
PINK = "#eba3b6"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"

MONOGRAMA = (
  '<path d="M204.77 0C235.539 0 254.787 33.2885 239.437 59.9551L141.891 229.411L8.98075 65.1621C-12.183 39.0082 '
  '6.43132 0.000141945 40.0755 0H204.77Z" fill="#8F8F8F"/>'
  '<path d="M218.56 324.158C236.233 345.998 270.324 343.292 284.33 318.938L287.17 314H287.248L178.507 502.841C171.367 '
  '515.239 158.15 522.881 143.844 522.881H41.9276C11.1516 522.881 -8.09548 489.579 7.26839 462.912L141.839 229.348L218.56 '
  '324.158Z" fill="#626262"/>'
  '<path d="M398.846 0.0380859C400.995 0.0380805 403.088 0.200518 405.117 0.511719C431.98 4.79989 447.501 35.2121 433.279 '
  '59.9414L284.33 318.938C270.324 343.292 236.234 345.998 218.561 324.158L141.84 229.347L262.418 20.0693C269.559 7.67596 '
  '282.774 0.0390986 297.077 0.0390625L398.846 0.0380859Z" fill="#ffffff"/>')


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def estrellas(w, h, n, semilla):
    r = random.Random(semilla)
    return "".join(
        f'<circle cx="{r.uniform(0, w):.0f}" cy="{r.uniform(0, h):.0f}" r="{r.uniform(0.5, 1.3):.2f}" fill="{INK}" opacity="{r.uniform(0.1, 0.45):.2f}"/>'
        for _ in range(n)
    )


def texto(x, y, t, tam=13, color=INK, fuente=SANS, peso=None, extra=""):
    p = f' font-weight="{peso}"' if peso else ""
    return f'<text x="{x}" y="{y}" font-family="{fuente}" font-size="{tam}" fill="{color}"{p}{extra}>{esc(t)}</text>'


def envolver(t, ancho, tam, factor=0.56):
    return textwrap.wrap(t, max(8, int(ancho / (tam * factor))))


def svg(w, h, aria, cuerpo, css="", semilla=1):
    estilo = (
        "<style>"
        + css
        + "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"
        + "</style>"
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{esc(aria)}">'
        f"{estilo}"
        f'<defs><clipPath id="marco"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>'
        f'<g clip-path="url(#marco)"><rect width="{w}" height="{h}" fill="{BG}"/>{estrellas(w, h, int(w * h / 3200), semilla)}{cuerpo}</g>'
        f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="{LINE}"/>'
        "</svg>\n"
    )


def tarjeta(nombre, aria, etiqueta, titulo, dibujo, css="", desc="", tags="", accion="read the case →", w=440, h=270, alto_dibujo=150, semilla=1):
    """Tarjeta de proyecto: el dibujo arriba y el texto debajo."""
    partes = [dibujo, f'<line x1="24" y1="{alto_dibujo}" x2="{w - 24}" y2="{alto_dibujo}" stroke="{LINE}"/>']
    y = alto_dibujo + 24
    partes.append(texto(24, y, etiqueta, 10, MID, MONO, extra=' letter-spacing="1.6"'))
    y += 24
    if desc:
        partes.append(texto(24, y, titulo, 20, INK, SANS, 700))
        for linea in envolver(desc, w - 48, 13.5)[:2]:
            y += 20
            partes.append(texto(24, y, linea, 13.5, MID))
    else:
        for i, linea in enumerate(envolver(titulo, w - 48, 17, 0.55)[:2]):
            partes.append(texto(24, y + i * 22, linea, 17, INK, SANS, 650))
    partes.append(texto(24, h - 18, tags, 10.5, DIM, MONO))
    partes.append(texto(w - 24, h - 18, accion, 11, AMB, MONO, extra=' text-anchor="end"'))
    escribir(nombre, svg(w, h, aria, "".join(partes), css, semilla))


escritos = []


def escribir(nombre, contenido):
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / nombre).write_text(contenido, encoding="utf-8", newline="\n")
    escritos.append(nombre)


def fases(nombre, tramos):
    """Keyframes de opacidad a partir de tramos visibles [(desde%, hasta%)], con fundidos cortos."""
    marcas = {0: 0, 100: 0}
    for a, b in tramos:
        marcas[max(0, a - 2)] = 0
        marcas[a] = 1
        marcas[b] = 1
        marcas[min(100, b + 2)] = 0
    pasos = "".join(f"{p}%{{opacity:{v}}}" for p, v in sorted(marcas.items()))
    return f"@keyframes {nombre}{{{pasos}}}"


# =============================================================== portada
def portada():
    W, H = 900, 250
    c = []
    ax, ay = 112, 125
    marcas = "".join(
        f'<line x1="0" y1="-62" x2="0" y2="{-71 if i % 4 == 0 else -67}" stroke="{MID}" stroke-width="1.3" stroke-linecap="round" opacity="0.45" transform="rotate({i * 7.5})"/>'
        for i in range(48)
    )
    c.append(f'<g transform="translate({ax} {ay})"><g class="anillo">{marcas}</g></g>')
    c.append(f'<g transform="translate({ax - 26} {ay - 31}) scale(0.1185)">{MONOGRAMA}</g>')
    c.append(texto(214, 100, "Yoiber", 44, INK, SANS, 700, ' letter-spacing="-1"'))
    c.append(texto(216, 130, "Full-stack developer · Lima, Peru", 16, MID))
    c.append(f'<line x1="216" y1="150" x2="472" y2="150" stroke="{LINE}"/>')
    c.append(texto(216, 174, "Systems that keep working", 13, INK, MONO))
    c.append(texto(216, 194, "when nobody is watching.", 13, INK, MONO))
    c.append(texto(216, 222, "yoiber.com", 12, AMB, MONO))

    # La consola: lo que pasa en sus sistemas mientras nadie mira. Cada línea sale de un caso real.
    px, py, pw, ph = 500, 26, 376, 198
    c.append(f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="#191817" stroke="{LINE}"/>')
    c.append(f'<circle class="vivo" cx="{px + 18}" cy="{py + 19}" r="3.5" fill="{AMB}"/>')
    c.append(texto(px + 30, py + 23, "LIVE", 10, MID, MONO, extra=' letter-spacing="1.6"'))
    c.append(texto(px + pw - 16, py + 23, "while nobody is watching", 10, DIM, MONO, extra=' text-anchor="end"'))
    c.append(f'<line x1="{px}" y1="{py + 34}" x2="{px + pw}" y2="{py + 34}" stroke="{LINE}"/>')
    lineas = [
        ("06:42:10", "onboard", "QR scanned on vessel E-03", INK),
        ("06:42:11", "onboard", "7 h 28 min on board · billed", INK),
        ("06:43:02", "sunat", "service down · retrying", RED),
        ("06:43:40", "sunat", "B001-16 accepted · code 0", INK),
        ("06:44:05", "remezon", "M 4.2 Arequipa · 107 km deep", INK),
        ("06:45:00", "docugraph", "answer + p. 683 in 25 ms", INK),
    ]
    css = []
    for i, (hora, fuente, msg, color) in enumerate(lineas):
        y = py + 58 + i * 23
        c.append(
            f'<g class="l l{i}">'
            + texto(px + 16, y, hora, 10.5, DIM, MONO)
            + texto(px + 82, y, fuente, 10.5, AMB if color == INK else RED, MONO)
            + texto(px + 154, y, msg, 10.5, color, MONO)
            + "</g>"
        )
        css.append(f".l{i}{{animation-delay:{0.4 + i * 1.3:.1f}s}}")
    c.append(f'<rect class="cursor" x="{px + 16}" y="{py + ph - 22}" width="7" height="12" fill="{AMB}"/>')
    estilo = (
        ".anillo{animation:gira 240s linear infinite;transform-origin:0 0}"
        "@keyframes gira{to{transform:rotate(360deg)}}"
        ".vivo{animation:late 1.6s ease-in-out infinite}"
        "@keyframes late{50%{opacity:.25}}"
        ".l{opacity:0;animation:log 14s infinite both}"
        "@keyframes log{0%{opacity:0;transform:translateY(4px)}3%{opacity:1;transform:none}82%{opacity:1}88%,100%{opacity:0}}"
        ".cursor{animation:late 1s steps(1) infinite}" + "".join(css)
    )
    escribir("hero.svg", svg(W, H, "Yoiber, full-stack developer in Lima, Peru. Systems that keep working when nobody is watching.", "".join(c), estilo, 7))


# =============================================================== SUNAT
def sunat():
    c = []
    # boleta
    c.append('<g class="doc">')
    c.append(f'<path d="M44,26 h76 v92 l-6.3,6 l-6.3,-6 l-6.3,6 l-6.3,-6 l-6.3,6 l-6.3,-6 l-6.3,6 l-6.3,-6 l-6.3,6 l-6.3,-6 l-6.3,6 l-6.4,-6 z" fill="{INK}"/>')
    c.append(texto(54, 44, "B001-16", 9.5, "#222", MONO, 700))
    for k, w in enumerate([52, 40, 46]):
        c.append(f'<rect x="54" y="{54 + k * 10}" width="{w}" height="3" fill="#bdbdb8"/>')
    c.append(texto(54, 96, "S/ 36.00", 10, "#222", MONO, 700))
    c.append(f'<path class="firma" d="M56,110 c6,-10 10,8 16,-2 s8,-8 12,2 s8,4 14,-6" fill="none" stroke="#c8962e" stroke-width="1.8" stroke-linecap="round"/>')
    c.append("</g>")
    # paquete en camino
    c.append(f'<g class="pkt"><rect x="132" y="66" width="22" height="16" rx="2" fill="{AMB}"/><path d="M132,66 l11,8 l11,-8" fill="none" stroke="#1f1e1d" stroke-width="1.2"/></g>')
    c.append(f'<line x1="134" y1="90" x2="300" y2="90" stroke="{LINE}" stroke-dasharray="3 5"/>')
    # SUNAT
    c.append(f'<rect x="300" y="40" width="112" height="80" rx="8" fill="#1b1a19" stroke="{MID}"/>')
    c.append(texto(356, 66, "SUNAT", 13, INK, MONO, 700, ' text-anchor="middle" letter-spacing="1"'))
    c.append(f'<g class="caida">{texto(356, 90, "service down", 10, RED, MONO, extra=" text-anchor=\"middle\"")}{texto(356, 106, "↻ retrying", 10, RED, MONO, extra=" text-anchor=\"middle\"")}</g>')
    c.append(f'<g class="ok"><circle cx="330" cy="96" r="9" fill="{AMB}"/><path d="M325,96 l4,4 l7,-8" fill="none" stroke="#1f1e1d" stroke-width="2"/>'
             f'{texto(345, 92, "code 0", 10, AMB, MONO)}{texto(345, 106, "accepted", 10, AMB, MONO)}</g>')
    css = (
        ".firma{stroke-dasharray:90;stroke-dashoffset:90;animation:firma 9s infinite}"
        "@keyframes firma{0%{stroke-dashoffset:90}12%,100%{stroke-dashoffset:0}}"
        ".pkt{opacity:0;animation:pkt 9s infinite}"
        "@keyframes pkt{0%,13%{opacity:0;transform:translateX(0)}15%{opacity:1;transform:translateX(0)}32%{opacity:1;transform:translateX(150px)}"
        "36%{opacity:1;transform:translateX(120px)}46%{opacity:1;transform:translateX(120px)}60%{opacity:1;transform:translateX(150px)}62%,100%{opacity:0;transform:translateX(150px)}}"
        ".caida{animation:caida 9s infinite}" + fases("caida", [(33, 47)])
        + ".ok{animation:ok 9s infinite}" + fases("ok", [(63, 96)])
    )
    tarjeta("case-sunat.svg", "Case: Peruvian electronic invoicing. The receipt is signed, sent to SUNAT, retried while the service is down, and accepted with code 0.",
            "CASE · A KIP-UP PRODUCT", "The receipt leaves the system and the tax office accepts it", "".join(c), css,
            tags="UBL 2.1 · digital signature · SOAP", semilla=21)


# =============================================================== a bordo (ancha)
QR = [
    "1111111001011",
    "1000001010001",
    "1011101011101",
    "1011101000111",
    "1000001010001",
    "1111111010101",
    "0000000011100",
    "1101011101011",
    "0010100100110",
    "1111111010011",
    "1000001001101",
    "1011101110100",
    "1111111011011",
]


def qr(x, y, tam, color=INK):
    return "".join(f'<rect x="{x + k * tam}" y="{y + f * tam}" width="{tam}" height="{tam}" fill="{color}"/>'
                   for f, fila in enumerate(QR) for k, ch in enumerate(fila) if ch == "1")


def a_bordo():
    W, H = 900, 280
    c = []
    c.append(texto(32, 50, "CASE · FIELD OPERATIONS", 10, MID, MONO, extra=' letter-spacing="1.6"'))
    for i, l in enumerate(["Man-hours per technician,", "on every vessel"]):
        c.append(texto(32, 84 + i * 28, l, 24, INK, SANS, 700, ' letter-spacing="-0.3"'))
    for i, l in enumerate(envolver("A service company sends technicians to its clients' vessels and bills by the man-hour. Every vessel carries a QR code: they scan it when they board and when they leave, and the hours add up on their own.", 330, 13.5)):
        c.append(texto(32, 150 + i * 20, l, 13.5, MID))
    c.append(texto(32, H - 22, "React Native · Node · Prisma · MySQL", 10.5, DIM, MONO))
    c.append(texto(370, H - 22, "read the case →", 11, AMB, MONO, extra=' text-anchor="end"'))

    ox = 420
    c.append(f'<rect x="{ox}" y="20" width="460" height="240" rx="12" fill="#1b1a19" stroke="{LINE}"/>')
    # el barco con su QR pegado
    c.append(f'<path d="M{ox + 30},176 L{ox + 230},176 L{ox + 206},212 L{ox + 54},212 Z" fill="#2c2b29" stroke="{MID}" stroke-width="1.2"/>')
    c.append(f'<rect x="{ox + 92}" y="128" width="84" height="48" fill="#262523" stroke="{MID}" stroke-width="1.2"/>')
    c.append(f'<line x1="{ox + 134}" y1="128" x2="{ox + 134}" y2="96" stroke="{MID}" stroke-width="1.5"/>')
    c.append(f'<rect x="{ox + 106}" y="136" width="34" height="34" rx="2" fill="{INK}"/>')
    c.append(qr(ox + 108.5, 138.5, 2.25, "#1f1e1d"))
    c.append(texto(ox + 158, 166, "E-03", 10, MID, MONO))
    for k, (y, op) in enumerate([(220, 0.5), (232, 0.3), (244, 0.18)]):
        d = "M" + " ".join(f"{ox + x:.0f},{y + 2.5 * math.sin(x / 16 + k):.1f}" for x in range(0, 461, 8))
        c.append(f'<path d="{d}" fill="none" stroke="{MID}" stroke-width="1.1" opacity="{op}"/>')
    # el teléfono que escanea
    c.append(f'<g class="tel"><rect x="{ox + 196}" y="58" width="40" height="70" rx="7" fill="#111" stroke="{INK}" stroke-width="1.5"/>'
             f'<rect class="haz" x="{ox + 202}" y="70" width="28" height="2" fill="{AMB}"/></g>')
    c.append(f'<g class="marca"><circle cx="{ox + 216}" cy="44" r="9" fill="{AMB}"/>'
             f'<path d="M{ox + 211},44 l3.5,3.5 l6,-7" fill="none" stroke="#1f1e1d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></g>')
    # las marcas y las horas que salen solas
    c.append(f'<rect x="{ox + 262}" y="40" width="182" height="188" rx="8" fill="#1f1e1d" stroke="{LINE}"/>')
    c.append(texto(ox + 276, 62, "R. QUISPE · E-03", 9.5, MID, MONO, extra=' letter-spacing="1"'))
    filas = [("boarded", "06:42", "f0"), ("left", "14:10", "f1")]
    for k, (que, hora, clase) in enumerate(filas):
        y = 90 + k * 26
        c.append(f'<g class="{clase}">' + texto(ox + 276, y, que, 11, MID, MONO) + texto(ox + 430, y, hora, 11, INK, MONO, extra=' text-anchor="end"') + "</g>")
    c.append(f'<line x1="{ox + 276}" y1="132" x2="{ox + 430}" y2="132" stroke="{LINE}"/>')
    c.append('<g class="f2">' + texto(ox + 276, 158, "on board", 11, MID, MONO) + texto(ox + 430, 158, "7 h 28 min", 13, AMB, MONO, 700, ' text-anchor="end"') + "</g>")
    c.append('<g class="f3">' + texto(ox + 276, 190, "this week", 10, DIM, MONO) + texto(ox + 430, 190, "41 HH", 11, INK, MONO, extra=' text-anchor="end"') + "</g>")
    c.append('<g class="f3">' + texto(ox + 276, 210, "billed to client", 10, DIM, MONO) + texto(ox + 430, 210, "E-03", 11, INK, MONO, extra=' text-anchor="end"') + "</g>")
    css = (
        ".tel{animation:tel 8s infinite}@keyframes tel{0%{transform:translateY(-14px);opacity:0}8%{opacity:1}18%,80%{transform:translateY(0);opacity:1}90%,100%{opacity:0}}"
        ".haz{animation:haz 1s ease-in-out infinite alternate}@keyframes haz{to{transform:translateY(48px)}}"
        ".marca{animation:marca 8s infinite}" + fases("marca", [(22, 34), (52, 64)])
        + ".f0{animation:f0 8s infinite}" + fases("f0", [(24, 92)])
        + ".f1{animation:f1 8s infinite}" + fases("f1", [(54, 92)])
        + ".f2{animation:f2 8s infinite}" + fases("f2", [(62, 92)])
        + ".f3{animation:f3 8s infinite}" + fases("f3", [(70, 92)])
    )
    escribir(
        "case-onboard.svg",
        svg(W, H, "Case: man-hours per technician on every vessel. Each vessel carries a QR code that technicians scan when they board and leave; their hours add up on their own, for billing the client and paying the crew.", "".join(c), css, 31),
    )


# =============================================================== agenda
def agenda():
    c = []
    cols, filas = 5, 6
    x0, y0, cw, rh = 64, 34, 70, 18
    for k in range(cols):
        c.append(f'<circle cx="{x0 + k * cw + cw / 2 - 4}" cy="18" r="6" fill="{LINE}"/>')
    for f in range(filas + 1):
        c.append(f'<line x1="{x0 - 8}" y1="{y0 + f * rh}" x2="{x0 + cols * cw - 8}" y2="{y0 + f * rh}" stroke="{LINE}"/>')
        if f < filas:
            c.append(texto(24, y0 + f * rh + 13, f"{8 + f * 2:02d}:00", 9, DIM, MONO))
    r = random.Random(4)
    citas = []
    for k in range(cols):
        f = 0
        while f < filas:
            if r.random() < 0.62:
                largo = 1 if r.random() < 0.7 else 2
                largo = min(largo, filas - f)
                citas.append((k, f, largo))
                f += largo
            else:
                f += 1
    for i, (k, f, largo) in enumerate(citas):
        color = INK if (k + f) % 3 else MID
        c.append(f'<rect class="cita" style="animation-delay:{i * 0.18:.2f}s" x="{x0 + k * cw}" y="{y0 + f * rh + 2}" width="{cw - 16}" height="{largo * rh - 4}" rx="3" fill="{color}" opacity="0.85"/>')
    c.append(f'<g class="ahora"><line x1="{x0 - 12}" y1="{y0}" x2="{x0 + cols * cw - 4}" y2="{y0}" stroke="{AMB}" stroke-width="1.6"/>'
             f'<circle cx="{x0 - 12}" cy="{y0}" r="3" fill="{AMB}"/></g>')
    css = (
        ".cita{opacity:0;animation:cita 12s infinite both}"
        "@keyframes cita{0%{opacity:0}4%,88%{opacity:.85}94%,100%{opacity:0}}"
        f".ahora{{animation:baja 12s linear infinite}}@keyframes baja{{0%{{transform:translateY(0)}}100%{{transform:translateY({filas * rh}px)}}}}"
    )
    tarjeta("case-schedule.svg", "Case: twenty modules around the day's schedule, the system a therapy center with several locations runs on every day.",
            "CASE · CUSTOM SYSTEM", "Twenty modules around the day's schedule", "".join(c), css,
            tags="Django · ASGI · Redis · PostgreSQL", semilla=41)


# =============================================================== DocuGraph
def docugraph():
    c = []
    for k in range(4):
        c.append(f'<rect x="{30 + k * 5}" y="{28 + k * 5}" width="62" height="82" rx="3" fill="{["#3a3936", "#55544f", "#8a8a85", INK][k]}"/>')
    for k in range(5):
        c.append(f'<rect x="54" y="{56 + k * 8}" width="{36 - (k % 2) * 10}" height="2.5" fill="#bdbdb8"/>')
    c.append(texto(64, 136, "3,100 pages", 9.5, DIM, MONO, extra=' text-anchor="middle"'))
    c.append(f'<rect x="124" y="20" width="294" height="114" rx="8" fill="#151413" stroke="{LINE}"/>')
    pregunta = '> how does the planner pick a scan?'
    c.append(f'<g>{texto(138, 44, pregunta, 10.5, INK, MONO)}<rect class="tapa" x="150" y="33" width="262" height="15" fill="#151413"/></g>')
    c.append('<g class="r1">' + texto(138, 70, "380 tokens of evidence", 10.5, MID, MONO) + "</g>")
    c.append('<g class="r2">' + texto(138, 90, "[PostgreSQL 17.11, p. 683]", 10.5, AMB, MONO) + "</g>")
    c.append('<g class="r3">' + texto(138, 118, "25 ms · 0 API calls · 0 bytes out", 10, DIM, MONO) + "</g>")
    css = (
        ".tapa{animation:escribe 9s steps(24) infinite;transform-box:fill-box;transform-origin:100% 50%}"
        "@keyframes escribe{0%,4%{transform:scaleX(1)}28%,94%{transform:scaleX(0)}100%{transform:scaleX(1)}}"
        ".r1{animation:r1 9s infinite}" + fases("r1", [(34, 94)])
        + ".r2{animation:r2 9s infinite}" + fases("r2", [(42, 94)])
        + ".r3{animation:r3 9s infinite}" + fases("r3", [(50, 94)])
    )
    tarjeta("oss-docugraph.svg", "DocuGraph MCP: ask a 3,000-page PDF a question and get the paragraph and the page number, in 25 ms and without network.",
            "OPEN SOURCE · RUST · MCP", "DocuGraph MCP", "".join(c), css,
            desc="Ask a 3,000-page PDF a question. Get the paragraph, the page number and nothing else.",
            tags="25 ms per query · no API keys", accion="code →", h=286, semilla=61)


# =============================================================== Kuidy Lyrics
def kuidy_lyrics():
    c = []
    # una ventana de juego, de fondo
    c.append(f'<rect x="24" y="16" width="392" height="88" rx="6" fill="#171615" stroke="{LINE}"/>')
    for k in range(7):
        c.append(f'<path d="M{24 + k * 60},104 l40,-{20 + (k * 13) % 30} l30,{12 + (k * 7) % 14}" fill="none" stroke="{LINE}"/>')
    # la pastilla flotante con tres líneas de letra (barras, sin letra real)
    c.append(f'<rect x="96" y="30" width="248" height="60" rx="14" fill="#2a2927" opacity="0.92" stroke="#4a4945"/>')
    anchos = [168, 204, 132]
    for i, w in enumerate(anchos):
        x = 220 - w / 2
        y = 44 + i * 16
        c.append(f'<rect x="{x}" y="{y}" width="{w}" height="6" rx="3" fill="{DIM if i != 1 else MID}"/>')
    c.append(f'<rect class="barre" x="118" y="60" width="204" height="6" rx="3" fill="{AMB}"/>')
    # 392 MB contra 20 MB
    c.append(texto(24, 124, "Electron", 9.5, DIM, MONO) + f'<rect x="84" y="117" width="290" height="7" rx="3.5" fill="{LINE}"/>' + texto(416, 124, "392 MB", 9.5, DIM, MONO, extra=' text-anchor="end"'))
    c.append(texto(24, 140, "Rust", 9.5, AMB, MONO) + f'<rect class="rust" x="84" y="133" width="15" height="7" rx="3.5" fill="{AMB}"/>' + texto(108, 140, "20 MB", 9.5, AMB, MONO))
    css = (
        ".barre{animation:barre 4s linear infinite;transform-box:fill-box;transform-origin:0 50%}"
        "@keyframes barre{0%{transform:scaleX(0)}90%,100%{transform:scaleX(1)}}"
    )
    tarjeta("oss-kuidy-lyrics.svg", "Kuidy Lyrics: synced lyrics floating over any Windows window. The Rust version weighs 20 MB instead of 392 MB.",
            "OPEN SOURCE · RUST · WINDOWS", "Kuidy Lyrics", "".join(c), css,
            desc="Synced lyrics floating over any window, games in borderless fullscreen included.",
            tags="one process instead of five", accion="code →", h=286, semilla=71)


# =============================================================== Remezón
def remezon():
    c = [f'<rect width="440" height="150" fill="#f5f5f1"/>']
    # el perfil del relieve y el mar, como en la vista de corte
    c.append(f'<path d="M0,30 L150,30 L170,26 L200,14 L230,10 L262,16 L300,22 L440,26 L440,0 L0,0 Z" fill="#f5f5f1"/>')
    c.append(f'<path d="M0,30 L150,30 L150,34 L0,34 Z" fill="#b8d3e5"/>')
    c.append(f'<path d="M150,30 L170,26 L200,14 L230,10 L262,16 L300,22 L440,26" fill="none" stroke="#1b1d1f" stroke-width="1.4"/>')
    for k, y in enumerate([54, 78, 102, 126]):
        c.append(f'<line x1="0" y1="{y}" x2="440" y2="{y}" stroke="#1b1d1f" stroke-opacity="0.12"/>')
        c.append(f'<text x="432" y="{y - 3}" font-family="Georgia, serif" font-style="italic" font-size="8" fill="#646a71" text-anchor="end">{(k + 1) * 100} km</text>')
    r = random.Random(7)
    puntos = []
    for _ in range(46):
        x = r.uniform(120, 300)
        prof = max(4, (x - 120) * 0.62 + r.gauss(0, 6))
        puntos.append((x, 30 + prof * 0.24))
    for _ in range(9):
        puntos.append((r.uniform(330, 380), r.uniform(120, 140)))
    for k, (x, y) in enumerate(puntos):
        prof = (y - 30) / 0.24
        color = "#d7301f" if prof < 60 else "#1a9850" if prof < 300 else "#2166ac"
        c.append(f'<circle class="s" style="animation-delay:{k * 0.08:.2f}s" cx="{x:.0f}" cy="{y:.0f}" r="{r.uniform(1.6, 3.4):.1f}" fill="{color}" stroke="#1b1d1f" stroke-width="0.4"/>')
    c.append(texto(16, 62, "REMEZÓN", 13, "#1b1d1f", SANS, 800, ' letter-spacing="2.4"'))
    c.append(f'<text x="16" y="78" font-family="Georgia, serif" font-style="italic" font-size="10" fill="#3d4247">the Nazca plate, drawn by its earthquakes</text>')
    css = ".s{animation:s 7s infinite both}@keyframes s{0%{opacity:0;transform:scale(.2)}6%,88%{opacity:1;transform:none}96%,100%{opacity:0}}.s{transform-box:fill-box;transform-origin:center}"
    tarjeta("oss-remezon.svg", "Remezón: Peru's earthquakes live and in 3D, each one at the depth where it started; seen from the side they draw the Nazca plate.",
            "OPEN SOURCE · LIVE DATA", "Remezón", "".join(c), css,
            desc="Peru's earthquakes live and in 3D, each one at the depth where it started.",
            tags="Nuxt · Vue · TresJS", accion="code →", h=286, semilla=141)


# =============================================================== Daebon
def daebon():
    c = []
    # el libreto engrapado, con el resaltador y el sello
    c.append(f'<rect x="150" y="16" width="140" height="122" rx="4" fill="#f4c6d3" transform="rotate(-4 220 77)"/>')
    c.append(f'<g transform="rotate(-4 220 77)"><rect x="150" y="16" width="12" height="122" fill="#1f1e1d" opacity="0.85"/>'
             f'<rect x="153" y="30" width="6" height="6" fill="{MID}"/><rect x="153" y="118" width="6" height="6" fill="{MID}"/>'
             + texto(172, 38, "S#1. My list (night)", 8.5, "#b5334f", MONO)
             + texto(172, 78, "대본", 30, "#1f1e1d", SANS, 800)
             + f'<rect class="resalta" x="172" y="92" width="96" height="9" fill="#ffe45a" opacity="0.9"/>'
             + texto(172, 100, "ep. 7 airs tonight", 9, "#1f1e1d", MONO)
             + f'<g class="sello"><rect x="246" y="108" width="28" height="22" rx="3" fill="none" stroke="#c0392b" stroke-width="2"/>'
             + texto(260, 124, "끝", 13, "#c0392b", SANS, 800, ' text-anchor="middle"') + "</g></g>")
    css = (
        ".resalta{animation:resalta 6s infinite both;transform-box:fill-box;transform-origin:0 50%}"
        "@keyframes resalta{0%{transform:scaleX(0)}20%,88%{transform:scaleX(1)}96%,100%{transform:scaleX(0)}}"
        ".sello{animation:sello 6s infinite}" + fases("sello", [(40, 92)])
    )
    tarjeta("oss-daebon.svg", "Daebon: an Asian drama tracker styled as a Korean script, for the web and Android, with where to watch each show legally.",
            "OPEN SOURCE · WEB AND ANDROID", "Daebon", "".join(c), css,
            desc="My drama list, styled as a Korean script: the episodes I'm missing and where to watch them.",
            tags="Svelte · Capacitor · Node · TMDB", accion="code →", h=286, semilla=151)


# =============================================================== Tsuzuku
# La «つ» de Dela Gothic One, la misma del ícono de Tsuzuku: sacada una vez de la fuente con
# fontTools y normalizada a 100 de ancho (74,4 de alto), con el eje y hacia abajo.
TSU = "M7 48.6Q15.7 49.1 24.8 49.1Q52.6 49.1 64.7 44.5Q72.6 41.5 72.6 32.7Q72.6 28.3 68 25.4Q63.4 22.4 52.7 22.4Q43.5 22.4 30.4 24.2Q17.4 26 5.4 29.7L0 6.5Q18.1 2.9 30.9 1.5Q43.7 0 54.7 0Q76.5 0 88.2 7.8Q100 15.7 100 32.3Q100 42.8 95.8 51.3Q91.6 59.7 82.6 64.5Q72.8 69.9 56.9 72Q40.9 74.1 18.2 74.4Q17.3 67.8 14.9 61.7Q12.4 55.5 7 48.6Z"


def tsuzuku():
    c = []
    # trama de puntos que se achica hacia el centro, como en el ícono
    r = []
    for fila in range(10):
        for col in range(30):
            x = col * 15 + (7 if fila % 2 else 0)
            y = fila * 15
            d = math.hypot(x, 150 - y) / 260
            rad = 5 * max(0, 1 - d) ** 0.9
            if rad > 0.4:
                r.append(f'<circle cx="{x}" cy="{y}" r="{rad:.2f}" fill="{AMB}" opacity="0.55"/>')
    c.append("".join(r))
    c.append(f'<g transform="translate(36 42) scale(0.92)"><path d="{TSU}" fill="{INK}"/></g>')
    c.append(texto(160, 40, "Your list", 12, INK, SANS, 650))
    c.append(texto(160, 56, "6 of 10 seen · 2 to watch", 10, MID, MONO))
    for k in range(10):
        clase = "seg v" if k < 6 else ("seg s" if k < 8 else "seg f")
        c.append(f'<rect class="{clase}" style="animation-delay:{k * 0.15:.2f}s" x="{160 + k * 22}" y="68" width="18" height="10" rx="1" '
                 f'fill="{INK if k < 6 else AMB if k < 8 else "none"}" stroke="{INK if k < 6 else AMB if k < 8 else DIM}" stroke-width="1.2"/>')
    c.append(f'<g class="prox"><rect x="160" y="94" width="150" height="20" fill="{AMB}" transform="skewX(-8)"/>'
             f'{texto(178, 108, "Ep 9 airs in 2 d 4 h", 10.5, "#1f1e1d", MONO, 700)}</g>')
    c.append(texto(410, 40, "つづく", 13, AMB, SANS, 700, ' writing-mode="vertical-rl" text-anchor="start"'))
    css = (
        ".seg{animation:seg 6s infinite both}@keyframes seg{0%{opacity:0}6%,90%{opacity:1}96%,100%{opacity:0}}"
        ".prox{animation:prox 6s infinite}" + fases("prox", [(30, 90)])
    )
    tarjeta("oss-tsuzuku.svg", "Tsuzuku: anime tracker for the web and Android, with your list episode by episode and when the next one airs.",
            "OPEN SOURCE · WEB AND ANDROID", "Tsuzuku", "".join(c), css,
            desc="Anime tracker on the AniList API: your list, the week's schedule and where to watch legally.",
            tags="Svelte · TypeScript · Capacitor", accion="code →", h=286, semilla=81)


# =============================================================== km 0
def km0():
    c = []
    for x in range(10, 440, 34):
        c.append(f'<line x1="{x}" y1="0" x2="{x + 26}" y2="150" stroke="{LINE}"/>')
    for y in range(12, 150, 30):
        c.append(f'<line x1="0" y1="{y}" x2="440" y2="{y - 10}" stroke="{LINE}"/>')
    grabado = "M206,72 L240,78 L262,98 L300,104 L322,90 L360,96 L400,82"
    antes = "M58,118 L86,108 L112,112 L138,92 L170,86 L206,72"
    c.append(f'<path d="{grabado}" fill="none" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>')
    c.append(f'<path class="antes" d="{antes}" fill="none" stroke="{AMB}" stroke-width="3" stroke-linecap="round" stroke-dasharray="1 7"/>')
    c.append(f'<circle cx="206" cy="72" r="5" fill="{BG}" stroke="{INK}" stroke-width="2"/>')
    c.append(texto(214, 62, "you hit start here", 9.5, MID, MONO))
    c.append(f'<g class="placa"><rect x="34" y="124" width="48" height="20" rx="3" fill="{INK}"/><rect x="36.5" y="126.5" width="43" height="15" rx="2" fill="none" stroke="#1f1e1d"/>'
             f'{texto(58, 138, "KM 0", 10, "#1f1e1d", MONO, 800, " text-anchor=\"middle\"")}</g>')
    c.append(f'<circle cx="400" cy="82" r="4" fill="{AMB}"/>')
    css = (
        ".antes{stroke-dasharray:1 7;animation:antes 7s infinite}"
        "@keyframes antes{0%{opacity:0}8%{opacity:1}90%{opacity:1}97%,100%{opacity:0}}"
        ".placa{animation:placa 7s infinite}" + fases("placa", [(24, 92)])
    )
    tarjeta("oss-km0.svg", "km 0: an Android recorder that rebuilds the stretch you walked before hitting start, with a KM 0 plate where you really started.",
            "OPEN SOURCE · ANDROID", "km 0", "".join(c), css,
            desc="If you hit start halfway through a walk, it rebuilds the missing stretch from Health Connect.",
            tags="Kotlin · Capacitor · OSRM", accion="code →", h=286, semilla=91)


# =============================================================== demos
def comandas():
    c = []
    c.append(f'<rect x="28" y="22" width="110" height="80" rx="8" fill="#1b1a19" stroke="{LINE}"/>')
    c.append(texto(40, 42, "TABLE 4", 9, MID, MONO, extra=' letter-spacing="1.2"'))
    c.append(texto(40, 62, "2× ceviche", 10.5, INK, MONO) + texto(40, 80, "1× chicha", 10.5, INK, MONO))
    c.append(f'<g class="ticket"><rect x="150" y="48" width="44" height="30" rx="3" fill="{AMB}"/>'
             f'<rect x="156" y="55" width="30" height="2.5" fill="#1f1e1d"/><rect x="156" y="62" width="22" height="2.5" fill="#1f1e1d"/></g>')
    c.append(f'<rect x="282" y="18" width="134" height="88" rx="6" fill="#111" stroke="{MID}"/>')
    c.append(texto(294, 36, "KITCHEN", 9, MID, MONO, extra=' letter-spacing="1.2"'))
    c.append('<g class="nuevo">' + f'<rect x="294" y="46" width="110" height="46" rx="4" fill="#2a2927" stroke="{AMB}"/>'
             + texto(302, 62, "NEW · table 4", 9.5, AMB, MONO) + texto(302, 80, "2× ceviche …", 9.5, INK, MONO) + "</g>")
    css = (
        ".ticket{animation:ticket 5s infinite}"
        "@keyframes ticket{0%{transform:translateX(0);opacity:0}8%{opacity:1}40%{transform:translateX(110px);opacity:1}46%,100%{transform:translateX(110px);opacity:0}}"
        ".nuevo{animation:nuevo 5s infinite}" + fases("nuevo", [(44, 94)])
    )
    tarjeta("demo-comandas.svg", "Kip-Up Comandas: the waiter's order shows up on the kitchen screen.", "DEMO · KIP-UP", "Kip-Up Comandas", "".join(c), css,
            desc="The waiter takes the order and it shows up on the kitchen screen.", tags="Next.js · Socket.IO", accion="open →", h=250, alto_dibujo=124, semilla=101)


def contenido():
    c = []
    c.append(f'<rect x="40" y="14" width="60" height="100" rx="10" fill="#1b1a19" stroke="{MID}"/>')
    c.append(f'<path d="M64,50 l16,11 l-16,11 z" fill="{INK}"/>')
    c.append(texto(70, 100, "V-014", 9, AMB, MONO, extra=' text-anchor="middle"'))
    for k in range(3):
        c.append(f'<g class="msg m{k}"><rect x="118" y="{34 + k * 22}" width="72" height="16" rx="8" fill="#2a2927" stroke="{LINE}"/>'
                 f'<rect x="128" y="{41 + k * 22}" width="{40 - k * 6}" height="2.5" fill="{MID}"/></g>')
    c.append(f'<path d="M204,64 h22" stroke="{DIM}" stroke-width="1.5"/><path d="M222,59 l6,5 l-6,5" fill="none" stroke="{DIM}" stroke-width="1.5"/>')
    c.append(f'<rect x="244" y="18" width="172" height="92" rx="8" fill="#1b1a19" stroke="{LINE}"/>')
    c.append(texto(256, 36, "SOLD THIS MONTH", 9, MID, MONO, extra=' letter-spacing="1.2"'))
    for k, (v, h) in enumerate([("V-011", 22), ("V-012", 34), ("V-013", 18), ("V-014", 52)]):
        x = 262 + k * 38
        c.append(f'<rect class="barra b{k}" x="{x}" y="{100 - h}" width="22" height="{h}" rx="2" fill="{AMB if k == 3 else MID}"/>')
    css = (
        ".msg{opacity:0;animation:msg 6s infinite both}@keyframes msg{0%{opacity:0;transform:translateX(-10px)}8%,86%{opacity:1;transform:none}94%,100%{opacity:0}}"
        ".m1{animation-delay:.5s}.m2{animation-delay:1s}"
        ".barra{animation:sube 6s infinite both;transform-box:fill-box;transform-origin:50% 100%}"
        "@keyframes sube{0%{transform:scaleY(0)}20%,88%{transform:scaleY(1)}96%,100%{transform:scaleY(0)}}"
        ".b1{animation-delay:.2s}.b2{animation-delay:.4s}.b3{animation-delay:1.4s}"
    )
    tarjeta("demo-contenido.svg", "Kip-Up Contenido: from a TikTok video to a sale in soles, with what each video sold every month.", "DEMO · KIP-UP", "Kip-Up Contenido", "".join(c), css,
            desc="From a TikTok video to a sale in soles: what every video sold, month by month.", tags="NestJS · TikTok API", accion="open →", h=250, alto_dibujo=124, semilla=111)


def nazca():
    # colibri.json: el contorno del colibrí de yoiberdev/nazca (src/world/figures.js), normalizado.
    datos = json.loads((Path(__file__).resolve().parent / "colibri.json").read_text(encoding="utf-8"))
    alto = 100
    ancho = alto / datos["h"]
    ox, oy = (440 - ancho) / 2, (124 - alto) / 2
    pts = " ".join(f"{ox + x * ancho:.1f},{oy + y * ancho:.1f}" for x, y in datos["pts"])
    c = [f'<rect width="440" height="124" fill="#2a2420" opacity="0.5"/>']
    c.append(f'<polygon points="{pts}" fill="none" stroke="{LINE}" stroke-width="1.6" stroke-linejoin="round"/>')
    c.append(f'<polygon class="linea" points="{pts}" fill="none" stroke="{AMB}" stroke-width="1.8" stroke-linejoin="round" pathLength="1000"/>')
    css = (
        ".linea{stroke-dasharray:1000;stroke-dashoffset:1000;animation:traza 7s ease-in-out infinite}"
        "@keyframes traza{0%{stroke-dashoffset:1000;opacity:1}70%{stroke-dashoffset:0;opacity:1}90%{opacity:1}100%{stroke-dashoffset:0;opacity:0}}"
    )
    tarjeta("demo-nazca.svg", "Nazca: the hummingbird of the Nazca lines, drawn as one line that never crosses itself.", "LIVE · 3D", "Nazca", "".join(c), css,
            desc="A dawn flight over the lines: your cursor's light uncovers the figures in the sand.", tags="Svelte · Threlte · three.js", accion="open →", h=250, alto_dibujo=124, semilla=121)


def ajolote():
    c = []
    px = 6  # el ajolote de frente, bloque a bloque: branquias, ojos con brillo y la sonrisa
    cuerpo = [
        "..G..............G..",
        ".G.G............G.G.",
        "G...GPPPPPPPPPPG...G",
        "...GPPPPPPPPPPPPG...",
        "..GPPPPPPPPPPPPPPG..",
        "...PPWEPPPPPPWEPP...",
        "...PPEEPPPPPPEEPP...",
        "...PPPPPPPPPPPPPP...",
        "....PPPMMMMMMPPP....",
        ".....PPPPPPPPPP.....",
    ]
    ox, oy = 220 - len(cuerpo[0]) * px / 2, 30
    colores = {"G": "#d9708f", "P": PINK, "E": "#1f1e1d", "W": INK, "M": "#b8546f"}
    for f, fila in enumerate(cuerpo):
        for k, ch in enumerate(fila):
            if ch in colores:
                clase = ' class="ojo"' if ch in "EW" else (' class="branquia"' if ch == "G" else "")
                c.append(f'<rect{clase} x="{ox + k * px}" y="{oy + f * px}" width="{px}" height="{px}" fill="{colores[ch]}"/>')
    for k in range(4):
        c.append(f'<circle class="burbuja u{k}" cx="{ox + 20 + k * 26}" cy="20" r="{2 + k % 2}" fill="none" stroke="{MID}" stroke-width="1"/>')
    c.append(f'<path d="M0,112 Q110,96 220,108 T440,104 L440,124 L0,124 Z" fill="#2c2b29"/>')
    css = (
        ".ojo{animation:parpadea 4s infinite;transform-box:fill-box;transform-origin:center}"
        "@keyframes parpadea{0%,92%,100%{transform:scaleY(1)}95%{transform:scaleY(.15)}}"
        ".branquia{animation:branquia 2.2s ease-in-out infinite}@keyframes branquia{50%{opacity:.55}}"
        ".burbuja{animation:burbuja 4s ease-in infinite;opacity:0}"
        "@keyframes burbuja{0%{transform:translateY(60px);opacity:0}20%{opacity:.8}100%{transform:translateY(-14px);opacity:0}}"
        ".u1{animation-delay:1s}.u2{animation-delay:2.1s}.u3{animation-delay:3s}"
    )
    tarjeta("demo-ajolote.svg", "Ajolote: a block axolotl in its cave, drawn in code.", "LIVE · 3D", "Ajolote", "".join(c), css,
            desc="My pet on the web: a block axolotl in its cave. Click it and it flips.", tags="Svelte · Threlte", accion="open →", h=250, alto_dibujo=124, semilla=131)


if __name__ == "__main__":
    portada()
    sunat()
    a_bordo()
    agenda()
    docugraph()
    kuidy_lyrics()
    remezon()
    daebon()
    tsuzuku()
    km0()
    comandas()
    contenido()
    nazca()
    ajolote()
    print("escritos:", ", ".join(escritos))
