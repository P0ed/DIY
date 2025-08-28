import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from random import random
from lib.tools import *

wp: Workplane = Workplane()

def bounds(wp: Workplane) -> BoundBox:
	return wp.combine().objects[0].BoundingBox()

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

def box(w, h, t) -> Workplane:
	return wp.box(w, h, t)
def cylinder(l: float, r: float) -> Workplane:
	return wp.cylinder(l, r)
def cone(r1: float, r2: float, h: float) -> Workplane:
	return Workplane(Solid.makeCone(r1, r2, h))

def grid(tfm: Callable[[int, int], Optional[Workplane]]) -> Workplane:
    return sum(compact([
		map_opt(mov((x - 1.5) * inch, (y - 2.5) * inch)) (tfm(x, y))
		for x in range(4) for y in range(6)
	]))

def lemo(wt: float) -> Workplane:
    return cylinder(wt, 9.1 / 2).intersect(wp.box(8.3, 9.1, wt))

def holes(w: float, h: float, l: float, r: float) -> Workplane:
    return com(mirror('XZ', 'YZ'), mov(w, h)) (
		cylinder(l, r)
	)

def hexNut(d: float, l: float) -> Workplane:
	return rotz(random() * 360) (
		wp.polygon(6, d)
		.extrude(l)
		.intersect(
			wp.circle(d / 2).extrude(l).chamfer(l / 3)
		)
	)

def pomona4mm() -> Workplane:
	return (
		cone(6.35, 6.15, 6.35).edges('>Z').chamfer(0.5)
		- mov(z = 6.35) (cylinder(12.5, 2.1))
	)

def toggle(pos: bool) -> Workplane:
	return (
		com(mov(z = 3.175 / 2), rotz(90)) (
			cylinder(4, 3.175).edges('>Z').chamfer(0.5)
		)
		+ com(mov(0, -2 if pos else 2, 9), rotx(13 if pos else -13)) (
			rotz(90) (cylinder(14, 1.3).fillet(1.299))
		)
		+ hexNut(8.5, 1.5)
	)

def knob() -> Workplane:
	return mov(z = 6.0) (
		dif([
			rotz(90) (cylinder(12.0, 6.35)),
			com(mirror('YZ'), mov(13.5, 0, 8), roty(75)) (box(20, 20, 20)),
		])
		.edges('>Z').chamfer(0.15)
		- mov(0, 5, 6.249) (box(1.5, 10.0, 1.5).fillet(0.749))
		- mov(z = 3 - 9.499 / 2) (cylinder(9.5, 6.35 / 2))
	)

def bourns51() -> Workplane:
	return (
		com(mov(z = 2.75), rotz(90)) (
			cylinder(5.5, 9.5 / 2).edges('>Z').chamfer(0.5)
		)
		+ com(mov(z = 4.5 + 5), rotz(90 + random() * 120 - 60)) (
			cylinder(10, 6.35 / 2).edges('>Z').chamfer(0.5)
			- mov(z = 5) (box(7, 1.5, 3))
		)
		+ hexNut(14, 2.36)
	)

def led5() -> Workplane:
	return rotz(90) (
		wp.circle(2.5).extrude(4.5).edges('>Z').fillet(2.499)
	)

def xxx(w: float, h: float, t: float, wt: float, ws: float, c: float = 0.5, ir: float = 2.0) -> Workplane:
		cnt = round((w - wt * 2) / ws)
		return sum([
			com(mirror('XZ'), mov(y = h / 2 - wt / 2)) (box(w, wt, t)),
			com(mirror('YZ'), mov(x = w / 2 - wt / 2)) (box(wt, h, t)),
			*([
				mirror('YZ') (mov(ws * i - w / 2, ws * i - h / 2) (
					rotz(-45) (box(ws * i * 2 * s2, wt, t).chamfer(c))
				))
				for i in range(1, cnt)
			]),
		]).intersect(
			box(w, h, t).edges('|Z').fillet(ir).edges().chamfer(c)
		)
