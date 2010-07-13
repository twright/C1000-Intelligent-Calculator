#!/usr/bin/env python3

from decimal import Decimal, getcontext
from copy import deepcopy, copy
from functools import reduce

from ntypes import handle_type, constant, nint

# Set precision for numbers
# getcontext().prec = 3

def boole_composite_integral(f,a,b,m):
    h = (b-a)/(4*m)
    print(type(h))
    x = lambda k: a + k*h
    return (2*h/45)*sum( 7*f(x(4*k-4)) + 32*f(x(4*k-3)) + 12*f(x(4*k-2))
            + 32*f(x(4*k-2)) + 7*f(x(4*k)) for k in range(1,m) )

class Function:
    ''' A class to hold arbitrary algebraic functions '''
    def __init__(self, abscissa):
        self.abscissa = abscissa

    def evaluate(n): pass

    def numerical_integral(self, a, b, n=100): 
        ''' The numerical integral of the function using the composite 3/8
        Simpson's Rule
        (see http://mathworld.wolfram.com/Newton-CotesFormulas.html) '''
    #    getcontext().prec = 50
        return boole_composite_integral(lambda x: self.evaluate(x), a,b,n)

#        h = (Decimal(repr(b)) - Decimal(repr(a))) / n
#        x = lambda i: a + i*h
#        f = lambda i: Decimal(self.evaluate( i ))

#        print(x(n), b)
#        print([(i, i+1, i+2) for i in range(1,n,3)])

#       Cumulative 3/8
#        return (3*h/8)*(f(0) + sum(3*f(i) + 3*f(i+1) + 2*f(i+2) 
#            for i in range(1,n,3)) + f(n))

#       Combined / expanded formula
#        return h*( (17*f(0) + 59*f(1) + 43*f(2) + 49*f(3))/48
#            + sum( f(i) for i in range(4,n-3) )
#            + (17*f(n-3) + 59*f(n-2) + 43*f(n-1) + 49*f(n))/48 )

#       Composite Boole's Rule
#        x = lambda i: a + k*h
#        return (2*h/45) * sum(7*f(x(0)) + 32*f(x(1)) + 12*f(x(2))
#            + 32*f(x(3)) + 7*f(x(4)) for k in range(1,4*n))

#       Open formula
#        return (8*h/945)*(460*f(1) - 954*f(2) + 2196*f(3) - 2459*f(4)
#            + 2196*f(5) - 954*f(6) + 460*f(7))

    def trapezoidal_integral(self, a, b, n=100):
        ''' Numerically integrate functions via the Trapezium Rule '''
        h = (Decimal(repr(b)) - Decimal(repr(a))) / n
        x = lambda i: a + i*h
        f = lambda i: Decimal(self.evaluate( x(i) ))
        
        return h*( f(0)/2
            + sum( f(i) for i in range(1,n) ) + f(n)/2 ) 

    def limit(self, lower, upper):
        ''' Calculate the limit of a funtion between 2 points '''
        return self.evaluate(upper) - self.evaluate(lower)


class Equality:
    def __init__(self, a, b):
        self.a = a; self.b = b

    def __repr__(self):
        return str(self.a) + ' = ' + str(self.b)

    def roots(self, n=100):
        return (self.a - self.b).roots(n)


class Term(Function):
    ''' A class holding a polynomial term '''
    def __init__(self, coefficient, abscissa, power):
        self.coefficient = handle_type(coefficient)
        self.power = handle_type(power)
        Function.__init__(self, abscissa)

    def __str__(self):
        ''' Output the term nicely via assorted logic '''
        if self.coefficient == 0: return ''
        else: return \
            (str(self.coefficient) 
                if self.coefficient != 1 or self.power == 0 else '')\
            + (self.abscissa if self.power != 0 else '')\
            + ('^' + str(self.power) if 0 != self.power != 1 else '')

    def sign(self):
        ''' Return 0, 1 or -1 depending on the sign of the coefficient '''
        return (0, 1, -1)[(self.coefficient > 0) + 2*(self.coefficient < 0)]

    def __abs__(self):
        ''' Return a version of the term, with the coefficient positive '''
        a = deepcopy(self); a.coefficient = abs(a.coefficient)
        return a 

    def differential(self):
        ''' Return the differential '''
        if self.power == 0:
            return Term(0, self.abscissa, 0)
        else:
            return Term(self.coefficient * self.power, self.abscissa,
                self.power - 1)

    def integral(self):
        ''' Return the indefinite integral '''
        if self.coefficient == 0:
            return constant()
        else:
            return Term(self.coefficient/(self.power + 1),
                self.abscissa, self.power + 1)

    def evaluate(self, x):
        ''' Returns the value of the term for x '''
        return self.coefficient * handle_type(x) ** self.power

    def __eq__(a, b):
        ''' Compare whether 2 terms are equal '''
        return a.coefficient == b.coefficient\
            and a.abscissa == b.abscissa\
            and a.power == b.power

    def __repr__(self):
        ''' Print a representation of the term '''
        return "Term(%s, '%s', %s)"\
            % (self.coefficient, self.abscissa, self.power)

    def invert(self):
        ''' Return a copy of the term with its coefficient inverted '''
        a = deepcopy(self); a.coefficient *= -1
        return a


