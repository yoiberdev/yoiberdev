#!/usr/bin/env python3
"""Genera las tarjetas del perfil desde la API de GitHub. Sin dependencias externas.

POR QUE NO SE USAN LOS SERVICIOS DE SIEMPRE (github-readme-stats, streak-stats).
Tres razones, y las tres se han visto pasar: dependen de una instancia de Vercel o de Heroku
que se cae o se queda sin cuota justo cuando alguien mira el perfil; no cuentan el trabajo
privado, que aqui es el 98 % de la actividad; y su diseño es el de todo el mundo. Estas se
generan cada noche con un Action, viven en el repositorio y se ven igual aunque el mundo arda.

QUE SE ENSEÑA Y QUE NO. Las tarjetas de siempre ponen en grande las estrellas y los seguidores.
Con 3 estrellas y 6 seguidores eso es un autogol. Se enseñan las cifras que son ciertas y
significan algo: contribuciones del año, cuanto de eso es trabajo privado de cliente, commits,
revisiones, la constancia y los lenguajes por bytes de codigo real.

PALETA. La misma de yoiber.com: fondo calido #1f1e1d, tres tonos de gris y el ambar como unico
acento. Nada de azul marino: el tema del sitio es el espacio.
"""
import json, os, sys, urllib.request, datetime as dt
from collections import defaultdict

LOGIN = os.environ.get("GH_LOGIN", "yoiberdev")
TOKEN = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
if not TOKEN:
    sys.exit("Falta GH_TOKEN")

