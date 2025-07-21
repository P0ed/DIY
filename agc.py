from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar, Any
from functools import reduce
from cadquery import exporters, Vector, Workplane

import sys, os
sys.path.append(os.path.abspath("."))
from lib.ddd import lemo, grid
from lib.tools import *

wt: float = 3.3
wt2: float = 2.0

cw: float = 101.0
ch: float = 161.0
w: float = cw + 9.0 * 2
h: float = ch + wt * 2
t: float = 30.0
t2: float = t / 2.0
col: float = 9.0
hol: float = col / 2

c: float = 2.5
c2: float = 0.25

cell: float = inch
scuth: float = (h - wt * 6) / 2 - wt * 2

wp = Workplane()

def holes(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return sum([
        wp.cylinder(l, r).translate((w / 2 - d, h / 2 - d, 0)),
        wp.cylinder(l, r).translate((-w / 2 + d, h / 2 - d, 0)),
        wp.cylinder(l, r).translate((w / 2 - d, -h / 2 + d, 0)),
        wp.cylinder(l, r).translate((-w / 2 + d, -h / 2 + d, 0)),
        wp.cylinder(l, r).translate((w / 2 - d, 0, 0)),
        wp.cylinder(l, r).translate((-w / 2 + d, 0, 0)),
    ])

def hcuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return sum([
        (
            wp.box(r * 4, r * 4, l + c2 * 2)
            .edges("+Z")
            .fillet(r)
            .edges()
            .chamfer(c2)
            .translate((w / 2 - d + r, h / 2 - d + r, c2))
            .mirror("YZ", union = True)
            .mirror("XZ", union = True)
        ),
        (
            wp.box(r * 4, r * 2 + pl, l + c2 * 2)
            .edges("+Z")
            .fillet(r)
            .edges()
            .chamfer(c2)
            .translate((w / 2 - d + r, 0, c2))
            .mirror("YZ", union = True)
        ),
        (
            wp.box(r * 4 + c2 * 2, r * 4 + c2 * 2, c2 * 2 + pl)
            .edges("+Z")
            .fillet(r + c2)
            .edges()
            .chamfer(c2)
            .translate((w / 2 - d + r, h / 2 - d + r, l / 2))
            .mirror("YZ", union = True)
            .mirror("XZ", union = True)
        ),
        (
            wp.box(r * 4 + c2 * 2, r * 2 + pl + c2 * 2, c2 * 2 + pl)
            .edges("+Z")
            .fillet(r + c2)
            .edges()
            .chamfer(c2)
            .translate((w / 2 - d + r, 0, l / 2))
            .mirror("YZ", union = True)
        ),
    ])

def brick(side: float = 1.0) -> Workplane:
    return dif([
        (
            wp.box(w, h, t2).edges("+Z").chamfer(c)
            .intersect(
                wp.box(w, h, t2 + c2 * 2)
                .edges("+Z").chamfer(c)
                .edges().chamfer(c2)
                .translate((0, 0, c2 * side))
            )
        ),
        (
            wp.box(cw, ch, t2)
            .edges("|Z")
            .fillet(2.0)
            .edges()
            .chamfer(c2 * 2)
            .translate((0, 0, wt2 * side))
        ),
        (
            wp.box((col - wt) * 2, scuth, t2)
            .edges("|X")
            .fillet(2.0)
            .edges()
            .chamfer(c2 * 2)
            .translate((w / 2, h / 4 - col / 4, wt * side))
            .mirror("YZ", union = True)
            .mirror("XZ", union = True)
        ),
    ])

def case() -> Workplane:
    return sum([
        dif([
            brick(1.0),
            holes(w, h, hol, t2, 2.5 / 2).translate((0, 0, 0)),
            lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90).translate((-inch, h / 2 - wt / 2, wt2 / 2)),
            lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90).translate((inch, h / 2 - wt / 2, wt2 / 2)),
        ]),
    ]).translate((0, 0, t2 / 2))

def makePanel(ptn: Callable[[int, int], bool]) -> Workplane:
    return dif([
        brick(-1.0),
        grid(lambda x, y: (
            wp.cylinder(t2, inch / 8 + 0.2)
            if ptn(x, y) and y < 3 else
            wp.cylinder(t2, 9.7 / 2)
        )),
        holes(w, h, hol, t2, 3.1 / 2),
        hcuts(w, h, hol, wt, wt).translate((0, 0, t2 / 2 - wt / 2)),
    ]).translate((0, 0, t2 / 2))

top = makePanel(pattern("<>"))
bot = case()
comp = bot + top.translate((0, 0, t2))

exporters.export(top, "TOP.stl")
exporters.export(bot, "BOT.stl")
exporters.export(comp, "COMP.stl")

exporters.export(top, "TOP.step")
exporters.export(bot, "BOT.step")
