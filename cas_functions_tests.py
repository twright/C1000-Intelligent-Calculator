#!/usr/bin/env python3.1
''' Test the functionality of core cas functions like type handling,
the nint datatype and hstr's (html strings) '''

from decimal import Decimal
import unittest

from cas_core import Integer
import cas_expressions as ce
from cas_functions import *
from cas_functions import Polynomial

class Functions(unittest.TestCase):
    y = Polynomial('x',1,1,2,3,4,5)
    z = Function('t')

    def test_limit(self):
        ''' Tests that functions can correctly be limited between 2 values '''
        self.assertEqual(self.y.integral().limit(1,2), Decimal('51.0'))

    def test_init(self):
        ''' Test that the init function accepts and reject abscissas correctly '''
        self.assertRaises(AssertionError, Function, 'xy')
        self.assertIsNotNone(Polynomial('x'))
        self.assertIsNotNone(Polynomial('t'))

    def test_addition(self):
        ''' Test addition identities '''
        self.assertEqual(self.z + 0, self.z)
        self.assertEqual(0 + self.z, self.z)

    def test_subtraction(self):
        ''' Test subtraction identities '''
        self.assertEqual(self.z - 0, self.z)

    def test_multiplication(self):
        ''' Test multiplication identities '''
        self.assertEqual(0*self.z, 0)
        self.assertEqual(self.z*0, 0)
        self.assertEqual(1*self.z, self.z)
        self.assertEqual(self.z*1, self.z)

    def test_division(self):
        ''' Test division identities '''
        self.assertEqual(self.z/1, self.z)
        self.assertEqual(0/self.z, 0)

    def test_powers(self):
        ''' Test indicies identities '''
        self.assertEqual(self.z**0, 1)
        self.assertEqual(self.z**2, Power(self.z, 2))

class Polynomials(unittest.TestCase):
    y = Polynomial('x',1,1,2,3,4,5)
      
    def test_evaluate(self):
        ''' Evaluate works for sample values '''
        xys = ((3,'1029'),(0,'0'),(1,'7'),(.1,'0.102'),(-4,'-4228'))
        for a, b in xys:
            self.assertEqual(str(self.y.evaluate(a)), b)

    def test_differential(self):
        ''' Tests polynomials can be correctly differentiated '''
        self.assertEqual(str(self.y.differential()),
            '20x^4 + 6x^2 + 1')
        
    def test_integral(self):
        ''' Tests polynomials can be correctly integrated '''
        self.assertEqual(str(self.y.integral()),
            '0.667x^6 + 0.5x^4 + 0.5x^2 + c')

    def test_append(self):
        ''' Tests elements can be appended to functions '''
        import copy
        z = copy.deepcopy(self.y); z.append(3.141, 666)
        self.assertEqual(str(z), '3.14x^666 + 4x^5 + 2x^3 + x')

    def test_abs(self):
        ''' Tests abs works '''
        self.assertEqual(str(abs(Term(-16.5,'t',3))), '16.5t^3')
        self.assertEqual(str(abs(Term(12.5,'t',3))), '12.5t^3')

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

    def test_equality(self):
        ''' Tests that equal terms are considered equal and unequal, unequal '''
        self.assertEqual(Term(3,'x',2), Term(3,'x',2))
        self.assertNotEqual(Term(3,'x',2), Term(2,'x',3))
        self.assertNotEqual(Term(3,'x',2), Term(3,'x',3))
        self.assertNotEqual(Term(3,'x',2), Term(2,'x',2))
        self.assertNotEqual(Term(3,'x',2), Term(3,'y',2))
        self.assertEqual(Term(2,'x',0), 2)
        self.assertEqual(Term(0,'x',2), Term(0,'x',5))
        self.assertEqual(Term(0,'x',5), 0)

    def test_powers(self):
        ''' Tests that sample powers are correctly evaluated '''
        self.assertEqual(Term(3,'x',2)**4, Term(81,'x',8))
        self.assertEqual(Term(4,'x',2)**0, 1)
        self.assertEqual(Term(4,'x',3)**1.1, Power(Term(4,'x',3), 1.1))
        self.assertEqual(Term(4,'x',2), InproperTerm(0.25,'x',-2))

    def test_convert_other(self):
        ''' Tests that various types are correctly converted '''
        vals = [ (2,Term(2,'x',0)), (3.2,Term(3.2,'x',0)), (2+1j,Term(2+1j,'x',0)) ]
        for a, b in vals:
            self.assertEqual(Term(0,'x',0)._convert_other(a), b)
        self.assertRaises(Exception, Term, 'sdf', 'x', 2)

    def test_as_gnuplot_expression(self):
        ''' Tests the expression is correctly converted to the gnuplot format '''
        vals = [ (Term(5,'x',2), '5*x**2'), (Term(3,'y',1), '3*x'),
            (Term(1,'x',2), 'x**2') ]
        for a, b in vals:
            self.assertEqual(a.as_gnuplot_expression(), b)

    def test_multiplication(self):
        ''' Tests that ax^n * bx^m = ab*x^(n+m) '''
        vals = [ (Term(3,'x',2),Term(4,'x',1),Term(12,'x',3)),
        (1,Term(6,'x',3),Term(6,'x',3)), (Term(6,'x',3),1,Term(6,'x',3)),
        (0,Term(6,'x',3),Integer(0)), (Term(6,'x',3),0,Integer(0)),
        (Term(2,'x',1),Term(3,'y',1),ce.Term(6,ce.Factor('x',1),ce.Factor('y',1))),
        (Term(2,'x',2),Term(3,'y',1),ce.Term(6,ce.Factor('y',1),ce.Factor('x',2))),
        (Term(2.1,'x',2),Term(3,'x',2),Term(6.3,'x',4)) ]
        for a, b, c in vals:
            self.assertEqual(a*b, c)

    def test_subtraction(self):
        pass

    def test_addition(self):
        pass

    def test_division(self):
        pass

    def test_repr(self):
        pass

