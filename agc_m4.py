from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar, Any
from functools import reduce
from cadquery import exporters, Vector, Workplane
from ocp_vscode import show

import sys, os
sys.path.append(os.path.abspath("."))
from lib.ddd import *
from lib.tools import *

m4xr: float = 4.1 / 2
m4dr: float = 3.4 / 2

wt: float = 3.0
wt2: float = 1.5
wtt: float = 4.5

cw: float = 4 * inch
ch: float = 6 * inch
col: float = 12.0
hol: float = col / 2
w: float = cw + col
h: float = ch + col * 2
t: float = 30.0
t2: float = t / 2.0
t3: float = t2 / 2.0
c1: float = 1.0
c2: float = 0.5

def box_fc(w, h, t, fe, fr, c) -> Workplane:
	return (
        wp.box(w, h, t)
		.edges(fe).fillet(fr)
		.edges().chamfer(c)
	)

def hcuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return sum([
        mirror2('XZ', 'YZ') (
            box_fc((r + d) * 2, (r + d) * 2, l + c1, "+Z", r, c2)
            .translate((w / 2, h / 2, c2 - l / 2))
        ),
        mirror2('XZ', 'YZ') (
            box_fc((r + d + c2) * 2, (r + d + c2) * 2, c1 + pl, "+Z", r + c2, c2)
            .translate((w / 2, h / 2, 0))
        ),
    ])

def brick(wall: float, dir: float) -> Workplane:
    return dif([
        (
            wp.box(w, h, t2)
            .edges("+Z").chamfer(wtt)
            .intersect(
                wp.box(w, h, t2 + c1)
                .edges("+Z").chamfer(wtt)
                .edges("not +Z").chamfer(c2)
                .translate((0, 0, c2 * dir))
            )
        ),
        com2(mov(0, 0, wall * dir), sum) ([
            box_fc(cw, ch, t2, "|Z", 2.0, c2),
            box_fc(w - col * 2, h - wt * 2, t2, '|Z', 2.0, c2),
        ]),
        mirror("YZ") (
            box_fc(wt * 2, h - col * 2, t2 + 4.0, '|X', 2.0, c2)
            .translate((w / 2, 0, -wtt - 2.0 if dir != 1 else 0))
        ),
    ])

def makeTop(ptn: Callable[[int, int], bool]) -> Workplane:
    hole_large = wp.cylinder(t2, 9.53 / 2 + 0.1)
    hole_small = wp.cylinder(t2, inch / 8 + 0.1)
    return com2(mov(0, 0, t3), dif) ([
        brick(wt, -1.0),
        grid(ptn_map(ptn, lambda: hole_large, lambda: hole_small)),
        holes(w, h, hol, t2, m4xr),
        hcuts(w, h, hol, wtt, hol * s2).translate((0, 0, t3)),
        com(mirror("XZ"), mov(0, 1.5 * inch, t3)) (
            box_fc(4 * inch - wt, 3 * inch - wt, 2.0, '|Z', 2.0, c2)
        ),
    ])

def makeBot() -> Workplane:
    return com(mov(0, 0, t3), dif) ([
        brick(wt, 1.0),
        holes(w, h, hol, t2, m4dr),
        com(mirror("XZ"), mov(0, 1.5 * inch + wt2 / 2, wt - t3)) (
            box_fc(4 * inch, 3 * inch - wt2, 2.0, '|Z', 2.0, c2)
        ),
        com(mirror("XZ"), mov(0, (h - col) / 2 - wt, wt - t3)) (
            box_fc(w - col * 2, col, 2.0, '|Z', 2.0, c2),
        ),
        com(mirror("YZ"), mov(inch, h / 2 - wt / 2, 1.0)) (
             lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90)
        ),
    ])

bot = makeBot()
top = makeTop(ptn_all)

comp = bot + top.translate((0, 0, t2 + pl))

show(bot, top.translate((0, 0, t2 + pl)))

exporters.export(top, "STL/AGCM401.stl")
exporters.export(bot, "STL/AGCM410.stl")
exporters.export(comp, "STL/AGCM411.stl")
exporters.export(top, "STEP/AGCM401.step")
exporters.export(bot, "STEP/AGCM410.step")
