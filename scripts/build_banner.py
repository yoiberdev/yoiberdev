#!/usr/bin/env python3
"""Genera los banners de portada oficiales adaptados geométricamente a CADA plataforma:
Cada familia de proporción (3:1, 3.78:1, 4:1) tiene su propia geometría SVG pura
para que los círculos, textos y diales nunca se deformen ni estiren.

Plataformas y resoluciones cubiertas:
  1. Ko-fi:           1200 x 400 px   (3:1 exacta)
  2. Twitter / X:     1500 x 500 px   (3:1 exacta)
  3. Buy Me a Coffee: 1600 x 423 px   (3.78:1 medida oficial de BMC)
  4. LinkedIn:        1584 x 396 px   (4:1 exacta para perfil personal)
  5. Panorámico 4:1:  1600 x 400 px   (4:1 estándar)
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

def generate_banner_svg(w: int, h: int) -> str:
    """Genera un SVG matemáticamente calibrado para la relación de aspecto exacta w x h."""
    s = []
    cid = f"clip-{w}x{h}"
    gid = f"glow-{w}x{h}"
    tid = f"traj-{w}x{h}"
    wid = f"wave-{w}x{h}"
    sid = f"swp-{w}x{h}"

    scale = h / 400.0

    s.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
             f'aria-label="Yoiber · Full-stack developer banner">')
    s.append('<defs>')
    s.append(f'<clipPath id="{cid}"><rect width="{w}" height="{h}" rx="16"/></clipPath>')
    s.append(f'<radialGradient id="{gid}" cx="85%" cy="30%" r="60%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.12"/>'
             f'<stop offset="100%" stop-color="{BG}" stop-opacity="0"/></radialGradient>')
    s.append(f'<linearGradient id="{tid}" x1="0%" y1="100%" x2="100%" y2="0%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.2"/>'
             f'<stop offset="70%" stop-color="{AMB}" stop-opacity="0.95"/>'
             f'<stop offset="100%" stop-color="#ffffff" stop-opacity="1"/></linearGradient>')
    s.append(f'<linearGradient id="{wid}" x1="0%" y1="0%" x2="100%" y2="0%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.35"/>'
             f'<stop offset="50%" stop-color="{AMB}" stop-opacity="0.85"/>'
             f'<stop offset="100%" stop-color="{MID}" stop-opacity="0.4"/></linearGradient>')
    s.append(f'<linearGradient id="{sid}" x1="0%" y1="0%" x2="100%" y2="100%">'
             f'<stop offset="0%" stop-color="{AMB}" stop-opacity="0.35"/>'
             f'<stop offset="100%" stop-color="{AMB}" stop-opacity="0"/></linearGradient>')
    s.append('<style>')
    s.append('@import url("https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&amp;family=Space+Grotesk:wght@500;700&amp;display=swap");')
    s.append('text { text-rendering: geometricPrecision; }')
    s.append('</style>')
    s.append('</defs>')

    s.append(f'<g clip-path="url(#{cid})">')
    s.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>')
    s.append(f'<rect width="{w}" height="{h}" fill="url(#{gid})"/>')

    # Rejilla técnica de fondo
    for gx in range(80, w, 80):
        s.append(f'<line x1="{gx}" y1="0" x2="{gx}" y2="{h}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')
    for gy in range(40, h, 60):
        s.append(f'<line x1="0" y1="{gy}" x2="{w}" y2="{gy}" stroke="{LINE}" stroke-width="0.7" stroke-dasharray="3 9" opacity="0.4"/>')

    # Cruces de esquina
    for cx, cy in [(20, 20), (w-20, 20), (20, h-20), (w-20, h-20)]:
        s.append(f'<path d="M{cx-8} {cy} L{cx+8} {cy} M{cx} {cy-8} L{cx} {cy+8}" stroke="{DIM}" stroke-width="1" opacity="0.55"/>')

    # Barra superior
    s.append(f'<text x="40" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" letter-spacing="1.5">// SYSTEMS ARCHITECTURE &#183; EDGE &#183; TELEMETRY</text>')
    s.append(f'<text x="{w-40}" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end" letter-spacing="1">12&#176;02\'36"S 77&#176;01\'42"W &#183; LIMA, PERU</text>')
    s.append(f'<line x1="40" y1="44" x2="{w-40}" y2="44" stroke="{LINE}" stroke-width="1"/>')

    # SECTOR DERECHO: Radar de telemetría calibrado
    # El centro del radar se adapta según la anchura disponible
    ratio = w / h
    if ratio >= 3.7:
        rx = w - int(250 * scale)
        ry = int(h * 0.52)
        radar_r = int(98 * scale)
    else: # 3:1 (1200x400 / 1500x500)
        rx = w - int(210 * scale)
        ry = int(h * 0.52)
        radar_r = int(92 * scale)

    radar_outer = int(radar_r * 1.4)
    s.append(f'<circle cx="{rx}" cy="{ry}" r="{radar_outer}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="4 6" opacity="0.6"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="{radar_r}" fill="none" stroke="{LINE}" stroke-width="1" opacity="0.75"/>')
    s.append(f'<circle cx="{rx}" cy="{ry}" r="{int(radar_r*0.5)}" fill="none" stroke="{LINE}" stroke-width="0.8" stroke-dasharray="2 4" opacity="0.5"/>')
    s.append(f'<line x1="{rx-radar_outer-15}" y1="{ry}" x2="{rx+radar_outer+15}" y2="{ry}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')
    s.append(f'<line x1="{rx}" y1="{ry-radar_outer-15}" x2="{rx}" y2="{ry+radar_outer+15}" stroke="{LINE}" stroke-width="0.8" opacity="0.55"/>')

    # Ticks del aro
    radar_ticks = []
    for i in range(72):
        angle = i * 360 / 72
        largo = int(8 * scale) if i % 6 == 0 else int(4.5 * scale)
        col = AMB if i % 18 == 0 else (MID if i % 6 == 0 else DIM)
        radar_ticks.append(f'<line x1="0" y1="{-radar_r}" x2="0" y2="{-radar_r-largo}" stroke="{col}" stroke-width="1.1" '
                           f'transform="rotate({angle:.1f})" opacity="0.7"/>')
    s.append(f'<g transform="translate({rx} {ry})"><g>{" ".join(radar_ticks)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="120s" repeatCount="indefinite"/></g></g>')

    # Barrido
    sw_x = int(-radar_r * 0.5)
    sw_y = int(-radar_r * 0.866)
    s.append(f'<g transform="translate({rx} {ry})"><g><path d="M 0 0 L {sw_x} {sw_y} A {radar_r} {radar_r} 0 0 1 0 {-radar_r} Z" fill="url(#{sid})"/>'
             f'<line x1="0" y1="0" x2="0" y2="{-radar_r}" stroke="{AMB}" stroke-width="1.5" opacity="0.85"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="12s" repeatCount="indefinite"/></g></g>')

    # Curva de trayectoria ascendente
    traj_start_x = int(w * 0.44) if ratio >= 3.7 else int(w * 0.42)
    traj_d = f"M {traj_start_x} {h-int(42*scale)} C {traj_start_x+int(190*scale)} {h-int(75*scale)}, {w-int(380*scale)} {int(160*scale)}, {w-50} {int(65*scale)}"
    s.append(f'<path d="{traj_d}" fill="none" stroke="{LINE}" stroke-width="1" stroke-dasharray="6 6" opacity="0.7"/>')
    s.append(f'<path d="{traj_d}" fill="none" stroke="url(#{tid})" stroke-width="2.6" stroke-linecap="round"/>')
    s.append(f'<circle cx="{w-50}" cy="{int(65*scale)}" r="5" fill="{AMB}"/>')
    s.append(f'<circle cx="{w-50}" cy="{int(65*scale)}" r="8.5" fill="none" stroke="{AMB}" stroke-width="1.2" opacity="0.6"/>')

    # Onda de audio / flujo de datos (Kuidy Lyrics tribute)
    wx = rx - int(340 * scale)
    wy = int(h * 0.77)
    wave_bars = [4, 8, 14, 22, 12, 18, 30, 46, 26, 18, 34, 52, 60, 42, 24, 38, 54, 28, 18, 36, 48, 32, 20, 10, 24, 16, 8, 4]
    bw = max(4, int(5.2 * scale))
    gap = max(2, int(3.2 * scale))
    for idx, bh in enumerate(wave_bars):
        scaled_bh = int(bh * scale)
        x_pos = wx + idx * (bw + gap)
        s.append(f'<rect x="{x_pos}" y="{wy - scaled_bh/2:.1f}" width="{bw}" height="{scaled_bh}" rx="2" fill="url(#{wid})" opacity="0.8">'
                 f'<animate attributeName="height" values="{scaled_bh};{scaled_bh*1.35:.1f};{scaled_bh*0.75:.1f};{scaled_bh}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/>'
                 f'<animate attributeName="y" values="{wy - scaled_bh/2:.1f};{wy - (scaled_bh*1.35)/2:.1f};{wy - (scaled_bh*0.75)/2:.1f};{wy - (scaled_bh*0.75)/2:.1f}" dur="{1.4 + (idx%5)*0.2:.2f}s" repeatCount="indefinite"/></rect>')

    s.append(f'<text x="{wx}" y="{wy + int(42*scale)}" font-family="{MONO}" font-size="{9.5*scale:.1f}" fill="{DIM}" letter-spacing="1">LIVE STREAM // 16 kB RING &#183; 0-LATENCY OVERLAY</text>')

    # Placas HUD
    hud_x1 = rx - int(300 * scale)
    hud_x2 = rx - int(175 * scale)
    hud_y = int(66 * scale)
    s.append(f'<g transform="translate({hud_x1} {hud_y})"><rect width="112" height="23" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="56" y="15" font-family="{MONO}" font-size="9.5" fill="{AMB}" text-anchor="middle" font-weight="600">BUFFER: 16 kB</text></g>')
    s.append(f'<g transform="translate({hud_x2} {hud_y})"><rect width="102" height="23" rx="4" fill="#242321" stroke="{LINE}" stroke-width="1"/>'
             f'<text x="51" y="15" font-family="{MONO}" font-size="9.5" fill="{MID}" text-anchor="middle">LOSS: 0.0%</text></g>')

    # SECTOR IZQUIERDO: Monograma y Perfil
    mx = int(120 * scale)
    my = int(h * 0.44)
    mono_r = int(64 * scale)
    marcas_mono = []
    for i in range(48):
        a = i * 360 / 48
        largo = int(8 * scale) if i % 4 == 0 else int(4 * scale)
        col = AMB if i % 12 == 0 else (MID if i % 4 == 0 else DIM)
        marcas_mono.append(f'<line x1="0" y1="{-mono_r-4}" x2="0" y2="{-mono_r-4-largo}" stroke="{col}" stroke-width="1.2" '
                           f'stroke-linecap="round" opacity="0.55" transform="rotate({a:.1f})"/>')

    s.append(f'<g transform="translate({mx} {my})"><g>{" ".join(marcas_mono)}'
             f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="180s" repeatCount="indefinite"/></g></g>')
    s.append(f'<circle cx="{mx}" cy="{my}" r="{mono_r}" fill="#191817" stroke="{LINE}" stroke-width="1.2"/>')
    mono_scale = 0.132 * scale
    s.append(f'<g transform="translate({mx - int(29*scale)} {my - int(35*scale)}) scale({mono_scale:.4f})">{MONOGRAMA}</g>')

    # Textos de perfil
    tx = mx + mono_r + int(36 * scale)
    s.append(f'<text x="{tx}" y="{int(128*scale)}" font-family="{MONO}" font-size="{11.5*scale:.1f}" fill="{AMB}" letter-spacing="2" font-weight="600">DEVELOPER &amp; SYSTEMS CREATOR</text>')
    s.append(f'<text x="{tx}" y="{int(178*scale)}" font-family="{SANS}" font-size="{48*scale:.1f}" font-weight="700" fill="{INK}" letter-spacing="-1.5">Yoiber</text>')
    s.append(f'<text x="{tx}" y="{int(214*scale)}" font-family="{SANS}" font-size="{16.5*scale:.1f}" fill="{MID}">Full-stack developer &#183; distributed systems, field devices, live data</text>')

    sep_width = int(w * 0.38)
    s.append(f'<line x1="{tx}" y1="{int(236*scale)}" x2="{tx+sep_width}" y2="{int(236*scale)}" stroke="{LINE}" stroke-width="1.2"/>')

    s.append(f'<text x="{tx}" y="{int(264*scale)}" font-family="{MONO}" font-size="{13.5*scale:.1f}" font-weight="600" fill="{AMB}">yoiber.com</text>')
    s.append(f'<text x="{tx+int(115*scale)}" y="{int(264*scale)}" font-family="{MONO}" font-size="{13*scale:.1f}" fill="{MID}">&#183; React 19 &#183; TypeScript &#183; Rust &#183; Go &#183; Docker</text>')

    s.append(f'<text x="{tx}" y="{int(306*scale)}" font-family="{MONO}" font-size="{11.5*scale:.1f}" fill="{DIM}">&#171; The best error message is the one that never appears. &#187;</text>')

    s.append(f'<rect width="{w}" height="{h}" fill="none" stroke="{LINE}" stroke-width="1.5" rx="16"/>')
    s.append('</g>')
    s.append('</svg>')
    return "\n".join(s)

def export_target(svg_content: str, svg_file: pathlib.Path, png_file: pathlib.Path, w: int, h: int):
    with open(svg_file, "w", encoding="utf-8") as f:
        f.write(svg_content)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", str(png_file), str(svg_file)], check=True)
    print(f"✓ {png_file.name} [{w}x{h} px, {png_file.stat().st_size // 1024} KB]")

def main():
    print("Generando familia de banners por proporción...")

    # 1. Familia 3.78:1 -> Buy Me a Coffee (1600 x 423)
    svg_bmc = generate_banner_svg(1600, 423)
    export_target(svg_bmc, ASSETS / "banner.svg", ASSETS / "banner.png", 1600, 423)
    export_target(svg_bmc, ASSETS / "banner-buymeacoffee.svg", ASSETS / "banner-buymeacoffee.png", 1600, 423)
    # Retina BMC
    subprocess.run(["rsvg-convert", "-w", "3200", "-h", "846", "-o", str(ASSETS / "banner-buymeacoffee@2x.png"), str(ASSETS / "banner.svg")], check=True)
    subprocess.run(["rsvg-convert", "-w", "3200", "-h", "846", "-o", str(ASSETS / "banner@2x.png"), str(ASSETS / "banner.svg")], check=True)
    print(f"✓ banner@2x.png [3200x846 px, {(ASSETS / 'banner@2x.png').stat().st_size // 1024} KB]")

    # 2. Familia 3:1 -> Ko-fi (1200 x 400) y Twitter/X (1500 x 500)
    svg_3x1 = generate_banner_svg(1200, 400)
    export_target(svg_3x1, ASSETS / "banner-3x1.svg", ASSETS / "banner-1200x400.png", 1200, 400)
    # Copia explícita banner-kofi.png
    subprocess.run(["cp", str(ASSETS / "banner-1200x400.png"), str(ASSETS / "banner-kofi.png")], check=True)
    print(f"✓ banner-kofi.png [1200x400 px, {(ASSETS / 'banner-kofi.png').stat().st_size // 1024} KB]")

    # Twitter / X (misma proporción 3:1 pero a 1500x500)
    svg_twitter = generate_banner_svg(1500, 500)
    export_target(svg_twitter, ASSETS / "banner-twitter.svg", ASSETS / "banner-twitter.png", 1500, 500)

    # 3. Familia 4:1 -> LinkedIn (1584 x 396) y Panorámico (1600 x 400)
    svg_linkedin = generate_banner_svg(1584, 396)
    export_target(svg_linkedin, ASSETS / "banner-4x1.svg", ASSETS / "banner-linkedin.png", 1584, 396)

    svg_1600x400 = generate_banner_svg(1600, 400)
    export_target(svg_1600x400, ASSETS / "banner-1600x400.svg", ASSETS / "banner-1600x400.png", 1600, 400)

if __name__ == "__main__":
    main()
