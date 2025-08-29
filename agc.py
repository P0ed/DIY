from typing import Callable, List
from cadquery import Workplane
from lib.ddd import *
from lib.tools import *
from lib.thread import thread

def agc(
		modules: int = 1,
		potsPtn: Callable[[int], Pattern] = lambda i: ptn_x,
		tglsPtn: Callable[[int], Pattern] = lambda i: ptn_d,
		threads: bool = False
	) -> List[Workplane]:

	m4r: float = 4.0 / 2
	m4xr: float = 4.2 / 2
	m4dr: float = 3.3 / 2
	wt: float = 3.0
	wt2: float = 1.5
	cw: float = 4 * inch
	ch: float = 6 * inch
	col: float = 12.0
	hol: float = col / 2
	w: float = modules * cw + 0.5 * inch
	h: float = 7 * inch
	t: float = 30.0
	t2: float = t / 2.0
	t3: float = t2 / 2.0
	c1: float = 1.0
	c2: float = 0.5
	crh: float = (2 - s2) * hol
	ir: float = 2.0

	def box_fc(w, h, t, fe = '|Z', fr = ir, c = c2) -> Workplane:
		return (
			wp.box(w, h, t)
			.edges(fe).fillet(fr)
			.edges().chamfer(c)
		)

	def module(tfm: Callable[[int], Workplane]) -> Workplane:
		return com(mov(-cw / 2 * (modules - 1)), sum) ([
			com(mov(i * cw), tfm) (i) for i in range(modules)
		])

	def lcuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
		return mirror('XZ', 'YZ') (
			box_fc((r + d) * 2, (r + d) * 2, l + c1, '+Z', r, c2)
			.translate((w / 2, h / 2, c2 - l / 2))
		)

	def ucuts(w: float, h: float, d: float, l: float, r: float) -> Workplane:
		return mirror('XZ', 'YZ') (
			box_fc(r * 2 + pl, (r + d) * 2, l + c1, '+Z', r, c2)
			.translate((w / 2, h / 2, c2 - l / 2))
		)

	def brick(wall: float, dir: float) -> Workplane:
		return dif([
			(
				box(w, h, t2)
				.edges('+Z').chamfer(crh)
				.edges('<Z').chamfer(c2)

				if dir > 0 else

				box(w, h, t2)
				.edges('+Z' if dir > 0 else '+Z or >Z')
				.chamfer(crh)
			),
			com(mov(0, 0, wall * dir), sum) ([
				box_fc(w - col, h - col * 2, t2, '|Z', ir, c2),
				module(lambda _: box_fc(
					(w - col) / modules - col, h - wt * 2, t2, '|Z', ir, c2
				)),
			]),
			module(lambda _: com(mirror('XZ'), mov(0, ch / 4, -t3 * dir)) (
				(cut := box_fc(cw - wt2, ch / 2 - wt2, 1 + pl, '|Z'))
				+ mov(z = wt * dir) (cut)
			)),
			mirror('YZ') (
				box_fc(wt * 2, h - col * 2, t2 + ir * 2, '|X', ir, c2)
				.translate((w / 2, 0, -wt * 2 - ir if dir != 1 else 0))
			),
		])

	def makeTop() -> Workplane:
		return dif([
			brick(wt, -1.0),
			module(lambda m: grid(ptn_map(
				lambda: cylinder(t2, 9.53 / 2 + 0.05),
				oder(ptn_top, potsPtn(m)),
				lambda: cylinder(t2, 6.35 / 2 + 0.05)
			))),
			holes(w / 2 - hol, h / 2 - hol, t2, m4xr),
			lcuts(w, h, hol, wt * 2, hol * s22).translate((0, 0, t3)),
			*([] if modules != 2 else [
				holes(0, h / 2 - hol, t2, m4xr),
				ucuts(0, h, hol, wt * 2, hol * s22).translate((0, 0, t3))
			]),
			*([] if modules != 3 else [
				holes(cw / 2, h / 2 - hol, t2, m4xr),
				ucuts(cw, h, hol, wt * 2, hol * s22).translate((0, 0, t3))
			]),
		])

	def makeBot() -> Workplane:
		return dif([
			brick(wt, 1.0),
			holes(w / 2 - hol, h / 2 - hol, t2, m4dr),
			mov(0, 0, -t3 / 2) (holes(w / 2 - hol, h / 2 - hol, t3, m4xr)),
			*([] if modules != 2 else [
				holes(0, h / 2 - hol, t2, m4dr),
				mov(z = -t3 / 2) (holes(0, h / 2 - hol, t3, m4xr)),
			]),
			*([] if modules != 3 else [
				holes(cw / 2, h / 2 - hol, t2, m4dr),
				mov(z = -t3 / 2) (holes(cw / 2, h / 2 - hol, t3, m4xr)),
			]),
			com(mirror('YZ'), mov((modules * 2 - 1) * inch, h / 2 - wt2, 1.25)) (
				com(roty(90), rotx(90)) (lemo0BCutout(wt))
			),
		])

	def threadCut(body: Workplane) -> Workplane:
		return com(rotz(180), mov((col / 2 - w) / 2, (col * 3 / 2 - h) / 2)) (
			sum([
				body - holes(w / 2 - hol, h / 2 - hol, t2, m4r),
				mov(w / 2 - hol, h / 2 - hol) (
					Workplane(thread('M4', t3, 'internal'))
				),
			])
			.intersect(mov(w / 2, h / 2) (wp.box(col, col * 3, t)))
		)

	def controls() -> Workplane:
		return module(lambda m: grid(ptns_map(
			(ptn_top, pomona1581),
			(potsPtn(m), bourns51),
			(tglsPtn(m), toggle),
			(ptn_all, clb300),
		))) \
		+ com(mirror('YZ'), mov((modules * 2 - 1) * inch, h / 2, 1.25 - t * 0.75)) (
			com(rotz(180), roty(90), rotx(90)) (lemoECG0B())
		)

	def extraLove() -> Workplane:
		return module(lambda i: grid(ptns_map(
			(potsPtn(i), knob),
		)))

	bot = makeBot()
	top = makeTop()
	cts = controls()
	xtr = extraLove()
	thd = threadCut(bot) if threads else None

	return [
		mov(z = -t3 - pl) (bot),
		mov(z = t3 + pl) (top),
		mov(z = t2 - 0.5) (cts),
		mov(z = t2 + 5) (xtr),
		*([] if thd is None else [thd]),
	]