now = dt.datetime.now(dt.timezone.utc)
frm = now - dt.timedelta(days=365)
QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    followers{totalCount}
    repositories(first:100, ownerAffiliations:OWNER, isFork:false, orderBy:{field:STARGAZERS, direction:DESC}){
      totalCount
      nodes{ stargazerCount isPrivate
        languages(first:10, orderBy:{field:SIZE, direction:DESC}){ edges{ size node{ name color } } } }
    }
    contributionsCollection(from:$from,to:$to){
      totalCommitContributions totalPullRequestContributions totalIssueContributions
      totalPullRequestReviewContributions restrictedContributionsCount
      totalRepositoriesWithContributedCommits
      contributionCalendar{ totalContributions weeks{ contributionDays{ date contributionCount } } }
    }
  }
}"""
req = urllib.request.Request("https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN, "from": frm.isoformat(), "to": now.isoformat()}}).encode(),
    headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json", "User-Agent": "profile-stats"})
data = json.load(urllib.request.urlopen(req, timeout=60))
if "errors" in data:
    sys.exit(f"GraphQL: {data['errors']}")
u = data["data"]["user"]
cc = u["contributionsCollection"]
cal = cc["contributionCalendar"]
days = [d for w in cal["weeks"] for d in w["contributionDays"]]

def streaks(days):
    longest = run = cur = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    seq = list(reversed(days))
    if seq and seq[0]["contributionCount"] == 0:
        seq = seq[1:]                      # hoy aun puede estar a cero: no rompe la racha
    for d in seq:
        if d["contributionCount"] > 0: cur += 1
        else: break
    return cur, longest
cur_streak, long_streak = streaks(days)

total    = cal["totalContributions"]
private  = cc["restrictedContributionsCount"]
commits  = cc["totalCommitContributions"]
prs      = cc["totalPullRequestContributions"]
issues   = cc["totalIssueContributions"]
reviews  = cc["totalPullRequestReviewContributions"]
proyectos= cc["totalRepositoriesWithContributedCommits"]
activos  = sum(1 for d in days if d["contributionCount"] > 0)

lang = defaultdict(int); color = {}
for r in u["repositories"]["nodes"]:
    for e in r["languages"]["edges"]:
        lang[e["node"]["name"]] += e["size"]; color[e["node"]["name"]] = e["node"]["color"] or "#93938f"
repos_total = u["repositories"]["totalCount"]
top = sorted(lang.items(), key=lambda x: -x[1])[:6]
lang_total = sum(v for _, v in top) or 1

# ------------------------------------------------------------------ paleta y utiles
BG, INK, MID, DIM, LINE, AMB = "#1f1e1d", "#f4f4f2", "#93938f", "#6a6a66", "#3a3936", "#ffd166"
# Cinco pasos para el mapa de calor: los tres tonos del motor y el ambar arriba del todo.
HEAT = ["#282725", "#3d3d3a", "#6a6a66", "#a8a8a2", AMB]
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif"
def fmt(n): return f"{n:,}"

def estrellas(w, h, n, semilla=7):
    """Campo de estrellas determinista: la misma semilla da el mismo cielo, asi el fichero solo
    cambia cuando cambian los datos y no ensucia el historial con ruido cada noche."""
    s, out = semilla, []
    for _ in range(n):
        s = (1103515245 * s + 12345) % 2147483648; x = s % w
        s = (1103515245 * s + 12345) % 2147483648; y = s % h
        s = (1103515245 * s + 12345) % 2147483648; r = 0.5 + (s % 100) / 120
        s = (1103515245 * s + 12345) % 2147483648; o = 0.10 + (s % 100) / 260
        out.append(f'<circle cx="{x}" cy="{y}" r="{r:.2f}" fill="{INK}" opacity="{o:.2f}"/>')
    return "".join(out)

MONOGRAMA = (
  '<path d="M204.77 0C235.539 0 254.787 33.2885 239.437 59.9551L141.891 229.411L8.98075 65.1621C-12.183 39.0082 '
  '6.43132 0.000141945 40.0755 0H204.77Z" fill="#8F8F8F"/>'
  '<path d="M218.56 324.158C236.233 345.998 270.324 343.292 284.33 318.938L287.17 314H287.248L178.507 502.841C171.367 '
  '515.239 158.15 522.881 143.844 522.881H41.9276C11.1516 522.881 -8.09548 489.579 7.26839 462.912L141.839 229.348L218.56 '
  '324.158Z" fill="#626262"/>'
  '<path d="M398.846 0.0380859C400.995 0.0380805 403.088 0.200518 405.117 0.511719C431.98 4.79989 447.501 35.2121 433.279 '
  '59.9414L284.33 318.938C270.324 343.292 236.234 345.998 218.561 324.158L141.84 229.347L262.418 20.0693C269.559 7.67596 '
  '282.774 0.0390986 297.077 0.0390625L398.846 0.0380859Z" fill="#ffffff"/>')

def marco(w, h, id_):
    """Fondo comun de todas las tarjetas: el fondo calido, el cielo y un borde de un pixel."""
    return (f'<defs><clipPath id="c{id_}"><rect width="{w}" height="{h}" rx="14"/></clipPath></defs>'
            f'<g clip-path="url(#c{id_})"><rect width="{w}" height="{h}" fill="{BG}"/>{estrellas(w, h, int(w*h/2600))}</g>'
            f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="14" fill="none" stroke="{LINE}"/>')

def titulo(x, y, txt, extra=""):
    t = f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="10.5" fill="{MID}" letter-spacing="1.6">{txt}</text>'
    return t + extra

os.makedirs("assets", exist_ok=True)
escritos = []
def escribe(nombre, cuerpo):
    with open(f"assets/{nombre}", "w", encoding="utf-8") as f: f.write(cuerpo)
    escritos.append(nombre)

# ------------------------------------------------------------------ 1. tarjeta de cifras
W, H = 452, 232
# Las filas se eligen a mano y NO se ponen las que valen cero: una tarjeta formal con
# "Pull requests 0" y "Code reviews 0" es un autogol. El trabajo de aqui es de cliente, en
# repositorios privados y sin flujo de revision publica; se enseña lo que hay, no lo que falta.
filas = [("Contributions", fmt(total), INK), ("Private work", fmt(private), AMB),
         ("Public commits", fmt(commits), INK), ("Projects touched", fmt(proyectos), INK),
         ("Active days", f"{activos} / 365", INK), ("Repositories", fmt(repos_total), INK)]
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
     f'aria-label="Last 12 months: {fmt(total)} contributions, {fmt(private)} of them private work">', marco(W, H, "a"),
     titulo(22, 32, "LAST 12 MONTHS"),
     f'<text x="{W-22}" y="32" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end">{now.date().isoformat()}</text>']
for i, (lab, val, col) in enumerate(filas):
    y = 62 + i * 27
    s.append(f'<g opacity="0"><animate attributeName="opacity" to="1" dur="0.45s" begin="{0.07*i:.2f}s" fill="freeze"/>'
             f'<text x="22" y="{y}" font-family="{SANS}" font-size="13" fill="{MID}">{lab}</text>'
             f'<text x="{W-22}" y="{y}" font-family="{MONO}" font-size="15" font-weight="600" fill="{col}" text-anchor="end">{val}</text>'
             f'<line x1="22" y1="{y+9}" x2="{W-22}" y2="{y+9}" stroke="{LINE}"/></g>')
s.append(f'<text x="22" y="{H-16}" font-family="{MONO}" font-size="10" fill="{DIM}">'
         f'{100*private//max(1,total)}% of it in private client repositories</text>')
s.append("</svg>")
escribe("stats.svg", "\n".join(s))

# ------------------------------------------------------------------ 2. tarjeta de constancia
W2, H2 = 424, 232
r, cx, cy = 44, 96, 118
# El aro mide los DIAS ACTIVOS del año, no la racha contra su propio maximo: con la racha
# actual igual a la mas larga el aro salia cerrado del todo y no medía nada.
frac = activos / 365
circ = 2 * 3.14159 * r
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W2} {H2}" width="{W2}" height="{H2}" role="img" '
     f'aria-label="Current streak {cur_streak} days, longest {long_streak} days, {activos} active days this year">',
     marco(W2, H2, "b"), titulo(22, 32, "CONSISTENCY"),
     f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="6"/>',
     f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{AMB}" stroke-width="6" stroke-linecap="round" '
     f'transform="rotate(-90 {cx} {cy})" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{circ:.1f}">'
     f'<animate attributeName="stroke-dashoffset" to="{circ*(1-frac):.1f}" dur="1.1s" begin="0.2s" fill="freeze"/></circle>',
     f'<text x="{cx}" y="{cy+2}" font-family="{MONO}" font-size="30" font-weight="700" fill="{INK}" text-anchor="middle">{activos}</text>',
     f'<text x="{cx}" y="{cy+22}" font-family="{MONO}" font-size="9.5" fill="{MID}" text-anchor="middle" letter-spacing="1">ACTIVE DAYS</text>',
     f'<text x="{cx}" y="{cy+r+26}" font-family="{MONO}" font-size="10" fill="{DIM}" text-anchor="middle">{100*activos//365}% of the year</text>']
der = [("Current streak", f"{cur_streak} d"), ("Longest streak", f"{long_streak} d"),
       ("Busiest day", f"{max(d['contributionCount'] for d in days)}"),
       ("Avg. per active day", f"{total/max(1,activos):.1f}")]
for i, (lab, val) in enumerate(der):
    y = 74 + i * 34
    s.append(f'<text x="180" y="{y}" font-family="{SANS}" font-size="12.5" fill="{MID}">{lab}</text>'
             f'<text x="{W2-22}" y="{y}" font-family="{MONO}" font-size="15" font-weight="600" fill="{INK}" text-anchor="end">{val}</text>'
             f'<line x1="180" y1="{y+10}" x2="{W2-22}" y2="{y+10}" stroke="{LINE}"/>')
s.append("</svg>")
escribe("streak.svg", "\n".join(s))

# ------------------------------------------------------------------ 3. actividad de 52 semanas
W3, H3 = 900, 282
weeks = cal["weeks"][-52:]
# ESCALA POR CUARTILES, no lineal contra el maximo: con un dia de 60 y la mayoria entre 1 y 10,
# la escala lineal metia el 95 % de los dias en el nivel mas bajo y el calendario salia plano.
_nz = sorted(d["contributionCount"] for w in weeks for d in w["contributionDays"] if d["contributionCount"] > 0)
_q = [_nz[int(len(_nz) * f)] for f in (0.35, 0.65, 0.88)] if _nz else [1, 1, 1]
cs, gap, hx, hy = 12, 3.2, 24, 62
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W3} {H3}" width="{W3}" height="{H3}" role="img" '
     f'aria-label="Contribution calendar: {fmt(total)} contributions over the last 52 weeks">',
     marco(W3, H3, "c"), titulo(24, 34, "CONTRIBUTION CALENDAR &#183; 52 WEEKS"),
     f'<text x="{W3-24}" y="34" font-family="{MONO}" font-size="10.5" fill="{DIM}" text-anchor="end">{fmt(total)} total</text>']
vistos = set()
for wi, w in enumerate(weeks):
    for d in w["contributionDays"]:
        di = dt.date.fromisoformat(d["date"]).weekday()
        c = d["contributionCount"]
        lvl = 0 if c == 0 else 1 + sum(c > t for t in _q)
        s.append(f'<rect x="{hx + wi*(cs+gap):.1f}" y="{hy + di*(cs+gap):.1f}" width="{cs}" height="{cs}" rx="2.5" '
                 f'fill="{HEAT[lvl]}" opacity="0"><animate attributeName="opacity" to="1" dur="0.4s" '
                 f'begin="{0.012*wi:.2f}s" fill="freeze"/></rect>')
    p = dt.date.fromisoformat(w["contributionDays"][0]["date"])
    if p.day <= 7 and (p.year, p.month) not in vistos:
        vistos.add((p.year, p.month))
        s.append(f'<text x="{hx + wi*(cs+gap):.1f}" y="{hy + 7*(cs+gap) + 14:.0f}" font-family="{MONO}" font-size="9.5" fill="{DIM}">{p.strftime("%b")}</text>')
# lenguajes, debajo
by = H3 - 58
s.append(f'<text x="24" y="{by-10}" font-family="{MONO}" font-size="10.5" fill="{MID}" letter-spacing="1.6">LANGUAGES BY BYTES OF CODE</text>')
cx2 = 24.0
for i, (name, size) in enumerate(top):
    w = max(5, (W3 - 48) * size / lang_total)
    s.append(f'<rect x="{cx2:.1f}" y="{by}" width="0" height="8" rx="4" fill="{color[name]}">'
             f'<animate attributeName="width" to="{w-2:.1f}" dur="0.8s" begin="{0.08*i:.2f}s" fill="freeze"/></rect>')
    cx2 += w
lx = 24.0
for name, size in top:
    pct = 100 * size / lang_total
    s.append(f'<circle cx="{lx+4}" cy="{by+26}" r="3.5" fill="{color[name]}"/>'
             f'<text x="{lx+13}" y="{by+30}" font-family="{SANS}" font-size="11.5" fill="{INK}">{name} '
             f'<tspan fill="{DIM}">{pct:.0f}%</tspan></text>')
    lx += 30 + 6.9 * (len(name) + 4)
s.append("</svg>")
escribe("activity.svg", "\n".join(s))

# ------------------------------------------------------------------ 4. cabecera
W4, H4 = 900, 200
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W4} {H4}" width="{W4}" height="{H4}" role="img" '
     f'aria-label="Yoiber, full-stack developer">', marco(W4, H4, "d")]
# anillo de marcas, el mismo gesto que la intro de yoiber.com
ax, ay, ar = 128, 100, 62
marcas = []
for i in range(48):
    a = i * 360 / 48
    largo = 9 if i % 4 == 0 else 5
    marcas.append(f'<line x1="0" y1="{-ar}" x2="0" y2="{-ar-largo}" stroke="{MID}" stroke-width="1.3" '
                  f'stroke-linecap="round" opacity="0.45" transform="rotate({a:.1f})"/>')
s.append(f'<g transform="translate({ax} {ay})"><g>{"".join(marcas)}'
         f'<animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="240s" repeatCount="indefinite"/></g></g>')
s.append(f'<g transform="translate({ax-26} {ay-31}) scale(0.1185)">{MONOGRAMA}</g>')
s.append(f'<text x="248" y="88" font-family="{SANS}" font-size="40" font-weight="700" fill="{INK}" letter-spacing="-1">Yoiber</text>'
         f'<text x="248" y="118" font-family="{SANS}" font-size="16" fill="{MID}">Full-stack developer &#183; distributed systems, field devices, live data</text>'
         f'<line x1="248" y1="136" x2="{W4-40}" y2="136" stroke="{LINE}"/>'
         f'<text x="248" y="158" font-family="{MONO}" font-size="12" fill="{AMB}">yoiber.com</text>'
         f'<text x="336" y="158" font-family="{MONO}" font-size="12" fill="{DIM}">&#183; Lima, Peru</text>')
s.append("</svg>")
escribe("header.svg", "\n".join(s))

# ------------------------------------------------------------------ 5. pie: la trayectoria
W5, H5 = 900, 150
s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W5} {H5}" width="{W5}" height="{H5}" role="img" '
     f'aria-label="A trajectory leaving the horizon">', marco(W5, H5, "e"),
     f'<path d="M0 {H5-26} Q 300 {H5-30} {W5} {H5-52}" fill="none" stroke="{LINE}" stroke-width="1"/>']
s.append(f'<path id="tray" d="M40 {H5-30} C 300 {H5-40}, 560 {H5-90}, {W5-60} 26" fill="none" stroke="{AMB}" '
         f'stroke-width="1.6" stroke-linecap="round" stroke-dasharray="1200" stroke-dashoffset="1200" opacity="0.85">'
         f'<animate attributeName="stroke-dashoffset" to="0" dur="3.2s" begin="0.3s" fill="freeze"/></path>')
s.append(f'<circle r="3.5" fill="{AMB}"><animateMotion dur="3.2s" begin="0.3s" fill="freeze" '
         f'path="M40 {H5-30} C 300 {H5-40}, 560 {H5-90}, {W5-60} 26"/></circle>')
s.append(f'<text x="40" y="{H5-58}" font-family="{MONO}" font-size="11" fill="{MID}">'
         f'The best error message is the one that never appears.</text>')
s.append("</svg>")
escribe("footer.svg", "\n".join(s))

print(f"escritos: {', '.join(escritos)}")
print(f"datos: {total} contribuciones ({private} privadas), {commits} commits, {prs} PR, {reviews} revisiones, "
      f"{proyectos} proyectos, racha {cur_streak}/{long_streak}, {activos} dias activos, langs {[n for n,_ in top]}")
