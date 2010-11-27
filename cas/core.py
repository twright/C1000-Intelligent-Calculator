#!/usr/bin/env python3.1
''' Provides core types/classes from use throughout the Computer Algebra
System representing simple objects such as Integers and Constants
whilst providing functions to allocate types. '''

from decimal import Decimal, getcontext, localcontext
import re
from functools import reduce, partial
from operator import add, mul
from copy import copy, deepcopy
from numbers import Number

from dmath import pi
import cas.numerical_methods as nm

m_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_brackets') and a._brackets['m'] else str(a)
d_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_brackets') and a._brackets['d'] else str(a)
p_str = lambda a: '(' + str(a) + ')' if hasattr(a, '_brackets') and a._brackets['p'] else str(a)
evaluate = lambda y, x, variable=None: y(x, variable) if hasattr(y, '__call__') else y

def handle_type (x):
    from cas.numeric import Integer, Complex, Real
    ''' Takes in a variable a and output it in the most desirable type '''
    if isinstance(x, Integer) or isinstance(x, Real)\
        or isinstance(x,Complex): #or isinstance(x, Constant):
        return x
    elif isinstance(x, int):
        return Integer(x)
    elif isinstance(x, Decimal):
        return Real(x)
    elif isinstance(x, str) and re.match(r'^[0-9]+$', x):
        return Integer(x)
    elif isinstance(x, float):
        return +Real(repr(x))
    elif isinstance(x, complex):
        if abs(x.imag) < 0.0001:
            return +Real.from_float(x.real)
        else:
            return Complex(x)
    else:
        return x

def expand(a):
    if isinstance(a, Sum):
        return sum(map(expand, a))
    elif isinstance(a, Product) and len(a) == 2 and isinstance(a[1], Sum):
        return sum(map(lambda b: a[0] * b, a[1]))
    elif isinstance(a, Product) and len(a) > 2:
        return expand(a[0] * expand(a[1:]))
        #return reduce(add,map(lambda b: expand(a[-1]) * b, a[:-1]),0)
        #reduce(mul,map(lambda b: a[0]*b,a[1:]),1)
    else:
        return a

def is_poly(a):
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
    pd = partial(partial_differential, x=x)
    if isinstance(y,Number):
        return 0
    elif isinstance(y,Symbol):
        return 1 if y == x else y
    elif isinstance(y,Sum):
        return reduce(add, map(pd, y), 0)
    elif isinstance(y,Product) and is_poly(y):
        return y[0] * pd(y[1])
    elif isinstance(y,Power) and is_poly(y):
        return y.b() * pd(y.a()) * (y.a() ** (y.b() + (-1)))
    else:
        return NotImplemented
        
def partial_integral(y, x):
    return _partial_integral(x,y) + Symbol('c')
        
def _partial_integral(y, x):
    pi = partial(partial_integral, x=x)
    if isinstance(y,Number):
        return y*x
    elif isinstance(y,Symbol):
        return (1/2) * (x ** 2)
    elif isinstance(y,Sum):
        return reduce(add, map(pi, y), 0)
    elif isinstance(y,Product) and is_poly(y):
        return y[0] * pi(y[1])
    elif isinstance(y,Power) and is_poly(y):
        return ( 1 / (y.b() + 1) ) * (y.a()) ** (y.b() + 1)
    else:
        return NotImplemented
        
class Algebra:
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
    
    def __neg__(self):
        return (-1) * self
    
    def __pow__(self, other):
        return self if other == 1 else 1 if other == 0 else Power(self, other)
        
    def numerical_integral(self, method, a, b, *n):
        f = lambda x: float(self(x))
        return Decimal.from_float(method(f, float(a), float(b), *n)).normalize()
        
    def trapezoidal_integral(self, *a):
        return self.numerical_integral(nm.trapezoidal_composite_integral, *a)
        
    def romberg_integral(self, *a):
        return self.numerical_integral(nm.romberg_integral, *a)

class Symbol(Algebra):
    def __init__(self, name):
        assert isinstance(name, str)
        self.__name = name
        
    def __call__(self, x, variable=None):
        if variable in (self, None):
            return x
        else:
            return self
        
    def __eq__(self, other):
        return str(self) == str(other)
        
    def __mul__(self, other):
        return self ** 2 if self == other\
        else Algebra.__mul__(self, other) if isinstance(other, Symbol)\
        or isinstance(other, Number)\
        else NotImplemented
    
    __rmul__ = __mul__
        
    def __repr__(self):
        return str(self.__name)
        
    _brackets = {'m':0,'d':0,'p':0}

