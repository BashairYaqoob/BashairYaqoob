"""Karachi landmarks drawn in the city's isometric projection. Scenery, not data.

Behind the grid: Mazar-e-Quaid (floodlit marble, as at night), Frere Hall, Empress Market,
Bahria Icon Tower, with a food street of stalls under fairy lights between them. On the seafront: Teen Talwar. On the beach:
a Sea View camel.
"""
from __future__ import annotations

from ..iso import CA, CB, P, S, SA, depth, front_plane, pts, side_plane
from ..svg import INK

# face colours: (top, front, side), true hues under night floodlights
WOOD = ("#8A5E3C", "#6F4A2F", "#573A25")      # food-stall counters
# canopy colours for the food street, kept to the card's amber/gold palette: (top/front, side)
CANOPIES = [("#C98A3A", "#9C6A2A"), ("#B8742F", "#8E5823"), ("#D9A04A", "#A97A33")]
FAIRY = ["#FFD58C", "#F4B04A", "#FFF3D1", "#FFC36B"]   # warm, in the card's amber/gold theme
LIMESTONE = ("#D6C39A", "#B49E73", "#8A7853")  # Frere Hall: pale yellow Karachi limestone
SLATE = ("#6B6C7A", "#585966", "#474855")      # Frere Hall roofs
SANDSTONE = ("#DDB878", "#BE965A", "#91703F")  # Empress Market: golden Jodhpur sandstone
TERRACOTTA = ("#9A5A40", "#824B35", "#6A3D2B")  # Empress Market roofs
MARBLE = ("#E4E9F1", "#C2CAD8", "#98A3B7")     # Mazar-e-Quaid: white marble, floodlit
GLASS = ("#B8C3CE", "#8D9AA8", "#6A7684")      # Bahria Icon Tower: silver glass


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
    arches = "#3B4560"
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
    out = [box(x0, y0, x1, y1, 0, 26, LIMESTONE), gable(x0, y0, x1, y1, 26, 10, SLATE)]
    fl = (x1 - x0) * S
    win = "".join(arch(u, 6, 5, 11) for u in (8, 18, fl - 23, fl - 13))
    out.append(f'<path fill="{INK["gold"]}" opacity=".9" transform="{front_plane(x0, y1)}" d="{win}"/>')
    tx0, tx1, ty0, ty1 = 21.3, 22.6, -2.6, -1.3          # the central tower stands proud of the hall
    out += [box(tx0, ty0, tx1, ty1, 0, 62, LIMESTONE), pyramid(tx0, ty0, tx1, ty1, 62, 22, SLATE)]
    out.append(f'<path fill="{INK["gold"]}" opacity=".9" transform="{front_plane(tx0, ty1)}" d="{arch((tx1-tx0)*S/2-3, 40, 6, 12)}"/>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def empress_market():
    x0, y0, x1, y1 = 33.0, -3.9, 40.2, -1.7
    out = [box(x0, y0, x1, y1, 0, 22, SANDSTONE), gable(x0, y0, x1, y1, 22, 9, TERRACOTTA)]
    fl = (x1 - x0) * S
    win = "".join(arch(u, 5, 5, 10) for u in range(10, int(fl) - 10, 13))
    out.append(f'<path fill="{INK["gold"]}" opacity=".85" transform="{front_plane(x0, y1)}" d="{win}"/>')
    tx0, tx1, ty0, ty1 = 35.9, 37.3, -2.5, -1.1          # clock tower at the front
    out += [box(tx0, ty0, tx1, ty1, 0, 74, SANDSTONE), pyramid(tx0, ty0, tx1, ty1, 74, 26, TERRACOTTA)]
    tw = (tx1 - tx0) * S
    out.append(f'<g transform="{front_plane(tx0, ty1)}"><circle cx="{tw/2:.1f}" cy="-62" r="5" fill="{INK["gold"]}" opacity=".85"/>'
               f'<path d="M{tw/2:.1f} -62 v-3.5 M{tw/2:.1f} -62 h2.6" stroke="#5A4228" stroke-width="1"/></g>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def bahria_icon():
    x0, y0, x1, y1 = 47.0, -4.6, 49.3, -2.4
    out = [box(x0, y0, x1, y1, 0, 176, GLASS),
           box(x0 + .35, y0 + .35, x1 - .35, y1 - .35, 176, 200, GLASS),
           box(x0 + .7, y0 + .7, x1 - .7, y1 - .7, 200, 212, GLASS)]
    fl = (x1 - x0) * S
    stripes = "".join(f'<rect x="{u:.1f}" y="-170" width="1.2" height="164"/>' for u in (5, fl / 2, fl - 6))
    out.append(f'<g fill="#F3F6FA" opacity=".5" transform="{front_plane(x0, y1)}">{stripes}</g>')
    sx, sy = P((x0 + x1) / 2, (y0 + y1) / 2, 212)
    out.append(f'<path d="M{sx:.1f} {sy:.1f} v-24" stroke="#9AA6B4" stroke-width="1.2"/>'
               f'<circle class="beacon" cx="{sx:.1f}" cy="{sy-25:.1f}" r="1.6" fill="{INK["coral"]}"/>')
    return depth((x0 + x1) / 2, (y0 + y1) / 2), "".join(out)


def stall(x, y, n):
    """One food stall: a wooden counter with a lit front, posts, a striped canopy and a bulb."""
    top, side = CANOPIES[n % len(CANOPIES)]
    x0, x1, y0, y1 = x, x + 1.15, y, y + .8
    out = [box(x0, y0, x1, y1, 0, 9, WOOD)]
    fl = (x1 - x0) * S
    out.append(f'<g transform="{front_plane(x0, y1)}"><rect x="2" y="-8" width="{fl-4:.1f}" height="5" fill="{INK["gold"]}" opacity=".8"/></g>')
    for px, py in ((x0, y1), (x1, y1), (x1, y0)):                       # canopy posts
        (ax, ay), (bx, by) = P(px, py, 9), P(px, py, 17)
        out.append(f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="#3A2A1C" stroke-width=".9"/>')
    cx0, cx1, cy0, cy1 = x0 - .12, x1 + .12, y0 - .12, y1 + .25          # canopy overhangs the counter
    out.append(gable(cx0, cy0, cx1, cy1, 17, 5, (top, top, side)))
    # cream stripes on the sloping front of the canopy
    for k in range(1, 4):
        ux = cx0 + (cx1 - cx0) * k / 4
        (ax, ay), (bx, by) = P(ux, cy1, 17), P(ux, (cy0 + cy1) / 2, 22)
        out.append(f'<path d="M{ax:.1f} {ay:.1f} L{bx:.1f} {by:.1f}" stroke="#F3E9D2" stroke-opacity=".55" stroke-width="1.6"/>')
    bx, by = P((x0 + x1) / 2, y1, 15)
    out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="1.6" fill="#FFF3D1"/>'
               f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="6" fill="{INK["gold"]}" opacity=".18"/>')
    return depth(x0 + .5, y0 + .4), "".join(out)


def fairy_string(xa, xb, y=-1.05, z=50, sag=5, step=7, seed=0):
    """Poles at both ends and a sagging string of twinkling bulbs between them."""
    (ax, ay), (bx, by) = P(xa, y, z), P(xb, y, z)
    mx, my = (ax + bx) / 2, (ay + by) / 2 + sag * 2
    out = []
    for px in (xa, xb):
        (gx, gy), (tx, ty) = P(px, y), P(px, y, z + 1)
        out.append(f'<path d="M{gx:.1f} {gy:.1f} L{tx:.1f} {ty:.1f}" stroke="#4A3A2A" stroke-width="1.1"/>')
    out.append(f'<path d="M{ax:.1f} {ay:.1f} Q{mx:.1f} {my:.1f} {bx:.1f} {by:.1f}" fill="none" stroke="#2A2A36" stroke-width=".6"/>')
    count = max(3, int(((bx - ax) ** 2 + (by - ay) ** 2) ** .5 // step))
    for j in range(1, count):
        t = j / count
        qx = (1 - t) ** 2 * ax + 2 * (1 - t) * t * mx + t * t * bx
        qy = (1 - t) ** 2 * ay + 2 * (1 - t) * t * my + t * t * by
        c = FAIRY[(j + seed) % len(FAIRY)]
        out.append(f'<g class="fl" style="animation-delay:{((j * 7 + seed * 3) % 23) / 10:.1f}s">'
                   f'<circle cx="{qx:.1f}" cy="{qy+1:.1f}" r="4.2" fill="{c}" opacity=".22"/>'
                   f'<circle cx="{qx:.1f}" cy="{qy+1:.1f}" r="1.7" fill="{c}"/></g>')
    return "".join(out)


# twinkle for the fairy lights; the card adds this to its stylesheet
FAIRY_CSS = ".fl{animation:fl 2.6s ease-in-out infinite}@keyframes fl{50%{opacity:.35}}"


def food_street():
    """Clusters of stalls where plain towers used to stand, each under a run of fairy lights."""
    clusters = [(0.6, 3), (12.6, 4), (25.8, 4), (41.6, 4), (50.4, 2)]   # (first week, stalls)
    items, strings, n = [], [], 0
    for c, (x, count) in enumerate(clusters):
        for j in range(count):
            items.append(stall(x + j * 1.45, -2.3, n))
            n += 1
        strings.append(fairy_string(x - .3, x + count * 1.45 - .05, seed=c))
    return items, "".join(strings)


def behind_the_city():
    """All landmarks behind the grid, in painter's order. Returns (svg, mazar dome tip)."""
    mz_depth, mz_svg, tip = mazar()
    stalls, strings = food_street()
    items = [(mz_depth, mz_svg), frere_hall(), empress_market(), bahria_icon(), *stalls]
    # fairy lights hang in front of the stalls, so they go on last
    return "".join(svg for _, svg in sorted(items, key=lambda t: t[0])) + strings, tip


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


def camel(x, y, walk=5.0, scale=1.6):
    """A Sea View camel with a saddle and tassels, pacing up and down the beach."""
    cx, cy = P(x, y)
    dx, dy = walk * S * CA, walk * S * SA   # one stretch of beach along the week axis
    body = "#C9A46C"                        # sandy camel
    shade = "#9C7B4C"
    legs = lambda xs, cls: "".join(
        f'<path class="{cls}" d="M{lx} -10 L{lx} 0" stroke="{shade}" stroke-width="1.9" stroke-linecap="round"/>' for lx in xs)
    go, back = "translate(0,0)", f"translate({dx:.0f}px,{dy:.0f}px)"
    css = (f"@keyframes walk{{0%{{transform:{go} scaleX(1)}}44%{{transform:{back} scaleX(1)}}"
           f"48%{{transform:{back} scaleX(1)}}48.4%{{transform:{back} scaleX(-1)}}"     # pause, then turn
           f"52%{{transform:{back} scaleX(-1)}}96%{{transform:{go} scaleX(-1)}}"
           f"99.6%{{transform:{go} scaleX(-1)}}100%{{transform:{go} scaleX(1)}}}}"
           ".walk{animation:walk 30s linear infinite}"
           ".legA,.legB{transform-box:fill-box;transform-origin:top;animation:step .9s ease-in-out infinite alternate}"
           ".legB{animation-delay:-.9s}@keyframes step{from{transform:rotate(12deg)}to{transform:rotate(-12deg)}}")
    svg = (f'<g transform="translate({cx:.1f} {cy:.1f})"><g class="walk"><g transform="scale({scale})">'
           f'<ellipse cx="3" cy="0.5" rx="15" ry="2" fill="#000" opacity=".25"/>'
           + legs((-9, 5), "legA") + legs((-5, 9), "legB") +
           f'<path fill="{body}" stroke="{shade}" stroke-width=".6" d="M-12 -14 C-12 -22 -6 -27 -1 -22 C2 -28 8 -24 9 -17 '
           f'L14 -21 L17 -30 L22 -31 L22 -27 L19 -26 L16 -14 C14 -10 10 -9 8 -10 L-8 -10 C-11 -10 -12 -12 -12 -14z"/>'
           f'<path d="M-6 -21 h11 l-1 6 h-9z" fill="#B23A3A"/>'
           f'<path d="M-5 -15 v3 M-1 -15 v3.5 M3 -15 v3" stroke="{INK["gold"]}" stroke-width="1"/>'
           f'<circle cx="20" cy="-29" r=".8" fill="#2A2018"/></g></g></g>')
    return svg, css
