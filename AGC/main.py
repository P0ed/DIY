from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar, Any
from functools import reduce
from cadquery import exporters, Vector, Workplane

import sys, os
sys.path.append(os.path.abspath("."))
from lib.ddd import thread

pl: float = 0.001
s2: float = sqrt(2) / 2
inch: float = 25.4

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

c: float = 1
c2: float = 0.5

cell: float = inch
scuth: float = (h - wt * 6) / 2 - wt * 2

wp = Workplane()

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')
def id(x: A) -> A:
    return x
def com2(l: Callable[[B], C], r: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: l(r(x))
def com(xs: List[Callable[[Any], Any]]) -> Callable[[Any], Any]:
    return reduce(com2, xs, id)
def flat(xs: List[List[A]]) -> List[A]:
    return reduce(list.__add__, xs)
def sum(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x + y, xs)
def dif(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x - y, xs)

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
    ])

def grid(tfm: Callable[[int, int], Workplane]) -> Workplane:
    return sum([tfm(x, y).translate(((x - 1.5) * inch, (y - 2.5) * inch, 0)) for x in range(4) for y in range(6)])

def lemo() -> Workplane:
    return wp.cylinder(wt, 9.1 / 2).intersect(wp.box(8.3, 9.1, wt))

def case() -> Workplane:
    return sum([
        dif([
            wp.box(w, h, t2).edges("+Z").chamfer(c * 2).intersect(wp.box(w, h, t2 + c2 * 2).chamfer(c2).translate((0, 0, c2))),
            (
                wp.box(cw, ch, t2)
                .chamfer(c2)
                .translate((0, 0, wt2))
            ),
            (
                wp.box((col - wt) * 2, scuth, t2)
                .chamfer(c2)
                .translate((w / 2, h / 4 - col / 4, wt))
                .mirror("YZ", union = True)
                .mirror("XZ", union = True)
            ),
            holes(w, h, hol, t2, 2.5 / 2).translate((0, 0, 0)),
            lemo().rotate((0, 0, 0), (1, 0, 0), 90).translate((-inch, h / 2 - wt / 2, wt2 / 2)),
            lemo().rotate((0, 0, 0), (1, 0, 0), 90).translate((inch, h / 2 - wt / 2, wt2 / 2)),
        ]),
    ]).translate((0, 0, t2 / 2))

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
        wp.box(w, h, t2).edges("+Z").chamfer(c * 2).intersect(wp.box(w, h, t2 + c2 * 2).chamfer(c2).translate((0, 0, -c2))),
        (
            wp.box(cw, ch, t2)
            .chamfer(c2)
            .translate((0, 0, -wt2))
        ),
        (
            wp.box((col - wt) * 2, scuth, t2)
            .chamfer(c2)
            .translate((w / 2, h / 4 - col / 4, -wt))
            .mirror("YZ", union = True)
            .mirror("XZ", union = True)
        ),
        grid(lambda x, y: (
            wp.cylinder(t2, inch / 8 + 0.2)
            if ptn(x, y) and y < 3 else
            wp.cylinder(t2, 9.7 / 2)
        )),
        holes(w, h, hol, t2, 3.1 / 2),
        hcuts(w, h, hol, wt, 3.5).translate((0, 0, t2 / 2 - wt / 2)),
    ]).translate((0, 0, t2 / 2))

panel = makePanel(pattern("<>"))
exporters.export(panel, "TOP.stl")

unit = case()
exporters.export(unit, "BOT.stl")
comp = unit + panel.translate((0, 0, t2))
exporters.export(comp, "COMP.stl")
