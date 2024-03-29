#!/usr/bin/env python
''' Tests for matrix functionality. '''
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

from decimal import Decimal

import py.test

from cas.matrices import *

def test_identity_matrix():
    assert identity_matrix(2) == Matrix([[1,0],[0,1]])
    assert identity_matrix(3) == Matrix([[1,0,0],[0,1,0],[0,0,1]])

def test_diagonal_matrix():
    assert diagonal_matrix(1,2) == Matrix([[1,0],[0,2]])
    assert diagonal_matrix(1,2,3) == Matrix([[1,0,0],[0,2,0],[0,0,3]])

class TestMatrix():
    def test_init(self):
        assert Matrix([[1,2],[4,5]]) is not None
        assert Matrix([[1,2,3],[4,5,6],[7,8,9]]) is not None
        assert Matrix([[1,2,4],[4,5,6]]) is not None
        assert Matrix([[1,2],[3,4],[5,6]]) is not None
        assert Matrix(2,2) is not None
        assert Matrix(3,3) is not None
        with py.test.raises(ValueError): Matrix([[1,2],[3]])
        with py.test.raises(ValueError): Matrix(-1,2)
        with py.test.raises(ValueError): Matrix(0,2)
        with py.test.raises(ValueError): Matrix([1,2],[3,4])

    def test_order(self):
        assert Matrix([[1,2,3],[4,5,6]]).order() == (2,3)
        assert Matrix([[1,2],[3,4],[5,6]]).order() == (3,2)
        assert Matrix([[1,2],[3,4]]).order() == (2,2)

    def test_equality(self):
        assert Matrix([[1,2],[3,4]]) == Matrix([[1,2],[3,4]])
        assert Matrix([[1,2],[3,4]]) != Matrix([[1,2],[4,3]])

    def test_addition(self):
        assert Matrix([[1,2],[3,4]]) + Matrix([[6,7],[8,9]]) == Matrix([[7,9],[11,13]])
        assert Matrix([[1,2],[3,4],[5,6]]) + Matrix([[2,3],[1,5],[3,4]])\
            == Matrix([[3,5],[4,9],[8,10]])
        assert Matrix([[2,1,7],[4,3,1],[2,4,9]]) + Matrix([[3,1,0],[-2,3,4],[8,2,1]])\
            == Matrix([[5,2,7],[2,6,5],[10,6,10]])
        with py.test.raises(TypeError):
            Matrix([[1,2],[3,4]]) + Matrix([[1,2],[4,5],[5,6]])

    def test_subtraction(self):
        assert Matrix([[2,7],[4,1]]) - Matrix([[1,2],[3,4]]) == Matrix([[1,5],[1,-3]])

    def test_negation(self):
        assert -Matrix([[1,2],[3,4]]) == Matrix([[-1,-2],[-3,-4]])

    def test_multiplication(self):
        assert 2*Matrix([[1,2],[3,4]]) == Matrix([[2,4],[6,8]])
        assert 5*Matrix([[1,3],[2,1],[4,7]]) == Matrix([[5,15],[10,5],[20,35]])
        assert Matrix([[1,2],[3,4]]) * Matrix([[5,6],[7,8]])\
            == Matrix([[19,22],[43,50]])
        assert Matrix([[1,2,3],[4,5,6],[7,8,9]])\
            * Matrix([[2,1,3],[1,2,6],[2,4,1]])\
            == Matrix([[10,17,18],[25,38,48],[40,59,78]])
        assert Matrix([[1,2,3],[4,5,6]]) * Matrix([[1,3],[2,4],[5,1]])\
            == Matrix([[20,14],[44,38]])
        assert Matrix([[4,2],[3,6],[1,4]]) * Matrix([[2,1],[3,6]])\
            == Matrix([[14,16],[24,39],[14,25]])
        assert Matrix([[-8,3,9],[2,4,-6]]) * Matrix([[3,-6,2],[4,6,-1],[1,-9,3]])\
            == Matrix([[-3,-15,8],[16,66,-18]])

    def test_minor(self):
        a = Matrix([[1,2,3],[4,5,6],[7,8,9]])
        assert a.minor(0,0) == Matrix([[5,6],[8,9]])
        assert a.minor(1,1) == Matrix([[1,3],[7,9]])
        assert a.minor(1,0) == Matrix([[2,3],[8,9]]) # TODO: check correct order
        b = Matrix([[1,2],[3,4]])
        assert b.minor(0,0) == Matrix([[4]])

    def test_determinant(self):
        assert Matrix([[1,2],[3,4]]).determinant() == -2
        assert Matrix([[1,3,5],[4,7,-2],[2,1,6]]).determinant() == -90
        with py.test.raises(ValueError): Matrix([[1,2],[3,4],[5,6]]).determinant()

    def test_adjugate(self):
        assert Matrix([[1,2],[3,4]]).adjgate() == Matrix([[4,-2],[-3,1]])
        assert Matrix([[1,2,3],[4,5,6],[7,8,9]]).adjgate()\
            == Matrix([[-3,6,-3],[6,-12,6],[-3,6,-3]])
        with py.test.raises(ValueError): Matrix([[1,2],[3,4],[5,6]]).adjgate()

    def test_inverse(self):
        I = Integer; D = Decimal
        assert Matrix([[I(1),I(2)],[I(3),I(4)]]).inverse()\
            == Matrix([[D(-2),D(1)],[D('1.5'), D('-0.5')]])
        assert Matrix([[I(1),I(3),I(2)],[I(1),I(2),I(1)],[I(3),I(1),I(2)]]).inverse()\
            == Matrix([[D('-0.75'),D(1),D('0.25')],[D('-0.25'),D(1),D('-0.25')],
                [D('1.25'),D(-2),D('0.25')]])
        with py.test.raises(ValueError):
            Matrix([[1,2,3],[4,5,6],[7,8,9]]).inverse()

    def test_charactoristic_polynomial(self):
        from cas.core import Symbol
        x = Symbol('x')
        assert Matrix([[1,2],[3,4]]).characteristic_polynomial()\
            == x**2 - 5*x - 2
        print Matrix([[1,3,2],[4,5,2],[2,3,1]]).characteristic_polynomial()
        assert Matrix([[1,3,2],[4,5,2],[2,3,1]]).characteristic_polynomial()\
            == -x**3 + 7*x**2 + 11*x + 3

    def test_eigenvalues(self):
        xs = (5.372, -0.372)
        for a, b in zip(Matrix([[1,2],[3,4]]).eigenvalues(), xs):
            assert abs(a - b) < a.__class__('0.001')

    def test_transpose(self):
        assert Matrix([[1,2],[3,4]]).transpose() == Matrix([[1,3],[2,4]])
        assert Matrix([[1,2],[3,4],[5,6]]).transpose() == Matrix([[1,3,5],[2,4,6]])
        assert Matrix([[1,2,3],[4,5,6]]).transpose() == Matrix([[1,4],[2,5],[3,6]])
        assert Matrix([[1,2,3]]).transpose() == Matrix([[1],[2],[3]])
        assert Matrix([[1,2,3],[4,5,6],[7,8,9]]).transpose()\
            == Matrix([[1,4,7],[2,5,8],[3,6,9]])

    def test_LU_decomposition(self):
        from cas.core import Product
        assert Matrix([[1,2],[3,4]]).LU_decomposition()\
            == Product(Matrix([[1,0],[3,1]]), Matrix([[1,2],[0,-2]]))
        assert Matrix([[1,2,3],[4,5,6],[7,8,9]]).LU_decomposition()\
            == Product(Matrix([[1,0,0],[4,1,0],[7,2,1]]),
                Matrix([[1,2,3],[0,-3,-6],[0,0,0]]))

