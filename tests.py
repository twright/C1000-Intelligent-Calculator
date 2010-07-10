#!/usr/bin/env python3.1
from cas import *
from ntypes import *
from decimal import Decimal
import unittest

class Function(unittest.TestCase):
    y = polynomial('x',1,1,2,3,4,5)
    def test_limit(self):
        self.assertEqual(self.y.integral().limit(1,2), Decimal('51.0'))

class Polynomial(unittest.TestCase):
    y = polynomial('x',1,1,2,3,4,5)  
    def test_evaluate(self):
        ''' Evaluate works for sample values '''
        xys = ((3,'1029'),(0,'0'),(1,'7'),(.1,'0.102'),(-4,'-4228'))
        for a, b in xys:
            self.assertEqual(str(self.y.evaluate(a)), b)
    def test_differential(self):
        self.assertEqual(str(self.y.differential()), '1 + 6*x^2 + 20*x^4')
    def test_integral(self): 
        self.assertEqual(str(self.y.integral()),'0.5*x^2 + 0.5*x^4 + 0.667*x^6 + c')


class Term(unittest.TestCase):
    vals = (
    (4,5.57,'4*t^5.57'),
    (4.45345,5.57,'4.45*t^5.57'),
    (4,3,'4*t^3'),
    (4,-3,'4*t^-3'),
    (-4,3,'-4*t^3'),
    (0,-3,''),
    (7,0,'7'),
    (7,1,'7*t'),
    (1,1,'t'),
    (1,0,'1'),
    (1000000000000000000000000000000,1111111111111111111111111,'1000000000000000000000000000000*t^1111111111111111111111111')
    )
    def test_str(self):
        for a,b,string in self.vals:
            self.assertEqual(str(term(a,'t',b)), string) # a*x^b
    def test_calculus(self):
        for a,b,c in self.vals:
            self.assertEqual(term(a,'t',b).differential().integral(), term(a,'t',b))
    def test_sign(self):
        for a,b,c in self.vals:
            y = term(a,'x',b)
            if a == 0: self.assertEqual(y.sign(), 0)
            elif a > 0: self.assertEqual(y.sign(), 1)
            elif a < 0: self.assertEqual(y.sign(), -1)

class Constant(unittest.TestCase):
    def test_equality(self):
        vals = (2, Decimal('5.6'), -2, 0, Decimal('Inf'))
        for x in vals:
            self.assertEqual(x, constant())

class NInt(unittest.TestCase):
    vals = [(3,4,Decimal('0.75')),(8,4,2)]
    def test_divisions(self):
        for a,b,c in self.vals:
            self.assertEqual(nint(a) / nint(b), c)

if __name__ == '__main__':
    unittest.main()
