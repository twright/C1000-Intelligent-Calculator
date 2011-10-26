#!/usr/bin/env python

from functools import partial
try:
    from .sorting_c import schwartzian_transform, mergesort
except:
    pass

sort = partial(schwartzian_transform, f=mergesort)
