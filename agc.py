from typing import Callable, List
from functools import reduce
from cadquery import Workplane
from ocp_vscode import show

import sys, os
sys.path.append(os.path.abspath('.'))
from lib.ddd import *
from lib.tools import *
from lib.export import export
from lib.thread import thread

m4r: float = 4.0 / 2
m4xr: float = 4.2 / 2
m4dr: float = 3.3 / 2

wt: float = 3.0
wt2: float = 1.5

units: int = 3
cw: float = 4 * inch
ch: float = 6 * inch
col: float = 12.0
hol: float = col / 2
w: float = units * cw + 0.5 * inch
h: float = 7 * inch
t: float = 30.0
t2: float = t / 2.0
t3: float = t2 / 2.0
c1: float = 1.0
c2: float = 0.5
ir: float = 2.0

def box_fc(w, h, t, fe, fr, c) -> Workplane:
	return (
        wp.box(w, h, t)
		.edges(fe).fillet(fr)
		.edges().chamfer(c)
	)

def hcuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
    return sum([
        mirror('XZ', 'YZ') (
            box_fc((r + d) * 2, (r + d) * 2, l + c1, '+Z', r, c2)
            .translate((w / 2, h / 2, c2 - l / 2))
        ),
        mirror('XZ', 'YZ') (
            box_fc((r + d + c2) * 2, (r + d + c2) * 2, c1 + pl, '+Z', r + c2, c2)
            .translate((w / 2, h / 2, 0))
        ),
    ])

def brick(wall: float, dir: float) -> Workplane:
    return dif([
        (
            wp.box(w, h, t2)
            .edges('+Z').chamfer(wt2 * 3)
            .intersect(
                wp.box(w, h, t2 + c1)
                .edges('+Z').chamfer(wt2 * 3)
                .edges('not +Z').chamfer(c2)
                .translate((0, 0, c2 * dir))
            )
        ),
        com2(mov(0, 0, wall * dir), sum) ([
            box_fc(w - col, h - col * 2, t2, '|Z', ir, c2),
            box_fc(w - col * 2, h - wt * 2, t2, '|Z', ir, c2),
        ]),
        mirror('YZ') (
            box_fc(wt * 2, h - col * 2, t2 + 4.0, '|X', ir, c2)
            .translate((w / 2, 0, -wt - 2.0 if dir != 1 else 0))
        ),
    ])

def makeTop(ptn: Callable[[int, int], bool] = ptn_all) -> Workplane:
	hole_large = wp.cylinder(t2, 9.53 / 2 + 0.1)
	hole_small = wp.cylinder(t2, inch / 8 + 0.1)

	return dif([
		brick(wt, -1.0),
		com(mov(-cw / 2 * (units - 1)), sum) ([
			com(mov(cw * i), sum) ([
				grid(ptn_map(ptn, lambda: hole_large, lambda: hole_small)),
				com(mirror('XZ'), mov(0, 1.5 * inch, t3)) (
					box_fc(cw - wt, ch / 2 - wt, 2.0, '|Z', ir, c2)
				),
			])
			for i in range(units)
		]),
		holes(w, h, hol, t2, m4xr),
		hcuts(w, h, hol, wt * 2, hol * s2).translate((0, 0, t3)),
	])

def makeBot() -> Workplane:
    return dif([
        brick(wt, 1.0),
        holes(w, h, hol, t2, m4dr),
        mov(0, 0, -t3 / 2) (holes(w, h, hol, t3, m4xr)),
        com(mirror('XZ'), mov(0, (h / 2 - col + wt2) / 2, wt - t3)) (
            box_fc(w - 4 * wt, h / 2 - col - wt2, 2.0, '|Z', ir, c2)
        ),
        com(mirror('XZ'), mov(0, (h - col) / 2 - wt, wt - t3)) (
            box_fc(w - col * 2, col, 2.0, '|Z', ir, c2),
        ),
        com(mirror('YZ'), mov(inch, h / 2 - wt / 2, 1.0)) (
             lemo(wt).rotate((0, 0, 0), (1, 0, 0), 90)
        ),
    ])

def threadCut(body: Workplane) -> Workplane:
    return com(rotz(180), mov((col / 2 - w) / 2, (col * 3 / 2 - h) / 2)) (
		sum([
			body - holes(w, h, hol, t2, m4r),
			mov(w / 2 - hol, h / 2 - hol) (Workplane(thread('M4', t3, 'internal'))),
		])
		.intersect(mov(w / 2, h / 2) (wp.box(col, col * 3, t)))
	)

bot: Workplane = makeBot()
top: Workplane = makeTop()
stk: List[Workplane] = [
	mov(z = -t3 - pl) (bot),
	mov(z = t3 + pl) (top),
]
# thd: Workplane = threadCut(1, bot)

export('AGC01', bot)
export('AGC10', top)
export('AGC11', sum(stk), step = False)
# export('AGC01_Thread', thd, stl = False, step = False)
show(stk)
