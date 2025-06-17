from cadquery import exporters, Vector, Workplane
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce

s2 = sqrt(2) / 2

l = 36.0
w = 9.0
t = 2.0

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

unit = dif([
    wp.ellipse(w / 2, l / 2).extrude(t).chamfer(c2),
]).translate((0, 0, t / 2))

exporters.export(unit, "spoon.stl")
