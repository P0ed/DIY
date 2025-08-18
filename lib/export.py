import os
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *
from lib.ddd import *

def three_view(wp: Workplane) -> Workplane:
    box = bounds(wp)
    return com(mov(box.xlen / 2 + box.ylen / 2, 0, box.ylen / 2 + box.zlen / 2), sum) ([
		mov() (wp),
        mov(box.xlen / 2 + box.ylen / 2 + 32) (
            wp.rotate((0, 0, 0), (0, 0, 1), 90)
        ),
        mov(0, 0, box.ylen / 2 + box.zlen / 2 + 32) (
            wp.rotate((0, 0, 0), (1, 0, 0), 90)
		),
	])

def render(path: str, wp: Workplane, margin: float = 32.0, hidden: bool = False):
	view = three_view(wp).rotate((0, 0, 0), (0, 1, 0), 90)
	box = bounds(view)

	view.export(path, opt = {
		"width": (box.xlen + margin * 2) * 4,
		"height": (box.ylen + margin * 2) * 4,
		"marginLeft": margin,
		"marginTop": margin,
		"showAxes": False,
		"projectionDir": (0, -1, 0),
		"strokeWidth": 0.25,
		"strokeColor": (8, 8, 8),
		"hiddenColor": (223, 223, 223),
		"showHidden": hidden,
	})

def export(bot: Workplane, top: Workplane):
	bbox: BoundBox = bounds(bot)
	tbox: BoundBox = bounds(top)

	comp = sum([
		mov(0, 0, -bbox.zlen / 2 - pl) (bot),
		mov(0, 0, tbox.zlen / 2 + pl) (top),
	])

	[os.makedirs(dir, exist_ok=True) for dir in ["STL", "STEP", "SVG"]]

	bot.export("STL/AGC01.stl")
	top.export("STL/AGC10.stl")
	comp.export("STL/AGC11.stl")

	render("SVG/AGC01.svg", bot)
	render("SVG/AGC10.svg", top)
	render("SVG/AGC11.svg", comp)

	bot.export("STEP/AGC01.step")
	top.export("STEP/AGC10.step")
