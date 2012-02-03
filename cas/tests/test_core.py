#!/usr/bin/env python
''' Tests for the core funcitonality of the cas. '''
from __future__ import division
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import py.test
from decimal import Decimal

from cas.core import *
from cas.numeric import Integer
from cas.core import handle_type as ht


class TestHandleType():

    def test_int(self):
        xs = [0, 1, -1, 2, 1000, 34, '34']
        for x in xs:
            assert isinstance(handle_type(x), Integer)

    def test_decimal(self):
        xs = [34.2, 0.2, '3.4', 4/5, 3.4+0j, 3+0j]
        for x in xs:
            assert isinstance(handle_type(x), Decimal)

    def test_complex(self):
        xs = [1j, 2j, -1j, 2+3j, 3-2.2j]
        for x in xs:
            assert isinstance(handle_type(x), complex)


class TestExpand():

    def setup_class(self):
        self.x = Symbol('x')

    def test_products(self):
        data = [[self.x*(1 + self.x), 'x^2 + x'],
            [(self.x + 1)*self.x, 'x^2 + x'],
            [(self.x + 1)*(self.x - 1), 'x^2 - 1'],
            [Sin(self.x)*(1 + Sin(self.x)), 'sin(x) + sin(x)^2'],
            [self.x*self.x*self.x, 'x^3'],
            [Sin(self.x)*Sin(self.x)*Sin(self.x), 'sin(x)^3']]
        for y, s in data:
            assert str(expand(y)) == s

    def test_sums(self):
        data = [[self.x + self.x*(self.x + 1) + 7, 'x^2 + 2x + 7']]
        for y, s in data:
            assert str(expand(y)) == s


class TestIsPoly():

    def setup_class(self):
        self.x = Symbol('x')

    def test_polynomials(self):
        xs = [1, self.x, 3*self.x, self.x**2, 3*self.x**3,
            4*self.x**3 - 2*self.x**2 + self.x - 7]
        for x in xs:
            assert is_poly(x)

    def test_non_polynomials(self):
        # TODO: Add more test cases for this
        xs = [Sin(self.x), Cos(self.x), Tan(self.x), Ln(self.x)]
        for x in xs:
            assert not is_poly(x)


class TestPartialDifferential():

    def setup_class(self):
        self.x = Symbol('x')

    def test_polynomials(self):
        data = [[1, '0'], [self.x, '1'], [self.x**5, '5x^4'],
            [self.x**2 - 2*self.x - 2, '2x - 2']]
        for y, s in data:
            assert str(partial_differential(y, self.x)) == s

    def test_functions(self):
        # TODO: Support for d(tan x)/dx = sec(x)^2 etc.
        data = [[Sin(self.x), 'cos(x)'], [Cos(self.x), '-sin(x)'],
            [Ln(self.x), 'x^-1']]
        for y, s in data:
            assert str(partial_differential(y, self.x)) == s

    def test_rules(self):
        data = [[(self.x**2 + 3)**(ht(1)/ht(2)), 'x(x^2 + 3)^(-1/2)']]
        for y, s in data:
            print y, partial_differential(y, self.x), s
            assert str(partial_differential(y, self.x)) == s

    def test_products(self):
        data = [[self.x * Cos(self.x) * Sin(self.x),
            '-xsin(x)sin(x) + xcos(x)^2 + cos(x)sin(x)']]
        for y, s in data:
            print y, partial_differential(y, self.x), s
            assert str(partial_differential(y, self.x)) == s


class TestPartialIntegral():

    def setup_class(self):
        self.x = Symbol('x')

    def test_polynomials(self):
        data = [[1, 'x + c'], [self.x, '(1/2)x^2 + c'],
            [2*self.x**5, '(1/3)x^6 + c'],
            [self.x**2 - 2*self.x - 2, '(1/3)x^3 - x^2 - 2x + c']]
        for y, s in data:
            assert str(partial_integral(y, self.x)) == s

    def test_functions(self):
        data = [[Sin(self.x), '-cos(x) + c'], [Cos(self.x), 'sin(x) + c'],
            [1/self.x, 'ln(x) + c']]
        for y, s in data:
            assert str(partial_integral(y, self.x)) == s


