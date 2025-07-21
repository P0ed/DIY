from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar, Any
from functools import reduce
from cadquery import exporters, Vector, Workplane

import sys, os
sys.path.append(os.path.abspath("."))
from lib.ddd import *
from lib.tools import *

m4xr: float = 4.1 / 2
m4dr: float = 3.4 / 2

wt: float = 4.0
wt2: float = 2.0

cw: float = 102.0
ch: float = 153.0
w: float = cw + 12.0
h: float = ch + 28.0
t: float = 30.0
t2: float = t / 2.0
col: float = 12.0
hol: float = col / 2
c1: float = 0.5
c2: float = 0.25

def box_fc(w, h, t, fe, fr, c) -> Workplane:
	return (
        wp.box(w, h, t)
		.edges(fe).fillet(fr)
		.edges().chamfer(c)
	)

def hcuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return sum([
        mirror2('XZ', 'YZ') (
            box_fc(r * 4, r * 4, l + c1, "+Z", r, c2)
            .translate((w / 2, h / 2, c2))
        ),
        mirror2('XZ', 'YZ') (
            box_fc(r * 4 + c1, r * 4 + c1, c1 + pl, "+Z", r + c2, c2)
            .translate((w / 2, h / 2, 0))
        ),
        # com2(mirror('XZ'), mov(0, h / 2)) (
        #      wp.box(w + wt * 6, col * 2, wt * 2 + pl).chamfer(wt * 1)
        # ),
    ])

def brick(side: float = 1.0) -> Workplane:
    return dif([
        (
            wp.box(w, h, t2)
            .edges("+Z").chamfer(wt)
            .intersect(
                wp.box(w, h, t2 + c1)
                .edges("+Z").chamfer(wt)
                .edges().chamfer(c2)
                .translate((0, 0, c2 * side))
            )
        ),
        (
            box_fc(cw, ch, t2, "|Z", 2.0, c1)
            .translate((0, 0, wt2 * side))
        ),
        (
            box_fc(w - (col + wt2) * 2, h - wt * 2, t2, '|Z', 2.0, c1)
            .translate((0, 0, wt2 * side))
        ),
        (
            box_fc(wt2 * 2, h - 28.0, t2, '|X', 2.0, c1)
            .translate((w / 2, 0, wt * side))
            .mirror("YZ", union = True)
        ),
    ])

def makeTop(ptn: Callable[[int, int], bool]) -> Workplane:
    hole_large = wp.cylinder(t2, 9.53 / 2 + 1)
    hole_small = wp.cylinder(t2, inch / 8 + 0.1)
    return com2(mov(0, 0, t2 / 2), dif) ([
        brick(-1.0),
        grid(ptn_map(ptn, lambda: hole_small, lambda: hole_large)),
        holes(w, h, hol, t2, m4xr),
        hcuts(w, h, hol, wt * 2, 6.0).translate((0, 0, t2 / 2)),
    ])

def makeBot() -> Workplane:
    return sum([
        dif([
            brick(1.0),
            holes(w, h, hol, t2, m4dr),
            lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90).translate((-inch, h / 2 - wt / 2, wt2 / 2)),
            lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90).translate((inch, h / 2 - wt / 2, wt2 / 2)),
        ]),
    ]).translate((0, 0, t2 / 2))

top = makeTop(pattern("<>"))
bot = makeBot()
comp = bot + top.translate((0, 0, t2))

exporters.export(top, "STL/AGCM401.stl")
exporters.export(bot, "STL/AGCM410.stl")
exporters.export(comp, "STL/AGCM411.stl")
exporters.export(top, "STEP/AGCM401.step")
exporters.export(bot, "STEP/AGCM410.step")
