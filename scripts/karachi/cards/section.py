"""Chapter headers. Transparent, so they ship in a dark and a light variant (<picture>)."""
from __future__ import annotations

from .. import content as K
from ..svg import PAGE, document, esc

W, H = 1000, 92


def render(key: str, theme: str) -> str:
    no, title, cmd = K.SECTIONS[key]
    c = PAGE[theme]
    body = f'''<text class="s i" x="0" y="58" style="font-size:44px" fill="{c['accent']}">{no}</text>
<text class="s" style="font-size:38px" x="66" y="58" fill="{c['fg']}">{esc(title)}</text>
<text class="m" style="font-size:12px" x="{W}" y="56" text-anchor="end" fill="{c['muted']}">$ {esc(cmd)}</text>
<path d="M0 78 H{W}" stroke="{c['rule']}"/>
<path d="M0 78 H120" stroke="{c['accent']}" stroke-width="2"/>'''
    return document(W, H, body, text_for_fonts=no + title + "$ " + cmd, families=("mono", "serif"),
                    title=f"{no} — {title}", animated=False)
