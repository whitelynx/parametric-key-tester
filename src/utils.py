from collections.abc import Sequence
from math import pi, cos

from solid import *
from solid.utils import *


def cylinder_outer(r, h, segments=16, center=False):
   fudge = 1 / cos(pi / segments)
   adjusted_r = [ri * fudge for ri in r] if isinstance(r, Sequence) else r * fudge

   return cylinder(h=h, r=adjusted_r, segments=segments, center=center)
