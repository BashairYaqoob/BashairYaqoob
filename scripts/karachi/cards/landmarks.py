"""Karachi landmarks drawn in the city's isometric projection. Scenery, not data.

Behind the grid: Mazar-e-Quaid (floodlit marble, as at night), Frere Hall, Empress Market,
Bahria Icon Tower and a few anonymous towers. On the seafront: Teen Talwar. On the beach:
a Sea View camel.
"""
from __future__ import annotations

from ..iso import CA, CB, P, S, SA, depth, front_plane, pts, side_plane
from ..svg import INK

# face colours: (top, front, side)
FAR = ("#1C2E50", "#132341", "#0D1932")      # anonymous towers in the haze
STONE = ("#3A3F5C", "#2A2F4A", "#1F2339")     # Frere Hall / Empress Market sandstone at night
MARBLE = ("#B4BFD4", "#909DB8", "#6D7A97")    # Mazar-e-Quaid under floodlights
GLASS = ("#22385E", "#18294A", "#101D38")     # Bahria Icon Tower


def box(x0, y0, x1, y1, z0, z1, faces, extra=""):
    top, front, side = faces
    return (f'<polygon fill="{side}" points="{pts(P(x1, y0, z0), P(x1, y1, z0), P(x1, y1, z1), P(x1, y0, z1))}"{extra}/>'
            f'<polygon fill="{front}" points="{pts(P(x0, y1, z0), P(x1, y1, z0), P(x1, y1, z1), P(x0, y1, z1))}"{extra}/>'
            f'<polygon fill="{top}" points="{pts(P(x0, y0, z1), P(x1, y0, z1), P(x1, y1, z1), P(x0, y1, z1))}"{extra}/>')


def pyramid(x0, y0, x1, y1, z, rise, faces):
    top, front, side = faces
    apex = P((x0 + x1) / 2, (y0 + y1) / 2, z + rise)
    return (f'<polygon fill="{side}" points="{pts(P(x1, y0, z), P(x1, y1, z), apex)}"/>'
            f'<polygon fill="{front}" points="{pts(P(x0, y1, z), P(x1, y1, z), apex)}"/>')


def gable(x0, y0, x1, y1, z, rise, faces):
    """Pitched roof with its ridge running along the weeks axis."""
    top, front, side = faces
    ym = (y0 + y1) / 2
    return (f'<polygon fill="{top}" points="{pts(P(x0, y1, z), P(x1, y1, z), P(x1, ym, z + rise), P(x0, ym, z + rise))}"/>'
            f'<polygon fill="{side}" points="{pts(P(x1, y0, z), P(x1, y1, z), P(x1, ym, z + rise))}"/>')


def arch(u, v, w, h):
    """Pointed (Mughal/gothic) arch in a face's plane, u from the face's left, v above its base."""
    r = w / 2
    return (f'M{u:.1f} {-v:.1f} v{-(h - r):.1f} Q{u:.1f} {-(v + h + r * .5):.1f} {u + r:.1f} {-(v + h + r * .35):.1f} '
            f'Q{u + w:.1f} {-(v + h + r * .5):.1f} {u + w:.1f} {-(v + h - r):.1f} V{-v:.1f}z')


