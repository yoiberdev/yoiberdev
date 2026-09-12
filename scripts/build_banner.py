#!/usr/bin/env python3
"""Genera los banners de portada oficiales para redes (Buy Me a Coffee, Ko-fi, LinkedIn, GitHub).
Usa la misma tecnología vectorial (SVG puro y renderizado nítido a PNG) y paleta de yoiber.com:
  - Fondo cálido #1f1e1d
  - Acento ámbar #ffd166
  - Tipografía Space Grotesk / JetBrains Mono
  - Dial de telemetría a 72 marcas, haz de barrido de radar y trayectoria espacial.

Genera:
  - assets/banner.svg                (1600 x 423 px vectorial con animaciones SMIL)
  - assets/banner.png                (1600 x 423 px, medida oficial de Buy Me a Coffee)
  - assets/banner@2x.png             (3200 x 846 px, Retina para Buy Me a Coffee / 4K)
  - assets/banner-1600x400.png       (1600 x 400 px, variante panorámica 4:1)
  - assets/banner-1200x400.png       (1200 x 400 px, proporción 3:1 recomendada para Ko-fi)
"""
import os
import subprocess
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
ASSETS.mkdir(exist_ok=True)

BG = "#1f1e1d"
INK = "#f4f4f2"
MID = "#93938f"
DIM = "#6a6a66"
LINE = "#3a3936"
AMB = "#ffd166"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', 'JetBrains Mono', monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, 'DejaVu Sans', 'Space Grotesk', sans-serif"

MONOGRAMA = (
  '<path d="M204.77 0C235.539 0 254.787 33.2885 239.437 59.9551L141.891 229.411L8.98075 65.1621C-12.183 39.0082 '
  '6.43132 0.000141945 40.0755 0H204.77Z" fill="#8F8F8F"/>'
  '<path d="M218.56 324.158C236.233 345.998 270.324 343.292 284.33 318.938L287.17 314H287.248L178.507 502.841C171.367 '
  '515.239 158.15 522.881 143.844 522.881H41.9276C11.1516 522.881 -8.09548 489.579 7.26839 462.912L141.839 229.348L218.56 '
  '324.158Z" fill="#626262"/>'
  '<path d="M398.846 0.0380859C400.995 0.0380805 403.088 0.200518 405.117 0.511719C431.98 4.79989 447.501 35.2121 433.279 '
  '59.9414L284.33 318.938C270.324 343.292 236.234 345.998 218.561 324.158L141.84 229.347L262.418 20.0693C269.559 7.67596 '
  '282.774 0.0390986 297.077 0.0390625L398.846 0.0380859Z" fill="#ffffff"/>')

