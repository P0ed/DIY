import os
from cadquery import Vector, Workplane, Face, Solid, Shell, BoundBox
from math import sin, cos, pi, floor, sqrt
from typing import Union, Tuple, Sequence, Optional, Callable, List, Dict, TypeVar
from functools import reduce
from lib.tools import *
from lib.ddd import *

def export(bot: Workplane, top: Workplane):
	bbox: BoundBox = bot.combine().objects[0].BoundingBox()
	tbox: BoundBox = top.combine().objects[0].BoundingBox()

	comp = sum([
		mov(0, 0, -bbox.zlen / 2) (bot),
		mov(0, 0, tbox.zlen / 2 + pl) (top),
	])

	os.makedirs("STL", exist_ok=True)
	os.makedirs("STEP", exist_ok=True)
	os.makedirs("SVG", exist_ok=True)

	top.export("STL/AGC01.stl")
	bot.export("STL/AGC10.stl")
	comp.export("STL/AGC11.stl")

	render("SVG/AGC11.svg", three(comp))
	top.export("STEP/AGC01.step")
	bot.export("STEP/AGC10.step")


def render(path: str, wp: Workplane):
	box = wp.combine().objects[0].BoundingBox()
	wp.export(path, opt = {
		"width": box.xlen * 8 + 64,
		"height": box.ylen * 8 + 64,
		"marginLeft": 32,
		"marginTop": 32,
		"showAxes": False,
		"projectionDir": (0, 0, 1),
		"strokeWidth": 0.25,
		"strokeColor": (255, 0, 0),
		"hiddenColor": (0, 0, 255),
		"showHidden": False,
		# "focus": 100,
	})
