"""Project card: number, title, what it does, how it works (pipeline), what it's built with."""
from __future__ import annotations

from ..svg import INK, document, esc

W, H = 500, 330
CH = 10.5 * 0.6  # mono advance at 10.5px


def _pipeline(steps, x0, y0, max_x):
    """Pills joined by arrows, wrapping onto new rows; lights up in order."""
    out, x, y = [], x0, y0
    pending_arrow = None  # drawn only if the next pill lands on the same row
    for k, step in enumerate(steps):
        w = len(step) * CH + 18
        if x + w > max_x:
            x, y = x0, y + 30
            out.append(f'<text class="m" x="{x0-14}" y="{y+15}" style="font-size:11px" fill="{INK["dim"]}">↳</text>')
        elif pending_arrow is not None:
            out.append(f'<path d="M{pending_arrow:.1f} {y+10.5} h12" stroke="{INK["amber"]}" stroke-width="1" marker-end="url(#ah)"/>')
        t = 0.5 + k * 0.22
        out.append(f'<g class="pill" style="animation-delay:{t:.2f}s">'
                   f'<rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="21" rx="10.5" fill="{INK["night"]}" stroke="{INK["line2"]}"/>'
                   f'<text class="m" x="{x+9:.1f}" y="{y+14.5}" style="font-size:10.5px" fill="{INK["text"]}">{esc(step)}</text></g>')
        pending_arrow = x + w + 3
        x += w + 20
    return "".join(out), y + 21


def render(p: dict) -> str:
    x = 30
    body = [f'<rect x="4" y="4" width="{W-8}" height="{H-8}" rx="12" fill="{INK["night2"]}" stroke="{INK["line"]}"/>',
            f'<text class="s i" x="{x}" y="52" style="font-size:30px" fill="{INK["amber"]}">{p["no"]}</text>',
            f'<text class="s" x="{x+42}" y="52" style="font-size:28px" fill="{INK["cream"]}">{esc(p["title"])}</text>',
            f'<circle class="pulse" cx="{x+4}" cy="76" r="3" fill="{INK["teal"]}"/>',
            f'<text class="m" x="{x+14}" y="80" style="font-size:10.5px;letter-spacing:.08em" fill="{INK["teal"]}">{esc(p["kind"].upper())}</text>']
    for j, line in enumerate(p["blurb"]):
        body.append(f'<text class="m" x="{x}" y="{112+j*19}" style="font-size:12.5px" fill="{INK["text"]}">{esc(line)}</text>')
    py = 112 + len(p["blurb"]) * 19 + 14
    body.append(f'<text class="m" x="{x}" y="{py}" style="font-size:9.5px;letter-spacing:.2em" fill="{INK["muted"]}">HOW IT WORKS</text>')
    pipe, bottom = _pipeline(p["flow"], x, py + 10, W - 30)
    body.append(pipe)
    sy = H - 34
    body.append(f'<path d="M{x} {sy-20} H{W-30}" stroke="{INK["line"]}" stroke-dasharray="1 4"/>')
    body.append(f'<text class="m" x="{x}" y="{sy}" style="font-size:11px" fill="{INK["gold"]}">'
                + f'<tspan fill="{INK["dim"]}"> / </tspan>'.join(esc(s) for s in p["stack"]) + "</text>")
    body.append(f'<text class="m arrow" x="{W-28}" y="48" text-anchor="end" style="font-size:16px" fill="{INK["amber"]}">↗</text>')
    css = (".pill{animation:fade .6s ease-out backwards}"
           ".pill rect{animation:glow 4.8s ease-in-out infinite;animation-delay:inherit}"
           f"@keyframes glow{{0%,18%,100%{{stroke:{INK['line2']}}}6%{{stroke:{INK['amber']}}}}}"
           ".arrow{animation:nudge 3s ease-in-out infinite}@keyframes nudge{50%{transform:translate(2px,-2px)}}"
           ".pulse{animation:pulse 2.4s ease-in-out infinite}@keyframes pulse{50%{opacity:.3}}")
    defs = (f'<marker id="ah" viewBox="0 0 6 6" refX="5" refY="3" markerWidth="6" markerHeight="6" orient="auto">'
            f'<path d="M0 0L6 3L0 6z" fill="{INK["amber"]}"/></marker>')
    text = p["no"] + p["title"] + p["kind"].upper() + "".join(p["blurb"]) + "HOWITWORKS" + "".join(p["flow"]) + "".join(p["stack"]) + "/↗↳"
    desc = f'{p["title"]} — {p["kind"]}. {" ".join(p["blurb"])} Pipeline: {" → ".join(p["flow"])}. Built with {", ".join(p["stack"])}.'
    return document(W, H, "".join(body), css=css, defs=defs, text_for_fonts=text, families=("mono", "serif"),
                    title=p["title"], desc=desc)
