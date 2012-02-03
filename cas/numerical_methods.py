#!/usr/bin/env python
''' This module includes a collection of numerical methods for use in analysis.
This module draws from methods at:
    - http://mathworld.wolfram.com/Newton-CotesFormulas.html
'''
from __future__ import division, nested_scopes
__author__ = 'Thomas Wright <tom.tdw@gmail.com>'

from operator import mul
from functools import reduce
from copy import copy
from decimal import Decimal, getcontext, localcontext

def pi(n=None):
    ''' Estimate pi using n terms of the Chudnovsky brothers' formula. By 
    default this will attempt to calculate it to the maximum number of digits 
    storable in a decimal number. '''
    from math import factorial
    D = Decimal
    if n == None: n = round(getcontext().prec/D(14)) + 10
    with localcontext():
        getcontext().prec += 5
        f = lambda k: factorial(6*k)*D(13591409 + 545140134*k)\
            / (factorial(3*k)*factorial(k)**3*D(-640320)**(3*k))
        return 426880*D(10005)**D('0.5') / sum([f(k) for k in range (100)])

def to_fraction(x, places=10):
    ''' Convert the decimal x to a fraction, a / b'''
    # Based upon algorithm at http://homepage.smc.edu/kennedy_john/DEC2FRAC.PDF
    max_runs = 50; i = 0
    sign = 1 if x >= 0 else -1
    z = abs(x)
    if z == int(z): return (x, 1)
    a = 0; b = 1; B = 0
    while i < max_runs:
        z = (z - int(z))**(-1)
        t = copy(b)
        b = b * int(z) + B
        a = int(round(abs(x) * b))
        B = copy(t)
        if abs(x - x.__class__(a)/x.__class__(b))\
            < 5*x.__class__(10)**(-places) or z == int(z):
            break
        i += 1

    return (sign * a, b)

def trapezoidal_composite_integral(f,a,b,m=100):
    ''' Order 1 Newton-Cotes approximation over m strips. '''
    h = (b-a)/(m)
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return h*( fx(0)/2 + sum(fx(n) for n in range(1,m)) + fx(m)/2 )

def simpson_composite_integral(f,a,b,m=100):
    ''' Order 2 Newton-Cotes approximation over m strips. '''
    m = 2*int(round(m/2))
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (h/3)*(fx(0) + sum(4*fx(n-1) + 2*fx(n) for n in range(2,m,2))
        + 4*fx(m-1) + fx(m))

def simpson38_composite_integral(f,a,b,m=100):
    ''' Order 3 Newton-Cotes approximation over m strips. '''
    m = 3*int(round(m/3))
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (3*h/8)*(sum(3*fx(n-2) + 3*fx(n-1) + 2*fx(n) for n in range(3,m,3))
        + fx(m))

def boole_composite_integral(f,a,b,m=100):
    ''' Order 4 Newton-Cotes approximation over m strips. '''
    m = 4*int(round(m/4))
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (2*h/45)\
        * sum(7*fx(n-4) + 32*fx(n-3) + 12*fx(n-2) + 32*fx(n-1) + 7*fx(n)
        for n in range(4,m,5))

def romberg_integral(f,a,b,n=7,m=7):
    ''' A recursive implementation of Romberg's method of integration.
    See http://en.wikipedia.org/wiki/Romberg's_method. '''
  #  if m == -1: m = n
    R = lambda N,M: romberg_integral(f,a,b,N,M)
    h = lambda n: (b-a)/(2**n)
    assert (n >= m)
    if n == 0 and m == 0:
        return (1/2)*(b-a)*(f(a) + f(b))
    elif m == 0:
        return (1/2)*R(n-1, 0) + h(n)\
            * sum(f(a + (2*k - 1)*h(n)) for k in range(1, 2**(n-1) + 1))
    else:
        return (4**m * R(n, m-1) - R(n-1, m-1)) / (4**m - 1)

def durand_kerner_roots(f, order, n=100):
    ''' Numerically locate all roots (real and complex) of Polynomial of
        leading coefficient 1 using n iterations of the Durand-Kerner method.
        See: http://en.wikipedia.org/wiki/Durand-Kerner_method '''
    xs = [ (0.4+0.9j)**k for k in range(order) ]
    product = lambda ys: reduce(mul, ys, 1)
    for k in range(n):
        for i in range(order):
            xs[i] -= f(xs[i])\
                / product(xs[i] - xs[j] for j in range(order) if i != j)
    return xs
