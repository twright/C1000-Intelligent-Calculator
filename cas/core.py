#!/usr/bin/env python3.1
''' Provides core types/classes from use throughout the Computer Algebra
System representing simple objects such as Integers and Constants
whilst providing functions to allocate types. '''

from decimal import Decimal
import re
from functools import reduce
from operator import mul
from copy import copy, deepcopy
from numbers import Number

from dmath import pi
import cas.numerical_methods as nm

def handle_type (x):
    ''' Takes in a variable a and output it in the most desirable type '''
    if isinstance(x, Integer) or isinstance(x, Real)\
        or isinstance(x,Complex) or isinstance(x, Constant):
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
        #    print('string:', repr(x.real))
            return +Real.from_float(x.real)
        else:
            return Complex(x)
    else:
        return +Real(x)

# Deprecated and replaced by Complex class
#def print_complex(a):
#    ''' Nicely print a complex number '''
#    r, i = +Decimal().from_float(a.real), +Decimal().from_float(a.imag)
#    if abs(r) < Decimal('0.001') and abs(i) < Decimal('0.001'): return '0'
#    elif abs(i) < Decimal('0.001'): return str(r)
#    elif abs(r) < Decimal('0.001'): return str(i) + 'i'
#    else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'i'

class Integer(int):
    ''' An extended integer class, providing better mathematical
    handling of integers '''
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, Decimal):
            if self % other == 0:
                return Integer(self // other)
            else:
                return Real(self) / Real(other)
        else:
            return NotImplemented
        # Exact representation of fractions would probably be preferable in
        # the long run.
        # elif isinstance(other, Integer):
        #    return Fraction(a,b)

    def __sub__(self, other):
        if isinstance(other, int):
            return Integer(int(self) - int(other))
        else:
            return NotImplemented

    def __pow__(self,other):
        if isinstance(other, int):
            return Integer(int(self)**int(other))
    #    if isinstance(other, Decimal):
    #        return Decimal(int(self)**other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, int):
            return Integer(int(other) - int(self))

    def __add__(self, other):
        if isinstance(other, int):
            return Integer(int(self) + int(other))
        else:
            return NotImplemented
    __radd__ = __add__

    def __mul__(self, other):
        if isinstance(other, int):
            return Integer(int(self) * int(other))
        else:
            return NotImplemented
    __rmul__ = __mul__
    
    def __pos__(self):
        return self

    def _factors(self):
        ''' Naively factorise an integer using trial division. '''
        a = self

        if a < 0:
            a = abs(a)
            yield Integer(-1)

        i = Integer(2)
        while a > 1:
            if a % i == 0:
                yield i
                a /= i
            else:
                i += 1

    def factors(self):
        return Product(*self._factors())

    def bracketed_str(self):
        return str(self)

class Real(Decimal):
    ''' A class to provide better handling of real numbers '''
    def __str__(self):
    
        # Print integers plainly
        if self == int(self): return str(int(self))
        
        # Show pi in full
        if self == pi(): return super().__str__()
    
        # Display small fractions as such
        a, b = nm.to_fraction(self)
        if abs(a) < 100 and b < 100: return '{}/{}'.format(a,b)
        
        # Display small fractional coefficients of pi in exact form
        # TODO: Fix this as it is extremely buggy
        q = self / pi(); a, b = nm.to_fraction(q, 10);
        if abs(a) < 100 and b < 100 or True: return '{}pi/{}'.format(a if a != 1 else '',b)
        
        # Otherwise display as a decimal
        return super().__str__()
        
    def __repr__(self):
        return "'" + super().__str__() + "'"
        
    def bracketed_str(self):
        return '(' + str(self) + ')'
    
    def __float__(self):
        return float(super().__str__())
        
    def __add__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__add__(other, context))
    __radd__ = __add__

    def __sub__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__sub__(other, context))

    def __rsub__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__rsub__(other, context))

    def __mul__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__mul__(other, context))
    __rmul__ = __mul__

    def __truediv__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__truediv__(other, context))

    def __rtruediv__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__truediv__(other, context))


    def __pow__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Real(super().__pow__(other))

    def __pos__(self, context=None):
        return Real(super().__pos__(context))
    
    def __neg__(self, context=None):
        return Real(super().__neg__(context))
        
    def __deepcopy__(self, memo=None):
        return Real(eval(repr(self)))
    __copy__ =  __deepcopy__
        
    def _convert_other(self, other):
        if isinstance(other, Real):
            return other
      #  elif isinstance(other, float):
      #      return 
        # Might break for Constant
        elif isinstance(other, Constant):
            return Real(0)
        elif isinstance(other, Number):
            return Real(other)
        else:
            return NotImplemented

