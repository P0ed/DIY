import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *

wp: Workplane = Workplane()

def mov(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.translate((x, y, z))

def mirror(*plane: str) -> Callable[[Workplane], Workplane]:
	return lambda wp: reduce(lambda r, p: r.mirror(p, union = True), plane, wp)

def grid(tfm: Callable[[int, int], Workplane]) -> Workplane:
    return sum([tfm(x, y).translate(((x - 1.5) * inch, (y - 2.5) * inch, 0)) for x in range(4) for y in range(6)])

def lemo(wt: float) -> Workplane:
    return wp.cylinder(wt, 9.1 / 2).intersect(wp.box(8.3, 9.1, wt))

def holes(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return com(mirror("XZ"), mirror("YZ"), mov(w / 2 - d, h / 2 - d)) (
		wp.cylinder(l, r)
	)

def three(wp: Workplane) -> Workplane:
    box = wp.combine().objects[0].BoundingBox()
    return sum([
		mov() (wp),
        mov(box.xlen / 2 + box.ylen / 2 + 32) (
            wp.rotate((0, 0, 0), (0, 0, 1), 90)
        ),
        mov(0, 0, box.ylen / 2 + box.zlen + 32) (
            wp.rotate((0, 0, 0), (1, 0, 0), 90)
		),
	])
