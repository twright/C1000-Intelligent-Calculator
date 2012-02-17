#!/usr/bin/env python
''' Test the accuracy of numerical methods. '''
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

from math import *

import py.test

from cas.numerical_methods import *

def almost_equal(a, b, percentage=1):
    return 100 * abs( (a - b) / b if b != 0 else a - b ) <= percentage
    
class TestNumericalRoots():
    def setup_class(self):
        self.data = (
            (lambda x: x**2 - x - 6, 2), (lambda x: x**2 - 1, 2),
            (lambda x: x**2 + 1, 2), (lambda x: x, 1),
            (lambda x: x**2 - (3/4)*x + 7/9, 2),
            (lambda x: x**3 - 3*x**2 + (1/7)*x - 5, 3)
        )
    
    def test_durand_kerner(self):
        for f, order in self.data:
            xs = durand_kerner_roots(f, order)
            for x in xs:
                assert almost_equal(f(x), 0)

class TestNumericalIntegration():
    def setup_class(self):
        self.data = (
            (lambda x: x**2 - x, 1, 3, 14/3),
            (lambda x: x**8 - 2*x**5 + x, 2, 8, 14825694),
            (lambda x: 3.4*x**3 + 2.3*x, 2, 5, 541.8),
            (lambda x: 4*x**2 - 0.1*x, 0.4, 4.8, 146.226666666667),
            (lambda x: 8*x - 1, -2, 4, 42),
            (lambda x: 9*x**3 - 2*x, 2, -4, 528),
            (lambda x: (x**8 - 3*x**6 - 2*x) / (7*x**4 - 2), 1, 3, 3.05245021),
            (lambda x: x**2 * log(x), 2, 4, 21.503665000),
        #    (lambda x: x**4 * cos(2*x), -pi, pi, None),
        )

    def test_romberg(self):
        for f, a, b, integral in self.data:
            assert almost_equal(romberg_integral(f, a, b, 7, 4),
                integral, 0.0000005)

    def test_trapezoid_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(trapezoidal_composite_integral(f, a, b),
                integral, 1)

    def test_simpson_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(simpson_composite_integral(f, a, b, 100),
                integral, 1)

    def test_simpson38_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(simpson38_composite_integral(f, a, b),
                integral, 1)

    @py.test.mark.xfail
    def test_boyle_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(boyle_composite_integral(f, a, b),
                integral, 1)