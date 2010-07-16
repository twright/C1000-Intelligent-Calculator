#!/usr/bin/env python3.1

from decimal import Decimal, getcontext
from copy import deepcopy, copy
from functools import reduce

from ntypes import handle_type, constant, nint

# Set precision for numbers
# getcontext().prec = 3

def boole_composite_integral(f,a,b,m):
    h = (b-a)/(4*m)
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
        return boole_composite_integral(lambda x: float(self.evaluate(x)), float(a),float(b),n)

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
        h = (float(b) - float(a)) / n
        x = lambda i: float(a) + i*h
        f = lambda i: float(self.evaluate( x(i) ))
        
        return h*( f(0)/2
            + sum( f(i) for i in range(1,n) ) + f(n)/2 ) 

    def limit(self, lower, upper):
        ''' Calculate the limit of a funtion between 2 points '''
        return self.evaluate(upper) - self.evaluate(lower)

class Fraction(Function):
    def __init__(self, abscissa, numerator, denominator):
        assert(abscissa == numerator.abscissa == denominator.abscissa)
        self.numerator = numerator
        self.denominator = denominator
        Function.__init__(self, abscissa)

    def __str__(self):
        return '(' + str(self.numerator) + ') / (' + str(self.denominator) + ')'

    def evaluate(self, x):
        return self.numerator.evaluate(x) / self.denominator.evaluate(x)

    def roots(self, n=100):
        return numerator.roots(n) + denominator.roots(n)

    def simplify(self):
        power = lambda t: t.power
        a = Polynomial(self.abscissa); b = Polynomial(self.abscissa)
        lowest_power = min(map(power, self.numerator.terms + self.denominator.terms))
        reduce_power = lambda t: t / Term(1, self.abscissa, lowest_power)
        a.terms = list(map(reduce_power, self.numerator.terms)) 
        b.terms = list(map(reduce_power, self.denominator.terms)) 
        return Fraction(self.abscissa, a.simplify(), b.simplify())

    def differential(self):
        ''' Making use of the quotient rule,
        if f(x) = g(x) / h(x)
        then f'(x) = ( g'(x)*h(x) - h'(x)*g(x) ) / h(x)^2 '''
        return ((self.numerator.differential()*self.denominator - self.denominator.differential()*self.numerator)
            / self.denominator**2).simplify()

    def as_gnuplot_expression(self):
        return '(' + self.numerator.as_gnuplot_expression() + ') / ('\
            + self.denominator.as_gnuplot_expression() + ')'

class Product(Function):
    def __init__(self, abscissa, g, h):
        super().__init__(abscissa)
        self.g = g
        self.h = h
        self.sort_terms()

    def sort_terms(self):
        if (isinstance(self.h, Power) ^ isinstance(self.g, Power)):
            if isinstance(self.g, Power):
                self.g, self.h = self.h, self.g

    def __mul__(a, b):
        return Product(a.abscissa, self.g*b, self.h)

    def __str__(self):
        bracket = lambda a: ('(%s)' if isinstance(a, Polynomial) else '%s') % str(a)
        return  bracket(self.g) + ' * ' + bracket(self.h)

    def as_gnuplot_expression(self):
        return '(' + self.g.as_gnuplot_expression() + ') * ('\
            + self.h.as_gnuplot_expression() + ')'


class Power(Function):
    def __init__(self, abscissa, polynomial, power):
        super().__init__(abscissa)
        self.function = polynomial
        self.power = power

    def __str__(self):
        return '(' + str(self.function) + ')^' + str(self.power)

    def __mul__(a, b):
        return Product(a.abscissa, a, b)
    __rmul__ = __mul__

    def differential(self):
        ''' Drawing on chain rule, 
        if f(x) = g(x)^n
        then f'(x) = n * g'(x) * g(x)^(n-1) '''
        return self.power * self.function.differential() * self.function ** (self.power - 1)

    def evaluate(self, x):
        return self.function.evaluate(x) ** self.power

    def as_gnuplot_expression(self):
        return '(' + self.function.as_gnuplot_expression() + ')**' + str(self.power)


class Equality:
    def __init__(self, a, b):
        assert(a.abscissa == b.abscissa)
        self.a = a; self.b = b
        self.abscissa = a.abscissa

    def __repr__(self):
        return str(self.a) + ' = ' + str(self.b)

    def roots(self, n=100):
        return (self.a - self.b).simplify().roots(n)


