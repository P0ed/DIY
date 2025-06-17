import sys, os
sys.path.append(os.path.abspath("lib"))
from ddd import thread
from cadquery import exporters, Vector, Workplane
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce

inch = 25.4
s2 = sqrt(2) / 2

h = 7 * inch
mw = 4.25 * inch
w = mw + 0.25 * inch
t = 28.0

holx = 9.0
holy = 6.5

wt1 = 3.3
wt2 = 2.0
wt3 = 1.5

c1 = 1
c2 = 0.5
c3 = 0.25

wp = Workplane()

def sum(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x + y, xs)
def dif(xs: List[Workplane]) -> Workplane:
    return reduce(lambda x, y: x - y, xs)
T = TypeVar('T')
def flat(xs: List[List[T]]) -> List[T]:
    return reduce(list.__add__, xs)

def holes(w: float, h: float, dw: float, dh: float, l: float, r: float) -> Workplane:
    return sum([
        wp.cylinder(l, r).translate((w / 2 - dw, h / 2 - dh, 0)),
        wp.cylinder(l, r).translate((-w / 2 + dw, h / 2 - dh, 0)),
        wp.cylinder(l, r).translate((w / 2 - dw, -h / 2 + dh, 0)),
        wp.cylinder(l, r).translate((-w / 2 + dw, -h / 2 + dh, 0)),
    ])

def grid(tfm: Callable[[], Workplane]) -> Workplane:
    return sum([tfm().translate(((x - 1.5) * inch, (y - 2.5) * inch, 0)) for x in range(4) for y in range(6)])

def lemo() -> Workplane:
    return wp.cylinder(wt2, 9.2 / 2).intersect(wp.box(8.4, 9.2, wt2))

unit = dif([
    wp.box(w, h, t).chamfer(c2),
    (
        wp.box(w - wt2 * 2, h - wt2 * 2, t - wt2 * 3)
        .chamfer(c2)
        .translate((0, 0, -wt2 / 2))
    ),
    (
        wp.box(4.25 * inch + 0.7, h + c2 * 2, wt2 + c2 * 2)
        .chamfer(c2)
        .translate((0, 0, (t - wt2 + c2 * 2) / 2))
    ),
    (
        wp.box(4.25 * inch - wt3 * 2, h - 24.0, wt2 * 2 + c2 * 2)
        .chamfer(c2)
        .translate((0, 0, (t - wt2 * 2 - c2 * 2) / 2))
    ),
    holes(mw, h, holx, holy, wt2 * 2, 3.3 / 2).translate((0, 0, t / 2 - wt2)),
    lemo().rotate((0, 0, 0), (1, 0, 0), 90).translate((-inch, h / 2 - wt2 / 2)),
    lemo().rotate((0, 0, 0), (1, 0, 0), 90).translate((0, h / 2 - wt2 / 2)),
    lemo().rotate((0, 0, 0), (1, 0, 0), 90).translate((inch, h / 2 - wt2 / 2))
]).translate((0, 0, t / 2))

panel = dif([
    (
        wp.box(4.25 * inch, 7 * inch, wt2)
        .chamfer(c2)
    ),
    holes(mw, h, holx, holy, wt2, 3.3 / 2),
    grid(lambda: wp.cylinder(wt2, 9.7 / 2))
]).translate((0, 0, wt2 / 2))

#m4 = thread(4.0, 0.8, 5, 0.8 / 3, 0.2)

exporters.export(unit, "Case.stl")
exporters.export(panel, "Panel.stl")

unit = unit + panel.translate((0, 0, t - wt2))
exporters.export(unit, "Case+Panel.stl")

