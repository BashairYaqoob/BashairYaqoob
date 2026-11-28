"""Karachi — The City of Lights, isometric edition.

The city is GitHub's contribution graph stood up in 3D:
  * a 53 × 7 grid of plots — columns are weeks (oldest on the left), rows are weekdays
    (Sunday at the back, Saturday on the seafront), exactly like the graph on a profile
  * one building per day: height and lit windows follow that day's contribution count;
    GitHub's level (1-4) sets how bright the windows burn
  * quiet days stay as low, dark houses — Karachi's low-rise sprawl around the lit towers
Landmarks in the haze across the harbour (Mazar-e-Quaid, Frere Hall, Empress Market) are
scenery, not data.
"""
from __future__ import annotations

import math
import random

from ..data import Year
from ..svg import INK, document, esc
from .city import WINDOW

W, H = 1000, 640
S = 15.5                      # plot size in px
AX, AY = math.radians(15), math.radians(40)   # screen angles of the week and weekday axes
CA, SA, CB, SB = math.cos(AX), math.sin(AX), math.cos(AY), math.sin(AY)
OX, OY = 60 + 7 * S * CB, 262  # screen position of the back-left corner of the grid
MARGIN = 0.15                 # gap between neighbouring buildings, as a share of a plot
TALLEST = 150                 # px height of the busiest day
FLOOR = 7.5                   # px per storey

FACE = dict(top="#1B2C4F", front="#0F1D37", side="#0A1528", edge="#22355A")
LIT_TOP = "#2A3550"


def _skyline_behind():
    """Landmarks standing just behind the grid's back (Sunday) edge, in perspective order."""
    def at(week):  # screen x and ground y a little behind the back edge at a given week
        x, y = P(week, -0.8)
        return x, y

    def mazar(week, s=.95):
        x, b = at(week)
        p = lambda v: v * s
        x -= p(55)
        return (f'<path d="M{x:.1f} {b:.1f} v{-p(46):.1f} h{p(110):.1f} v{p(46):.1f}z"/>'
                f'<path d="M{x+p(14):.1f} {b-p(46):.1f} C{x+p(12):.1f} {b-p(104):.1f} {x+p(52):.1f} {b-p(118):.1f} {x+p(55):.1f} {b-p(132):.1f} '
                f'C{x+p(58):.1f} {b-p(118):.1f} {x+p(98):.1f} {b-p(104):.1f} {x+p(96):.1f} {b-p(46):.1f}z"/>'
                + "".join(f'<path class="arch" d="M{x+p(a):.1f} {b:.1f} v{-p(20):.1f} q{p(9):.1f} {-p(14):.1f} {p(18):.1f} 0 v{p(20):.1f}"/>'
                          for a in (12, 46, 80)))

    def frere(week):
        x, b = at(week)
        x -= 46
        return (f'<path d="M{x:.1f} {b:.1f} v-40 l8 -10 h16 v-10 h10 v-38 l12 -30 l12 30 v38 h10 v10 h16 l8 10 v40z"/>'
                f'<path class="arch" d="M{x+34:.1f} {b-60:.1f} q8 -12 16 0"/>')

    def empress(week):
        x, b = at(week)
        x -= 40
        return (f'<path d="M{x:.1f} {b:.1f} v-36 l10 -8 h20 v-86 l4 -6 v-14 l6 -16 l6 16 v14 l4 6 v86 h20 l10 8 v36z"/>'
                f'<circle class="clock" cx="{x+40:.1f}" cy="{b-112:.1f}" r="5"/>')

    def tower(week, w, h):
        x, b = at(week)
        return f'<rect x="{x:.1f}" y="{b-h:.1f}" width="{w}" height="{h}"/>'

    return "".join([tower(3, 16, 92), mazar(9), tower(16, 20, 150), tower(18, 14, 118), frere(24),
                    tower(31, 22, 176), tower(33, 16, 140), empress(39), tower(46, 20, 160), tower(50, 14, 120)])


def P(x, y, z=0.0):
    """World (week, weekday, height px) → screen."""
    return OX + S * (x * CA - y * CB), OY + S * (x * SA + y * SB) - z