class Complex(complex):
    ''' A class to provide better handling of complex numbers '''
    def __str__(self):
        r, i = +Real().from_float(self.real), +Real().from_float(self.imag)
        small = Real('0.001')
        if abs(r) < small and abs(i) < small: return '0'
        elif abs(i) < small: return str(r)
        elif abs(r) < small: return str(i) + 'i'
        else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'i'
    __repr__ = __str__
    
    def bracketed_str(self):
        r, i = +Real().from_float(self.real), +Real().from_float(self.imag)
        small = Real('0.001')
        return '(' + str(self) + ')' if abs(r) > small < abs(i) else str(self)

    def _convert_other(self, other):
        if isinstance(other, Decimal):
            return Complex(float(other))
        elif isinstance(other, Complex):
            return other
        # Might break for Constant
        elif isinstance(other, Number):
            return Complex(other)
        else:
            return NotImplemented

    def __add__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__add__(other))
    __radd__ = __add__

    def __sub__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__sub__(other))

    def __rsub__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__rsub__(other))

    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__mul__(other))
    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__truediv__(other))

    def __rtruediv__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__truediv__(other))


    def __pow__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return Complex(super().__pow__(other))

    # Due to the limitations of floating point complex numbers, equality
    # is approximate
    def __eq__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        # Euclidean normal / magnitude of complex number
        # TODO: Convert to method
        mag = lambda a: ( a.real**2 + a.imag**2 )**(1/2)
        return mag(self - other) < 0.01

    def __pos__(self):
        return Complex(super().__pos__())

    def __neg__(self):
        return Complex(super().__neg__())

    def conjugate(self):
        return Complex(super().conjugate())

class Algebra():
    ''' The base class for all algebraic types '''
    def __add__(self, other):
        if other == 0:
            return self
        else:
            return NotImplemented
    __radd__ = __add__

    def __sub__(self, other):
        if other == 0:
            return self
        else:
            return NotImplemented

    def __mul__(self, other):
        if other == 1:
            return self
        elif other == 0:
            return Integer(0)
        else:
            return NotImplemented
    __rmul__ = __mul__

    def __truediv__(self, other):
        if other == 1:
            return self
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if other == 0:
            return Integer(0)
        else:
            return NotImplemented

    def __pow__(self, other):
        if other == 0:
            return Integer(1)
        elif other == 1:
            return self

class Product(Algebra):
    ''' A representation of the product of n terms '''
    def __init__(self, *a):
        ''' Initialise factors from a list of arguments '''
        self._factors = list(a)
        super().__init__()

    def _simplify_multiply(self):
        return reduce(mul, self._factors, Integer(1))

    def simplify(self):
        return self._simplify_multiply()

    def __getitem__(self, i):
        return self._factors[i]

    def __mul__(self):
        if isinstance(other, Product):
            return Product(self.factors, other.factors)

    def __str__(self):
        return '*'.join(map(str, self._factors))

    def __eq__(self, other):
        # TODO: Add handling for products which may not be simplified
        return self.simplify() == other

    def __len__(self):
        return len(self._factors)

    def as_gnuplot_expression(self):
        return '*'.join(map(lambda a: a.as_gnuplot_expression(), self._factors))

class Constant(Number, Algebra):
    ''' A class to represent an unknown constant term '''
    name = 'c'
    def sign(self): return 1
    def __eq__(self, other):
        return isinstance(other, Number)\
            or hasattr(other, 'power') and other.power == 0\
            or hasattr(other, 'coefficient') and other.coefficient == 0
    def __str__(self): return self.name
    bracketed_str = __str__
    def __repr__(self): return 'Constant()'
    def __abs__(self): return self
    def __add__(self, other):
        return Constant() if other == self else NotImplemented
    __rsub__ = __sub__ = __radd__ = __add__
    def evaluate(self, x): return Integer(0)
    def differential(self): return Integer(0)
    def __pos__(self): return self

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
