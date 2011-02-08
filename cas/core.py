#!/usr/bin/env python3.1
''' Provides core types/classes from use throughout the Computer Algebra
System representing simple objects such as Symbol, Products, Sums and Fractions
whilst providing functions to allocate types. '''
from __future__ import division, unicode_literals
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import re
from decimal import Decimal
from functools import reduce, partial
from operator import add, mul
from numbers import Number

import dmath
import math
import cas.numerical_methods as nm
#from cas.matrices import Matrix

# Convert object to strings based on their precedence
#m_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_brackets') and a._brackets['m'] else ('*' if isinstance(a, Function) else '') + str(a)
m_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_hints') and 'm' in a._hints else str(a)
m_str.__doc__ = ''' Convert an object to a string within the context of a product '''
d_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_hints') and 'd' in a._hints else str(a)
d_str.__doc__ = ''' Convert an object to a string within the context of a fraction '''
p_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_hints') and 'p' in a._hints else str(a)
p_str.__doc__ = ''' Convert an object to a string within the context of indices '''
a_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_hints') and 'a' in a._hints else str(a)
a_str.__doc__ = ''' Convert an object to a string within the context of a sum '''
order = lambda a: a.order() if hasattr(a, 'order') else 0
order.__doc__ = ''' Return the order of an equation '''
evaluate = lambda y, x, variable=None: y(x, variable) if hasattr(y, '__call__') else y
evaluate.__doc__ = ''' Evaluate y at x '''

def handle_type (x):
    ''' Takes in a variable (x) and output it in the most desirable type '''
    from cas.numeric import Integer, Complex, Real
    if isinstance(x, Integer) or isinstance(x, Real) or isinstance(x,Complex):
        return x
    elif isinstance(x, int):
        return Integer(x)
    elif isinstance(x, Decimal):
        return Real(x)
    elif isinstance(x, str) and re.match(r'^[0-9]+$', x):
        return Integer(x)
    elif isinstance(x, str) and re.match(r'^[0-9]+\.[0-9]+$', x):
        return Real(x)
    elif isinstance(x, float):
        return +Real(repr(x))
    elif isinstance(x, complex):
        if abs(x.imag) < 0.0001:
            return +Real.from_float(x.real)
        else:
            return Complex(x)
    else:
        return x
ht = handle_type

def expand(a):
    ''' Fully expand an equation '''
    if isinstance(a, Sum):
        return sum(map(expand, a))
    elif isinstance(a, Product) and len(a) == 2 and isinstance(a[1], Sum):
        return sum(map(lambda b: expand(a[0] * b), a[1]))
    elif isinstance(a, Product) and len(a) > 2:
        return expand(a[0] * expand(a[1:]))
    else:
        return a

def is_poly(a):
    ''' Determine whether an equation is in a polynomial-like form '''
    if isinstance(a,(Symbol, Number)):
        return True
    elif isinstance(a,Sum):
        return reduce(lambda a,b: a and b, map(is_poly, a))
    elif isinstance(a,Product) and len(a) == 2:
        return is_poly(a[0]) and is_poly(a[1])
    elif isinstance(a,Power):
        return isinstance(a.a(), Symbol) and isinstance(a.b(), Number)
    else:
        return False

def partial_differential(y, x):
    ''' Return the partial differential of y with respect to x '''
    pd = partial(partial_differential, x=x)
    if isinstance(y,Number):
        return 0
    elif hasattr(y, 'partial_differential'):
        return y.partial_differential(x)
    elif isinstance(y,Ln):
        return pd(y.x()) / y.x()
    elif isinstance(y,Sin):
        return pd(y.x()) * Cos(y.x())
    elif isinstance(y,Cos):
        return pd(y.x()) * -Sin(y.x())
    elif isinstance(y,Tan):
        return pd(y.x()) / Cos(y.x())**2
    else:
        return NotImplemented

def _partial_integral(y, x):
        ''' A recursive function to perform the actual integration'''
        ht = handle_type
        assert isinstance(x, Symbol)
        if isinstance(y,Number):
            return y*x
        elif hasattr(y, 'partial_integral'):
            return y.partial_integral(x)
        else:
            return NotImplemented

def partial_integral(y, x):
    ''' Return the partial integral of y with respect to x '''
    # Expand the expression and add + c
    I = expand(_partial_integral(y,x))
    return I + Symbol('c') if I != NotImplemented else NotImplemented