def mazar():
    x0, y0, x1, y1 = 6.9, -4.7, 10.6, -1.8
    base, top = 6, 44
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fl, sl = (x1 - x0) * S, (y1 - y0) * S
    out = [box(5.9, -5.7, 11.6, -0.8, 0, base, MARBLE),           # the raised platform
           box(x0, y0, x1, y1, base, top, MARBLE)]
    arches = "#283452"
    out.append(f'<path fill="{arches}" transform="{front_plane(x0, y1, base)}" d="{arch(fl/2-11, 0, 22, 26)}"/>')
    out.append(f'<path fill="{arches}" opacity=".8" transform="{side_plane(x1, y0, base)}" d="{arch(sl/2-9, 0, 18, 24)}"/>')
    # drum and the tall pointed dome; a dome's outline is the same from every angle
    bx, by = P(cx, cy, top)
    dw, dh, drum = 46, 46, 9
    out.append(f'<path fill="url(#marble)" d="M{bx-dw/2+2:.1f} {by:.1f} v{-drum} h{dw-4} v{drum} '
               f'a{dw/2-2:.1f} {(dw/2-2)*.33:.1f} 0 0 1 {-(dw-4):.1f} 0z"/>')
    dy = by - drum
    out.append(f'<path fill="url(#marble)" d="M{bx-dw/2:.1f} {dy:.1f} C{bx-dw/2:.1f} {dy-dh*.62:.1f} {bx-dw*.16:.1f} {dy-dh*.78:.1f} {bx:.1f} {dy-dh:.1f} '
               f'C{bx+dw*.16:.1f} {dy-dh*.78:.1f} {bx+dw/2:.1f} {dy-dh*.62:.1f} {bx+dw/2:.1f} {dy:.1f} '
               f'a{dw/2:.1f} {dw/2*.33:.1f} 0 0 1 {-dw:.1f} 0z"/>')
    return depth(cx, cy), "".join(out), (bx, dy - dh)


