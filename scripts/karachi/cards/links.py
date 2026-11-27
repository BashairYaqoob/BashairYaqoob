"""Link tiles, one per destination, so each can be its own <a> in the README."""
from __future__ import annotations

from .. import content as K
from ..svg import INK, document, esc

W, H = 250, 72

ICONS = {  # simple monoline icons drawn in a 24×24 box
    "linkedin": '<rect x="1" y="1" width="22" height="22" rx="4"/><path d="M7 10v7M7 7v.01M11 17v-7M11 13a3 3 0 0 1 6 0v4"/>',
    "portfolio": '<circle cx="12" cy="12" r="10.5"/><path d="M1.5 12h21M12 1.5c3.5 3.5 3.5 17.5 0 21M12 1.5c-3.5 3.5 -3.5 17.5 0 21"/>',
    "email": '<rect x="1" y="4" width="22" height="16" rx="3"/><path d="M2 6l10 7l10 -7"/>',
    "github": '<path d="M7 20c-4 1-4-2-6-2.5M15 23v-3.5c0-1 .1-1.4-.5-2 2.8-.3 5.5-1.4 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.2 4.2 0 0 0-.1-3.2s-1.1-.3-3.5 1.3a12 12 0 0 0-6.2 0C6.5 4.8 5.4 5.1 5.4 5.1a4.2 4.2 0 0 0-.1 3.2A4.6 4.6 0 0 0 4 11.5c0 4.6 2.7 5.7 5.5 6-.6.6-.6 1.2-.5 2V23"/>',
}


def render(slug: str) -> str:
    _, label, value, _ = next(l for l in K.LINKS if l[0] == slug)
    body = (f'<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="10" fill="{INK["night2"]}" stroke="{INK["line"]}"/>'
            f'<g transform="translate(20 24)" fill="none" stroke="{INK["amber"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{ICONS[slug]}</g>'
            f'<text class="s" x="60" y="34" style="font-size:20px" fill="{INK["cream"]}">{esc(label)}</text>'
            f'<text class="m" x="60" y="52" style="font-size:10.5px" fill="{INK["muted"]}">{esc(value)}</text>'
            f'<text class="m" x="{W-22}" y="40" text-anchor="end" style="font-size:14px" fill="{INK["amber"]}">↗</text>')
    return document(W, H, body, text_for_fonts=label + value + "↗", families=("mono", "serif"),
                    title=f"{label}: {value}", animated=False)
