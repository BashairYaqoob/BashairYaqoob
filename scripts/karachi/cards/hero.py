"""Hero: editorial night poster — serif ASCII name, tagline, neofetch detail panel and a
line-drawn Karachi skyline whose windows switch on one by one."""
from __future__ import annotations

import random
from pathlib import Path

from .. import content as K
from ..svg import INK, document, esc

W = 1000
ART_DIR = Path(__file__).resolve().parents[1]
FS = 14.5          # ASCII font size; JetBrains Mono advance is 0.6em
LH = FS * 1.08
SKY = 0.7  # skyline drawing scale
CW = FS * 0.6


def _art(word):
    return (ART_DIR / f"art_{word.lower()}.txt").read_text().rstrip("\n").split("\n")


def _skyline(rnd, ground=160):
    """Line drawing: generic towers plus Mazar-e-Quaid, Frere Hall and Empress Market."""
    out, wins = [], []
    plan = [(0, "t", 20, 70), (24, "t", 28, 46), (58, "mazar"), (160, "t", 22, 96), (186, "frere"),
            (276, "t", 26, 58), (306, "empress"), (386, "t", 22, 84), (412, "t", 30, 52), (446, "t", 18, 76)]
    for item in plan:
        x, kind = item[0], item[1]
        if kind == "t":
            w, h = item[2], item[3]
            out.append(f'<rect x="{x}" y="{ground-h}" width="{w}" height="{h}"/>')
            if rnd.random() < .4:
                out.append(f'<rect x="{x+w*.5:.0f}" y="{ground-h-5}" width="{w*.32:.0f}" height="5"/>')
            for wy in range(ground - h + 8, ground - 6, 9):
                for wx in range(x + 5, x + w - 4, 7):
                    if rnd.random() < .17:
                        wins.append((wx, wy))
        elif kind == "mazar":
            out.append(f'<path d="M{x} {ground} V{ground-42} H{x+96} V{ground}"/>'
                       f'<path d="M{x+12} {ground-42} C{x+10} {ground-92} {x+45} {ground-104} {x+48} {ground-116} '
                       f'C{x+51} {ground-104} {x+86} {ground-92} {x+84} {ground-42}"/>'
                       + "".join(f'<path d="M{x+a} {ground} v-18 q8 -12 16 0 v18"/>' for a in (10, 40, 70)))
        elif kind == "frere":
            out.append(f'<path d="M{x} {ground} v-38 l8 -10 h14 v-10 h9 v-34 l11 -28 l11 28 v34 h9 v10 h14 l8 10 v38"/>'
                       f'<path d="M{x+33} {ground-56} q8 -12 16 0"/>')
        elif kind == "empress":
            out.append(f'<path d="M{x} {ground} v-34 l9 -7 h18 v-80 l4 -6 v-12 l6 -15 l6 15 v12 l4 6 v80 h18 l9 7 v34"/>'
                       f'<circle cx="{x+37}" cy="{ground-104}" r="5"/>')
    lights = "".join(
        f'<rect class="w{" tw" if rnd.random() < .14 else ""}" style="animation-delay:{2.2 + rnd.random()*2.4:.2f}s" '
        f'x="{wx}" y="{wy}" width="3" height="4"/>' for wx, wy in wins)
    return f'<g class="ln">{"".join(out)}<path d="M-16 {ground} H480"/></g><g fill="{INK["amber"]}">{lights}</g>'