def frere_hall():
    x0, y0, x1, y1 = 19.2, -4.3, 24.6, -1.7
    out = [box(x0, y0, x1, y1, 0, 26, STONE), gable(x0, y0, x1, y1, 26, 10, STONE)]
    fl = (x1 - x0) * S
    win = "".join(arch(u, 6, 5, 11) for u in (8, 18, fl - 23, fl - 13))
    out.append(f'<path fill="{INK["amber"]}" opacity=".45" transform="{front_plane(x0, y1)}" d="{win}"/>')
    tx0, tx1, ty0, ty1 = 21.3, 22.6, -2.6, -1.3          # the central tower stands proud of the hall
    out += [box(tx0, ty0, tx1, ty1, 0, 62, STONE), pyramid(tx0, ty0, tx1, ty1, 62, 22, STONE)]
    out.append(f'<path fill="{INK["amber"]}" opacity=".5" transform="{front_plane(tx0, ty1)}" d="{arch((tx1-tx0)*S/2-3, 40, 6, 12)}"/>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def empress_market():
    x0, y0, x1, y1 = 33.0, -3.9, 40.2, -1.7
    out = [box(x0, y0, x1, y1, 0, 22, STONE), gable(x0, y0, x1, y1, 22, 9, STONE)]
    fl = (x1 - x0) * S
    win = "".join(arch(u, 5, 5, 10) for u in range(10, int(fl) - 10, 13))
    out.append(f'<path fill="{INK["amber"]}" opacity=".4" transform="{front_plane(x0, y1)}" d="{win}"/>')
    tx0, tx1, ty0, ty1 = 35.9, 37.3, -2.5, -1.1          # clock tower at the front
    out += [box(tx0, ty0, tx1, ty1, 0, 74, STONE), pyramid(tx0, ty0, tx1, ty1, 74, 26, STONE)]
    tw = (tx1 - tx0) * S
    out.append(f'<g transform="{front_plane(tx0, ty1)}"><circle cx="{tw/2:.1f}" cy="-62" r="5" fill="{INK["gold"]}" opacity=".85"/>'
               f'<path d="M{tw/2:.1f} -62 v-3.5 M{tw/2:.1f} -62 h2.6" stroke="#2A2F4A" stroke-width="1"/></g>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def bahria_icon():
    x0, y0, x1, y1 = 47.0, -4.6, 49.3, -2.4
    out = [box(x0, y0, x1, y1, 0, 176, GLASS),
           box(x0 + .35, y0 + .35, x1 - .35, y1 - .35, 176, 200, GLASS),
           box(x0 + .7, y0 + .7, x1 - .7, y1 - .7, 200, 212, GLASS)]
    fl = (x1 - x0) * S
    stripes = "".join(f'<rect x="{u:.1f}" y="-170" width="1.2" height="164"/>' for u in (5, fl / 2, fl - 6))
    out.append(f'<g fill="#5FA8C8" opacity=".35" transform="{front_plane(x0, y1)}">{stripes}</g>')
    sx, sy = P((x0 + x1) / 2, (y0 + y1) / 2, 212)
    out.append(f'<path d="M{sx:.1f} {sy:.1f} v-24" stroke="#5B7398" stroke-width="1.2"/>'
               f'<circle class="beacon" cx="{sx:.1f}" cy="{sy-25:.1f}" r="1.6" fill="{INK["coral"]}"/>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def anonymous_towers():
    spec = [(1.6, 2.9, 86), (13.6, 15.0, 112), (15.6, 16.7, 88), (26.6, 28.1, 142), (28.8, 29.9, 110),
            (42.4, 43.8, 124), (51.0, 52.2, 98)]
    return [(depth((x0 + x1) / 2, -2.4), box(x0, -3.2, x1, -1.6, 0, h, FAR)) for x0, x1, h in spec]


def behind_the_city():
    """All landmarks behind the grid, in painter's order. Returns (svg, mazar dome tip)."""
    mz_depth, mz_svg, tip = mazar()
    items = [(mz_depth, mz_svg), frere_hall(), empress_market(), bahria_icon(), *anonymous_towers()]
    return "".join(svg for _, svg in sorted(items, key=lambda t: t[0])), tip


def teen_talwar(x, y):
    """The three swords monument at Clifton, on a small roundabout on the seafront."""
    cx, cy = P(x, y)
    out = [f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="26" ry="11" transform="rotate(15 {cx:.1f} {cy:.1f})" fill="#152440" stroke="#22355A"/>',
           box(x - .55, y - .55, x + .55, y + .55, 0, 6, ("#C9D2E3", "#9AA6C0", "#76829F"))]
    bx, by = P(x, y, 6)
    for dx, dy, h in ((-7, 1.5, 58), (0, -2, 68), (7, 1.5, 58)):
        sx, sy = bx + dx, by + dy
        out.append(f'<polygon fill="#C9D2E3" points="{pts((sx-2.4, sy), (sx+2.4, sy), (sx+.6, sy-h), (sx, sy-h-6))}"/>'
                   f'<polygon fill="#8C98B4" points="{pts((sx, sy), (sx+2.4, sy), (sx+.6, sy-h), (sx, sy-h-6))}"/>'
                   f'<path d="M{sx-5:.1f} {sy-9:.1f} h10" stroke="#D9E0EC" stroke-width="1.6" stroke-linecap="round"/>')
    return "".join(out)


def camel(x, y, scale=1.6):
    """A Sea View camel with a saddle and tassels, standing on the beach."""
    cx, cy = P(x, y)
    body = "#2A2838"
    return (f'<g transform="translate({cx:.1f} {cy:.1f}) scale({scale})" stroke="#4A4862" stroke-width=".6">'
            f'<path fill="{body}" d="M-12 -14 C-12 -22 -6 -27 -1 -22 C2 -28 8 -24 9 -17 L14 -21 L17 -30 L22 -31 '
            f'L22 -27 L19 -26 L16 -14 C14 -10 10 -9 8 -10 L-8 -10 C-11 -10 -12 -12 -12 -14z"/>'
            f'<path d="M-9 -10 L-10 0 M-5 -10 L-4 0 M5 -10 L4 0 M9 -10 L10 0" stroke="{body}" stroke-width="1.8"/>'
            f'<path d="M-6 -21 h11 l-1 6 h-9z" fill="{INK["ember"]}" stroke="none" opacity=".9"/>'
            f'<path d="M-5 -15 v3 M-1 -15 v3.5 M3 -15 v3" stroke="{INK["gold"]}" stroke-width="1"/></g>')
