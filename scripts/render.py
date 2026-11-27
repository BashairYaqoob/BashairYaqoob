"""Render every profile card into assets/.

    python scripts/render.py

Animated cards are written twice: assets/<name>.svg (animated) and assets/static/<name>.svg
(final frame), which the README serves to visitors who prefer reduced motion.
STATIC=1 makes the animated set static too (handy for full-page preview screenshots).
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from karachi import content as K  # noqa: E402
from karachi import svg  # noqa: E402
from karachi.cards import arsenal, city, footer, hero, links, project, section  # noqa: E402
from karachi.data import load  # noqa: E402

OUT = svg.ROOT / "assets"


def animated_cards(year):
    yield "hero.svg", hero.render
    yield "city.svg", lambda: city.render(year)
    yield "arsenal.svg", arsenal.render
    for p in K.PROJECTS:
        yield f"projects/{p['slug']}.svg", lambda p=p: project.render(p)


def main() -> None:
    year = load()
    forced_static = svg.STATIC
    for name, make in animated_cards(year):
        svg.STATIC = forced_static
        svg.write(OUT / name, make())
        svg.STATIC = True
        svg.write(OUT / "static" / name, make())
    svg.STATIC = forced_static
    for key in K.SECTIONS:
        for theme in ("dark", "light"):
            svg.write(OUT / "sections" / f"{key}-{theme}.svg", section.render(key, theme))
    for slug, *_ in K.LINKS:
        svg.write(OUT / "links" / f"{slug}.svg", links.render(slug))
    svg.write(OUT / "footer.svg", footer.render())
    for path in sorted(OUT.rglob("*.svg")):
        print(f"{path.stat().st_size/1024:7.1f} KB  {path.relative_to(svg.ROOT)}")


if __name__ == "__main__":
    main()
