#!/usr/bin/env python3.1
''' Provides core types/classes from use throughout the Computer Algebra
System representing simple objects such as Integers and Constants
whilst providing functions to allocate types. '''

from decimal import Decimal
import re

def handle_type (x):
    ''' Takes in a variable a and output it in the most desirable type '''
    if type(x) == Integer: return x
    elif type(x) == Decimal: return x
    elif type(x) == int: return Integer(x)
    elif type(x) == str and re.match(r'^[0-9]+$', x): return Integer(x)
    elif type(x) == float: return Decimal(repr(x)).normalize()
    elif type(x) == complex: return x
    else: return Decimal(x).normalize()

def print_complex(a):
    ''' Nicely print a complex number '''
    r, i = Decimal().from_float(a.real).normalize(),\
        Decimal().from_float(a.imag).normalize()
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

class StrWithHtml():
    ''' An extended string also holding a html version '''
    # TODO: Extend concept to any object with a .html() method
    def __init__(self, plain, html):
        self.plain, self.html = str(plain), str(html)
    def __str__(self):
        return str(self.plain)
