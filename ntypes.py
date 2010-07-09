#!/usr/bin/env python3.1

from fractions import Fraction
from decimal import Decimal

class nint(int):
    def __truediv__(a, b):
        if a % b == 0:
            return a // b
        else:
            return Decimal(a) / Decimal(b)
        #    return Fraction(a,b)
