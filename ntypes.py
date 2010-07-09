#!/usr/bin/env python3.1

from fractions import Fraction
from decimal import Decimal

def handle_type (a):
    if type(a) == int: return nint(a)
    elif type(a) == float: return Decimal(repr(a))
    else: return Decimal(a)

class nint(int):
    ''' An extended integer class, providing better mathematical
    handling of integers '''
    def __truediv__(a, b):
        if a % b == 0: return a // b
        else: return Decimal(a) / Decimal(b)
        #    return Fraction(a,b)

# class nconst(Decimal):
