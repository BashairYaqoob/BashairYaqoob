"""Karachi — The City of Lights.

Data mapping (chronology preserved, like GitHub's own graph):
  * one building per week, oldest on the left, newest on the right
  * seven floors per building, one per day, Sunday at street level
  * a floor's windows light up when that day had contributions; GitHub's level (1-4)
    sets how bright they burn
  * building height follows the week's total (square-root scale so quiet weeks still read)
Landmarks in the haze behind (Mazar-e-Quaid, Frere Hall, Empress Market) are scenery, not data.
"""
from __future__ import annotations

import math
import random

from ..data import Year
from ..svg import INK, document, esc

W, H = 1000, 580
X0, X1 = 56, W - 56
GROUND = 418
MAX_H, MIN_H = 176, 30
WINDOW = {0: "#16264A", 1: "#A8692F", 2: "#F4B04A", 3: "#FFD58C", 4: "#FFF3D1"}


def _landmarks(base):
    """Far-plane silhouettes, drawn from each building's real proportions, simplified."""
    def mazar(x, s=1.0):  # square marble base with arched faces, tall pointed dome
        p = lambda v: v * s
        return (f'<path d="M{x} {base} v{-p(46)} h{p(110)} v{p(46)}z"/>'
                f'<path d="M{x+p(14)} {base-p(46)} C{x+p(12)} {base-p(104)} {x+p(52)} {base-p(118)} {x+p(55)} {base-p(132)} '
                f'C{x+p(58)} {base-p(118)} {x+p(98)} {base-p(104)} {x+p(96)} {base-p(46)}z"/>'
                + "".join(f'<path class="arch" d="M{x+p(a)} {base} v{-p(20)} q{p(9)} {-p(14)} {p(18)} 0 v{p(20)}"/>'
                          for a in (12, 46, 80)))

    def frere(x):  # gothic hall with stepped wings and a central tower + pointed roof
        return (f'<path d="M{x} {base} v-40 l8 -10 h16 v-10 h10 v-38 l12 -30 l12 30 v38 h10 v10 h16 l8 10 v40z"/>'
                f'<path class="arch" d="M{x+34} {base-60} q8 -12 16 0"/><path class="arch" d="M{x+12} {base} v-18 q6 -8 12 0 v18 M{x+68} {base} v-18 q6 -8 12 0 v18"/>')

    def empress(x):  # long market hall, slim clock tower with spire
        return (f'<path d="M{x} {base} v-36 l10 -8 h20 v-86 l4 -6 v-14 l6 -16 l6 16 v14 l4 6 v86 h20 l10 8 v36z"/>'
                f'<circle class="clock" cx="{x+40}" cy="{base-112}" r="5"/>')

    def tower(x, w, h):
        return f'<rect x="{x}" y="{base-h}" width="{w}" height="{h}"/>'

    return "".join([
        tower(64, 18, 150), mazar(112, 1.25), tower(292, 22, 196), tower(320, 15, 160),
        frere(436), tower(600, 26, 214), tower(632, 18, 176), empress(742), tower(880, 24, 186),
    ])


