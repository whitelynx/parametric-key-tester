from collections.abc import Sequence
from math import pi, cos

from solid2 import cube, cylinder


def cylinder_outer(r, h, segments=16, center=False):
    fudge = 1 / cos(pi / segments)
    adjusted_r = [ri * fudge for ri in r] if isinstance(r, Sequence) else r * fudge

    return cylinder(h=h, r=adjusted_r, segments=segments, center=center)


nothing = cube((1, 1, 1), center=True) - cube((2, 2, 2), center=True)


def optional(condition):
    return lambda part: part if condition else nothing
