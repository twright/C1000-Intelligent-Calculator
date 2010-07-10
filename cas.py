#!/usr/bin/env python3.1

import math
from ntypes import handle_type, constant
from decimal import *
from functools import *

# Set precision for numbers
getcontext().prec = 3

class function:
    ''' A class to hold arbitrary algebraic functions '''
    def __init__(self,abscissa):
        self.abscissa = abscissa
    def evaluate(n): pass
    def numerical_integral(self,a,b,n=100): 
        ''' The numerical integral of the function using the composite 3/8
        Simpson's Rule
        (see http://mathworld.wolfram.com/Newton-CotesFormulas.html) '''
    #    getcontext().prec = 50
        h = (b - a) / n
        x = lambda i: a + i*h
        f = lambda i: float(self.evaluate( x(i) ))

        return h*( (17/48)*f(0) + (59/48)*f(1) + (43/48)*f(2) + (49/48)*f(3)\
            + sum([f(i) for i in range(4,n-3)])\
            + (17/48)*f(n-3) + (59/48)*f(n-2) + (43/48)*f(n-1) + (49/48)*f(n) )
    def trapezoidal_integral(self,a,b,n=100):
        ''' Numerically integrate functions via the Trapezium Rule'''
        h = (b - a) / n
        x = lambda i: a + i*h
        f = lambda i: float(self.evaluate( x(i) ))
        
        return h*( (1/2)*f(0) + sum([ f(i) for i in range(1,n) ]) + (1/2)*f(n) ) 
    def limit(self,lower,upper):
        '''
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print (y.integral().limit(1,2))
        51.0
        '''
        return self.evaluate(upper) - self.evaluate(lower)

class term(function):
    ''' A class holding a polynomial term '''
    def __init__(self, coefficient, abscissa, power):
        self.coefficient = handle_type(coefficient)
        self.power = handle_type(power)
        function.__init__(self, abscissa)
    def __str__(self):
        ''' Output the term nicely via assorted logic '''
        if self.coefficient == 0: return ''
        else: return \
            ('', str(self.coefficient))[self.coefficient != 1 or self.power == 0] \
            + ('', '*')[self.coefficient != 1 and self.power != 0] \
            + ('', self.abscissa)[self.power != 0] \
            + ('', '^' + str(self.power))[0 != self.power != 1]
    def sign(self):
        ''' Return 0, 1 or -1 depending on the sign of the coefficient '''
        return (0, 1, -1)[(self.coefficient > 0) + 2*(self.coefficient < 0)]
    def __abs__(self):
        ''' Return a version of the term, with the coefficient positive 
        >>> y = term(-16.5,'t',3); print (abs(y))
        16.5*t^3
        >>> y = term(12.5,'t',3); print (abs(y))
        12.5*t^3
        '''
        return term(abs(self.coefficient), self.abscissa, self.power)
    def differential(self):
        '''
        >>> y = term(4,'t',3); print (y.differential())
        12*t^2
        '''
        if self.power == 0:
            return term(0, self.abscissa, 0)
        else:
            return term(self.coefficient * self.power, self.abscissa, self.power - 1)
    def integral(self):
        '''
        >>> y = term(4,'t',3); print (y.integral())
        t^4
        '''
        if self.coefficient == 0:
            return constant()
        else:
            return term(self.coefficient/(self.power + 1), self.abscissa, self.power + 1)
    def evaluate(self,x):
        ''' Returns the value of the term for x
        >>> y = term (3, 'x', 2)
        >>> print(y.evaluate(5))
        75
        >>> print(y.evaluate(4.5))
        60.6
        >>> print(y.evaluate(0))
        0
        >>> print(y.evaluate(-4))
        48
        '''
        return self.coefficient * handle_type(x) ** self.power
    def __eq__(a,b):
        return a.coefficient == b.coefficient\
            and a.abscissa == b.abscissa\
            and a.power == b.power
    def __repr__(self):
        return "term(%s, '%s', %s)"\
            % (self.coefficient, self.abscissa, self.power)

class polynomial(function):
    ''' A class representing a polynomial '''
    def __init__(self, abscissa, *nums):
        function.__init__(self, abscissa)
        self.terms = [ term(a, abscissa, b) for (a,b) in zip (nums[::2], nums[1::2]) ]
    def __str__(self):
        ''' A list comprehension to combine the terms of the polynomial
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('f(y) =',y);
        f(y) = y + 2*y^3 + 4*y^5
        '''
        if len(self.terms) > 1:
            return ' '.join([str(self.terms[0])] + [('+', '-')[a.sign() == -1] \
                + ' ' + str(abs(a)) for a in self.terms[1:] if a.sign() != 0])
        elif len(self.terms) == 1:
            return str(self.terms[0])
        else:
            return ''
    def map_to_terms(self,f):
        ''' Allows list proccessing of terms '''
        y = polynomial(self.abscissa)
        y.terms = list(map(f, self.terms))
        return y
    def differential(self):
        ''' Calculate the differential of 
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('f`(y) =',y.differential())
        f`(y) = 1 + 6*y^2 + 20*y^4
        '''
        f = lambda x: x.differential()
        return (self.map_to_terms(f))
    def integral(self):
        ''' Calculate the indefinite integral of the expression
         - Integrate each term
         - Return a polynomial object based on the new terms
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('∫ f(y) dy =',y.integral())
        ∫ f(y) dy = 0.5*y^2 + 0.5*y^4 + 0.667*y^6 + c
        '''
        f = lambda x: x.integral()
        a = self.map_to_terms(f)
        a.terms += [ constant() ]
        return (a)
    def append(self, coefficient, power):
        ''' Add a term to the polynomial
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> y.append(3.141, 666)
        >>> print(y)
        y + 2*y^3 + 4*y^5 + 3.14*y^666
        '''
        self.terms += [ term(coefficient, self.abscissa, power) ]
    def newton_raphson(self, x0, n=100):
        x = Decimal(repr(x0))
        for i in range(n):
            x = x - self.evaluate(x) / self.differential().evaluate(x)
        return x
    def roots(self, n=100):
        ''' Numerically locate all roots (real and complex) of an equation using the Durand-Kerner method '''
        mul = lambda a, b: a * b
        roots = [ (0.4+0.9j)**n for n in range(len(self.terms)-1) ]
        print(roots)
        for i in range(n):
            for i in range(len(roots)):
            #    print(x - (self.evaluate(x)) / ( reduce(mul, [x - a for a in roots if not (a is x)]) ))
                roots[i] = roots[i] - (self.evaluate(roots[i])) / ( reduce(mul, [roots[i] - a for a in roots if not (a is roots[i])]) )
        return roots
    def evaluate(self, x):
        ''' Return the value of f(x)
         - Evalute each term
         - Sum them '''
        g = lambda a: a.evaluate(x)
        return sum(map(g, self.terms))

if __name__ == '__main__':
    import doctest
    getcontext().prec = 3
    doctest.testmod()
