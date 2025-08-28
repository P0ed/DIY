import cadquery as cq
from cadquery import Vector, Workplane, Face, Solid, Shell
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar, NewType, Any
from functools import reduce

VectorLike = Union[Tuple[float, float], Tuple[float, float, float], Vector]
Pattern = Callable[[int, int], bool]

pl: float = 0.001
s2: float = sqrt(2)
s22: float = s2 / 2
inch: float = 25.4

A = TypeVar('A')
B = TypeVar('B')
C = TypeVar('C')

def id(x: A) -> A:
	return x
def const(x: A) -> Callable[[B], A]:
	return lambda _: x
def map_opt(tfm: Callable[[A], B]) -> Callable[[Optional[A]], Optional[B]]:
	return lambda m: None if m is None else tfm(m)
def compact(xs: List[Optional[A]]) -> List[A]:
	return [x for x in xs if x is not None]
def com2(l: Callable[[B], C], r: Callable[[A], B]) -> Callable[[A], C]:
	return lambda x: l(r(x))
def com(*xs: Callable[[Any], Any]) -> Callable[[Any], Any]:
	return reduce(com2, xs, id)
def flat(xs: List[List[A]]) -> List[A]:
	return reduce(list.__add__, xs)
def sum(xs: List[Workplane]) -> Workplane:
	return reduce(lambda x, y: x + y, xs)
def dif(xs: List[Workplane]) -> Workplane:
	return reduce(lambda x, y: x - y, xs)

def und(l: Pattern, r: Pattern) -> Pattern:
	return lambda x, y: l(x, y) and r(x, y)
def oder(l: Pattern, r: Pattern) -> Pattern:
	return lambda x, y: l(x, y) or r(x, y)
def nicht(r: Pattern) -> Pattern:
	return lambda x, y: not r(x, y)

ptn_all = lambda x, y: True
ptn_top = lambda x, y: y > 2
ptn_bot = lambda x, y: y < 3
ptn_mdx = lambda x, y: x > 0 and x < 3
ptn_x = lambda x, y: (x + y % 2 + x // 2) % 2 == 0
ptn_d = lambda x, y: (x + y % 2 + x // 2) % 2 == 1
ptn_w = und(ptn_d, lambda x, y: y < 2)

def ptn_map(ptn: Pattern, true: Callable[[], A], false: Callable[[], A]) -> Callable[[int, int], A]:
	return lambda x, y: true() if ptn(x, y) else false()

def ptns_map(*ptns: Tuple[Pattern, Callable[[], A]]) -> Callable[[int, int], Optional[A]]:
	return lambda x, y: reduce(
		lambda r, e: e[1]() if r is None and e[0](x, y) else r,
		ptns,
		None
	)
