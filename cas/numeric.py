#!/usr/bin/env python3.1
''' Numeric types such as integer, reals and complex numbers. '''

from decimal import Decimal, getcontext, localcontext
from functools import reduce
from operator import mul
from copy import copy, deepcopy
from numbers import Number

from dmath import pi
from cas.core import handle_type
import cas.numerical_methods as nm
        
def _pow(a, b):
    if a > 0 or b == int(b):
        return handle_type(super(type(a),a).__pow__(b))
    else:
        return handle_type(handle_type(1j) * super(type(a),abs(a)).__pow__(b))

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
            return _pow(self, other)
        else:
            return NotImplemented
            
    def __rpow__(self, other):
        if isinstance(other, int):
            return _pow(other, self)
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
    prec_offset = 0 # Print this fewer signficant figures than are used intenally
    exact_form = True # Print fractions as fractions including pi and square roots
    
    def __str__(self):
        # Print integers plainly
        if abs(float(self) - int(self)) < 5 * 10**(-5):
            return str(int(self))
        
        if self.__class__.exact_form and abs(self) > Real('0.0001'):
            # Show pi in full
            if self == pi(): return super().__str__()
        
            # Display small fractions as such
            a, b = nm.to_fraction(self)
            if b < 50: return '{}/{}'.format(a,b) if b != 1 else str(a)
            
            # Display small fractional coefficients of pi in exact form
            q = self / pi(); a, b = nm.to_fraction(q);
            if b <= 12: 
                return (str(a) if a != 1 else '') + 'pi'\
                        + ('/' + str(b) if b != 1 else '')
            
            # Sort out square roots
            for n in [2,3,5,7,11,13]:
                q = self / handle_type(n) ** Real('0.5')
                a, b = nm.to_fraction(q)
                if b <= 100:
                    return (str(a) + '*' if a != 1 else '') + str(n) + '^(1/2)'\
                        + ('/' + str(b) if b != 1 else '')
        
        # Otherwise display as a decimal
        with localcontext():
            getcontext().prec -= self.__class__.prec_offset
            return str(+Decimal(self))
        
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
        return Real(super().__rtruediv__(other, context))


    def __pow__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return _pow(self, other)
        
    def __rpow__(self, other, context=None):
        other = self._convert_other(other)
        if other == NotImplemented: return other
        return _pow(other, self)

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
        # Might break for Constant
    #    elif isinstance(other, Constant):
    #        return Real(0)
        elif isinstance(other, Number) and not isinstance(other, complex):
            return Real(other)
        else:
            return NotImplemented

class Complex(complex):
    ''' A class to provide better handling of complex numbers '''
    def __str__(self):
        r, i = +Real().from_float(self.real), +Real().from_float(self.imag)
        R = str(r)
        I = ('-' if i < 0 else '+' if i != 1 else '') + (str(abs(i)) if abs(i) != 1 else '') + 'i'
        small = Real('0.001')
        if abs(r) < small and abs(i) < small: return '0'
        elif abs(i) < small: return R
        elif abs(r) < small: return I
        else: return R + I
    __repr__ = __str__
    
    def argument(self):
        from math import pi, atan
        r, i = abs(self.real), abs(self.imag)
        a = atan(i/r)
        if self.real >= 0 and self.imag >= 0: return handle_type(a)
        if self.real <= 0 and self.imag >= 0: return handle_type(pi - a)
        if self.real >= 0 and self.imag <= 0: return handle_type(-a)
        if self.real <= 0 and self.imag <= 0: return handle_type(a - pi)
    
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