class Algebra (object):
    ''' A class to hold an arbitrary algebraic expression; the superclass of all
    algebraic classes '''
    def __add__(self, other):
        return self if other == 0 else 2 * self if self == other else Sum(self, other)

    __radd__ = __add__

    def __sub__(self, other):
        return self + (-other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        return self if other == 1 else handle_type(0) if other == 0 else Product(self, other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return self if other == 1 else ht(1) if self == other\
            else Fraction(self, other)

    def __rtruediv__(self, other):
        return handle_type(0) if other == 0 else Fraction(other, self)

    def __neg__(self):
        return (-1) * self

    def __pow__(self, other):
        return self if other == 1 else 1 if other == 0 else Power(self, other)

    def numerical_integral(self, method, a, b, *n):
        ''' Numerically integrate between b and a using the specified method '''
        f = lambda x: float(self(x))
        return Decimal.from_float(method(f, float(a), float(b), *n)).normalize()

    def trapezoidal_integral(self, *a):
        ''' Numerically integrate via the trapezium rule '''
        return self.numerical_integral(nm.trapezoidal_composite_integral, *a)

    def simpson_integral(self, *a):
        ''' Numerically integrate via the trapezium rule '''
        return self.numerical_integral(nm.simpson_composite_integral, *a)

    def romberg_integral(self, *a):
        ''' Numerically integrate using Romberg's method (this is the most
        accurate method currently supported) '''
        return self.numerical_integral(nm.romberg_integral, *a)

    def limit(self, a, b, variable=None):
        ''' Take the limit between a and b '''
        return expand(self(b, variable=variable) - self(a, variable=variable))

    def as_gnuplot_expression(self):
        ''' Convert into the gnuplot format '''
        # TODO: Replace with something much more general
        from re import sub
        expr = str(self)
        expr = sub(r'[a-z]', r'x', expr, 100)
        # Add * from multiplication
        expr = sub(r'([0-9])x', r'\1*x', expr, 100)
        # Add * for bracket multiplication
        expr = sub(r'([^/ ])\(', r'\1*(', expr, 100)
        # Replace ^ with ** for powers
        expr = sub(r'\^', r'**', expr, 100)
        return expr

class Symbol(Algebra):
    ''' A class representing the variables in algebraic expressions '''
    def __init__(self, name):
        ''' A variable is defined in terms of its name '''
        assert isinstance(name, (str, unicode))
        self.__name = str(name)

    def __call__(self, x, variable=None):
        ''' A variable may take a numeric value when evaluated '''
        return x if variable in (self, None) else self

    def __eq__(self, other):
        ''' Variables of the same name are identical '''
        return str(self) == str(other)

    def __mul__(self, other):
        return self ** 2 if self == other\
        else Algebra.__mul__(self, other) if isinstance(other, Symbol)\
        or isinstance(other, Number)\
        else NotImplemented

    __rmul__ = __mul__

    def __rtruediv__(self, other):
        ''' a/x = ax^-1'''
        return other * self ** handle_type(-1)

    def order(self):
        ''' The order of a variable is one '''
        return 1

    def partial_differential(self, x):
        ''' Return the partial differential with respect to x. '''
        return ht(1) if self == x else y

    def partial_integral(self, x):
        ''' Return the partial integral with respect to x. '''
        return (ht(1)/ht(2)) * (x ** ht(2))

    def __repr__(self):
        ''' Display a variable in string form '''
        return str(self.__name)

    # This set identifies in which circumstances an expression needs to be
    # surrounded by brackets
    _hints = {}

def dedup(f, xs, identity):
    ''' Combine any elements possible in a sum or product.
    f   - the basic operation underlying the list (i.e. add, mul)
    xs  - the list of elements
    identity - the elements which when present in the list, does not change the
        list's overall value (i.e. 1 is the multiplicative identity)'''
    def can_simplify(a, b):
        ''' Determine whether calling f on two variable will result in a single
        element within the list. If f is called with this not being the case,
        it will infinitely recurse. '''
        # TODO: This bit really needs replacing with something much more robust
        I = isinstance
        if I(a, Number) and I(b, Number):
            return True
        elif I(a, Symbol) and I(b, Symbol) and a == b:
            return True
        elif I(a, Product) and I(b, (Symbol,Power)) and len(a) == 2 and a[1] == b:
            return True
        elif I(a, Product) and I(b, Product) and len(a) == len(b) == 2\
            and a[1] == b[1]:
            return True
        elif identity == 1 and I(a, Power) and I(b, Power) and a.a() == b.a():
            return True
        else:
            return False

    i = 1; prev = xs[0]
    while i < len(xs):
        if can_simplify(prev, xs[i]):
            prev = f(prev, xs[i])
        else:
            if prev != identity: yield prev
            prev = xs[i]
        i += 1
    if prev != identity or len(xs) == 1: yield prev

class Product(Algebra):
    ''' A class representing the product of multiple elements '''
    def __new__(self, *a):
        # Order the elements based upon their type and position within the alphabet,
        # to ensure the order is always deterministic
        I = isinstance
        rank_type = lambda a: (1*I(a, Number) + 2*I(a, Symbol) + 3*I(a, Power)
            + 4*I(a, Product) + 5*I(a, Sum) + 6*I(a, Function))
        rank = lambda a: 10000*rank_type(a) + (ord(str(a)) if I(a, Symbol)
            else ord(str(a.a())) if I(a, Power) and I(a.b(), Symbol)
            else 100)

        terms = list(dedup(mul, sorted(a, key=rank), 1))
        if len(terms) > 1 and terms[0] != 0:
            b = Algebra.__new__(self); b.__terms = terms
            return b
        else:
            # For the product of 1 element, just return that element
            return terms[0]

    def __call__(self, x, variable=None):
        ''' Evaluate self which variable is equal to x. '''
        ev = partial(evaluate, variable=variable, x=x)
        return reduce(mul, map(ev, self), 1)

    def __getitem__(self, i):
        ''' Return the term(s) at/in position or range i. '''
        if isinstance(i, slice):
            return reduce(mul, self.__terms[i], 1)
        else:
            return self.__terms[i]

    def order(self):
        ''' A method returning the order of a product. '''
        assert len(self) == 2
        return max(map(lambda a: a.order() if hasattr(a,'order') else 0, self))

    def __len__(self):
        ''' A method returning the length of a product. '''
        return len(self.__terms)

    def __eq__(self, other):
        ''' Products are equal if all terms are equal. '''
        listify = lambda a: list(a) if hasattr(a, '__getitem__') else [a]
        return listify(self) == listify(other)

    def __repr__(self):
        ''' Return the string representation of the product. '''
        return ('-' if isinstance(self[0], Number) and self[0] == -1 else m_str(self[0]))\
            + (''.join(map(m_str, self[1:])) if len(self) > 2 else m_str(self[1]))

    _hints = {'d','p'}

    def __mul__(self, other):
        return Product(*(list(self) + (list(other) if isinstance(other, Product) else [other])))

    __rmul__ = __mul__

    def __add__(self, other):
        # TODO: Replace with something more general
        if isinstance(other, self.__class__) and len(self) == len(other) == 2\
            and self[1] == other[1]:
            return Product(self[0] + other[0], self[1])
        elif isinstance(self, Product) and isinstance(other, (Symbol,Power))\
            and len(self) == 2 and self[1] == other:
            return Product(self[0] + handle_type(1), self[1])
        else:
            return Algebra.__add__(self, other)

    def partial_differential(self, x):
        ''' Return the partial differential with respect to x. '''
        if is_poly(self):
            return self[0] * partial_differential(self[1],x)
        else:
            return NotImplemented

    def partial_integral(self, x):
        ''' Return the partial integral with respect to x. '''
        if is_poly(self):
            return self[0] * _partial_integral(self[1], x)
        else:
            return NotImplemented


class Fraction(Algebra):
    ''' A class representing a fraction. '''
    def __init__(self, a, b):
        self.__numerator, self.__denominator = a, b

    def numerator(self):
        return self.__numerator

    def denominator(self):
        return self.__denominator

    def order(self):
        return order(self.numerator())

    def __repr__(self):
        return d_str(self.numerator()) + '/' + d_str(self.denominator())

    def partial_differential(self, x):
        ''' Return the partial differential with respect to x. '''
        # Quotant rule
        (partial_differential(self.numerator(),x)*self.denominator()
            - partial_differential(self.denominator(),x)*self.numerator())\
            / self.denominator()**2
            
    def __call__(self, x, variable=None):
        ''' Evaluate the fraction when variable = x '''
        return self.numerator()(x, variable) / self.denominator()(x, variable)

    _hints = {'m','d','p'}

class Sum(Algebra):
    ''' A class representing the sum of multiple terms. '''
    def __new__(self, *a):
        I = isinstance
        # Order elements based on type and order to insure the order is always
        # deterministic.
        rank_type = lambda a: (2*I(a,Power) + 2*I(a,Product) + 3*I(a,Symbol)
            + 4*I(a,Number))
        rank = lambda a: 10000 * rank_type(a) - (a.order() if hasattr(a,'order') else 100)

        terms = list(dedup(add, sorted(a, key=rank), ht(0)))
        if len(terms) > 1:
            b = Algebra.__new__(self); b.__terms = terms
            return b
        else:
            # For the sum of one element, just return that element
            return terms[0]

    def __call__(self, x, variable=None):
        ''' Evaluate self when variable is equal to x. '''
        return reduce(lambda a,b: evaluate(a,x,variable) + evaluate(b,x,variable), self, 0)

    def __getitem__(self, i):
        ''' Return the term(s) at/in position or range i. '''
        if isinstance(i, slice):
            return reduce(add, self.__terms[i], 0)
        else:
            return self.__terms[i]

    def __len__(self):
        return len(self.__terms)

    def __add__(self, other):
        return Sum(*(list(self) + (list(other) if isinstance(other, Sum) else [other])))

    def order(self):
        ''' Return the greatest order of any term. '''
        return max(map(lambda a: a.order() if hasattr(a,'order') else 0, self))

    def __eq__(self, other):
        ''' Products are equal if all terms are equal '''
        listify = lambda a: list(a) if hasattr(a, '__getitem__') else [a]
        return listify(self) == listify(other)

    def __repr__(self):
        ''' Return the string representation of the sum. '''
        def sf(a):
            if isinstance(a, Product) and isinstance(a[0], complex):
                return ' ' + ('- ' + m_str(handle_type(abs(a[0].imag)) if a[0].real > -0.00001 else -a[0])
                    if a[0].imag < 0 and a[0].real < 0.00001 else '+ ' + m_str(a[0])) + m_str(a[1:])
            if isinstance(a, Product) and isinstance(a[0], Number):
                return ' ' + ('-' if a[0] < 0 else '+') + ' ' + str(abs(a[0]) * a[1:])
            elif isinstance(a, complex):
                return ' ' + ('- ' + a_str(handle_type(abs(a.imag)) if a.real > -0.00001 else -a)
                    if a.imag < 0 and a.real < 0.00001 else '+ ' + a_str(a))
            elif isinstance(a, Number):
                return ' ' + ('-' if a < 0 else '+') + ' ' + a_str(abs(a))
            else:
                return ' + ' + a_str(a)

        listify = lambda a: list(a) if isinstance(a, Sum) else [a]

        return str(self[0]) + ''.join(map(sf, listify(self[1:])))

    _hints = {'m','p','d','a'}

    def roots(self, n=1000):
        ''' The Fundermental Theorum of Algebra states that a polynomial of
        order m will have m complex roots. This function will numerically locate  
        them using n iterations of the Durand-Kerner method and return them
        as a List. '''
        from cas.numeric import Complex
        assert is_poly(self)
        assert isinstance(n, int)
        
        # For order 1 polynomials there is only 1 trivial root
        if order(self) == 1:
            return [ - self[1] ] if isinstance(self[0], Symbol)\
                else [ - self[1] / self[0][1] ]

        # Scale the equation such that the leading coefficient is zero
        g = expand(self if isinstance(self[0], (Symbol, Power))\
            else self * (1 / self[0][0]))

        # Invoke the Durand-Kerner method
        f = lambda x: complex(g(x))
        roots = nm.durand_kerner_roots(f, self.order(), n)
        return map(Complex, roots)

    def factors(self):
        ''' Return a polynomial equation as the product of its irreducible
        factors '''
        if is_poly(self):
            a = 1 if isinstance(self[0], (Symbol, Power)) else self[0][0]
            x = self[0] if isinstance(self[0], Symbol)\
                else self[0].a() if isinstance(self[0], Power)\
                else self[0][1] if isinstance(self[0][0], Symbol)\
                else self[0].a()
            return a * reduce(mul, map(lambda c: x - c, self.roots()), 1)
        else:
            return NotImplemented

    def partial_differential(self, x):
        ''' Return the partial differential with respect to x. '''
        return reduce(add, map(partial(partial_differential,x=x), self), 0)

    def partial_integral(self, x):
        ''' Return the partial integral with respect to x. '''
        return reduce(add, map(partial(_partial_integral, x=x), self), ht(0))

class Power(Algebra):
    ''' A class representing a to the power b. '''
    def __init__(self, a, b):
        self.__a = a
        self.__b = b

    def __call__(self, x, variable=None):
        ev = partial(evaluate, variable=variable, x=x)
        return ev(self.a()) ** ev(self.b())

    def a(self):
        return self.__a

    def b(self):
        return self.__b

    order = b

    def __eq__(self, other):
        return self.a() == other.a() and self.b() == other.b()\
            if isinstance(other, self.__class__) else False

    def __mul__(self, other):
        return Power(self.a(), self.b() + other.b()) if isinstance(other, self.__class__) \
            and self.a() == other.a()\
            else self.a() ** (self.b() + handle_type(1)) if self.a() == other\
            else Algebra.__mul__(self, other) if not isinstance(other, Algebra)\
            else NotImplemented

    __rmul__ = __mul__

    def partial_differential(self, x):
        ''' Return the partial differential with respect to x. '''
        if is_poly(self):
            return self.b() * partial_differential(self.a(),x) * (self.a() ** (self.b() + ht(-1)))
        else:
            return NotImplemented

    def partial_integral(self, x):
        ''' Return the partial integral with respect to x. '''
        if is_poly(self):
            return ( ht(1) / (self.b() + ht(1)) ) * self.a() ** (self.b() + ht(1))
        else:
            return NotImplemented

    def __repr__(self):
        return p_str(self.__a) + '^' + p_str(self.__b)

class Function(Algebra):
    ''' A class representation a function of an algebraic expression '''
    def __init__(self, name, argument, action=None):
        assert isinstance(name, (str, unicode))
        self.__name = str(name)
        self.__argument = argument
        self.__action = action

    def x(self):
        ''' Return the expression the function is in terms of '''
        return self.__argument

    def __call__(self, x, variable=None):
        ''' Evaluate the function when variable is equal to x '''
        return self.__action(self.__argument(x, variable))

    def __repr__(self):
        ''' A string representation of the function '''
        return self.__name + '(' + str(self.__argument) + ')'

class Ln(Function):
    ''' A class representing the natural logarithm of an algebraic expression '''
    def __init__(self, argument):
        from cas.numeric import Integer
        Function.__init__(self, 'ln', argument, action=lambda x: dmath.log(x) if isinstance(x, (Decimal, Integer)) else math.log(x))

class Sin(Function):
    ''' A class representing the sine of an algebraic expression '''
    def __init__(self, argument):
        from cas.numeric import Integer
        Function.__init__(self, 'sin', argument, action=lambda x: dmath.sin(x) if isinstance(x, (Decimal, Integer)) else math.sin(x))

class Cos(Function):
    ''' A class representing the cosine of an algebraic expression '''
    def __init__(self, argument):
        from cas.numeric import Integer
        Function.__init__(self, 'cos', argument, action=lambda x: dmath.cos(x) if isinstance(x, (Decimal, Integer)) else math.cos(x))

class Tan(Function):
    ''' A class representing the tangent of an algebraic expression '''
    def __init__(self, argument):
        from cas.numeric import Integer
        Function.__init__(self, 'tan', argument, action=lambda x: dmath.tan(x) if isinstance(x, (Decimal, Integer)) else math.tan(x))

class List():
    ''' A list type suitable for displaying variables '''
    def __init__(self, *a):
        self.__values = list(map(handle_type, a))

    def __getitem__(self, i):
        if isinstance(i, slice):
            return List(self.__values[i])
        else:
            return self.__values[i]

    def __str__(self):
        return ', '.join(map(str, self.__values))

class StrWithHtml():
    ''' An extended string also holding a html version '''
    def __init__(self, plain, html):
        self.plain, self.html = str(plain), str(html)

    def __str__(self):
        return str(self.plain)

