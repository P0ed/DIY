import os
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *
from lib.ddd import *

def three_view(wp: Workplane) -> Workplane:
	box: BoundBox = bounds(wp)
	offset: float = box.xlen / 4

	return com(mov(box.xlen / 2 + box.ylen / 2, 0, box.ylen / 2 + box.zlen / 2), sum) ([
		mov() (wp),
        mov(box.xlen / 2 + box.ylen / 2 + offset) (
            wp.rotate((0, 0, 0), (0, 0, 1), -90)
        ),
        mov(0, 0, box.ylen / 2 + box.zlen / 2 + offset) (
            wp.rotate((0, 0, 0), (1, 0, 0), 90)
		),
	])

def render(path: str, wp: Workplane, hidden: bool = False):
	view = three_view(wp).rotate((0, 0, 0), (0, 1, 0), 90)
	margin: float = 30.0

	view.export(path, opt = {
		"width": 1280,
		"height": 960,
		"marginLeft": margin,
		"marginTop": margin,
		"showAxes": False,
		"projectionDir": (0, -1, 0),
		"strokeWidth": 0.25,
		"strokeColor": (8, 8, 8),
		"hiddenColor": (223, 223, 223),
		"showHidden": hidden,
	})

def export(name: str, wp: Workplane, stl: bool = True, svg: bool = True, step: bool = True, hidden: bool = False):
	[os.makedirs(dir, exist_ok=True) for dir in ["STL", "STEP", "SVG"]]

	if stl: wp.export("STL/" + name + ".stl")
	if svg: render("SVG/" + name + ".svg", wp, hidden = hidden)
	if step: wp.export("STEP/" + name + ".step")
