#!/usr/bin/env python3.1
''' Various abstract methods and functions '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

def gcd(a, b):
    ''' A recursive implementation of the euclidian greatest common divisor
    algorithm. '''
    def _gcd_div(a, b):
        if b == 0: return a
        else: return _gcd_div(b, a % b)

    def _gcd_sub(a, b):
        if a == 0: return b
        while b != 0:
            if a > b: a = a - b
            else: b = b - a
        return a

    if isinstance(a, int) and isinstance(b, int):
        return _gcd_div(a, b)
    else:
        return _gcd_sub(a, b)

if __name__ == '__main__':
    from cas.core import Symbol
    x = Symbol('x')
    print (gcd(6*x, 5*x))

