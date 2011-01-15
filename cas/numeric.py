#!/usr/bin/env python3.1
''' Numeric types such as integer, reals and complex numbers. '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from decimal import Decimal, getcontext, localcontext
from functools import reduce
from operator import mul
from copy import copy, deepcopy
from numbers import Number

from dmath import pi
from cas.cache import lru_cache
from cas.core import handle_type, a_str, m_str
import cas.numerical_methods as nm

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

    def __sub__(self, other):
        if isinstance(other, int):
            return Integer(int(self) - int(other))
        else:
            return NotImplemented

    def __pow__(self, other):
        if isinstance(other, int):
            return self.__class__(int(self) ** other)
        else:
            return NotImplemented

    def __rpow__(self, other):
        if isinstance(other, int):
            return Integer(other ** int(self))
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
        from cas.core import List
        return List(*self._factors())

# Use a least recently used cache to prevent redundant conversions of real numbers
# to strings.
@lru_cache(maxsize=1000)
def _real_str(y, exact_form, prec_offset):
    ''' Convert a Real number to a string, with nice display.
    Returns a tuple containing the string an a bool indicating whether changes
    have been made. The function works in floats and is cached for speed. '''
    small = 5 * 10**(-5)
    x = float(y)
    if abs(x - int(x)) < small:
        return (str(int(x)), False)

    if exact_form and abs(x) > small:
        # Show pi in full
        if abs(x - float(pi())) < small: return ('pi', True)

        # Display small fractions as such
        a, b = nm.to_fraction(x)
        if b < 50: return ('{}/{}'.format(a,b), True) if b != 1 else (str(a), False)

        # Display small fractional coefficients of pi in exact form
        q = x / float(pi()); a, b = nm.to_fraction(q);
        if b <= 12:
            return ((str(a) if a != 1 else '') + 'pi'\
                    + ('/' + str(b) if b != 1 else ''), True)

        # Sort out square roots
        for n in [2,3,5,6,7,10,11,13]:
            q = x / n ** 0.5
            a, b = nm.to_fraction(q)
            if b <= 100:
                return ((str(a) + '*' if a != 1 else '') + str(n) + '^(1/2)'\
                    + ('/' + str(b) if b != 1 else ''), True)

    # Otherwise display as a decimal
    with localcontext():
        getcontext().prec -= prec_offset
        return (str(+Decimal(y)), False)

class Real(Decimal):
    ''' A class to provide better handling of real numbers '''
    prec_offset = 0 # Print this fewer signficant figures than are used intenally
    exact_form = True # Print fractions as fractions including pi and square roots

    def __init__(self, x='0'):
        self.__string, a = _real_str(x, self.__class__.exact_form, self.__class__.prec_offset)
        self._hints = {'m','f','p'} if a else {}

    def __str__(self):
        return self.__string

    def __repr__(self):
        return "'" + super().__str__() + "'"

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
        return Real(super().__rtruediv__(other, context))


    def __pow__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return self.__class__(Decimal(self) ** other)

    def __rpow__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return self.__class__(Decimal(other) ** Decimal(self))

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
        elif isinstance(other, float):
            return Real(self.from_float(other))
        elif isinstance(other, Number) and not isinstance(other, complex):
            return Real(other)
        else:
            return NotImplemented

class Complex(complex):
    ''' A class to provide better handling of complex numbers '''
    def __new__(self, x):
        small = 0.00001
        # Complex numbers sufficiently small in magnitide should be replaced
        # with zero.
        if abs(x.real) < small and abs(x.imag) < small:
            return Integer(0)
        # Complex numbers very close to Real numbers should be replaced with the
        # Real number.
        elif abs(x.imag) < small:
            return handle_type(x.real)
        else:
            a = super().__new__(self, x)
            # Do not display brackets in multiplication if a number is close to
            # the set of imaginary numbers.
            if abs(x.real) < small: a._hints = {'a'}
            else: a._hints = {'d','m','p','a'}
            return a

    def __repr__(self):
        r, i = +Real().from_float(self.real), +Real().from_float(self.imag)
        small = Real('0.00001')
        R = a_str(r)
        I = (m_str(abs(i)) if -1 != i != 1 else '') + 'i'
        if abs(r) < small: return ('-' if i < 0 else '') + I
        else: return R + ('-' if i < 0 else '+') + I
    __str__ = __repr__

    def argument(self):
        ''' Return the complex argument of a number. '''
        from math import pi, atan
        r, i = abs(self.real), abs(self.imag)
        a = atan(i/r)
        if self.real >= 0 and self.imag >= 0: return handle_type(a)
        if self.real <= 0 and self.imag >= 0: return handle_type(pi - a)
        if self.real >= 0 and self.imag <= 0: return handle_type(-a)
        if self.real <= 0 and self.imag <= 0: return handle_type(a - pi)

    def _convert_other(self, other):
        if isinstance(other, complex):
            return other
        if isinstance(other, Number):
            return complex(float(other))
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
        return Complex(other - complex(self))

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

    # Due to the limitations of floating point complex numbers, equality is
    # approximate
    def __eq__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        # TODO: Convert to method
        mag = lambda a: ( a.real**2 + a.imag**2 )**(1/2)
        mag.__doc__ = ''' Euclidean normal / magnitude of complex number. '''
        return abs(self - other) < 0.01

    def __pos__(self):
        return Complex(super().__pos__())

    def __neg__(self):
        return Complex(super().__neg__())

    def conjugate(self):
        ''' Return the complex conjugate. '''
        return Complex(super().conjugate())

