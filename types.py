#!/usr/bin/env python3.1

from fractions import Fraction

class nint(int):
    def __truediv__(a, b):
        if a % b == 0:
            return a // b
        else:
            return Fraction(a,b)
