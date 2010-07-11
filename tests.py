#!/usr/bin/env python3
from cas import *
from ntypes import *
from decimal import Decimal
import unittest
import parser
from calculator import *

class Parsing(unittest.TestCase):
    polys = ['3x^3 - 5', '18x^7 - 2.7x', '18x^7 - 2.7x',
        'x^5 + 6x^3 - x', 'x^7 + 2.5x^4 + 1', 'x^3 - 2x^2 - 24x - 30']
    def test_polys(self):
        ''' Once parsed, each polynomial is converted to a string and
        compareed with the input '''
        for a in self.polys:
            self.assertEqual(a, str(parser.parsePoly(a)))

class HandlingTypes(unittest.TestCase):
    vals = [(3.4,Decimal), (1,nint), ('3.4',Decimal), ('4',nint)]
    def test_handle_type(self):
        for a, b in self.vals:
            self.assertEqual(type(handle_type(a)), b)

class Functions(unittest.TestCase):
    y = Polynomial('x',1,1,2,3,4,5)

    def test_limit(self):
        ''' Tests that functions can correctly be limited between 2 values '''
        self.assertEqual(self.y.integral().limit(1,2), Decimal('51.0'))


class Polynomials(unittest.TestCase):
    y = Polynomial('x',1,1,2,3,4,5)
      
    def test_evaluate(self):
        ''' Evaluate works for sample values '''
        xys = ((3,'1029'),(0,'0'),(1,'7'),(.1,'0.102'),(-4,'-4228'))
        for a, b in xys:
            self.assertEqual(str(self.y.evaluate(a)), b)

    def test_differential(self):
        ''' Tests polynomials can be correctly differentiated '''
        self.assertEqual(str(self.y.differential()), '1 + 6x^2 + 20x^4')
        
    def test_integral(self):
        ''' Tests polynomials can be correctly integrated '''
        self.assertEqual(str(self.y.integral()),
            '0.5x^2 + 0.5x^4 + 0.667x^6 + c')

    def test_append(self):
        ''' Tests elements can be appended to functions '''
        import copy
        z = copy.deepcopy(self.y); z.append(3.141, 666)
        self.assertEqual(str(z), 'x + 2x^3 + 4x^5 + 3.14x^666')

    def test_abs(self):
        ''' Tests abs works '''
        self.assertEqual(str(abs(Term(-16.5,'t',3))), '16.5t^3')
        self.assertEqual(str(abs(Term(12.5,'t',3))), '12.5t^3')


class NumericalMethods(unittest.TestCase):
# TODO: Sort out float vs decimal and precision
    pols = [ Polynomial('x', 1,2), Polynomial('x', 1,3,2,2,1,1,-5,0),
        Polynomial('x', 1,3,2,1,7,0), Polynomial('x', 4,3,2,1,7,0),
        Polynomial('x', 2,5,-5,4,-11,3,23,2,9,1,-18,0) ]

    def setUp(self):
        getcontext().prec = 50

    def test_newton_raphson(self):
        ''' Newton Raphson should correctly locate 1 root of the equation '''
        for y in self.pols:
            self.assertAlmostEqual(y.evaluate(y.newton_raphson(1, 10)),
                0, places=0)

    def test_roots(self):
        ''' The Durand-Kerner method should correctly locate all roots '''
        mag = lambda x: ( x.imag**2 + x.real**2 )**.5
        for y in self.pols:
            for x in y.roots(): 
                self.assertAlmostEqual(mag(y.evaluate(x)), 0, places=10)

    def test_numerical_integral(self):
        ''' Numerical integration should produce results close to the true
        value '''
        a = 3.4; b = 7.5
        reldiff = lambda a, b: abs(a - b) / a
        for y in self.pols:
            self.assertAlmostEqual(reldiff(float(y.integral().limit(a,b)),
            y.numerical_integral(a,b)), 0, places = 2)

    def test_trapezoidal_integral(self):
        ''' The trapezium rule should give an ok estimate of the integral '''
        a = 3.4; b = 7.5
        reldiff = lambda a, b: abs(a - b) / a
        for y in self.pols:
            self.assertAlmostEqual(reldiff(float(y.integral().limit(a,b)),
            y.trapezoidal_integral(a,b)), 0, places = 2)

    def tearDown(self):
        getcontext().prec = 3


class Terms(unittest.TestCase):
    vals = (
    (4,3,'4t^3'),
    (4,-3,'4t^-3'),
    (-4,3,'-4t^3'),
    (0,-3,''),
    (7,0,'7'),
    (7,1,'7t'),
    (1,1,'t'),
    (1,0,'1'),
    (1000000000000000000000000000000,1111111111111111111111111,'1000000000000000000000000000000t^1111111111111111111111111')
    )

    def test_str(self):
        ''' Tests functions are correctly printed '''
        for a,b,string in self.vals:
            self.assertEqual(str(Term(a,'t',b)), string) # a*x^b

    def test_calculus(self):
        ''' The integral of the differential should be equal to the original function '''
        for a,b,c in self.vals:
            self.assertEqual(Term(a,'t',b).differential().integral(),
                Term(a,'t',b))

    def test_sign(self):
        ''' The sign of a term's coefficient should be correctly reported '''
        for a,b,c in self.vals:
            y = Term(a,'x',b)
            if a == 0: self.assertEqual(y.sign(), 0)
            elif a > 0: self.assertEqual(y.sign(), 1)
            elif a < 0: self.assertEqual(y.sign(), -1)

    def test_evaluate(self):
        ''' Tests functions are correctly evaluated '''
        f = Term(3,'x',2)
        xys = [ (5,75),(4.5,Decimal('60.6')),(0,0),(-4,48),(2+3j,-15+36j) ]
        for x,y in xys:
            self.assertEqual(y, f.evaluate(x))


class Constants(unittest.TestCase):
    def test_equality(self):
        ''' Constants should be equal any number '''
        vals = (2, Decimal('5.6'), -2, 0, Decimal('Inf'))
        for x in vals:
            self.assertEqual(x, constant())


class NInts(unittest.TestCase):
    vals = [(3,4,Decimal('0.75')),(8,4,2)]
    def test_divisions(self):
        ''' Dividing integers should result in either a decimal or integer,
        depending on common factors '''
        for a,b,c in self.vals:
            self.assertEqual(nint(a) / nint(b), c)


class Calculations(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_solve(self):
        self.assertEqual(self.calc.evaluate('solve x^2 - 2x - 15'),
            'x = 5 or -3')
        self.assertEqual(self.calc.evaluate('solve x^3 - 19x - 30'),
            'x = 5 or -3 or -2')
        self.assertEqual(self.calc.evaluate('solve x^3 + 3x^2 - 6x - 8'),
            'x = 2 or -4 or -1')


if __name__ == '__main__':
    unittest.main()