class Equalities(unittest.TestCase):
    vals = [ (Equality(Polynomial('x', 2,3), Polynomial('x', 2,1, 3,2)), '2x^3 = 3x^2 + 2x'),
        (Equality(Integer(0), Polynomial('y', 4,2, -5,0)), '0 = 4y^2 - 5'),
        (Equality(Polynomial('z', 4,2, -5,0), Integer(0)), '4z^2 - 5 = 0'),
        (Equality(Integer(5), Term(1, 't', 1)), '5 = t'),
        (Equality(Term(1, 'x', 5), Integer(0)), 'x^5 = 0') ]

    def test_init(self):
        ''' Tests that equalities can be correctly created '''
        self.assertIsNotNone(Equality(Integer(0), Term(3, 'x', 2)))
        self.assertIsNotNone(Equality(Polynomial('t', 2,3, 2,1), Term(2,'t',1)))
        self.assertRaises(ValueError, Equality, Polynomial('y', 2,1), Polynomial('x', 1,2))

    def test_str(self):
        ''' Tests that equalities are correctly printed '''
        for a, b in self.vals:
            self.assertEqual(str(a), b)

    def test_roots(self):
        ''' Tests that sample equalities can correctly be solved '''
        # Evaluate functions or return variables
        getoreval = lambda f, x: f.evaluate(x) if isinstance(f, Function) else f
        for eq, string in self.vals:
            for root in eq.roots():
                self.assertAlmostEqual(getoreval(eq.a, root), getoreval(eq.b, root),
                    places = 7)

class NumericalMethods(unittest.TestCase):
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

    def test_romberg_integral(self):
        ''' Romberg integration should produce results very close to the true
        value '''
        # TODO: Make harsher when proper numerical integration finished
        a = 3.4; b = 7.5
        reldiff = lambda a, b: abs(a - b) / a
        for y in self.pols:
            self.assertAlmostEqual(reldiff(y.integral().limit(a,b),
            y.romberg_integral(a,b)), 0, places = 10)

    def test_trapezoidal_integral(self):
        ''' The trapezium rule should give an ok estimate of the integral '''
        a = 3.4; b = 7.5
        reldiff = lambda a, b: abs(a - b) / a
        for y in self.pols:
            self.assertAlmostEqual(reldiff(y.integral().limit(a,b),
            y.trapezoidal_integral(a,b)), 0, places = 2)

    def tearDown(self):
        getcontext().prec = 3

if __name__ == '__main__':
    unittest.main()
