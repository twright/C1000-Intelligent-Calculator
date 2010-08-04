#!/usr/bin/env python3.1
''' A module containing representations of algebraic functions in single variables
in the general form f(x) '''

from copy import deepcopy
from decimal import Decimal, getcontext, localcontext
from functools import reduce, partial
from numbers import Number

from .core import Constant, handle_type, Integer, Algebra, print_complex
import cas.core as core
import cas.multivariate as ce
import cas.numerical_methods as nm

# Set precision for numbers
# getcontext().prec = 3

class Function(Algebra):
    ''' A class to hold arbitrary algebraic functions '''
    def __init__(self, abscissa):
        assert(len(abscissa) == 1)
        self.abscissa = abscissa
        super().__init__()

    def evaluate(self, n): pass
    
    def roots(self): pass
    
    def differential(self): pass

    def maxima(self, n=100):
        ''' Calculate the maxima of a function by the turning points at which
        its second differential is negative '''
        return list(filter(lambda x: self.differential().differential().evaluate(x) < 0,
            self.differential().roots(n)))

    def minima(self, n=100):
        ''' Calculate the minima of a function by the turning points at which its
        second differential is positive '''
        return list(filter(lambda x: self.differential().differential().evaluate(x) > 0,
            self.differential().roots(n)))

#    def numerical_integral(self, a, b, n=100): 
#        ''' The numerical integral of the function using the composite 3/8
#        Simpson's Rule
#        (see http://mathworld.wolfram.com/Newton-CotesFormulas.html) '''
#    #    getcontext().prec = 50
#        return boole_composite_integral(lambda x: float(self.evaluate(x)),
#            float(a),float(b),n)
            
    def numerical_integral(self, method, a, b, *n):
        print( self, method, a, b, *n )
        f = lambda x: float(self.evaluate(x))
        return Decimal.from_float(method(f, float(a), float(b), *n)).normalize()

    def trapezoidal_integral(self, *a):
        ''' Numerically integrate functions via the Trapezium Rule with n strips '''
        return self.numerical_integral(nm.trapezoidal_composite_integral, *a)
        
    def simpson_integral(self, *a):
        return self.numerical_integral(nm.simpson_composite_integral, *a)

    def romberg_integral(self, *a):
        ''' Numerically integrate functions via the Romberg method comparing n
        values from interpolating polynomials of order n '''
        return self.numerical_integral(nm.romberg_integral, *a)

    def limit(self, lower, upper):
        ''' Calculate the limit of a funtion between 2 points '''
        return self.evaluate(upper) - self.evaluate(lower)

    def __pow__(self, other):
        if isinstance(other, Number):
            return Power(self, other)
        else:
            return NotImplemented

class Fraction(Function):
    def __init__(self, abscissa, numerator, denominator):
        assert(abscissa == numerator.abscissa == denominator.abscissa)
        self.numerator = numerator
        self.denominator = denominator
        Function.__init__(self, abscissa)

    def __str__(self):
        return '(' + str(self.numerator) + ') / (' + str(self.denominator) + ')'
        
#    def __mul__(self, other):
#        if isinstance(other,Fraction):
#            pass
#        else:
#            return Fraction(self.abscissa, self.numerator*other, self.denominator)
#    __rmul__ = __mul__

    def __mul__(self,other):
        if isinstance(other, Polynomial):
            return (self.numerator * other) / self.denominator
        else:
            return NotImplemented
    __rmul__ = __mul__

    def evaluate(self, x):
        return self.numerator.evaluate(x) / self.denominator.evaluate(x)

#    def roots(self, n=100):
#        return numerator.roots(n) + denominator.roots(n)

    def simplify(self):
        def areclose(a,b):
            ''' Determines whether 2 possibly complex numbers or Polynomials are
            aproximately equal '''
            r = lambda x: -x.terms[1].coefficient if isinstance(x, Polynomial) else x
            c = complex(r(a)) - complex(r(b))
            return abs(c.real) < 0.01 and abs(c.imag) < 0.01
            
        # Simplify a fraction of polynomials by removing the union of their
        # factors from the numerator and denominator
        # - should eventially be replaced a combination of greatest common
        # denominator algorithm and long division
        
        a = self.numerator.factors(); b = self.denominator.factors()
        
        moves = 0
        
        i = 0
        while i < len(a._factors):
            j = 0
            while j < len(b._factors):  
                if areclose(a._factors[i], b._factors[j]):
                    del a._factors[i]; del b._factors[j]
                    j -= 1; i -= 1; moves += 1
                j += 1
            i += 1
        
        if moves == 0:
            # Only reform object if no simplifications have been made; otherwise
            # this would recurse infinitely.
            return self
        else:       
            return a.simplify() / b.simplify()

