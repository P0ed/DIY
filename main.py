from typing import Callable, List
from cadquery import Workplane
from ocp_vscode import show
from lib.ddd import *
from lib.tools import *
from lib.export import export
from agc import agc

offsets: Callable[[int], Callable[[Workplane], Workplane]] = lambda m: mov(
	7.5 * inch if m == 2 else 4 * inch if m == 3 else 0,
	8 * inch if m == 3 else 0
)

units: List[List[Workplane]] = [
	map_lst(offsets(m)) (
		agc(
			m,
			const(und(ptn_bot, ptn_x)),
			lambda i: und(ptn_bot, ptn_d if i == 1 else ptn_w)
		)
	)
	for m in range(1, 4)
]

for i, parts in enumerate(units):
	export(f'AGC-{i + 1}M-01', parts[0])
	export(f'AGC-{i + 1}M-10', parts[1])
	export(f'AGC-{i + 1}M-11', sum([parts[0], parts[1]]), step = False)
	if i == 0 and len(parts) > 4: export(f'AGC-01T', parts[4], stl = False, step = False)

show(units)

# show(knob())