def build_svg_1600(w=1600, h=423):
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
             f'aria-label="Yoiber · Full-stack developer banner">')
    s.append('<defs>')
    s.append(f'<clipPath id="clip-bmc"><rect width="{w}" height="{h}" rx="16"/></clipPath>')
    s.append(f'<radialGradient id="ambGlow" cx="85%" cy="30%" r="60%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.12"/>'
             f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/></radialGradient>')
    s.append(f'<linearGradient id="trajGrad" x1="0%" y1="100%" x2="100%" y2="0%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.2"/>'
             f'<stop offset="70%" stop-color="{AMB}" stop-opacity="0.95"/>'
             f'<stop offset="100%" stop-color="#ffffff" stop-opacity="1"/></linearGradient>')
    s.append(f'<linearGradient id="waveGrad" x1="0%" y1="0%" x2="100%" y2="0%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.35"/>'
             f'<stop offset="50%" stop-color="{AMB}" stop-opacity="0.85"/>'
             f'<stop offset="100%" stop-color="{MID}" stop-opacity="0.4"/></linearGradient>')
    s.append(f'<linearGradient id="sweepGrad" x1="0%" y1="0%" x2="100%" y2="100%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.35"/>'
             f'<stop offset="100%" stop-color="{AMB}" stop-opacity="0"/></linearGradient>')
    s.append('<style>')
    s.append('@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;family=Space+Grotesk:wght@500;700&amp;display=swap");')
    s.append('text { text-rendering: geometricPrecision; }')
    s.append('</style>')
    s.append('</defs>')

    s.append('<g clip-path="url(#clip-bmc)">')
    s.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>')
    s.append(f'<rect width="{w}" height="{h}" fill="url(#ambGlow)"/>')

    # Rejilla técnica de fondo
    for x in range(80, w, 80):
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{h}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')
    for y in range(40, h, 60):
        s.append(f'<line x1="0" y1="{y}" x2="{w}" y2="{y}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')

    # Marcas de cruce en las esquinas
    for cx, cy in [(20, 20), (w-20, 20), (20, h-20), (w-20, h-20)]:
        s.append(f'<path d="M{cx-8} {cy} L{cx+8} {cy} M{cx} {cy-8} L{cx} {cy+8}" stroke="{DIM}" stroke-width="1" opacity="0.55"/>')

    # Barra superior
    s.append(f'<text x="40" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1.5">// SYSTEMS ARCHITECTURE &#183; EDGE &#183; TELEMETRY</text>')
    s.append(f'<text x="{w-40}" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end" letter-spacing="1">12&#176;02\'36"S 77&#176;01\'42"W &#183; LIMA, PERU</text>')
    s.append(f'<line x1="40" y1="44" x2="{w-40}" y2="44" stroke="{LINE}" stroke-width="1"/>')

    # SECTOR DERECHO: Radar y trayectoria
    rx, ry = w - 260, 220
    s.append(f'<circle cx="{rx}" cy="{ry}" r="140" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="100" fill="none" stroke="{LINE}" stroke-width="1" opacity="0.75"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="50" fill="none" stroke="{LINE}" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.5"/>')
    s.append(f'<line x1="{rx-160}" y1="{ry}" x2="{rx+160}" y2="{ry}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')
    s.append(f'<line x1="{rx}" y1="{ry-160}" x2="{rx}" y2="{ry+160}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')

    radar_ticks = []
    for i in range(72):
        angle = i * 360 / 72
        largo = 9 if i % 6 == 0 else 5
        col = AMB if i % 18 == 0 else (MID if i % 6 == 0 else DIM)
        radar_ticks.append(f'<line x1="0" y1="-100" x2="0" y2="{-100-largo}" stroke="{col}" stroke-width="1.1" '
                           f'transform="rotate({angle:.1f})" opacity="0.7"/>')
    s.append(f'<g transform="translate({rx} {ry})"><g>{" ".join(radar_ticks)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="120s" repeatCount="indefinite"/></g></g>')

    s.append(f'<g transform="translate({rx} {ry})"><g>'
             f'<path d="M 0 0 L -50 -86 A 100 100 0 0 1 0 -100 Z" fill="url(#sweepGrad)"/>'
             f'<line x1="0" y1="0" x2="0" y2="-100" stroke="{AMB}" stroke-width="1.5" opacity="0.85"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></g></g>')

    # Curva de trayectoria espacial
    traj_d = f"M 680 {h-45} C 900 {h-75}, {w-450} 170, {w-60} 70"
    s.append(f'<path d="{traj_d}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="6 6" opacity="0.7"/>')
    s.append(f'<path d="{traj_d}" fill="none" stroke="url(#trajGrad)" stroke-width="2.8" stroke-linecap="round"/>')
    s.append(f'<circle cx="{w-60}" cy="70" r="5.5" fill="{AMB}"/>')
    s.append(f'<circle cx="{w-60}" cy="70" r="9" fill="none" stroke="{AMB}" stroke-width="1.2" opacity="0.6"/>')

    # Onda de audio / datos (tributo a Kuidy Lyrics)
    wx, wy = w - 620, 320
    wave_bars = [4, 8, 14, 22, 12, 18, 30, 46, 26, 18, 34, 52, 60, 42, 24, 38, 54, 28, 18, 36, 48, 32, 20, 10, 24, 16, 8, 4]
    bw = 5.5
    for idx, bh in enumerate(wave_bars):
        x_pos = wx + idx * (bw + 3.5)
        s.append(f'<rect x="{x_pos}" y="{wy - bh/2:.1f}" width="{bw}" height="{bh}" rx="2" fill="url(#waveGrad)" opacity="0.8">'
                 f'<animate attributeName="height" values="{bh};{bh*1.35:.1f};{bh*0.75:.1f};{bh}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{wy - bh/2:.1f};{wy - (bh*1.35)/2:.1f};{wy - (bh*0.75)/2:.1f};{wy - bh/2:.1f}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/></rect>')

    s.append(f'<text x="{wx}" y="{wy + 45}" font-family="{MONO}" font-size="10" fill="{DIM}" letter-spacing="1">LIVE STREAM // 16 kB RING &#183; 0-LATENCY OVERLAY</text>')

    # HUD métricas
    s.append(f'<g transform="translate({w-600} 68)"><rect width="116" height="24" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="58" y="16" font-family="{MONO}" font-size="10" fill="{AMB}" text-anchor="middle" font-weight="600">BUFFER: 16 kB</text></g>')
    s.append(f'<g transform="translate({w-465} 68)"><rect width="106" height="24" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="53" y="16" font-family="{MONO}" font-size="10" fill="{MID}" text-anchor="middle">LOSS: 0.0%</text></g>')

    # SECTOR IZQUIERDO: Identidad, Monograma y Textos
    mx, my = 140, 180
    marcas_mono = []
    for i in range(48):
        a = i * 360 / 48
        largo = 9 if i % 4 == 0 else 4.5
        col = AMB if i % 12 == 0 else (MID if i % 4 == 0 else DIM)
        marcas_mono.append(f'<line x1="0" y1="-72" x2="0" y2="{-72-largo}" stroke="{col}" stroke-width="1.2" '
                           f'stroke-linecap="round" opacity="0.55" transform="rotate({a:.1f})"/>')

    s.append(f'<g transform="translate({mx} {my})"><g>{" ".join(marcas_mono)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="180s" repeatCount="indefinite"/></g></g>')
    s.append(f'<circle cx="{mx}" cy="{my}" r="68" fill="#191817" stroke="{LINE}" stroke-width="1.2"/>')
    s.append(f'<g transform="translate({mx-31} {my-37}) scale(0.14)">{MONOGRAMA}</g>')

    tx = 255
    s.append(f'<text x="{tx}" y="136" font-family="{MONO}" font-size="12" fill="{AMB}" letter-spacing="2" font-weight="600">DEVELOPER &amp; SYSTEMS CREATOR</text>')
    s.append(f'<text x="{tx}" y="190" font-family="{SANS}" font-size="52" font-weight="700" fill="{INK}" letter-spacing="-1.5">Yoiber</text>')
    s.append(f'<text x="{tx}" y="230" font-family="{SANS}" font-size="17.5" fill="{MID}">Full-stack developer &#183; distributed systems, field devices, live data</text>')

    s.append(f'<line x1="{tx}" y1="254" x2="{tx+620}" y2="254" stroke="{LINE}" stroke-width="1.2"/>')

    s.append(f'<text x="{tx}" y="284" font-family="{MONO}" font-size="14" font-weight="600" fill="{AMB}">yoiber.com</text>')
    s.append(f'<text x="{tx+120}" y="284" font-family="{MONO}" font-size="13.5" fill="{MID}">&#183; React 19 &#183; TypeScript &#183; Rust &#183; Go &#183; Docker</text>')

    s.append(f'<text x="{tx}" y="328" font-family="{MONO}" font-size="12" fill="{DIM}">&#171; The best error message is the one that never appears. &#187;</text>')

    s.append(f'<rect width="{w}" height="{h}" fill="none" stroke="{LINE}" stroke-width="1.5" rx="16"/>')
    s.append('</g>')
    s.append('</svg>')

    return "\n".join(s)

def main():
    # 1. Generar SVG base 1600x423 (Buy Me a Coffee oficial)
    svg_bmc = build_svg_1600(1600, 423)
    svg_path = ASSETS / "banner.svg"
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_bmc)
    print(f"Generado SVG: {svg_path} ({len(svg_bmc)} bytes)")

    # 2. PNG 1600x423 (medida oficial de Buy Me a Coffee)
    png_bmc = ASSETS / "banner.png"
    subprocess.run(["rsvg-convert", "-w", "1600", "-h", "423", "-o", str(png_bmc), str(svg_path)], check=True)
    print(f"Generado PNG (1600x423): {png_bmc} ({png_bmc.stat().st_size} bytes)")

    # 3. PNG Retina @2x (3200x846)
    png2x = ASSETS / "banner@2x.png"
    subprocess.run(["rsvg-convert", "-w", "3200", "-h", "846", "-o", str(png2x), str(svg_path)], check=True)
    print(f"Generado PNG @2x (3200x846): {png2x} ({png2x.stat().st_size} bytes)")

    # 4. PNG 1600x400 (variante panorámica 4:1)
    svg_400 = build_svg_1600(1600, 400)
    tmp_svg_400 = "/tmp/banner_1600x400.svg"
    with open(tmp_svg_400, "w", encoding="utf-8") as f:
        f.write(svg_400)
    png_400 = ASSETS / "banner-1600x400.png"
    subprocess.run(["rsvg-convert", "-w", "1600", "-h", "400", "-o", str(png_400), tmp_svg_400], check=True)
    print(f"Generado PNG (1600x400): {png_400} ({png_400.stat().st_size} bytes)")

    # 5. PNG 1200x400 (proporción 3:1 recomendada para Ko-fi)
    png_kofi = ASSETS / "banner-1200x400.png"
    subprocess.run(["rsvg-convert", "-w", "1200", "-h", "400", "-o", str(png_kofi), str(svg_path)], check=True)
    print(f"Generado PNG (1200x400 Ko-fi): {png_kofi} ({png_kofi.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