class TestAlgebra():

    def setup_class(self):
        self.a = Algebra()

    def test_addition(self):
        assert self.a + 0 == self.a

    def test_subtraction(self):
        assert self.a - 0 == self.a

    def test_multiplication(self):
        assert self.a * 0 == 0
        assert 0 * self.a == 0
        assert self.a * 1 == self.a
        assert 1 * self.a == self.a

    def test_division(self):
        assert self.a / 1 == self.a
        assert 0 / self.a == 0

    def test_powers(self):
        assert self.a ** 0 == 1
        assert self.a ** 1 == self.a


class TestSymbol():

    def setup_class(self):
        self.x, self.y, self.z = Symbol('x'), Symbol('y'), Symbol('z')

    def test_str(self):
        assert str(self.x) == 'x'
        assert str(self.y) == 'y'
        assert str(self.z) == 'z'

    def test_call(self):
        assert self.x(3) == 3
        assert str(self.y(4)) == '4'
        assert self.y(4, self.y) == 4

    def test_equality(self):
        assert self.x == self.x == Symbol('x')
        assert self.x != self.y
        assert self.y != self.z

    def test_multiplication(self):
        assert str(self.x * self.y) == 'xy' == str(self.y * self.x)
        assert str(self.x * self.x) == 'x^2'

    def test_division(self):
        assert self.x / self.x == 1
        assert str(self.y / self.x) == 'y/x'


# TODO: Add some tests for dedup


class TestProduct():

    def setup_class(self):
        self.x = Symbol('x')
        self.a, self.b, self.c, self.d = Symbol('a'), Symbol('b'),\
            Symbol('c'), Symbol('d')
        self.xs = Product(self.a, self.b, self.c, self.d)

    def test_equality(self):
        assert Product(2, 3) == Product(2, 3)
        assert Product(2, 3) == Product(3, 2)
        assert Product(3, 7) == 21
        assert Product(self.a,self.c) == Product(self.a,self.c)
        assert Product(self.b,self.d) == Product(self.d,self.b)

    def test_str(self):
        assert str(Product(2, self.a, self.b, self.c, self.d)) == '2abcd'

    def test_call(self):
        assert (2 * self.x)(3) == 6
        assert self.xs(5, self.c) == 5 * self.a * self.b * self.d
        assert self.xs(3, self.c)(5, self.d) == 15 * self.a * self.b

    def test_iteration(self):
        assert self.xs[1] == self.b
        for x in self.xs: assert x is not None
        assert len(self.xs) == 4

    def test_multiplication(self):
        assert (self.a * self.b) * (self.c * self.d) == self.xs
        assert (2*self.x) * (6*self.x) == 12*self.x**2

    def test_addition(self):
        assert 2*self.x + 5*self.x == 7*self.x
        s = Sin(self.x)
        print(list((2*s + (self.x + 3)*s)[0]))
        assert str(2*s + (self.x + 3)*s) == '(x + 5)sin(x)'


class TestFunctions(object):

    def setup_class(self):
        self.x = Symbol('x')

    def test_equality(self):
        assert Sin(self.x) == Sin(self.x)

# TODO: Insert tests for Functions, Sums, Powers and Fractions here.


class TestList():

    def test_str(self):
        assert str(List(1, 2, 3, 4)) == '1, 2, 3, 4'
        print(str(List(1, 2+0j, 0+5j, 3-4j)))
        assert str(List(1, 2+0j, 0+5j, 3-4j)) == '1, 2, 5i, 3-4i'


class TestStrWithHtml():

    def test_init(self):
        assert StrWithHtml('test', '<b>test</b>') is not None

    def test_str(self):
        assert str(StrWithHtml('test', '<b>test</b>')) == 'test'

