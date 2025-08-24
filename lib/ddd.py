import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from random import random
from lib.tools import *

wp: Workplane = Workplane()

def mov(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.translate((x, y, z))

def mirror(*plane: str) -> Callable[[Workplane], Workplane]:
	return lambda wp: reduce(lambda r, p: r.mirror(p, union = True), plane, wp)

def rotx(a: float) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.rotate((0, 0, 0), (1, 0, 0), a)
def roty(a: float) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.rotate((0, 0, 0), (0, 1, 0), a)
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

def hexNut(d: float, l: float) -> Workplane:
	return rotz(random() * 360) (
		wp.polygon(6, d)
		.extrude(l)
		.intersect(
			wp.circle(d / 2).extrude(l).chamfer(l / 5)
		)
	)

def pomona4mm() -> Workplane:
	return mov(z = 3.175) (
		wp.cylinder(6.35, 6.35).edges(">Z").chamfer(0.5)
		- mov(z = 3.175) (wp.cylinder(5.4, 2.1))
	)

def toggle(pos: bool) -> Workplane:
	return (
		mov(z = 3.175 / 2) (wp.cylinder(4, 3.175))
		+ com(mov(0, -2 if pos else 2, 9), rotx(13 if pos else -13)) (
			wp.cylinder(14, 1.3).fillet(1.299)
		)
		+ hexNut(8.5, 1.5)
	)

def bourns51() -> Workplane:
	return (
		mov(z = 12) (wp.cylinder(12.7, 5.5).edges(">Z").chamfer(0.5))
		+ mov(z = 4.5) (wp.cylinder(9, 9.5 / 2))
		+ hexNut(14, 2.36)
	)

def led5() -> Workplane:
	return (
		wp.circle(2.5).extrude(6).edges(">Z").fillet(2.499)
	)

def bounds(wp: Workplane) -> BoundBox:
	return wp.combine().objects[0].BoundingBox()

def box(w, h, t) -> Workplane:
	return wp.box(w, h, t)
def cylinder(l: float, r: float) -> Workplane:
	return wp.cylinder(l, r)
