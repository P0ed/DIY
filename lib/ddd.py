import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Optional, Callable, List, TypeVar
from functools import reduce
from random import random
from lib.tools import *

wp: Workplane = Workplane()

def bounds(w: Workplane) -> BoundBox:
	return w.combine().objects[0].BoundingBox()

def mov(x: float = 0.0, y: float = 0.0, z: float = 0.0) -> Callable[[Workplane], Workplane]:
	return lambda w: w.translate((x, y, z))

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

def lemo0BCutout(wt: float) -> Workplane:
    return cylinder(wt, 9.1 / 2).intersect(box(8.3, 9.1, wt))

def holes(w: float, h: float, l: float, r: float) -> Workplane:
    return com(mirror('XZ', 'YZ'), mov(w, h)) (
		cylinder(l, r)
	)

def hexNut(d: float, l: float) -> Workplane:
	return rotz(random() * 60) (
		wp.polygon(6, d)
		.extrude(l)
		.intersect(
			wp.circle(d / 2).extrude(l).chamfer(l / 3)
		)
	)

def lemoECG0B() -> Workplane:
	return rotz(90) (
		mov(z=3.5 / 2) (
			cylinder(3.5, 9 / 2).intersect(box(9, 8.2, 3.5))
		)
		+ mov(z=2.5 / 2) (
			cylinder(2.5, 12 / 2).edges('>Z').chamfer(1)
		)
		- rotz(45) (mirror('XZ', 'YZ') (rotz(-45) (mov(6) (
			box(1.4, 1.5, 5)
		))))
	)

def pomona1581() -> Workplane:
	return rotz(90) (
		(cone(6.35, 6.15, 6.35) - mov(z = 6.35) (cylinder(12.5, 2.1)))
		.edges('>Z').chamfer(0.5)
	)

def toggle(pos: Optional[bool] = None) -> Workplane:
	pos = random() < 0.5 if pos is None else pos
	return (
		com(mov(z = 4.2 / 2), rotz(90)) (
			cylinder(4.2, 3.175).edges('>Z').chamfer(0.5)
		)
		+ com(mov(0, -1.7 if pos else 1.7, 9), rotx(13 if pos else -13)) (
			rotz(90) (cylinder(14, 1.3).fillet(1.299))
		)
		+ hexNut(8.5, 1.5)
	)

def knob(angle: Optional[float] = None) -> Workplane:
	angle = random() * 120 - 60 if angle is None else angle
	return com(rotz(angle), mov(z = 6.35)) (
		dif([
			rotz(90) (cylinder(12.7, 6.35)),
			com(mirror('YZ'), mov(13.5, 0, 8), roty(75)) (box(20, 20, 20)),
		])
		.edges('>Z').chamfer(0.15)
		- mov(0, 5, 6.249) (box(1.5, 10.0, 1.5).fillet(0.749))
		- mov(z = 3 - 9.499 / 2) (cylinder(9.5, 6.35 / 2))
	)

def bourns51(angle: Optional[float] = None) -> Workplane:
	angle = random() * 120 - 60 if angle is None else angle
	return (
		com(mov(z = 2.5), rotz(90)) (
			cylinder(5, 9.5 / 2).edges('>Z').chamfer(0.5)
		)
		+ com(mov(z = 4 + 5), rotz(90 + angle)) (
			cylinder(10, 6.35 / 2).edges('>Z').chamfer(0.5)
			- mov(z = 5) (box(7, 1.5, 3))
		)
		+ hexNut(14, 2.36)
	)

def led5() -> Workplane:
	return rotz(90) (
		wp.circle(2.5).extrude(4.5).edges('>Z').fillet(2.499)
	)

def clb300() -> Workplane:
	sph = lambda z: mov(z=z) (wp.sphere(8))
	return rotz(90) (
		mov(z=0.9) (sph(7.2).intersect(sph(-7.2)))
		+ cylinder(1.8, 7.11 / 2)
	)

def frame(w: float, h: float, t: float, wt: float, c: float = 0.5, ir: float = 2.0) -> Workplane:
	return sum([
		com(mirror('XZ'), mov(y = h / 2 - wt / 2)) (box(w, wt, t)),
		com(mirror('YZ'), mov(x = w / 2 - wt / 2)) (box(wt, h, t)),
	]).intersect(
		box(w, h, t).edges('|Z').fillet(ir).edges().chamfer(c)
	)

def xxx(w: float, h: float, t: float, wt: float, ws: float, c: float = 0.5, ir: float = 2.0) -> Workplane:
	cnt = round((w - wt * 2) / ws)
	return sum([
		mirror('YZ') (mov(ws * i - w / 2, ws * i - h / 2) (
			rotz(-45) (box(ws * i * 2 * s2, wt, t).chamfer(c))
		))
		for i in range(1, cnt)
	]).intersect(
		box(w, h, t).chamfer(c)
	)
