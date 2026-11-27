"""Technical arsenal as a directory tree: grouped by what the tools are for, not a badge wall."""
from __future__ import annotations

from .. import content as K
from ..svg import INK, document, esc

W = 1000
ROW = 74
TOP = 92


def _wrap(items, max_chars):
    lines, cur = [], []
    for it in items:
        if cur and len(" · ".join(cur + [it])) > max_chars:
            lines.append(cur)
            cur = []
        cur.append(it)
    lines.append(cur)
    return lines


def render() -> str:
    H = TOP + len(K.ARSENAL) * ROW + 40
    rows = []
    for i, (folder, about, items) in enumerate(K.ARSENAL):
        y = TOP + i * ROW
        branch = "└──" if i == len(K.ARSENAL) - 1 else "├──"
        lines = _wrap(items, 52)
        rows.append(f'<g class="rise" style="animation-delay:{0.2 + i*0.12:.2f}s">'
                    f'<text class="m" x="48" y="{y+22}" style="font-size:15px" fill="{INK["dim"]}">{branch}</text>'
                    f'<text class="m b" x="92" y="{y+22}" style="font-size:16px" fill="{INK["amber"]}">{esc(folder)}</text>'
                    f'<text class="s i" x="92" y="{y+46}" style="font-size:18px" fill="{INK["muted"]}">{esc(about)}</text>')
        for j, line in enumerate(lines):
            spans = f'<tspan fill="{INK["dim"]}"> · </tspan>'.join(esc(t) for t in line)
            rows.append(f'<text class="m" x="420" y="{y+22+j*22}" style="font-size:15px" fill="{INK["text"]}">{spans}</text>')
        rows.append("</g>")
        if i < len(K.ARSENAL) - 1:
            rows.append(f'<path d="M52 {y+32} V{y+ROW+8}" stroke="{INK["line"]}"/>'
                        f'<path d="M92 {y+ROW-12} H{W-48}" stroke="{INK["line"]}" stroke-dasharray="1 4"/>')
    body = (f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{INK["night"]}" stroke="{INK["line"]}"/>'
            f'<text class="m" x="48" y="50" style="font-size:13px" fill="{INK["muted"]}">'
            f'<tspan fill="{INK["teal"]}">➜</tspan>  <tspan fill="{INK["gold"]}">~</tspan>  tree ~/arsenal -L 1'
            f'<tspan x="{W-48}" text-anchor="end" fill="{INK["dim"]}">grouped by what I use them for</tspan></text>'
            + "".join(rows))
    text = "".join(f + a + "".join(it) for f, a, it in K.ARSENAL) + "├──└──·➜~tree/arsenal-L1groupedbywhatIusethemfor"
    alt = "Technical arsenal. " + " ".join(f"{f} ({a}): {', '.join(it)}." for f, a, it in K.ARSENAL)
    return document(W, H, body, text_for_fonts=text, families=("mono", "serif"), title="Technical arsenal", desc=alt)
