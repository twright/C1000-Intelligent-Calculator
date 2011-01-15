#!/usr/bin/env python3.1
''' Test the accuracy of numerical methods. '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from math import *

import py.test

from cas.numerical_methods import *

def almost_equal(a, b, percentage=1):
    return 100 * abs( (a - b) / b ) <= percentage

class TestNumericalMethods():
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

    @py.test.mark.xfail
    def test_simpson38_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(simpson38_composite_integral(f, a, b),
                integral, 10)

    @py.test.mark.xfail
    def test_boyle_rule(self):
        for f, a, b, integral in self.data:
            assert almost_equal(boyle_composite_integral(f, a, b),
                integral, 10)