def dedup(f, xs, identity):
    # print(list(map(type, xs)))
    def can_simplify(a, b):
        I = isinstance
        if I(a, Number) and I(b, Number):
            return True
        elif I(a, Symbol) and I(b, Symbol) and a == b:
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
        # TODO: This bit really needs replacing with something alot more robust
        # print(list(xs), f)
        if can_simplify(prev, xs[i]):
            prev = f(prev, xs[i])
        else:
            if prev != identity: yield prev
            prev = xs[i]
        i += 1
    if prev != identity: yield prev

class Product(Algebra):
    def __init__(self, *a):
        order_type = lambda a: (1*isinstance(a, Number) + 2*isinstance(a, Symbol)
            + 3*isinstance(a, Power) + 4*isinstance(a, Product)
            + 5*isinstance(a, Sum))
        order = lambda a: 10000*order_type(a)\
            + (ord(str(a)) if isinstance(a, Symbol)
            else ord(str(a.a())) if isinstance(a, Power) and isinstance(a.b(), Symbol)
            else 100)
        terms = sorted(a, key=order)
        self.__terms = list(dedup(mul, terms, 1))
        
    def __call__(self, x, variable=None):
        ev = partial(evaluate, variable=variable, x=x)
        return reduce(mul, map(ev, self), 1)
        
    def __getitem__(self, i):
        if isinstance(i, slice):
            return reduce(mul, self.__terms[i], 1)
        else:
            return self.__terms[i]
        
    def order(self):
        return max(map(lambda a: a.order() if hasattr(a,'order') else 0, self))
        
    def __len__(self):
        return len(self.__terms)
    
    def __repr__(self):
        return ''.join(map(m_str, self))
        
    _brackets = {'m':0,'d':1,'p':1}
    
    def __mul__(self, other):
        return Product(*(list(self) + list(self._convert(other))))
        
    __rmul__ = __mul__
        
    def __add__(self, other):
        # TODO: Replace with something more general
        if isinstance(other, self.__class__) and len(self) == len(other) == 2\
            and self[1] == other[1]:
            return Product(self[0] + other[0], self[1])
        else:
            return Algebra.__add__(self, other)
        
    def _convert(self, other):
        return other if isinstance(other, self.__class__) else self.__class__(other)
        
def Fraction(Algebra):
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

class Sum(Algebra):
    def __init__(self, *a):
        I = isinstance
        order_type = lambda a: (1*I(a,Power) + 2*I(a,Product) + 3*I(a,Symbol) 
            + 4*I(a,Number))
        order = lambda a: 10000 * order_type(a) - (a.order() if hasattr(a,'order') else 100)
        terms = sorted(a, key=order)
        self.__terms = list(dedup(add, terms, 0))
        
    def __call__(self, x, variable=None):
        return reduce(lambda a,b: evaluate(a,x,variable) + evaluate(b,x,variable), self, 1)
            
    def __getitem__(self, i):
        if isinstance(i, slice):
            return reduce(add, self.__terms[i], 0)
        else:
            return self.__terms[i]
        
    def __len__(self):
        return len(self.__terms)
            
    def __add__(self, other):
        return Sum(*(list(self) + list(self._convert(other))))
        
    def order(self):
        return max(map(lambda a: a.order() if hasattr(a,'order') else 0, self))
        
    def _convert(self, other):
        return other if isinstance(other, self.__class__) else self.__class__(other)
        
    def __repr__(self):
        def sf(a):
            if isinstance(a, Product) and isinstance(a[0], Number):
                return ' ' + ('-' if a[0] < 0 else '-') + ' ' + str(abs(a[0]) * a[1:])
            elif isinstance(a, Number):
                return ' ' + ('-' if a < 0 else '+') + ' ' + str(abs(a))
            else:
                return ' + ' + str(a)

        listify = lambda a: list(a) if isinstance(a, Sum) else [a]

        return str(self[0]) + ''.join(map(sf, listify(self[1:])))
        #return ' + '.join(map(str, self))
        
    _brackets = {'m':1,'p':1,'d':1}
    
class Power(Algebra):
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
            else Algebra.__mul__(self, other) if not isinstance(other, Algebra)\
            else NotImplemented
            
    __rmul__ = __mul__
        
    def __repr__(self):
        return p_str(self.__a) + '^' + p_str(self.__b)

class List():
    def __init__(self, *a):
        self.values = list(map(handle_type, a))

    def __str__(self):
        return ', '.join(map(str, self.values))

class StrWithHtml():
    ''' An extended string also holding a html version '''
    # TODO: Extend concept to any object with a .html() method
    def __init__(self, plain, html):
        self.plain, self.html = str(plain), str(html)
    def __str__(self):
        return str(self.plain)
