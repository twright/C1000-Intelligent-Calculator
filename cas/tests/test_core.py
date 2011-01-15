#!/usr/bin/env python3.1
''' Tests for the core funcitonality of the cas. '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import py.test
from decimal import Decimal, getcontext, localcontext

from cas.core import *
from cas.numeric import Integer

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

class TestIsPoly():
    def setup_class(self):
        self.x = Symbol('x')

    def test_polynomials(self):
        xs = [1, self.x, 3*self.x, self.x**2, 3*self.x**3,
            4*self.x**3 - 2*self.x**2 + self.x - 7]
        for x in xs: assert is_poly(x)

    def test_non_polynomials(self):
        xs = [Sin(self.x), Cos(self.x), Tan(self.x), Ln(self.x)]
        for x in xs: assert not is_poly(x)

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

class TestProduct():
    def setup_class(self):
        self.a, self.b, self.c, self.d = Symbol('a'), Symbol('b'), Symbol('c'),\
            Symbol('d')
        self.xs = Product(self.a, self.b, self.c, self.d)

    def test_equality(self):
        assert Product(2, 3) == Product(2, 3)
        assert Product(2, 3) == Product(3, 2)
        assert Product(3, 7) == 21
        assert Product(self.a,self.c) == Product(self.a,self.c)
        assert Product(self.b,self.d) == Product(self.d,self.b)

    def test_str(self):
        assert str(Product(2, self.a, self.b, self.c, self.d)) == '2abcd'

    def test_iteration(self):
        assert self.xs[1] == self.b
        for x in self.xs: assert x is not None
        assert len(self.xs) == 4

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