def _pts(*pts):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)


def _building(i, k, day, peak, rnd, out, wins, extras):
    x0, x1 = i + MARGIN, i + 1 - MARGIN
    y0, y1 = k + MARGIN, k + 1 - MARGIN
    lit = bool(day.count)
    h = 10 + (TALLEST - 10) * math.sqrt(day.count / peak) if lit else 3 + rnd.random() * 3.5
    top = [P(x0, y0, h), P(x1, y0, h), P(x1, y1, h), P(x0, y1, h)]
    front = [P(x0, y1, 0), P(x1, y1, 0), P(x1, y1, h), P(x0, y1, h)]   # faces the sea (+weekday)
    side = [P(x1, y0, 0), P(x1, y1, 0), P(x1, y1, h), P(x1, y0, h)]    # faces the future (+week)
    out.append(f'<polygon class="sd" points="{_pts(*side)}"/><polygon class="fr" points="{_pts(*front)}"/>'
               f'<polygon class="{"tl" if lit else "tp"}" points="{_pts(*top)}"/>')
    if not lit:
        return h
    # windows, drawn in each face's own plane via an affine matrix: local u along the face, v up
    floors = max(1, int((h - 4) // FLOOR))
    face_len = (1 - 2 * MARGIN) * S
    color = WINDOW[day.level]
    t = 0.5 + i * 0.06 + k * 0.008
    fx, fy = P(x0, y1, 0)
    sx, sy = P(x1, y0, 0)
    rows_front, rows_side = [], []
    for f in range(floors):
        v = 3 + f * FLOOR
        for u in (2.0, face_len - 4.6):
            if rnd.random() < .86:
                rows_front.append(f'<rect x="{u:.1f}" y="{-v-3.4:.1f}" width="2.6" height="3.4"/>')
        if rnd.random() < .7:
            rows_side.append(f'<rect x="{face_len/2-1.2:.1f}" y="{-v-3.4:.1f}" width="2.4" height="3.4"/>')
    cls = "lw tw" if rnd.random() < .1 else "lw"
    wins.append(f'<g class="{cls}" style="animation-delay:{t:.2f}s" fill="{color}">'
                f'<g transform="matrix({CA:.4f} {SA:.4f} 0 1 {fx:.1f} {fy:.1f})">{"".join(rows_front)}</g>'
                f'<g transform="matrix({-CB:.4f} {SB:.4f} 0 1 {sx:.1f} {sy:.1f})" opacity=".7">{"".join(rows_side)}</g></g>')
    if h > 70 and rnd.random() < .6:  # rooftop aviation light
        cx, cy = P(i + .5, k + .5, h)
        extras.append(f'<path d="M{cx:.1f} {cy:.1f}v-9" stroke="#2B4068" stroke-width=".8"/>'
                      f'<circle class="beacon" style="animation-delay:{rnd.random()*2.6:.1f}s" cx="{cx:.1f}" cy="{cy-10:.1f}" r="1.4" fill="{INK["coral"]}"/>')
    elif rnd.random() < .35:  # rooftop water tank
        cx, cy = P(x0 + .2, y0 + .2, h)
        extras.append(f'<rect x="{cx:.1f}" y="{cy-4:.1f}" width="5" height="4" rx="1" fill="#14233F" stroke="#22355A" stroke-width=".5"/>')
    return h


def render(year: Year) -> str:
    rnd = random.Random(1947)
    weeks = year.weeks
    n = len(weeks)
    peak = max((d.count for d in year.days), default=1) or 1
    best = year.best_day

    # ground: the grid plate, a promenade along the seafront and the sea below it
    plate = [P(0, 0), P(n, 0), P(n, 7), P(0, 7)]
    prom = [P(0, 7), P(n, 7), P(n, 7.45), P(0, 7.45)]
    sea_top = [P(0, 7.45), P(n, 7.45)]
    sea = f'{_pts(*sea_top)} {W},{sea_top[1][1]:.1f} {W},{H} 0,{H} 0,{sea_top[0][1]:.1f}'

    cells = sorted(((i, k) for i in range(n) for k in range(7)), key=lambda c: c[0] * SA + c[1] * SB)
    blds, wins, extras, best_top = [], [], [], None
    for i, k in cells:
        day = weeks[i][k]
        if day.count is None:
            continue  # outside the 365-day window: an empty plot
        h = _building(i, k, day, peak, rnd, blds, wins, extras)
        if day.date == best.date:
            best_top = P(i + .5, k + .5, h)

    months = []
    for i, week in enumerate(weeks):
        for day in week:
            if day.count is not None and day.date.day == 1:
                lx, ly = P(i + .5, 7.95)
                months.append(f'<text class="m mo" transform="translate({lx:.1f} {ly:.1f}) rotate(15)" text-anchor="middle">{day.date:%b}</text>')

    waves = "".join(
        f'<g transform="translate(0 {34 + r*22})"><path class="wv" style="animation-delay:{r*.8:.1f}s" '
        f'd="M{P(-1, 7.45)[0]:.0f} {P(-1, 7.45)[1]:.0f} L{P(n+3, 7.45)[0]:.0f} {P(n+3, 7.45)[1]:.0f}" stroke-dasharray="{6+r*3} {10+r*4}"/></g>'
        for r in range(6))
    bx, by = best_top
    marker = (f'<path d="M{bx:.1f} {by-14:.1f} V{by-46:.1f}" stroke="{INK["gold"]}" stroke-width=".8" stroke-dasharray="2 2"/>'
              f'<circle cx="{bx:.1f}" cy="{by-49:.1f}" r="2.6" fill="{INK["gold"]}"/>'
              f'<text class="m tag" x="{bx-9:.1f}" y="{by-45:.1f}" text-anchor="end">brightest night · {best.date:%d %b} · {best.count}</text>')
    dhow = (f'<g transform="translate(150 {H-96})"><path d="M0 0h50l-9 8H8z" fill="#0A1A2A" stroke="#2A4560" stroke-width=".7"/>'
            f'<path d="M24 0V-34l18 30z" fill="#12263D" stroke="#2A4560" stroke-width=".7"/>'
            f'<circle class="beacon" cx="24" cy="-36" r="1.3" fill="{INK["amber"]}"/></g>')
    stars = "".join(
        f'<circle cx="{rnd.uniform(380, W-24):.0f}" cy="{rnd.uniform(150, 250):.0f}" r="{rnd.choice([.6, .8, 1.1])}" '
        f'opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(52))

    stats = [(f"{year.total}", "contributions"), (f"{year.active_days}", "nights lit"),
             (f"{year.longest_streak}", "longest streak")]
    stat_svg = "".join(
        f'<text class="m b stat" x="{W-56-(2-k)*142}" y="104" text-anchor="end">{esc(a)}</text>'
        f'<text class="m small" x="{W-56-(2-k)*142}" y="121" text-anchor="end">{esc(b)}</text>'
        for k, (a, b) in enumerate(stats))
    legend = "".join(f'<rect x="{56+k*14}" y="{H-38}" width="9" height="9" rx="1.5" fill="{WINDOW[k]}"/>' for k in range(5))

    title = "Karachi — The City of Lights"
    caption = "my GitHub year, built in 3D · one building per day, a lit window for every day I shipped code"
    span = f"{year.start:%d %b %Y} → {year.end:%d %b %Y}"
    foot = f"weeks run left → right, Sunday at the back, Saturday on the seafront · {span}"

    css = (
        f".m{{fill:{INK['muted']}}}text.m{{font-size:9.5px}}.small{{font-size:9.5px}}"
        f"text.m.stat{{font-size:20px;fill:{INK['gold']}}}text.m.tag{{font-size:10px;fill:{INK['gold']}}}"
        f"text.m.mo{{font-size:9px;fill:#5B6E92}}"
        f".far{{fill:#0F1C36;stroke:#22355A;stroke-width:.9}}.far .arch,.far .clock{{fill:none;stroke:#2B4068}}"
        f".tp{{fill:{FACE['top']}}}.tl{{fill:{LIT_TOP}}}.fr{{fill:{FACE['front']}}}.sd{{fill:{FACE['side']}}}"
        f".blds polygon{{stroke:{FACE['edge']};stroke-width:.5;stroke-linejoin:round}}"
        ".lw{animation:on .7s ease-out backwards}@keyframes on{from{opacity:0}}"
        ".tw{animation:on .7s ease-out backwards,tw 7s ease-in-out 6s infinite}"
        "@keyframes tw{45%{opacity:1}50%{opacity:.25}55%{opacity:1}}"
        ".beacon{animation:bl 2.8s steps(1) infinite}@keyframes bl{50%{opacity:.15}}"
        ".wv{fill:none;stroke:#1C3850;stroke-width:.9;animation:wv 9s ease-in-out infinite}"
        "@keyframes wv{50%{transform:translateX(-16px)}}"
    )
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050B18"/>'
        '<stop offset=".7" stop-color="#0D1833"/><stop offset="1" stop-color="#101A36"/></linearGradient>'
        '<linearGradient id="sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#08192C"/>'
        '<stop offset="1" stop-color="#040D19"/></linearGradient>'
        f'<radialGradient id="moonglow"><stop offset="0" stop-color="{INK["gold"]}" stop-opacity=".32"/>'
        f'<stop offset="1" stop-color="{INK["gold"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="haze" cx=".7" cy=".55" r=".55"><stop offset="0" stop-color="{INK["ember"]}" stop-opacity=".14"/>'
        f'<stop offset="1" stop-color="{INK["ember"]}" stop-opacity="0"/></radialGradient>'
                f'<clipPath id="card"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/></clipPath>'
    )
    body = f'''<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g fill="#C9D4EA">{stars}</g>
<circle cx="860" cy="210" r="48" fill="url(#moonglow)"/>
<path d="M868 191a21 21 0 1 0 9 36a17 17 0 1 1 -9 -36z" fill="{INK['gold']}" opacity=".92"/>
<rect width="{W}" height="{H}" fill="url(#haze)"/>
<g class="far">{_skyline_behind()}</g>
<polygon points="{sea}" fill="url(#sea)"/>
{waves}{dhow}
<polygon points="{_pts(*plate)}" fill="#0B1528" stroke="#1C2D4C" stroke-width=".8"/>
<polygon points="{_pts(*prom)}" fill="#152440"/>
<g class="blds">{"".join(blds)}</g>{"".join(extras)}{"".join(wins)}
{"".join(months)}
{marker}
<text class="m" x="{W-56}" y="{H-60}" text-anchor="end" style="font-size:9px;letter-spacing:.5em;fill:#2E4A66">ARABIAN SEA</text>
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{INK['line']}"/>
<text class="m" x="56" y="58" style="font-size:11px">$ ./render-city --3d --days {len(year.days)} --tz Asia/Karachi</text>
<text class="s" x="54" y="104" style="font-size:40px" fill="{INK['cream']}">Karachi <tspan fill="{INK['dim']}">—</tspan> <tspan class="i" fill="{INK['gold']}">The City of Lights</tspan></text>
<text class="m" x="56" y="130" style="font-size:10.5px">{esc(caption)}</text>
{stat_svg}
{legend}
<text class="m" x="{56+5*14+8}" y="{H-30}">dark → brightest · {esc(foot)}</text>'''
    desc = (f"An isometric Karachi night skyline built from GitHub contributions, {span}: a 53-by-7 grid laid out like "
            f"the contribution graph, one building per day, taller and brighter on busier days. {year.total} "
            f"contributions on {year.active_days} days; brightest day {best.date:%d %B %Y} with {best.count}.")
    text = (title + caption + foot + "".join(a + b for a, b in stats) + "JanFebMarAprMayJunJulAugSepOctNovDec"
            + "$./render-city--3d--days0123456789--tzAsia/KarachiARABIANSEAbrightest night·→")
    return document(W, H, body, css=css, defs=defs, text_for_fonts=text, families=("mono", "serif"),
                    title=title, desc=desc)
