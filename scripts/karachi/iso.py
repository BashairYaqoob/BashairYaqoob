"""The isometric projection shared by the city grid and its landmarks.

World units: x = weeks (one plot each), y = weekdays (one plot each), z = height in px.
"""
from __future__ import annotations

import math

S = 15.5                                      # plot size in px
AX, AY = math.radians(15), math.radians(40)   # screen angles of the week and weekday axes
CA, SA, CB, SB = math.cos(AX), math.sin(AX), math.cos(AY), math.sin(AY)
OX, OY = 60 + 7 * S * CB, 296                 # screen position of the grid's back-left corner


def P(x, y, z=0.0):
    """World (week, weekday, height px) → screen (x, y)."""
    return OX + S * (x * CA - y * CB), OY + S * (x * SA + y * SB) - z


def pts(*points):
    return " ".join(f"{x:.1f},{y:.1f}" for x, y in points)


def depth(x, y):
    """Painter's order: larger is nearer the viewer."""
    return x * SA + y * SB


def front_plane(x0, y, z0=0.0):
    """SVG matrix that maps (u px along +x, -v px up) onto the face at weekday y."""
    ox, oy = P(x0, y, z0)
    return f"matrix({CA:.4f} {SA:.4f} 0 1 {ox:.1f} {oy:.1f})"


def side_plane(x, y0, z0=0.0):
    """SVG matrix that maps (u px along +y, -v px up) onto the face at week x."""
    ox, oy = P(x, y0, z0)
    return f"matrix({-CB:.4f} {SB:.4f} 0 1 {ox:.1f} {oy:.1f})"
