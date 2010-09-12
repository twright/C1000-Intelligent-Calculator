#!/usr/bin/env python3.1
''' Tests for univariate functions. '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from decimal import Decimal, localcontext

import py.test

from ..core import Integer
import cas.multivariate as ce
from ..univariate import *

class TestFunction():
    def test_init(self):
        assert Function('x') != None
        assert Function('t') != None
        with py.test.raises(Exception): Function('xy')
        with py.test.raises(Exception): Function('')
        with py.test.raises(Exception): Function()

class TestPolynomial():
    def setup_method(self, method):
        self.y = Polynomial('x', 1,1, 2,3, 4,5)
        self.z = Polynomial('t')

    def test_init(self):
        assert Polynomial('x') != None
        assert Polynomial('t') != None
        assert Polynomial('x', 1,2, 3,4) != None
        with py.test.raises(Exception): Polynomial()
        with py.test.raises(Exception): Polynomial('')
        with py.test.raises(Exception): Polynomial('xy')
        with py.test.raises(Exception): Polynomial('x', 1)

    def test_limit(self):
        assert self.y.integral().limit(1,2) == Decimal('51.0')

    def test_evaluate(self):
        vals = (
            (3, 1029), (0, 0), (1, 7), (0.1, Decimal('0.10204')), (-4, -4228)
        )
        for a, b in vals:
            assert self.y.evaluate(a) == b

    def test_differential(self):
        # TODO: Test should directly test equality once possible
        assert str(self.y.differential()) == '20x^4 + 6x^2 + 1'

    def test_integral(self):
        with localcontext():
            getcontext().prec = 3
            assert str(self.y.integral()) == '0.667x^6 + 0.5x^4 + 0.5x^2 + c'

    def test_append(self):
        self.y.append(3.141, 666)
        with localcontext():
            getcontext().prec = 3
            assert str(self.y) == '3.14x^666 + 4x^5 + 2x^3 + x'

    def test_str(self):
        P = Polynomial
        vals = (
            (P('x', 1,0), '1'),
            (P('x', 1,1), 'x'),
            (P('x', -1,0), '-1'),
            (P('x', -1,1), '-x'),
            (P('t', 3,2, -1,1), '3t^2 - t'),
            (P('x', 3.2,4, 4.6,2, -2,0), '3.2x^4 + 4.6x^2 - 2'),
            (P('x', -2,5, 2,4, -1,3, 2.1,2, -2,1, 0.1,0),
                '-2x^5 + 2x^4 - x^3 + 2.1x^2 - 2x + 0.1'),
            (P('x', -2,3, 56,4), '56x^4 - 2x^3'),
        )

        for poly, string in vals:
            assert str(poly) == string

    def test_simplify(self):
        P = Polynomial
        vals = (
            (P('x', 2,1, 4,1, 2,2), P('x', 2,2, 6,1)),
            (P('x', 3,5, 2,5, 1.1,5, 2,2, 6,5, 3,2), P('x', 12.1,5, 5,2)),
        )

        for a, b in vals:
            assert str(a.simplify()) == str(b.simplify())
            assert a == b

    def test_equality(self):
        P = Polynomial
        equal = (
            (P('x', 1,2), P('x', 1,2)),
            (P('x', 1,2, 3,4), P('x', 3,4, 1,2)),
            (P('x', 1,2, 2,2), P('x', 3,2)),
            (P('x', 1,2, 3,4, 5,6), P('x', 1,2, 3,4, 5,6)),
            (P('x', 1,2, 3,4, 5,6), P('x', 1,2, 5,6, 3,4)),
            (P('x', 0,3), P('x', 0,2)),
            (P('x', 1,0), 1),
        )
        notequal = (
            (P('x', 1,1), P('x', 1,2)),
            (P('y', 1,2), P('x', 1,2))
        )

        for a, b in equal:
            assert a == b
        for a, b in notequal:
            assert a != b

    def test_as_gnuplot_expression(self):
        assert self.y.as_gnuplot_expression() == '4*x**5 + 2*x**3 + x'
        assert Polynomial('t', 2,3).as_gnuplot_expression() == '2*x**3'

    def test_addition(self):
        P = Polynomial
        assert P('x', 1,2) + P('x', 3,4) == P('x', 1,2, 3,4)
        assert P('x', 1,5, 3,4) + P('x', 0.1,5, 2,3) == P('x', 2,3, 3,4, 1.1,5)
        assert P('x', 1,2, 3,4) + Integer(5) == P('x', 3,4, 1,2, 5,0)
        assert P('x', 1,2, 3,4) + Decimal('4.2') == P('x', 3,4, 1,2, 4.2,0)

    def test_subtraction(self):
        P = Polynomial
        assert P('x', 1,2) - P('x', 3,4) == P('x', -3,4, 1,2)
        assert P('x', 1,5, 3,4) - P('x', 0.1,5, 2,3) == P('x', 0.9,5, 3,4, -2,3)

    def test_multiplication(self):
        P = Polynomial
        assert Integer(3) * P('x', 1,4, -2,2, 0.5,1, -0.7,0)\
            == P('x', 3,4, -6,2, 1.5,1, -2.1,0)
        assert Decimal('3.1') * P('x', 1,4, -2,2, 0.5,1, -0.7,0)\
            == P('x', 3.1,4, -6.2,2, 1.55,1, -2.17,0)
        assert Term(3,'x',1) * P('x', 1,4, -2,2, 0.5,1, -0.7,0)\
            == P('x', 3,5, -6,3, 1.5,2, -2.1,1)
        assert P('x', 3,1, -2.1,0) * P('x', -2,1, 4,0)\
            == P('x', -6,2, 16.2,1, -8.4,0)

    def test_order(self):
        P = Polynomial
        assert P('x', 1,3, -2,1, 1,0).order() == 3
        assert P('x', 2,1, -4,5, -3,0).order() == 5
        assert P('x', 1,0, -1,4).order() == 4
        assert P('x', 1,0).order() == 0
        assert P('x', 1,1, -2,0).order() == 1

    @py.test.mark.xfail # fails due to gaps in simplification
    def test_division(self):
        # Taken for q5 of question paper
        P = Polynomial
        assert P('x', 1,2, 4,1, 3,0) / P('x', 1,1, 1,0) == P('x', 1,1, 3,0)
        assert P('x', 1,2, -25,0) / P('x', 1,1, -5,0) == P('x', 1,1, 5,0)
        assert P('x', 1,2, -1,1, -6,0) / P('x', 1,2, 1,1, -12,0)\
            == P('x', 1,1, 2,0) / P('x', 1,1, 4,0)
    #    assert P('x', 1,1, 4,0)**6 * P('x', 1,1, 1,0) / P('x', 1,2, 5,1, 4,0)\
    #        == P('x', 1,1, 4,0)**5
        assert P('x', 2,1, 6,0) * P('x', 3,2, 8,1, -3,0) / P('x', 3,1, -1,0)\
            == 2 * P('x', 1,1, 3,0)**2
        assert (P('x', 4,1, 8,0) / 3) / (P('x', 1,2, -3,1, -10,0) / 4)\
            == 16 / (3 * P('x', 1,1, -5,0))

class TestTerm():
    def setup_method(self, method):
        T = Term
        self.sample = (
            (T(4,'x',3), '4x^3'), (T(4,'x',-3), '4x^-3'), (T(-4,'x',3), '-4x^3'),
            (T(0,'x',3), '0'), (T(7,'x',0), '7'), (T(7,'x',1), '7x'),
            (T(1,'x',1), 'x'), (T(2,'t',3), '2t^3'), (T(1,'x',0), '1'),
        )

    def test_init(self):
        # TODO: Sort out handling of non-Nononomials
        assert Term(2,'x',3) != None
        assert Term(-2,'t',3) != None
        assert Term(1.3,'x',2) != None
        assert Term(2+3j,'x',2) != None
        with py.test.raises(TypeError): Term()
        with py.test.raises(TypeError): Term(2,'x')

    def test_repr(self):
        assert repr(Term(1,'x', 4)) == "Term(1, 'x', 4)"

    def test_neg(self):
        assert -Term(3,'x',3) == Term(-3,'x',3)

    def test_str(self):
        for term, string in self.sample:
            assert str(term) == string

    def test_calculus(self):
        for f, string in self.sample:
            assert f.differential().integral() == f
            assert f.integral().differential() == f

class TestFraction():
    def test_init(self):
        assert Fraction('x', Polynomial('x', 2,3, 1,0),
            Polynomial('x', 4,3, 2,2, 1,1)) != None
        assert Fraction('x', Integer(1), Polynomial('x', 2,3, 4,0)) != None
        assert Fraction('t', Polynomial('t', 2,2, 4,3), Term(2,'t',4)) != None

    # TODO: Add new tests for different datatypes and non-bracketed types
    def test_str(self):
        F, P, T, I, D = Fraction, Polynomial, Term, Integer, Decimal
        sample = (
            (F('x', P('x', 1,1, 1,0), P('x', 1,1, -1,0)), '(x + 1) / (x - 1)'),
            (F('t', P('t', 4,3, 2,1, -5,0), P('t', 2,3, -4,0)), '(4t^3 + 2t - 5) / (2t^3 - 4)'),
        )
        for fraction, string in sample:
            assert str(fraction) == string

#    def test_mul(self):
#        F, P, T, I, D = Fraction, Polynomial, Term, Integer, Decimal

class TestProduct():
    def setup_method(self, method):
        self.A = Polynomial('x', 3,2, 1,1, -2,0)
        self.B = Polynomial('x', 2,4, 7,0)
        self.C = Term(2,'x',5)
        
    def test_init(self):
        assert Product('x', self.A, self.B) != None
        assert Product('x', self.A, self.B, self.C) != None
        
    def test_str(self):
        # TODO: Change when some guarentee of order is added
        assert str(Product('x', self.A, self.B)) == '(3x^2 + x - 2) * (2x^4 + 7)'
        print(Product('x', self.A, self.B, self.C))
        assert str(Product('x', self.A, self.B, self.C))\
            == '(3x^2 + x - 2) * (2x^4 + 7) * 2x^5'
        assert str(Product('x', self.A, self.B, Polynomial('x')._convert_other(self.C)))\
            == '(3x^2 + x - 2) * (2x^4 + 7) * 2x^5'