#        power = lambda t: t.power
#        a = Polynomial(self.abscissa); b = Polynomial(self.abscissa)
#        lowest_power = min(map(power, self.numerator.terms + self.denominator.terms))
#        reduce_power = lambda t: t / Term(1, self.abscissa, lowest_power)
#        a.terms = list(map(reduce_power, self.numerator.terms)) 
#        b.terms = list(map(reduce_power, self.denominator.terms))
#        b.sort_terms()
#        if b.order() == 0:
#            return a / b.terms[0].coefficient
#        return Fraction(self.abscissa, a.simplify(), b.simplify())

    def differential(self):
        ''' Making use of the quotient rule,
        if f(x) = g(x) / h(x)
        then f'(x) = ( g'(x)*h(x) - h'(x)*g(x) ) / h(x)^2 '''
        return ((self.numerator.differential()*self.denominator - self.denominator.differential()*self.numerator)
            / self.denominator**2).simplify()

    def as_gnuplot_expression(self):
        return '(' + self.numerator.as_gnuplot_expression() + ') / ('\
            + self.denominator.as_gnuplot_expression() + ')'

class Product(Function, core.Product):
    def __init__(self, abscissa, *factors):
        Function.__init__(self, abscissa)
        core.Product.__init__(self, *factors)
        
    def __str__(self):
        bracket = lambda a: ('(%s)' if isinstance(a, Polynomial) else '%s')\
            % str(a)
        return ' * '.join(map(bracket, self._factors))
        
#    def sort_terms(self):
#        if (isinstance(self.h, Power) ^ isinstance(self.g, Power)):
#            if isinstance(self.g, Power):
#                self.g, self.h = self.h, self.g

#    def __mul__(self, other):
#        return Product(self.abscissa, self.g*other, self.h)


class Power(Function):
    def __init__(self, function, power):
        super().__init__(function.abscissa)
        self.function = function
        self.power = handle_type(power)

    def __str__(self):
        return '(' + str(self.function) + ')^' + str(self.power)

    def __mul__(self, other):
        return Product(self.abscissa, self, other)
    __rmul__ = __mul__

    def __eq__(self, other):
        if isinstance(other, Power):
            return self.function == other.function and self.power == other.power

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
        '''  '''
        assert(isinstance(a, Function) or isinstance(b, Function))
        self.a = a; self.b = b
        if isinstance(a, Function) and isinstance(b, Function) and a.abscissa != b.abscissa:
            raise ValueError('Both functions must be in the same variable')
        self.abscissa = a.abscissa if isinstance(a,Function) else b.abscissa

    def __repr__(self):
        ''' Convert to string '''
        return str(self.a) + ' = ' + str(self.b)

    def roots(self, n=100):
        ''' Return all solutions of the quality '''
        return (self.a - self.b).simplify().roots(n)


