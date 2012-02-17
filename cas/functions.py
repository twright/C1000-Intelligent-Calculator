#!/usr/bin/env python
''' Various abstract methods and functions '''
from __future__ import division
__author__ = 'Tom Wright <tom.tdw@gmail.com>'
# Copyright 2012 Thomas Wright <tom.tdw@gmail.com>
# This file is part of C1000 Intelligent Calculator.
#
# C1000 Intelligent Calculator is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# C1000 Intelligent Calculator is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# C1000 Intelligent Calculator.  If not, see <http://www.gnu.org/licenses/>.

def gcd(a, b):
    ''' A recursive implementation of the euclidean greatest common divisor
    algorithm. '''
    def _gcd_div(a, b):
        return a if b == 1 else _gcd_div(b, a % b)

    def _gcd_sub(a, b):
        if a == 0: return b
        while b != 0:
            if a > b: a = a - b
            else: b = b - a
        return a

    if isinstance(a, int) and isinstance(b, int):
        return _gcd_div(a, b)
    else:
        return _gcd_sub(a, b)

if __name__ == '__main__':
    from cas.core import Symbol
    x = Symbol('x')
    print (gcd(6*x, 5*x))