def render(year: Year) -> str:
    rnd = random.Random(1947)
    weeks = year.weeks
    pitch = (X1 - X0) / len(weeks)
    bw = pitch - 3.4
    peak = max(year.week_total(i) for i in range(len(weeks))) or 1

    blds, roofs, wins, refl, months = [], [], [], [], []
    for i, week in enumerate(weeks):
        total = year.week_total(i)
        h = MIN_H + (MAX_H - MIN_H) * math.sqrt(total / peak) if total else MIN_H - 6 + rnd.random() * 6
        x = X0 + i * pitch
        y = GROUND - h
        fh = h / 7
        blds.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bw:.1f}" height="{h:.1f}"/>')
        roll = rnd.random()
        if roll < .34:  # rooftop water tank, the Karachi signature
            roofs.append(f'<rect x="{x+bw*.5:.1f}" y="{y-6:.1f}" width="{bw*.36:.1f}" height="4.2" rx="1"/>'
                         f'<path d="M{x+bw*.56:.1f} {y-1.8:.1f}v1.8M{x+bw*.8:.1f} {y-1.8:.1f}v1.8" stroke="#1B2C4B"/>')
        elif roll < .48 and h > 60:  # antenna with aviation light
            roofs.append(f'<path d="M{x+bw*.3:.1f} {y:.1f}v-9" stroke="#26395E" stroke-width=".8"/>'
                         f'<circle class="beacon" style="animation-delay:{rnd.random()*2.6:.1f}s" cx="{x+bw*.3:.1f}" cy="{y-10:.1f}" r="1.3" fill="{INK["coral"]}"/>')
        elif roll < .6 and h > 44:  # stair cabin
            roofs.append(f'<rect x="{x+1:.1f}" y="{y-5:.1f}" width="{bw*.42:.1f}" height="5"/>')

        for k, day in enumerate(week):  # k=0 is Sunday, at street level
            if day.count is None:
                continue
            wy = GROUND - (k + 1) * fh + fh * .26
            wh = max(fh * .48, 1.5)
            for j in range(2):
                wx = x + 2.3 + j * (bw - 4.6 - 3.6)
                if day.count:
                    lit = WINDOW[day.level]
                    cls = "lw tw" if rnd.random() < .07 else "lw"
                    t = 0.5 + i * 0.07 + k * 0.01
                    wins.append(f'<rect class="{cls}" style="animation-delay:{t:.2f}s" x="{wx:.1f}" y="{wy:.1f}" '
                                f'width="3.6" height="{wh:.1f}" fill="{lit}"/>')
                else:
                    wins.append(f'<rect x="{wx:.1f}" y="{wy:.1f}" width="3.6" height="{wh:.1f}" fill="{WINDOW[0]}"/>')
            if day.count:  # reflection on the water, further out for higher floors
                ry = GROUND + 20 + (GROUND - wy) * .36
                refl.append(f'<rect class="rf" style="animation-delay:{(i % 7) * .5:.1f}s" x="{x+bw/2-1-day.level/2:.1f}" '
                            f'y="{ry:.1f}" width="{2+day.level:.0f}" height="1.4" fill="{WINDOW[day.level]}" '
                            f'opacity="{.16+day.level*.07:.2f}"/>')
        for day in week:
            if day.count is not None and day.date.day == 1:
                months.append(f'<text class="m" x="{x+bw/2:.1f}" y="{GROUND+17}" text-anchor="middle">{day.date:%b}</text>')

    bi = year.best_week
    bx = X0 + bi * pitch + bw / 2
    btop = GROUND - (MIN_H + (MAX_H - MIN_H) * math.sqrt(year.week_total(bi) / peak))
    wk0 = weeks[bi][0].date
    marker = (f'<path d="M{bx:.1f} {btop-16:.1f} V{btop-44:.1f}" stroke="{INK["gold"]}" stroke-width=".8" stroke-dasharray="2 2"/>'
              f'<circle cx="{bx:.1f}" cy="{btop-47:.1f}" r="2.6" fill="{INK["gold"]}"/>'
              f'<text class="m tag" x="{bx-9:.1f}" y="{btop-43:.1f}" text-anchor="end">brightest week · {wk0:%d %b} · {year.week_total(bi)}</text>')

    stars = "".join(
        f'<circle cx="{rnd.uniform(24, W-24):.0f}" cy="{rnd.uniform(156, 290):.0f}" r="{rnd.choice([.6, .8, 1.1])}" '
        f'opacity="{rnd.uniform(.2, .7):.2f}"/>' for _ in range(64))
    wave_d = f"M{X0} 0 " + "q 20 -3 40 0 " + "t 40 0 " * 22
    waves = "".join(f'<g transform="translate(0 {GROUND+42+k*21})"><path class="wv" style="animation-delay:{k*.8:.1f}s" d="{wave_d}"/></g>'
                    for k, _ in enumerate(range(5)))
    dhow = (f'<g transform="translate(812 {GROUND+66})"><path d="M0 0h50l-9 8H8z" fill="#0A1A2A" stroke="#2A4560" stroke-width=".7"/>'
            f'<path d="M24 0V-34l18 30z" fill="#12263D" stroke="#2A4560" stroke-width=".7"/>'
            f'<circle class="beacon" cx="24" cy="-36" r="1.3" fill="{INK["amber"]}"/></g>')

    best = year.best_day
    stats = [(f"{year.total}", "contributions"), (f"{year.active_days}", "nights lit"),
             (f"{best.date.day} {best.date:%b}", f"brightest night · {best.count}")]
    stat_svg = "".join(
        f'<text class="m b stat" x="{W-56-(2-k)*142}" y="104" text-anchor="end">{esc(a)}</text>'
        f'<text class="m small" x="{W-56-(2-k)*142}" y="121" text-anchor="end">{esc(b)}</text>'
        for k, (a, b) in enumerate(stats))
    legend = "".join(f'<rect x="{56+k*14}" y="{H-38}" width="9" height="9" rx="1.5" fill="{WINDOW[k]}"/>' for k in range(5))

    title = "Karachi — The City of Lights"
    caption = "each building is a week of my GitHub year · each lit window, a day I shipped code"
    span = f"{year.start:%d %b %Y} → {year.end:%d %b %Y}"
    foot = f"floors run Sun → Sat, street to roof · {span}"

    css = (
        f".m{{fill:{INK['muted']}}}.small{{font-size:9.5px}}text.m.stat{{font-size:20px;fill:{INK['gold']}}}"
        f"text.m.tag{{font-size:10px;fill:{INK['gold']}}}text.m{{font-size:9.5px}}"
        f".far{{fill:#101F3B;stroke:#2B4068;stroke-width:1}}.far .arch,.far .clock{{fill:none;stroke:#34507E}}"
        f".blds{{fill:#0C182D;stroke:#1C2D4C;stroke-width:.6}}.roofs{{fill:#0C182D;stroke:#1C2D4C;stroke-width:.6}}"
        ".lw{animation:on .7s ease-out backwards}@keyframes on{from{opacity:0}}"
        ".tw{animation:on .7s ease-out backwards,tw 7s ease-in-out 6s infinite}"
        "@keyframes tw{45%{opacity:1}50%{opacity:.25}55%{opacity:1}}"
        ".beacon{animation:bl 2.8s steps(1) infinite}@keyframes bl{50%{opacity:.15}}"
        ".rf{animation:sh 4s ease-in-out infinite}@keyframes sh{50%{transform:translateX(2px);opacity:.06}}"
        ".wv{fill:none;stroke:#1C3850;stroke-width:.8;animation:wv 8s ease-in-out infinite}"
        "@keyframes wv{50%{transform:translateX(-14px)}}"
    )
    defs = (
        '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050B18"/>'
        '<stop offset=".64" stop-color="#0C1731"/><stop offset=".72" stop-color="#1B2442"/>'
        '<stop offset=".721" stop-color="#07172A"/><stop offset="1" stop-color="#040D19"/></linearGradient>'
        f'<radialGradient id="moonglow"><stop offset="0" stop-color="{INK["gold"]}" stop-opacity=".32"/>'
        f'<stop offset="1" stop-color="{INK["gold"]}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="haze" cx=".5" cy="1" r=".6"><stop offset="0" stop-color="{INK["ember"]}" stop-opacity=".17"/>'
        f'<stop offset="1" stop-color="{INK["ember"]}" stop-opacity="0"/></radialGradient>'
        f'<clipPath id="card"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/></clipPath>'
    )
    body = f'''<g clip-path="url(#card)">
<rect width="{W}" height="{H}" fill="url(#sky)"/>
<g fill="#C9D4EA">{stars}</g>
<circle cx="566" cy="206" r="48" fill="url(#moonglow)"/>
<path d="M574 187a21 21 0 1 0 9 36a17 17 0 1 1 -9 -36z" fill="{INK['gold']}" opacity=".92"/>
<rect y="{GROUND-230}" width="{W}" height="240" fill="url(#haze)"/>
<g class="far">{_landmarks(GROUND)}</g>
<g class="blds">{"".join(blds)}</g><g class="roofs">{"".join(roofs)}</g>{"".join(wins)}
<rect y="{GROUND}" width="{W}" height="2" fill="#22355A"/>
{"".join(months)}
{waves}{"".join(refl)}{dhow}
<text class="m" x="{W-56}" y="{H-60}" text-anchor="end" style="font-size:9px;letter-spacing:.5em;fill:#2E4A66">ARABIAN SEA</text>
{marker}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="none" stroke="{INK['line']}"/>
<text class="m" x="56" y="58" style="font-size:11px">$ ./render-city --weeks {len(weeks)} --tz Asia/Karachi</text>
<text class="s" x="54" y="104" style="font-size:40px" fill="{INK['cream']}">Karachi <tspan fill="{INK['dim']}">—</tspan> <tspan class="i" fill="{INK['gold']}">The City of Lights</tspan></text>
<text class="m" x="56" y="130" style="font-size:10.5px">{esc(caption)}</text>
{stat_svg}
{legend}
<text class="m" x="{56+5*14+8}" y="{H-30}">dark → brightest · {esc(foot)}</text>'''
    desc = (f"An illustrated Karachi night skyline generated from GitHub contributions, {span}. "
            f"One building per week, seven floors per building (one per day), windows lit on days with contributions. "
            f"{year.total} contributions on {year.active_days} days; brightest day {best.date:%d %B %Y} with {best.count}.")
    text = (title + caption + foot + "".join(a + b for a, b in stats) + "JanFebMarAprMayJunJulAugSepOctNovDec"
            + "$./render-city--weeks0123456789--tzAsia/KarachiARABIANSEAbrightest week·→")
    return document(W, H, body, css=css, defs=defs, text_for_fonts=text, families=("mono", "serif"),
                    title=title, desc=desc)