class Term(Function):
    ''' A class holding a polynomial term '''
    def __init__(self, coefficient, abscissa, power):
        self.coefficient = handle_type(coefficient)
        self.power = handle_type(power)
        super().__init__(abscissa)

    def __str__(self):
        ''' Output the term nicely via assorted logic '''
        s = lambda a: print_complex(a) if isinstance(a, complex) else str(+a)
        if self.coefficient == 0: return '0'
        else: return \
            (s(self.coefficient)
                if self.coefficient != 1 or self.power == 0 else ''
                if self.coefficient != -1 else '-')\
            + (self.abscissa if self.power != 0 else '')\
            + ('^' + str(self.power) if 0 != self.power != 1 else '')

    def simplify(self):
        if self.coefficient == 0:
            return Term(0, self.abscissa, 0)
        else:
            return self

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
        ''' The roots of ax^n are n zeros as it is already fully factorized '''
        return [0 for i in range(self.power)]

    def integral(self):
        ''' Return the indefinite integral '''
        if self.coefficient == 0:
            return Constant()
        else:
            return Term(self.coefficient/(self.power + 1),
                self.abscissa, self.power + 1)

    def evaluate(self, x):
        ''' Returns the value of the term for x '''
        if self.power == 0:
            return self.coefficient
        else:
            return self.coefficient * handle_type(x) ** self.power

    def __eq__(self, other):
        ''' Compare whether 2 terms are equal '''
        other = self._convert_other(other)
        if other == NotImplemented:
            return other

        a = self.simplify(); b = other.simplify()

        return a.coefficient == b.coefficient\
            and a.abscissa == b.abscissa\
            and a.power == b.power

    def __repr__(self):
        ''' Print a representation of the term '''
        return "Term(%s, '%s', %s)"\
            % (self.coefficient, self.abscissa, self.power)

    def __neg__(self):
        ''' Return a copy of the term with its coefficient inverted '''
        a = deepcopy(self); a.coefficient *= -1
        return a
    invert = __neg__

    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other

        if self.abscissa == other.abscissa:
            return Term(self.coefficient*other.coefficient, self.abscissa, self.power+other.power)
        else:
            return ce.Term(self.coefficient*other.coefficient,
                ce.Factor(self.abscissa, self.power),
                ce.Factor(other.abscissa, other.power))
    __rmul__ = __mul__

    def _convert_other(self, other):
        if isinstance(other, Term):
            return other
        elif isinstance(other, Number):
            return Term(other, self.abscissa, 0)
        else:
            return NotImplemented

    def __truediv__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        return Term(self.coefficient/other.coefficient, self.abscissa, self.power-other.power)
    __rtruediv__ = __truediv__

    def __sub__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        return self + other.invert()
    __rsub__ = __sub__

    def __add__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        c = Polynomial(self.abscissa)
        c.terms = [self, other]
        c.sort_terms()
        return c + Polynomial(self.abscissa,0,0)
    __radd__ = __add__

    def __pow__(self, m):
        m = handle_type(m)
        if isinstance(m, Number):
            return Term(self.coefficient**m, self.abscissa, self.power*m)
        else:
            return NotImplemented

    def __gt__(self, other):
        if self.power != other.power:
            return self.power > other.power
        else:
            return self.coefficient > other.coefficient

    def as_gnuplot_expression(self):
        ''' Convert into the gnuplot format '''
        from re import sub
        expr = str(self)
        expr = sub(r'[a-z]', r'x', expr, 100)
        # Add * from multiplication
        expr = sub(r'([0-9])x', r'\1*x', expr, 100) 
        # Replace ^ with ** for powers
        expr = sub(r'\^', r'**', expr, 100) 
        return expr