def render() -> str:
    rnd = random.Random(1947)
    a1, a2 = _art(K.NAME[0]), _art(K.NAME[1])
    y0 = 118
    rows = []
    for i, line in enumerate(a1):
        rows.append((56, y0 + i * LH, line, 0.25 + i * 0.06))
    y1 = y0 + len(a1) * LH - 2
    x2 = W - 56 - max(len(l) for l in a2) * CW
    for i, line in enumerate(a2):
        rows.append((x2, y1 + i * LH, line, 0.75 + i * 0.06))
    art_bottom = y1 + len(a2) * LH
    art_svg = "".join(f'<text class="art rise" style="animation-delay:{d:.2f}s" x="{x:.1f}" y="{y:.1f}">{esc(l)}</text>'
                      for x, y, l, d in rows)
    # the gold sheen: same text, masked by a band that sweeps across (CSS, so reduced-motion stops it)
    sheen = "".join(f'<text class="art" x="{x:.1f}" y="{y:.1f}">{esc(l)}</text>' for x, y, l, _ in rows)

    ty = art_bottom + 46
    t1, t2, t3 = K.TAGLINE

    # neofetch detail panel
    px, py, pw = 56, ty + 40, 560
    rows_h = 24
    ph = 74 + len(K.DETAILS) * rows_h + 62
    det = [f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="10" fill="{INK["night2"]}" fill-opacity=".72" stroke="{INK["line"]}"/>',
           f'<path d="M{px} {py+30} H{px+pw}" stroke="{INK["line"]}"/>',
           "".join(f'<circle cx="{px+18+k*16}" cy="{py+15}" r="4.5" fill="{c}"/>' for k, c in
                   enumerate([INK["coral"], INK["amber"], INK["teal"]])),
           f'<text class="m" x="{px+pw/2}" y="{py+19}" text-anchor="middle" style="font-size:11px" fill="{INK["muted"]}">bashair@karachi: ~ — neofetch</text>',
           f'<text class="m b" x="{px+22}" y="{py+58}" style="font-size:13.5px" fill="{INK["gold"]}">bashair<tspan fill="{INK["muted"]}">@</tspan>karachi</text>',
           f'<path d="M{px+22} {py+68} H{px+pw-22}" stroke="{INK["line2"]}" stroke-dasharray="2 4"/>']
    for k, (key, val) in enumerate(K.DETAILS):
        y = py + 94 + k * rows_h
        det.append(f'<g class="rise" style="animation-delay:{1.6 + k*0.1:.2f}s">'
                   f'<text class="m b" x="{px+22}" y="{y}" style="font-size:13px" fill="{INK["amber"]}">{esc(key)}</text>'
                   f'<text class="m" x="{px+112}" y="{y}" style="font-size:13px" fill="{INK["text"]}">{esc(val)}</text></g>')
    sy = py + 94 + len(K.DETAILS) * rows_h + 8
    det.append(f'<g class="rise" style="animation-delay:2.4s"><text class="m b" x="{px+22}" y="{sy}" style="font-size:13px" fill="{INK["amber"]}">Status</text>'
               f'<circle class="pulse" cx="{px+118}" cy="{sy-4.5}" r="4" fill="{INK["teal"]}"/>'
               f'<text class="m" x="{px+130}" y="{sy}" style="font-size:13px" fill="{INK["teal"]}">open to collaboration</text></g>')
    palette = [INK["night"], "#16264A", INK["dim"], INK["muted"], INK["ember"], INK["amber"], INK["gold"], INK["cream"]]
    det.append("".join(f'<rect x="{px+22+k*24}" y="{sy+16}" width="20" height="10" rx="2" fill="{c}" stroke="{INK["line"]}"/>'
                       for k, c in enumerate(palette)))

    # right column: what's on the workbench
    rx = px + pw + 40
    right = [f'<text class="m" x="{rx}" y="{py+22}" style="font-size:11px;letter-spacing:.2em" fill="{INK["amber"]}">ON THE WORKBENCH</text>',
             f'<path d="M{rx} {py+34} H{W-56}" stroke="{INK["line"]}"/>']
    bench = [("AI Video Interviewer", ["LangGraph interview engine on a", "live LiveKit + Gemini call"]),
             ("Blindspot AI", ["six-agent debate over decision", "documents · team hackathon"]),
             ("AI Season", ["learning agentic AI from scratch:", "LangChain, LangGraph, RAG"])]
    for k, (name, lines) in enumerate(bench):
        y = py + 64 + k * 72
        right.append(f'<g class="rise" style="animation-delay:{2.0 + k*0.15:.2f}s">'
                     f'<text class="s" x="{rx}" y="{y}" style="font-size:22px" fill="{INK["cream"]}">{esc(name)}</text>'
                     + "".join(f'<text class="m" x="{rx}" y="{y+20+j*17}" style="font-size:11.5px" fill="{INK["muted"]}">{esc(l)}</text>'
                               for j, l in enumerate(lines)) + "</g>")

    sky_ground = y1 + 7 * LH + 2
    skyline = (f'<g transform="translate(56 {sky_ground - 160*SKY:.1f}) scale({SKY})">{_skyline(rnd)}</g>')
    H = py + ph + 70
    meta = [("PROFILE · 2026", 56, "start"), (K.LOCALE.upper(), W / 2, "middle"), ("AI / ML · NLP · AGENTS", W - 56, "end")]
    meta_svg = "".join(f'<text class="m" x="{x}" y="62" text-anchor="{a}" style="font-size:11px;letter-spacing:.2em" fill="{INK["muted"]}">{esc(t)}</text>'
                       for t, x, a in meta)

    css = (
        f".art{{font-family:KMono,monospace;font-weight:700;font-size:{FS}px;white-space:pre;fill:{INK['cream']}}}"
        f"#sheen .art{{fill:{INK['gold']}}}"
        ".band{animation:sweep 7s cubic-bezier(.4,0,.2,1) 2.6s infinite}"
        "@keyframes sweep{0%{transform:translateX(0)}45%,100%{transform:translateX(1400px)}}"
        f".ln{{fill:none;stroke:{INK['muted']};stroke-width:1.1;vector-effect:non-scaling-stroke;stroke-linejoin:round;opacity:.85}}"
        ".w{animation:fade .5s ease-out backwards}"
        ".tw{animation:fade .5s ease-out backwards,tw 6s ease-in-out 5s infinite}"
        "@keyframes tw{40%{opacity:1}50%{opacity:.15}60%{opacity:1}}"
        ".pulse{animation:pulse 2.4s ease-in-out 3s infinite}@keyframes pulse{50%{opacity:.25}}"
    )
    defs = (
        '<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070E1F"/>'
        '<stop offset="1" stop-color="#101D37"/></linearGradient>'
        f'<radialGradient id="glow" cx=".3" cy=".22" r=".5"><stop offset="0" stop-color="{INK["amber"]}" stop-opacity=".09"/>'
        f'<stop offset="1" stop-color="{INK["amber"]}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="bandg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
        f'<mask id="sheenmask"><rect class="band" x="-260" y="0" width="200" height="{H}" fill="url(#bandg)" transform="skewX(-18)"/></mask>'
    )
    body = f'''<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="url(#bg)" stroke="{INK['line']}"/>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="16" fill="url(#glow)"/>
<rect x="16" y="16" width="{W-32}" height="{H-32}" rx="8" fill="none" stroke="{INK['line']}" stroke-dasharray="1 5"/>
{meta_svg}
<path d="M56 78 H{W-56}" stroke="{INK['line']}"/>
{art_svg}
<g id="sheen" mask="url(#sheenmask)">{sheen}</g>
<text class="s rise" style="animation-delay:1.3s;font-size:42px" x="54" y="{ty:.0f}" fill="{INK['cream']}">{esc(t1)}<tspan class="i" fill="{INK['gold']}">{esc(t2)}</tspan>{esc(t3)}</text>
{"".join(det)}
{"".join(right)}
{skyline}
<text class="m" x="{W-56}" y="{H-30}" text-anchor="end" style="font-size:10px;letter-spacing:.2em" fill="{INK['dim']}">01 — SCROLL ↓</text>'''
    used = ("".join(a1 + a2) + "".join(t for t, _, _ in meta) + "".join(k + v for k, v in K.DETAILS)
            + "bashair@karachi:~—neofetchStatusopentocollaborationONTHEWORKBENCH01—SCROLL↓"
            + "".join(n + "".join(ls) for n, ls in bench))
    return document(W, H, body, css=css, defs=defs, families=("mono", "serif"),
                    text_for_fonts=used + "".join(K.TAGLINE),
                    title="Bashair Yaqoob — AI/ML engineering student in Karachi",
                    desc="Bashair Yaqoob in ASCII lettering. Builds AI that listens, retrieves and acts. "
                         + "; ".join(f"{k}: {v}" for k, v in K.DETAILS) + ".")
