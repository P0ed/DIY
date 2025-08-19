import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *

wp: Workplane = Workplane()

def mov(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.translate((x, y, z))

def mirror(*plane: str) -> Callable[[Workplane], Workplane]:
	return lambda wp: reduce(lambda r, p: r.mirror(p, union = True), plane, wp)

def rotz(a: float) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.rotate((0, 0, 0), (0, 0, 1), a)

def grid(tfm: Callable[[int, int], Workplane]) -> Workplane:
    return sum([tfm(x, y).translate(((x - 1.5) * inch, (y - 2.5) * inch, 0)) for x in range(4) for y in range(6)])

def lemo(wt: float) -> Workplane:
    return wp.cylinder(wt, 9.1 / 2).intersect(wp.box(8.3, 9.1, wt))

def holes(w: float, h: float, dw: float, dh: float, l: float, r: float) -> Workplane:
    return com(mirror("XZ"), mirror("YZ"), mov(w / 2 - dw, h / 2 - dh)) (
		wp.cylinder(l, r)
	)

def bounds(wp: Workplane) -> BoundBox:
	return wp.combine().objects[0].BoundingBox()
