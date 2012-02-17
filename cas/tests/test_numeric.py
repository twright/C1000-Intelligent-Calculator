#!/usr/bin/env python
''' Tests for the core funcitonality of the cas. '''
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

import py.test
from decimal import Decimal, getcontext, localcontext
from functools import reduce
from operator import mul

from cas.numeric import *

class TestComplex():
    def test_str(self):
        xs = (
            (0+0j, '0'), (0.00001+0j, '0'), (-0.00001+0j, '0'), (1+0j, '1'),
            (1.342+0j, '1.34'), (1-0.01j, '1-0.01i'), (4.3+0.000003j, '43/10'),
            (0-2j, '-2i'), (0.000003+0.000002j, '0'), (0.000002-0.000001j, '0'),
            (4.5+0.000002j, '9/2'), (0.000003-0.2j, '-(1/5)i')
        )
        with localcontext():
            getcontext().prec = 3
            for x, string in xs:
                assert str(Complex(x)) == string

    def test_addition(self):
        # TODO: Update/change
        assert isinstance(Complex(3+2j) + Complex(-1+5j), Complex)
        
    # TODO: Add some more tests for complex numbers

class TestInteger():
    def test_init(self):
        assert Integer(3) == 3

    def test_division(self):
        assert Integer(4) / Integer(2) == Integer(2)
        assert Integer(3) / Integer(2) == Decimal('1.5')
        assert abs(Integer(2) / Decimal('1.1') - Decimal('1.82'))\
            < Decimal('0.01')
        with py.test.raises(ZeroDivisionError):
            Integer(3) / Integer(0)

    def test_addition(self):
        assert isinstance(Integer(3) + Integer(2), Integer)
        assert isinstance(Integer(3) + 2, Integer)
        assert Integer(3) + Integer(2) == 5
        assert Integer(2) + Decimal('0.01') == Decimal('2.01')

    def test_subtraction(self):
        assert isinstance(Integer(3) - Integer(2), Integer)
        assert isinstance(Integer(3) - 2, Integer)
        assert isinstance(3 - Integer(2), Integer)
        assert 3 - Integer(2) == 1
        assert Integer(3) - Integer(2) == 1
        assert Integer(2) - Decimal('0.01') == Decimal('1.99')

    def test_powers(self):
        assert isinstance(Integer(2) ** Integer(4), Integer)
        assert Integer(2) ** Integer(4) == 16
        assert Integer(4) ** Decimal('0.5') == Decimal('2')

    def test_multiplication(self):
        assert isinstance(Integer(3) * Integer(2), Integer)
        assert isinstance(Integer(3) * 2, Integer)
        assert isinstance(2 * Integer(3), Integer)
        assert Integer(3) * Integer(2) == 6

    def test_factors(self):
        xs = (
            (2, [2]), (4, [2,2]), (10, [2,5]), (-10, [-1,2,5]),
        )
        for x, facts in xs:
            assert list(Integer(x).factors()) == facts
            assert x == reduce(mul, facts, 1)