class Polynomial(Function):
    ''' A class representing a polynomial '''
    def __init__(self, abscissa, *nums):
        ''' Initiates the polynomial with a string containing the abscissa
        followed by pairs of coefficients and powers '''
        Function.__init__(self, abscissa)
        self.terms = [ Term(a, abscissa, b) for a, b
            in zip(nums[::2], nums[1::2]) ]
        self.sort_terms()

    def __str__(self):
        ''' A list comprehension to combine the terms of the polynomial '''
        if len(self.terms) > 1:
            return ' '.join([str(self.terms[0])] + [('+', '-')[a.sign() == -1]
                + ' ' + str(abs(a)) for a in self.terms[1:] if a.sign() != 0])
        elif len(self.terms) == 1:
            return str(self.terms[0])
        else:
            return ''
    __repr__ = __str__

    def map_to_terms(self, f):
        ''' Allows list processing of terms '''
        y = Polynomial(self.abscissa)
        y.terms = list(map(f, self.terms))
        y.sort_terms()
        return y

    def differential(self):
        ''' Calculate the differential of the expression
        >>> y = Polynomial('y',1,1,2,3,4,5)
        >>> print ('f`(y) =', y.differential())
        f`(y) = 1 + 6*y^2 + 20*y^4
        '''
        f = lambda x: x.differential()
        return (self.map_to_terms(f))

    def integral(self):
        ''' Calculate the indefinite integral of the expression
         - Integrate each term
         - Return a polynomial object based on the new terms
        >>> y = Polynomial('y',1,1,2,3,4,5)
        >>> print ('∫ f(y) dy =', y.integral())
        ∫ f(y) dy = 0.5*y^2 + 0.5*y^4 + 0.667*y^6 + c
        '''
        f = lambda x: x.integral()
        a = self.map_to_terms(f)
        a.terms += [ constant() ]
        return (a)

    def append(self, coefficient, power):
        ''' Add a term to the polynomial '''
        self.terms += [ Term(coefficient, self.abscissa, power) ]
        self.sort_terms()

    def newton_raphson(self, x0, n=100):
        ''' Find 1 root of an equation based upon an initial guess of x0 and
        n iteration of the Newton Raphson method:
            x' = x - f(x) / f'(x) '''
        x = Decimal(repr(x0))
        for i in range(n):
            x = x - self.evaluate(x) / self.differential().evaluate(x)
        return x

    def order(self):
        ''' Return the power of the equation (taken to be the greatest power
        of a term i.e. the power of the leading term) '''
        return self.terms[0].power

    def roots(self, n=100):
        ''' Numerically locate all roots (real and complex) of an equation
        using n iterations of the Durand-Kerner method '''
        mul = lambda a, b: a * b
        g = deepcopy(self)
        m = float(g.terms[0].coefficient) 
        if m != 1:
            for a in g.terms:
                a.coefficient = float(a.coefficient) / m
        roots = [ (0.4+0.9j)**n for n in range(g.order()) ]
        for i in range(n):
            for i in range(len(roots)):
                roots[i] = roots[i] \
                - (g.evaluate(roots[i]))\
                / ( reduce(mul, [roots[i]\
                - a for a in roots if a is not roots[i]]) )
        return roots
    def evaluate(self, x):
        ''' Return the value of f(x)
         - Evalute each term
         - Sum them '''
        g = lambda a: a.evaluate(x)
        return sum(map(g, self.terms))

    def sort_terms(self):
        power = lambda a: a.power
        self.terms.sort(key=power, reverse=True)

    def __sub__(a, b):
        if a.abscissa != b.abscissa: return None
        aterms = dict([(t.power, t) for t in a.terms])
        bterms = dict([(t.power, t) for t in b.terms])
        highest_power = max([a.order(), b.order()])
        c = Polynomial(a.abscissa)
        for i in range(highest_power, 0, -1):
            c.append((aterms[i].coefficient if i in aterms else 0) 
                - (bterms[i].coefficient if i in bterms else 0), i)
        return c
        
    def as_gnuplot_expression(self):
        ''' Convert into the gnuplot format '''
        from re import sub
        expr = str(self)
        # Add * from multiplication
        expr = sub(r'([0-9])x', r'\1*x', expr, 100) 
        # Replace ^ with ** for powers
        expr = sub(r'\^', r'**', expr, 100) 
        return expr

    __rsub__ = __sub__

if __name__ == '__main__':
    import doctest
    getcontext().prec = 3
    doctest.testmod()
