#!/usr/bin/env python3
"""Genera assets/stats.svg con métricas reales de GitHub (últimos 12 meses).
Usa la API GraphQL con el token de GH_TOKEN. Sin dependencias externas."""
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

# rachas
def streaks(days):
    cur = longest = run = 0
    for d in days:
        run = run + 1 if d["contributionCount"] > 0 else 0
        longest = max(longest, run)
    # racha actual: contar hacia atrás desde hoy (o ayer si hoy está a cero)
    seq = list(reversed(days))
    if seq and seq[0]["contributionCount"] == 0:
        seq = seq[1:]
    for d in seq:
        if d["contributionCount"] > 0: cur += 1
        else: break
    return cur, longest
cur_streak, long_streak = streaks(days)

stars = sum(r["stargazerCount"] for r in u["repositories"]["nodes"])
repos = u["repositories"]["totalCount"]
followers = u["followers"]["totalCount"]
total = cal["totalContributions"]  # ya incluye las privadas si el token las ve
private = cc["restrictedContributionsCount"]
commits = cc["totalCommitContributions"]
prs = cc["totalPullRequestContributions"]
issues = cc["totalIssueContributions"]
reviews = cc["totalPullRequestReviewContributions"]

# lenguajes por bytes
lang = defaultdict(int); color = {}
for r in u["repositories"]["nodes"]:
    for e in r["languages"]["edges"]:
        lang[e["node"]["name"]] += e["size"]; color[e["node"]["name"]] = e["node"]["color"] or "#8FA7B5"
top = sorted(lang.items(), key=lambda x: -x[1])[:6]
lang_total = sum(v for _, v in top) or 1

# --- SVG ---
W, H = 900, 300
BG, INK, MUTED, ACC, AMB = "#0B1620", "#E8F1F5", "#8FA7B5", "#35D0E0", "#F2B441"
SHADES = ["#132A3C", "#16505C", "#1E8A98", "#35D0E0", "#9BEAF2"]
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"
def fmt(n): return f"{n:,}".replace(",", " ")

out = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="GitHub activity of {LOGIN}: {fmt(total)} contributions in the last 12 months">',
 '<defs><clipPath id="s"><rect width="900" height="300" rx="16"/></clipPath>',
 '<pattern id="g" width="30" height="30" patternUnits="userSpaceOnUse"><path d="M30 0H0V30" fill="none" stroke="#132A3C"/></pattern></defs>',
 f'<g clip-path="url(#s)" font-family="{FONT}"><rect width="900" height="300" fill="{BG}"/><rect width="900" height="300" fill="url(#g)"/>']

# título
out.append(f'<text x="30" y="36" font-size="12" fill="{MUTED}" letter-spacing="2">ACTIVITY · LAST 12 MONTHS</text>')
out.append(f'<text x="870" y="36" font-size="11" fill="{MUTED}" text-anchor="end">updated {now.date().isoformat()}</text>')

# cifras grandes (2 filas x 3)
cells = [("contributions", total), ("public commits", commits), ("private work", private),
         ("stars earned", stars), ("current streak", f"{cur_streak}d"), ("longest streak", f"{long_streak}d")]
for i, (label, val) in enumerate(cells):
    x = 30 + (i % 3) * 150; y = 90 + (i // 3) * 74
    v = fmt(val) if isinstance(val, int) else val
    col = AMB if "streak" in label else INK
    out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="{0.15*i:.2f}s" fill="freeze"/>'
               f'<text x="{x}" y="{y}" font-size="30" font-weight="700" fill="{col}">{v}</text>'
               f'<text x="{x}" y="{y+18}" font-size="11" fill="{MUTED}" letter-spacing="1">{label.upper()}</text></g>')

# mapa de calor: últimas 26 semanas
weeks = cal["weeks"][-26:]
mx = max([d["contributionCount"] for w in weeks for d in w["contributionDays"]] + [1])
hx, hy, cs, gap = 500, 62, 11, 3
out.append(f'<text x="{hx}" y="52" font-size="11" fill="{MUTED}" letter-spacing="1">LAST 26 WEEKS</text>')
months_seen = set()
for wi, w in enumerate(weeks):
    for d in w["contributionDays"]:
        di = dt.date.fromisoformat(d["date"]).weekday()  # lunes=0
        c = d["contributionCount"]
        lvl = 0 if c == 0 else min(4, 1 + int(3 * c / mx))
        out.append(f'<rect x="{hx + wi*(cs+gap)}" y="{hy + di*(cs+gap)}" width="{cs}" height="{cs}" rx="2" fill="{SHADES[lvl]}" opacity="0">'
                   f'<animate attributeName="opacity" from="0" to="1" dur="0.4s" begin="{0.03*wi:.2f}s" fill="freeze"/></rect>')
    first = dt.date.fromisoformat(w["contributionDays"][0]["date"])
    key = (first.year, first.month)
    if first.day <= 7 and key not in months_seen:
        months_seen.add(key)
        out.append(f'<text x="{hx + wi*(cs+gap)}" y="{hy + 7*(cs+gap) + 12}" font-size="10" fill="{MUTED}">{first.strftime("%b")}</text>')

# lenguajes: barra apilada
bx, by, bw, bh = 30, 232, 840, 10
out.append(f'<text x="{bx}" y="{by-12}" font-size="11" fill="{MUTED}" letter-spacing="1">LANGUAGES</text>')
out.append(f'<text x="{bx+bw}" y="{by-12}" font-size="11" fill="{MUTED}" text-anchor="end">{repos} repos · {followers} followers</text>')
cx = bx
for i, (name, size) in enumerate(top):
    w = max(4, bw * size / lang_total)
    out.append(f'<rect x="{cx:.1f}" y="{by}" width="0" height="{bh}" rx="3" fill="{color[name]}">'
               f'<animate attributeName="width" from="0" to="{w:.1f}" dur="0.9s" begin="{0.1*i:.2f}s" fill="freeze"/></rect>')
    cx += w + 2
lx = bx
for name, size in top:
    pct = 100 * size / lang_total
    out.append(f'<circle cx="{lx+5}" cy="{by+30}" r="4" fill="{color[name]}"/>'
               f'<text x="{lx+14}" y="{by+34}" font-size="11" fill="{INK}">{name} <tspan fill="{MUTED}">{pct:.0f}%</tspan></text>')
    lx += 22 + 7.2 * (len(name) + 5)
out.append('</g></svg>')

os.makedirs("assets", exist_ok=True)
with open("assets/stats.svg", "w", encoding="utf-8") as f:
    f.write("\n".join(out))
print(f"stats.svg: {total} contributions, {commits} commits, {prs} PRs, {stars} stars, streak {cur_streak}/{long_streak}, langs {[n for n,_ in top]}")
