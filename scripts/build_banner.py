#!/usr/bin/env python3
"""Genera el banner de portada oficial para redes (Ko-fi, Buy Me a Coffee, LinkedIn, GitHub).
Usa exactamente la misma paleta, sistema tipográfico y estética vectorial que build_stats.py
y yoiber.com: fondo cálido #1f1e1d, acento ámbar #ffd166, dial de telemetría y trazas de ingeniería.

Genera:
  - assets/banner.svg      (vectorial SVG con animaciones SMIL)
  - assets/banner.png      (1200 x 400 píxeles, estándar para Ko-fi y Buy Me a Coffee)
  - assets/banner@2x.png   (2400 x 800 píxeles, Retina / alta resolución)
"""
import os
import subprocess
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ASSETS = RAIZ / "assets"
ASSETS.mkdir(exist_ok=True)

W, H = 1200, 400

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

def build_svg():
    s = []
    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
             f'aria-label="Yoiber · Full-stack developer banner">')
    s.append('<defs>')
    s.append(f'<clipPath id="clip-banner"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
    s.append(f'<radialGradient id="ambGlow" cx="85%" cy="30%" r="60%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.12"/>'
             f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/></radialGradient>')
    s.append(f'<linearGradient id="trajGrad" x1="0%" y1="100%" x2="100%" y2="0%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.25"/>'
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
    s.append(f'@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;family=Space+Grotesk:wght@500;700&amp;display=swap");')
    s.append('text { text-rendering: geometricPrecision; }')
    s.append('</style>')
    s.append('</defs>')

    s.append('<g clip-path="url(#clip-banner)">')
    # Fondo base y halo ambiental cálido
    s.append(f'<rect width="{W}" height="{H}" fill="{BG}"/>')
    s.append(f'<rect width="{W}" height="{H}" fill="url(#ambGlow)"/>')

    # Rejilla técnica de fondo
    for x in range(80, W, 80):
        s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{H}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')
    for y in range(40, H, 60):
        s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')

    # Marcas de cruce en las cuatro esquinas
    for cx, cy in [(20, 20), (W-20, 20), (20, H-20), (W-20, H-20)]:
        s.append(f'<path d="M{cx-8} {cy} L{cx+8} {cy} M{cx} {cy-8} L{cx} {cy+8}" stroke="{DIM}" stroke-width="1" opacity="0.55"/>')

    # Barra superior de estado / telemetría
    s.append(f'<text x="40" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1.5">// SYSTEMS ARCHITECTURE &#183; EDGE &#183; TELEMETRY</text>')
    s.append(f'<text x="{W-40}" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end" letter-spacing="1">12&#176;02\'36"S 77&#176;01\'42"W &#183; LIMA, PERU</text>')
    s.append(f'<line x1="40" y1="44" x2="{W-40}" y2="44" stroke="{LINE}" stroke-width="1"/>')

    # SECTOR DERECHO: Radar de telemetría y trayectoria orbital
    rx, ry = 980, 210
    # Círculos concéntricos de rango
    s.append(f'<circle cx="{rx}" cy="{ry}" r="130" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="90" fill="none" stroke="{LINE}" stroke-width="1" opacity="0.75"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="45" fill="none" stroke="{LINE}" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.5"/>')
    s.append(f'<line x1="{rx-145}" y1="{ry}" x2="{rx+145}" y2="{ry}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')
    s.append(f'<line x1="{rx}" y1="{ry-145}" x2="{rx}" y2="{ry+145}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')

    # Marcas del aro exterior (72 marcas a 5°, como en yoiber.com)
    radar_ticks = []
    for i in range(72):
        angle = i * 360 / 72
        largo = 8 if i % 6 == 0 else 4
        col = AMB if i % 18 == 0 else (MID if i % 6 == 0 else DIM)
        radar_ticks.append(f'<line x1="0" y1="-90" x2="0" y2="{-90-largo}" stroke="{col}" stroke-width="1.1" '
                           f'transform="rotate({angle:.1f})" opacity="0.7"/>')
    s.append(f'<g transform="translate({rx} {ry})"><g>{" ".join(radar_ticks)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="120s" repeatCount="indefinite"/></g></g>')

    # Haz de barrido del radar
    s.append(f'<g transform="translate({rx} {ry})"><g>'
             f'<path d="M 0 0 L -45 -78 A 90 90 0 0 1 0 -90 Z" fill="url(#sweepGrad)"/>'
             f'<line x1="0" y1="0" x2="0" y2="-90" stroke="{AMB}" stroke-width="1.5" opacity="0.85"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></g></g>')

    # Curva de trayectoria (renderizada sólida y viva para estáticos y animada para navegadores)
    traj_d = f"M 500 {H-40} C 680 {H-60}, 830 170, {W-60} 70"
    s.append(f'<path d="{traj_d}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="6 6" opacity="0.7"/>')
    s.append(f'<path d="{traj_d}" fill="none" stroke="url(#trajGrad)" stroke-width="2.6" stroke-linecap="round"/>')
    s.append(f'<circle cx="{W-60}" cy="70" r="5" fill="{AMB}"/>')
    s.append(f'<circle cx="{W-60}" cy="70" r="8" fill="none" stroke="{AMB}" stroke-width="1.2" opacity="0.6"/>')

    # Onda de audio / flujo de datos (homenaje a Kuidy Lyrics & telemetría en tiempo real)
    wx, wy = 715, 310
    wave_bars = [4, 8, 14, 20, 10, 16, 28, 42, 24, 18, 30, 48, 56, 38, 22, 34, 50, 26, 16, 32, 44, 30, 18, 10, 22, 14, 8, 4]
    bw = 5
    for idx, bh in enumerate(wave_bars):
        x_pos = wx + idx * (bw + 3)
        s.append(f'<rect x="{x_pos}" y="{wy - bh/2:.1f}" width="{bw}" height="{bh}" rx="2" fill="url(#waveGrad)" opacity="0.8">'
                 f'<animate attributeName="height" values="{bh};{bh*1.35:.1f};{bh*0.75:.1f};{bh}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{wy - bh/2:.1f};{wy - (bh*1.35)/2:.1f};{wy - (bh*0.75)/2:.1f};{wy - bh/2:.1f}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/></rect>')

    s.append(f'<text x="{wx}" y="{wy + 42}" font-family="{MONO}" font-size="9.5" fill="{DIM}" letter-spacing="1">LIVE STREAM // 16 kB RING &#183; 0-LATENCY OVERLAY</text>')

    # Placas HUD de métricas
    s.append(f'<g transform="translate(735 64)"><rect width="112" height="22" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="56" y="15" font-family="{MONO}" font-size="9.5" fill="{AMB}" text-anchor="middle" font-weight="600">BUFFER: 16 kB</text></g>')
    s.append(f'<g transform="translate(860 64)"><rect width="102" height="22" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="51" y="15" font-family="{MONO}" font-size="9.5" fill="{MID}" text-anchor="middle">LOSS: 0.0%</text></g>')

    # SECTOR IZQUIERDO: Identidad, Monograma y Tipografía
    mx, my = 120, 160
    marcas_mono = []
    for i in range(48):
        a = i * 360 / 48
        largo = 8 if i % 4 == 0 else 4
        col = AMB if i % 12 == 0 else (MID if i % 4 == 0 else DIM)
        marcas_mono.append(f'<line x1="0" y1="-68" x2="0" y2="{-68-largo}" stroke="{col}" stroke-width="1.2" '
                           f'stroke-linecap="round" opacity="0.55" transform="rotate({a:.1f})"/>')

    s.append(f'<g transform="translate({mx} {my})"><g>{" ".join(marcas_mono)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="180s" repeatCount="indefinite"/></g></g>')
    s.append(f'<circle cx="{mx}" cy="{my}" r="{64}" fill="#191817" stroke="{LINE}" stroke-width="1.2"/>')
    s.append(f'<g transform="translate({mx-29} {my-35}) scale(0.132)">{MONOGRAMA}</g>')

    # Textos de perfil
    tx = 225
    s.append(f'<text x="{tx}" y="126" font-family="{MONO}" font-size="11" fill="{AMB}" letter-spacing="2" font-weight="600">DEVELOPER &amp; SYSTEMS CREATOR</text>')
    s.append(f'<text x="{tx}" y="178" font-family="{SANS}" font-size="48" font-weight="700" fill="{INK}" letter-spacing="-1.5">Yoiber</text>')
    s.append(f'<text x="{tx}" y="214" font-family="{SANS}" font-size="16.5" fill="{MID}">Full-stack developer &#183; distributed systems, field devices, live data</text>')

    s.append(f'<line x1="{tx}" y1="236" x2="690" y2="236" stroke="{LINE}" stroke-width="1.2"/>')

    s.append(f'<text x="{tx}" y="264" font-family="{MONO}" font-size="13.5" font-weight="600" fill="{AMB}">yoiber.com</text>')
    s.append(f'<text x="{tx+110}" y="264" font-family="{MONO}" font-size="13" fill="{MID}">&#183; React 19 &#183; TypeScript &#183; Rust &#183; Go &#183; Docker</text>')

    s.append(f'<text x="{tx}" y="306" font-family="{MONO}" font-size="11.5" fill="{DIM}">&#171; The best error message is the one that never appears. &#187;</text>')

    # Borde exterior
    s.append(f'<rect width="{W}" height="{H}" fill="none" stroke="{LINE}" stroke-width="1.5" rx="16"/>')
    s.append('</g>')
    s.append('</svg>')

    return "\n".join(s)

def main():
    svg_content = build_svg()
    svg_path = ASSETS / "banner.svg"
    png_path = ASSETS / "banner.png"
    png2x_path = ASSETS / "banner@2x.png"

    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(svg_content)
    print(f"Generado SVG: {svg_path} ({len(svg_content)} bytes)")

    # Renderizado a PNG con rsvg-convert (1200x400)
    subprocess.run(["rsvg-convert", "-w", "1200", "-h", "400", "-o", str(png_path), str(svg_path)], check=True)
    print(f"Generado PNG: {png_path} ({png_path.stat().st_size} bytes)")

    # Renderizado a PNG Retina @2x (2400x800)
    subprocess.run(["rsvg-convert", "-w", "2400", "-h", "800", "-o", str(png2x_path), str(svg_path)], check=True)
    print(f"Generado PNG @2x: {png2x_path} ({png2x_path.stat().st_size} bytes)")

if __name__ == "__main__":
    main()
