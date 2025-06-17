import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce

VectorLike = Union[Tuple[float, float], Tuple[float, float, float], Vector]

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
    minDeg = deg
    e1_bottom = (Workplane("XY")
        .parametricCurve(helix(radius, 0, pitch, height, -d), N = N, minDeg = minDeg, maxDeg = deg, smoothing = smooth, tol = tol).val()
    )
    e1_top = (Workplane("XY")
        .parametricCurve(helix(radius, 0, pitch, height, d), N = N,  minDeg = minDeg, maxDeg = deg, smoothing = smooth, tol = tol).val()
    )
    e2_bottom = (Workplane("XY")
        .parametricCurve(helix(radius, radius_eps, pitch, height, -d / aspect), N = N, minDeg = minDeg, maxDeg = deg, smoothing = smooth, tol = tol).val()
    )
    e2_top = (Workplane("XY")
        .parametricCurve(helix(radius, radius_eps, pitch, height, d / aspect), N = N, minDeg = minDeg, maxDeg = deg, smoothing = smooth, tol = tol).val()
    )

    f1 = Face.makeRuledSurface(e1_bottom, e1_top)
    f2 = Face.makeRuledSurface(e2_bottom, e2_top)
    f3 = Face.makeRuledSurface(e1_bottom, e2_bottom)
    f4 = Face.makeRuledSurface(e1_top, e2_top)

    sh = Shell.makeShell([f1,f2,f3,f4])
    rv = Solid.makeSolid(sh)

    return rv
