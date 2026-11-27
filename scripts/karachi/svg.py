"""Low-level SVG helpers: design tokens, embedded font subsets, escaping, card shell."""
from __future__ import annotations

import base64
import html
import io
import os
from functools import lru_cache
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[2]
FONTS = ROOT / "assets" / "fonts"

# When True, every card renders its final frame with no motion. render.py flips this to write the
# static twins that README <picture> elements serve under prefers-reduced-motion. (Browsers don't
# pass that preference into SVGs loaded via <img>, so the SVG's own media query isn't enough.)
STATIC = os.environ.get("STATIC") == "1"

# ---- design tokens: Karachi at night ------------------------------------------------------
INK = dict(
    night="#081022", night2="#0E1A30", panel="#0E1A30", line="#1F3050", line2="#2A3D60",
    amber="#F4B04A", gold="#FFD58C", ember="#E07B3C", cream="#F3E9D2",
    text="#D9DFEA", muted="#8391AC", dim="#4F5E7C", teal="#4FB3A9", coral="#E5604F",
)
# Section headers sit directly on GitHub's page background, so they get a light variant too.
PAGE = {
    "dark": dict(fg="#F3E9D2", accent="#F4B04A", muted="#8391AC", rule="#2A3D60"),
    "light": dict(fg="#14213D", accent="#B8650F", muted="#5B6680", rule="#D5DBE6"),
}

FAMILIES = {
    "mono": [("JetBrainsMono-Regular.ttf", 400, "normal"), ("JetBrainsMono-Bold.ttf", 700, "normal")],
    "serif": [("InstrumentSerif-Regular.ttf", 400, "normal"), ("InstrumentSerif-Italic.ttf", 400, "italic")],
}
CSS_NAME = {"mono": "KMono", "serif": "KSerif"}


@lru_cache(maxsize=None)
def _subset_b64(filename: str, chars: str) -> str:
    font = TTFont(FONTS / filename)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern"]
    opts.hinting = False  # hinting tables are most of the weight and do nothing at these sizes
    opts.name_IDs = []  # drop the name table strings; not needed inside an SVG
    sub = subset.Subsetter(opts)
    sub.populate(text=chars)
    sub.subset(font)
    font.flavor = "woff2"  # Options.flavor alone doesn't change what save() writes
    buf = io.BytesIO()
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_css(text: str, families=("mono",)) -> str:
    """@font-face rules containing only the glyphs `text` needs."""
    chars = "".join(sorted(set(text + " ")))
    rules = []
    for fam in families:
        for filename, weight, style in FAMILIES[fam]:
            b64 = _subset_b64(filename, chars)
            rules.append(
                f"@font-face{{font-family:'{CSS_NAME[fam]}';font-weight:{weight};font-style:{style};"
                f"src:url(data:font/woff2;base64,{b64}) format('woff2');}}"
            )
    return "".join(rules)


def esc(s) -> str:
    return html.escape(str(s), quote=True)


BASE_CSS = (
    ".m{font-family:KMono,ui-monospace,monospace}.s{font-family:KSerif,Georgia,serif}.b{font-weight:700}"
    ".i{font-style:italic}"
    # entrance: elements are visible by default; the animation only plays *from* hidden.
    ".rise{animation:rise .7s cubic-bezier(.2,.7,.2,1) backwards}"
    "@keyframes rise{from{opacity:0;transform:translateY(8px)}}"
    ".fade{animation:fade .8s ease-out backwards}@keyframes fade{from{opacity:0}}"
)
REDUCED_CSS = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def document(width, height, body, *, css="", text_for_fonts="", families=("mono",), title="", desc="", defs="",
             animated=True):
    """animated=False marks a card that never moves, so no static twin or motion CSS is needed."""
    """Wrap body markup in a standalone SVG with fonts, base styles and reduced-motion handling."""
    motion_off = "" if not animated else ("*{animation:none!important}" if STATIC else REDUCED_CSS)
    fonts = font_css(text_for_fonts, families) if text_for_fonts else ""
    a11y = ""
    if title:
        a11y += f"<title>{esc(title)}</title>"
    if desc:
        a11y += f"<desc>{esc(desc)}</desc>"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img"{" aria-label=" + chr(34) + esc(title) + chr(34) if title else ""}>'
        f"{a11y}<defs>{defs}</defs><style>{fonts}{BASE_CSS}{css}{motion_off}</style>{body}</svg>"
    )


def delay(seconds: float) -> str:
    return f'style="animation-delay:{seconds:.2f}s"'


def write(path: Path, svg: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(svg, encoding="utf-8")