class Term(Function):
    ''' A class holding a polynomial term '''
    def __init__(self, coefficient, abscissa, power):
        self.coefficient = handle_type(coefficient)
        self.power = handle_type(power)
        super().__init__(abscissa)

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

    def roots(self,n=0):
        return [0 for i in range(self.power)]

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
        b = a._convert_other(b)
        if b == NotImplemented:
            return b

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

    def __mul__(a,b):
        b = a._convert_other(b)
        if b == NotImplemented:
            return b

        if isinstance(b, Term):
            return Term(a.coefficient*b.coefficient, a.abscissa, a.power+b.power)
        else:
            return NotImplemented
    __rmul__ = __mul__

    def _convert_other(self, other):
        if isinstance(other, Term):
            return other
        elif isinstance(other, nint) or isinstance(other, Decimal):
            return Term(other, self.abscissa, 0)
        else:
            return NotImplemented

    def __truediv__(a,b):
        b = a._convert_other(b)
        if b == NotImplemented:
            return b
        return Term(a.coefficient/b.coefficient, a.abscissa, a.power-b.power)

    def __sub__(a,b):
        b = a._convert_other(b)
        if b == NotImplemented:
            return b
        return a + b.invert()

    def __add__(a,b):
        b = a._convert_other(b)
        if b == NotImplemented:
            return b
        c = Polynomial(a.abscissa)
        c.terms = [a, b]
        c.sort_terms()
        return c + Polynomial(a.abscissa,0,0)


class Polynomial(Function):
    ''' A class representing a polynomial '''
    def __init__(self, abscissa, *nums):
        ''' Initiates the polynomial with a string containing the abscissa
        followed by pairs of coefficients and powers '''
        super().__init__(abscissa)
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
        if self.order() == 1:
            return [ - self.terms[1].coefficient / self.terms[0].coefficient ]

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
         - Evaluate each term
         - Sum them '''
        g = lambda a: a.evaluate(x)
        return sum(map(g, self.terms))

    def sort_terms(self):
        ''' Sort terms in order of descending power '''
        power = lambda a: a.power
        self.terms.sort(key=power, reverse=True)

    def simplify(a):
        a.sort_terms()
        b = Polynomial(a.abscissa)
        b.terms += [ a.terms[0] ]
        for i in range(1,len(a.terms)):
            if a.terms[i].coefficient != 0:
                if a.terms[i].power != b.terms[-1].power:
                    b.terms += [ a.terms[i] ]
                else:
                    b.terms[-1].coefficient += a.terms[i].coefficient
        return b

    def invert(self):
        return self.map_to_terms(lambda t: t.invert())

    def _convert_other(self, other):
        if isinstance(other, Polynomial):
            return other
        elif isinstance(other, Term):
            c = Polynomial(other.abscissa)
            c.terms = [ other ]
            return c
        elif isinstance(other,nint) or isinstance(other,Decimal):
            return Polynomial(self.abscissa, other, 0)
        else:
            return NotImplemented

    def __sub__(a, b):
        b = a._convert_other(b)
        return a + b.invert()
    __rsub__ = __sub__

    def __add__(a, b):
        b = a._convert_other(b)
        c = Polynomial(a.abscissa)
        c.terms = a.terms + b.terms
        return c.simplify()
    __radd__ = __add__

    def __mul__(a, b):
        b = a._convert_other(b)
        if b == NotImplemented:
            return b
        c = Polynomial(a.abscissa)
        for l in a.terms:
            for m in b.terms:
                c.terms += [ l * m ]
        return c.simplify()
    __rmul__ = __mul__

    def __truediv__(a,b):
        if isinstance(b, Polynomial):
            return Fraction(a.abscissa, a, b).simplify()
        elif isinstance(b, nint) or isinstance(b, Decimal):
            c = Polynomial(a.abscissa)
            for l in a.terms:
                c.terms += [ l / b ]
            return c.simplify()
        else:
            return NotImplemented

    def __pow__(self, m):
        if (isinstance(m, nint) or isinstance(m, int)):
            return reduce(lambda a,b: a * b, [self for i in range(m)])
        elif isinstance(m, Decimal):
            return Power(self.abscissa, self, m)
        
    def as_gnuplot_expression(self):
        ''' Convert into the gnuplot format '''
        from re import sub
        expr = str(self)
        # Add * from multiplication
        expr = sub(r'([0-9])x', r'\1*x', expr, 100) 
        # Replace ^ with ** for powers
        expr = sub(r'\^', r'**', expr, 100) 
        return expr

if __name__ == '__main__':
    import doctest
    getcontext().prec = 3
    doctest.testmod()
