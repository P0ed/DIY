import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *

wp: Workplane = Workplane()

def grid(tfm: Callable[[int, int], Workplane]) -> Workplane:
    return sum([tfm(x, y).translate(((x - 1.5) * inch, (y - 2.5) * inch, 0)) for x in range(4) for y in range(6)])

def lemo(wt: float) -> Workplane:
    return wp.cylinder(wt, 9.1 / 2).intersect(wp.box(8.3, 9.1, wt))

def mov(x: float, y: float, z: float) -> Callable[[Workplane], Workplane]:
	return lambda wp: wp.translate((x, y, z))

def holes(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return (
		wp.cylinder(l, r)
		.translate((w / 2 - d, h / 2 - d, 0))
		.mirror("YZ", union = True)
		.mirror("XZ", union = True)
	)

def box_fc(w, h, t, fe, fr, c) -> Workplane:
	return (
        wp.box(w, h, t)
		.edges(fe)
		.fillet(fr)
		.edges()
		.chamfer(c)
	)

# Threads:
def helix(r0, r_eps, p, h, d = 0, frac: float = 1e-1):
	def func(t):
		if t > frac and t < 1 - frac:
			z = h * t + d
			r = r0 + r_eps
		elif t <= frac:
			z = h * t + d * sin(pi / 2 * t / frac)
			r = r0 + r_eps * sin(pi / 2 * t / frac)
		else:
			z = h * t - d * sin(2 * pi - pi / 2 * (1 - t) / frac)
			r = r0 - r_eps * sin(2 * pi - pi / 2 * (1 - t) / frac)

		x = r * sin(-2 * pi / (p / h) * t)
		y = r * cos(2 * pi / (p / h) * t)

		return x, y, z

	return func

def thread(radius: float, pitch: float, height: float, d, radius_eps, aspect = 10, N = 100, deg = 3, smooth = None, tol = 1e-6):
	e1_bhx = helix(radius, 0, pitch, height, -d)
	e1_thx = helix(radius, 0, pitch, height, d)
	e2_bhx = helix(radius, radius_eps, pitch, height, -d / aspect)
	e2_thx = helix(radius, radius_eps, pitch, height, d / aspect)
	e1_bottom = wp.parametricCurve(e1_bhx, N = N, minDeg = deg, maxDeg = deg, smoothing = smooth, tol = tol).val()
	e1_top = wp.parametricCurve(e1_thx, N = N,  minDeg = deg, maxDeg = deg, smoothing = smooth, tol = tol).val()
	e2_bottom = wp.parametricCurve(e2_bhx, N = N, minDeg = deg, maxDeg = deg, smoothing = smooth, tol = tol).val()
	e2_top = wp.parametricCurve(e2_thx, N = N, minDeg = deg, maxDeg = deg, smoothing = smooth, tol = tol).val()

	f1 = Face.makeRuledSurface(e1_bottom, e1_top)
	f2 = Face.makeRuledSurface(e2_bottom, e2_top)
	f3 = Face.makeRuledSurface(e1_bottom, e2_bottom)
	f4 = Face.makeRuledSurface(e1_top, e2_top)

	sh = Shell.makeShell([f1,f2,f3,f4])
	rv = Solid.makeSolid(sh)

	return rv
