"""Closing line: the skyline fading out and the session ending."""
from __future__ import annotations

import random

from .. import content as K
from ..svg import INK, document, esc

W, H = 1000, 110


def render() -> str:
    rnd = random.Random(21)
    x, towers = 0.0, []
    while x < W:
        w = rnd.uniform(10, 26)
        h = rnd.uniform(8, 34)
        towers.append(f'<rect x="{x:.0f}" y="{70-h:.0f}" width="{w:.0f}" height="{h:.0f}"/>')
        x += w + rnd.uniform(1, 4)
    line = f"— connection closed by bashair@karachi · {K.LOCALE} —"
    body = (f'<g fill="{INK["line"]}" mask="url(#fadeout)">{"".join(towers)}</g>'
            f'<path d="M0 70 H{W}" stroke="{INK["line2"]}" mask="url(#fadeout)"/>'
            f'<text class="m" x="{W/2}" y="98" text-anchor="middle" style="font-size:12.5px" fill="{INK["muted"]}">{esc(line)}</text>')
    defs = ('<linearGradient id="fg" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
            '<stop offset=".5" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="fadeout"><rect width="{W}" height="{H}" fill="url(#fg)"/></mask>')
    return document(W, H, body, defs=defs, text_for_fonts=line, title="Connection closed", animated=False)
