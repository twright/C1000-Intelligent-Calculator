#!/usr/bin/env python3.1
''' Tests for the core funcitonality of the cas. '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import py.test
from decimal import Decimal, getcontext

from cas.core import *

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
            
class TestPrintComplex():
    def setup_class(self):
        getcontext().prec = 3

    def test_samples(self):
        xs = (
            (0+0j, '0'), (0.00001+0j, '0'), (-0.00001+0j, '0'), (1+0j, '1'),
            (1.342+0j, '1.34'), (1-0.01j, '1-0.0100i'), (4.3+0.00003j, '4.30'),
            (0-2j, '-2i'), (0.00003+0.00002j, '0'), (0.00002-0.00001j, '0'),
            (4.5+0.00002j, '4.5'), (0.00003-0.2j, '-0.200i')
        )
        for x, string in xs:
            assert print_complex(x) == string
            
class TestConstant():
    def setup_class(self):
        self.c = Constant()
        
    @py.test.mark.xfail
    def test_equality(self):
        from cas.univariate import Term
        equals = (Integer(0), Integer(-1), Decimal('3.4'), 3+4j, Term(1,'x',0))
        notequals = (Term(1,'x',1),)
        for x in equals:
            assert self.c == x
        for x in notequals:
            assert self.c != x
            
    @py.test.mark.xfail
    def test_str(self):
        assert str(self.c) == 'c'
        assert repr(self.c) == 'Constant()'
        
    @py.test.mark.xfail
    def test_subtraction(self):
        assert 3 - self.c == 0
        assert self.c - self.c == 0
        
    def test_evaluation(self):
        assert self.c.evaluate(3) == 0
        assert self.c.evaluate(Decimal('3.4')) == 0
        
    def test_differential(self):
        assert self.c.differential() == 0
        
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
            assert x == Integer(x).factors().simplify()
            assert Integer(x).factors() == Product(*facts)
            
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
    def test_equality(self):
        assert Product(2, 3) == Product(2, 3)
        assert Product(2, 3) == Product(3, 2)
        assert Product(3, 7) == 21
        
    def test_str(self):
        assert str(Product(1, 2, 3, 4)) == '1*2*3*4'
        
    def test_simplify(self):
        assert Product(1, 2, 3, 4).simplify() == 24
        
    def test_iteration(self):
        xs = Product(1, 2, 3, 4)
        assert xs[1] == 2
        for x in xs: assert x is not None
        assert len(xs) == 4
        
class TestList():
    def test_str(self):
        assert str(List(1, 2, 3, 4)) == '1, 2, 3, 4'
        assert str(List(1, 2+0j, 0+5j, 3-4j)) == '1, 2, 5i, 3-4i'
        
class TestStrWithHtml():
    def test_init(self):
        assert StrWithHtml('test', '<b>test</b>') is not None
        
    def test_str(self):
        assert str(StrWithHtml('test', '<b>test</b>')) == 'test'
