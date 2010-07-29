#!/usr/bin/env python3.1
''' Provides core types/classes from use throughout the Computer Algebra
System representing simple objects such as Integers and Constants
whilst providing functions to allocate types. '''

from decimal import Decimal
import re
from functools import reduce
from operator import mul
from copy import deepcopy

def handle_type (x):
    ''' Takes in a variable a and output it in the most desirable type '''
    if isinstance(x, Integer) or isinstance(x, Decimal) or isinstance(x, complex):
        return x
    elif isinstance(x, int):
        return Integer(x)
    elif isinstance(x, str) and re.match(r'^[0-9]+$', x):
        return Integer(x)
    elif isinstance(x, float):
        return +Decimal.from_float(x)
    else:
        return +Decimal(x)

def print_complex(a):
    ''' Nicely print a complex number '''
    r, i = +Decimal().from_float(a.real), +Decimal().from_float(a.imag)
    if abs(r) < Decimal('0.001') and abs(i) < Decimal('0.001'): return '0'
    elif abs(i) < Decimal('0.001'): return str(r)
    elif abs(r) < Decimal('0.001'): return str(i) + 'i'
    else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'i'

class Constant():
    ''' A class to represent an unknown constant term '''
    name = 'c'
    def sign(self): return 1
    def __eq__(self, other): return True
    def __str__(self): return self.name
    def __abs__(self): return self
    def evaluate(self, x): return Integer(0)
    def differential(self): return Integer(0)


class Integer(int):
    ''' An extended integer class, providing better mathematical
    handling of integers '''
    def __truediv__(self, other):
        if isinstance(other, int) or isinstance(other, Decimal):
            if self % other == 0:
                return self // other
            else:
                return Decimal(self) / Decimal(other)
        else:
            return NotImplemented
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
    
    def _factors(self):
        ''' Naively factorise an integer '''
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
        
    def __iter__(self, i):
        return self._factors[i]
        
    def __mul__(self):
        if isinstance(other, Product):
            return Product(self.factors, other.factors)
        
    def __str__(self):
        return '*'.join(map(str, self._factors))
        
    def as_gnuplot_expression(self):
        return '*'.join(map(lambda a: a.as_gnuplot_expression(), self._factors))
        
    def factors(self):
        return self
        
class List():
    def __init__(self, *a):
        self.values = list(a)
        
    def __str__(self):
        p = lambda a: print_complex(a) if isinstance(a, complex) else str(a)
        return ', '.join(map(p, self.values))

class StrWithHtml():
    ''' An extended string also holding a html version '''
    # TODO: Extend concept to any object with a .html() method
    def __init__(self, plain, html):
        self.plain, self.html = str(plain), str(html)
    def __str__(self):
        return str(self.plain)
