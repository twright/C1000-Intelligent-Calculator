#!/usr/bin/env python3.1

from fractions import Fraction
from decimal import Decimal, getcontext
import re

# Set precision for numbers
getcontext().prec = 3

def handle_type (a):
    int_pattern = re.compile('^[0-9]+$')
    if type(a) == nint: return a
    elif type(a) == Decimal: return a
    elif type(a) == int: return nint(a)
    elif type(a) == str and int_pattern.match(a): return nint(a)
    elif type(a) == float: return Decimal(repr(a)).normalize()
    elif type(a) == complex: return a
    else: return Decimal(a).normalize()

class constant():
    ''' A class to represent an unknown constant term '''
    name='c'
    def sign(self): return 1
    def __eq__(a,b): return True
    def __str__(self): return self.name
    def __abs__(self): return self
    def evaluate(self,a): return 0

class nint(int):
    ''' An extended integer class, providing better mathematical
    handling of integers '''
    def __truediv__(a, b):
        if isinstance(b, int) or isinstance(b, Decimal):
            if a % b == 0:
                return a // b
            else:
                return Decimal(a) / Decimal(b)
        else:
            return NotImplemented
        #    return Fraction(a,b)

    def __sub__(a,b):
        if isinstance(b,int):
            return nint(int(a) - int(b))
        else:
            return NotImplemented

    def __rsub__(a,b):
        if isinstance(b,int):
            return nint(int(b) - int(a))

    def __add__(a,b):
        if isinstance(b,int):
            return nint(int(a) + int(b))
        else:
            return NotImplemented
    __radd__ = __add__

    def __mul__(a,b):
        if isinstance(b,int):
            return nint(int(a) * int(b))
        else:
            return NotImplemented
    __rmul__ = __mul__

class hstr():
    ''' An extended string also holding a html version '''
    # TODO: Extend concept to any object with a .html() method
    def __init__(self,plain,html):
        self.plain, self.html = str(plain), str(html)
    def __str__(self):
        return str(self.plain)
