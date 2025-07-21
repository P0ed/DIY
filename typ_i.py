from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from cadquery import exporters, Vector, Workplane

import sys, os
sys.path.append(os.path.abspath("."))
from lib.ddd import grid, lemo
from lib.tools import *

pl: float = 0.001
s2: float = sqrt(2) / 2
inch: float = 25.4

h: float = 7 * inch
mw: float = 4.25 * inch
w: float = mw + 0.25 * inch
t: float = 30.0

holx: float = 9.0
holy: float = 6.5

wt1: float = 3.3
wt2: float = 2.0
wt3: float = 1.5

c1: float = 1
c2: float = 0.5
c3: float = 0.25

cell: float = inch

wp = Workplane()

def sum(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x + y, xs)
def dif(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x - y, xs)

def holes(w: float, h: float, dw: float, dh: float, l: float, r: float) -> Workplane:
    return sum([
        wp.cylinder(l, r).translate((w / 2 - dw, h / 2 - dh, 0)),
        wp.cylinder(l, r).translate((-w / 2 + dw, h / 2 - dh, 0)),
        wp.cylinder(l, r).translate((w / 2 - dw, -h / 2 + dh, 0)),
        wp.cylinder(l, r).translate((-w / 2 + dw, -h / 2 + dh, 0)),
    ])

def wafer(w: float, h: float, t: float) -> Workplane:
    hcc: int = round(w / cell) + 1
    vcc: int = round(h / cell) + 1
    return sum([
        wp.box(w, h, wt3),
        sum([wp.box(wt3, h + 2 * c2, t).chamfer(c2).translate((x * cell - (hcc - 1) * cell / 2, 0, 0)) for x in range(hcc)]),
        sum([wp.box(w + 2 * c2, wt3, t).chamfer(c2).translate((0, x * cell - (vcc - 1) * cell / 2, 0)) for x in range(vcc)])
    ])

def case() -> Workplane:
    return sum([
        dif([
            wp.box(w, h, t).chamfer(c2),
            (
                wp.box(w - wt2 * 2, h - wt2 * 2, t - wt2 * 3)
                .chamfer(c2)
                .translate((0, 0, -wt2 / 2))
            ),
            (
                wp.box(mw + 0.7, h + c2 * 2, wt2 + c2 * 2)
                .chamfer(c2)
                .translate((0, 0, (t - wt2 + c2 * 2) / 2))
            ),
            (
                wp.box(4.25 * inch - wt3 * 2, h - 24.0, wt2 * 2 + c2 * 2)
                .chamfer(c2)
                .translate((0, 0, (t - wt2 * 2 - c2 * 2) / 2))
            ),
            holes(mw, h, holx, holy, wt2 * 2, 3.3 / 2).translate((0, 0, t / 2 - wt2)),
            lemo(wt2).rotate((0, 0, 0), (1, 0, 0), 90).translate((-inch, h / 2 - wt2 / 2)),
            lemo(wt2).rotate((0, 0, 0), (1, 0, 0), 90).translate((0, h / 2 - wt2 / 2)),
            lemo(wt2).rotate((0, 0, 0), (1, 0, 0), 90).translate((inch, h / 2 - wt2 / 2)),
            wp.box(4 * inch, 6 * inch, wt2).translate((0, 0, (wt2 - t) / 2)),
        ]),
        wafer(4 * inch, 6 * inch, wt2).translate((0, 0, (wt2 - t) / 2)),
    ]).translate((0, 0, t / 2))

_patterns: dict[str, Callable[[int, int], bool]] = {
    "ll": lambda x, y: x > 0 and x < 3,
    "w": lambda x, y: not ((y == 0 and (x == 0 or x == 3)) or (y == 1 and (x == 1 or x == 2))),
    "<>": lambda x, y: not (((y == 0 or y == 2) and (x == 0 or x == 3)) or (y == 1 and (x == 1 or x == 2))),
    "x": lambda x, y: ((y == 0 or y == 2) and (x == 0 or x == 3)) or (y == 1 and (x == 1 or x == 2)),
}
def pattern(name: str) -> Callable[[int, int], bool]:
    return _patterns[name] or (lambda x, y: True)

def makePanel(ptn: Callable[[int, int], bool]) -> Workplane:
    return dif([
        sum([
            dif([
                wp.box(mw, h, wt2).chamfer(c3),
                wp.box(4 * inch, 6 * inch, wt2),
            ]),
            wafer(4 * inch, 6 * inch, wt2),
        ]),
        grid(lambda x, y: (
            wp.cylinder(wt2, inch / 8 + 0.2)
            if ptn(x, y) else
            wp.cylinder(wt2, 9.7 / 2)
        )),
        holes(mw, h, holx, holy, wt2, 3.3 / 2),
    ]).translate((0, 0, wt2 / 2))

panel = makePanel(pattern("<>"))
exporters.export(panel, "Panel.stl")

unit = case()
exporters.export(unit, "Case.stl")
comp = unit + panel.translate((0, 0, t - wt2))
exporters.export(comp, "Case_x_Panel.stl")

[exporters.export(makePanel(ptn), "Panel_" + name + ".stl") for name, ptn in patterns.items()]