class Polynomial(Function):
    ''' A class representing a polynomial '''
    # TODO: Consider renaming as it now accepts non-polynomials
    def __init__(self, abscissa, *nums):
        ''' Initiates the polynomial with a string containing the abscissa
        followed by pairs of coefficients and powers '''
        super().__init__(abscissa)
        self.terms = [ Term(a, abscissa, b) for a, b
            in zip(nums[::2], nums[1::2]) ]
        self.sort_terms()

    def __str__(self):
        ''' A list comprehension to combine the terms of the polynomial '''
        def term_str(a):
            if isinstance(a.coefficient, complex):
                if ('i' not in str(a)) and (str(a)[0] == '-'):
                    return '- ' + str(a)[1:]
                else:
                    return '+ ' + str(a)
            elif a.coefficient == 0:
                return ''
            else:
                return ('+', '-')[a.sign() == -1] + ' ' + str(abs(a))

        if len(self.terms) > 1:
            return ' '.join( [str(self.terms[0])] + list(map(term_str, self.terms[1:])) )
        elif len(self.terms) == 1:
            return str(self.terms[0])
        else:
            return ''
    __repr__ = __str__
    
    def __eq__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        return self.simplify().terms == other.simplify().terms

    def map_to_terms(self, f):
        ''' Allows list processing of terms '''
        y = Polynomial(self.abscissa)
        y.terms = list(map(f, self.terms))
        y.sort_terms()
        return y

    def differential(self):
        ''' Calculate the differential of the expression '''
        f = lambda x: x.differential()
        return (self.simplify().map_to_terms(f))

    def integral(self):
        ''' Calculate the indefinite integral of the expression
         - Integrate each term
         - Return a polynomial object based on the new terms '''
        f = lambda x: x.integral()
        a = self.map_to_terms(f)
        a.terms += [ Constant() ]
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
            
    def factors(self):
        def fact(a):
            ''' Returns a list of any valid factors of the coefficient a '''
            if a == 1:
                return []
            elif isinstance(a, Integer):
                return a.factors()._factors
            else:
                return [a]
            
        # TODO: tidy up this mess
        return Product(self.abscissa, 
            *(fact(self.terms[0].coefficient)
            + list(map(lambda a: Term(1,'x',1) - a, self.roots()))))

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
        power = lambda a: (a.power if a.coefficient != 0 else 0)\
            if isinstance(a, Term) else 0
        self.terms.sort(key=power, reverse=True)

    def simplify(self):
        self.sort_terms()
        result = Polynomial(self.abscissa)
        result.terms += [ self.terms[0] ]
        for i in range(1,len(self.terms)):
            if self.terms[i] != 0:
                if self.terms[i].power != result.terms[-1].power:
                    result.terms += [ self.terms[i] ]
                else:
                    result.terms[-1].coefficient += self.terms[i].coefficient
        return result

    def invert(self):
        return self.map_to_terms(lambda t: t.invert())

    def _convert_other(self, other):
        if isinstance(other, Polynomial):
            return other
        elif isinstance(other, Term):
            c = Polynomial(other.abscissa)
            c.terms = [ other ]
            return c
        elif isinstance(other,Integer) or isinstance(other,Decimal):
            return Polynomial(self.abscissa, other, 0)
        else:
            return NotImplemented

    def __sub__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        return self + other.invert()
    __rsub__ = __sub__

    def __add__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        c = Polynomial(self.abscissa)
        c.terms = self.terms + other.terms
        return c.simplify()
    __radd__ = __add__

    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other

        terms = []
        for l in self.terms:
            for m in other.terms:
                terms += [ l * m ]
        if reduce(lambda a, b: a and b, map(lambda t: isinstance(t, Term), terms)):
            c = Polynomial(self.abscissa); c.terms = terms
            return c.simplify()
        else:
            conv = lambda a: a if isinstance(a, ce.Term) else ce.Term(a.coefficient, Factor(a.abscissa, a.power))
            return ce.Polynomial(*map(conv, terms))
    __rmul__ = __mul__

    def __truediv__(self, other):
        if isinstance(other, Polynomial):
            return Fraction(self.abscissa, self, other).simplify()
        elif isinstance(other, Integer) or isinstance(other, Decimal):
            c = Polynomial(self.abscissa)
            for l in self.terms:
                c.terms += [ l / other ]
            return c.simplify()
        elif isinstance(other, Term):
            return self / self._convert_other(other)
        else:
            return NotImplemented
    #__rtruediv__ = __truediv__
    
    def __rtruediv__(self, other):
        if isinstance(other, Term):
            return self._convert_other(other) / self
        elif isinstance(other, Integer):
            return self._convert_other(other) / self
        else:
            return NotImplemented

    def __pow__(self, m):
        if m == 0:
            return 1
        elif (isinstance(m, Integer) or isinstance(m, int)) and m > 1:
            return reduce(lambda a,b: a * b, [self for i in range(m)])
        elif isinstance(m, Decimal) or m < 1:
            return Power(self, m)
        else:
            return NotImplemented
        
    def as_gnuplot_expression(self):
        ''' Convert into the gnuplot format '''
        from re import sub
        expr = str(self)
        expr = sub(r'[a-z]', r'x', expr, 100)
        # Add * from multiplication
        expr = sub(r'([0-9])x', r'\1*x', expr, 100) 
        # Replace ^ with ** for powers
        expr = sub(r'\^', r'**', expr, 100) 
        return expr
        

if __name__ == '__main__':
    import doctest
    getcontext().prec = 3
    doctest.testmod()
