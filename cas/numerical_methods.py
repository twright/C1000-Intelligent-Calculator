#!/usr/bin/env python3.1
''' This module includes a collection of numerical methods for use in analysis.
This module draws from methods at:
    - http://mathworld.wolfram.com/Newton-CotesFormulas.html
'''
__author__ = 'Thomas Wright <tom.tdw@gmail.com>'

from operator import mul
from functools import reduce
from copy import copy
from decimal import Decimal, getcontext

def to_fraction(x, places=10):
    ''' Convert the decimal x to a fraction, a / b'''
    # Based upon algorithm at http://homepage.smc.edu/kennedy_john/DEC2FRAC.PDF
    sign = 1 if x >= 0 else -1
    z = abs(x)
    if z == int(z): return (x, 1)
    a = 0; b = 1; B = 0
    while True:
        z = (z - int(z))**(-1)
        t = copy(b)
        b = b * int(z) + B
        a = round(abs(x) * b)
        # print ('a = {}, b = {}, z = {}, diff = {}'.format(a, b, z, abs(x - Decimal(a)/Decimal(b))))
        B = copy(t)
        if abs(x - x.__class__(a)/x.__class__(b)) < 5*x.__class__(10)**(-places) or z == int(z):
            break
            
    return (sign * a, b)

#    rs = sorted([x, 1]); xs = [1,0]; ys = [0,1]; qs = [0,int(rs[1]/rs[0])]
#    while float(abs(xs[1]/ys[1] - x)) > 5*10**(-places):
#        print('{}/{}'.format(xs[1],ys[1]))
#        rs += [ xs[1] / ys[1] ]
#        qs += [ int(rs[1]/rs[0]) ]
#        xs += [ xs[0] - qs[2] * xs[1] ]
#        ys += [ ys[0] - qs[2] * ys[1] ]
#        del rs[0]; del xs[0]; del ys[0]; del qs[0]
#        
#    return (xs[1], ys[1])
        
def trapezoidal_composite_integral(f,a,b,m=100):
    ''' order 1 Newton-Cotes aproximation over m strips '''
    h = (b-a)/(m)
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return h*( fx(0)/2 + sum(fx(n) for n in range(1,m)) + fx(m)/2 )
    
def simpson_composite_integral(f,a,b,m=100):
    ''' order 2 Newton-Cotes aproximation over m strips '''
    m = 2*round(m/2)
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (h/3)*(fx(0) + sum(4*fx(n-1) + 2*fx(n) for n in range(2,m,2))
        + fx(m))
        
def simpson38_composite_integral(f,a,b,m=100):
    ''' order 3 Newton-Cotes aproximation over m strips '''
    m = 3*round(m/3)
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (3*h/8)*(fx(0)
        + sum(3*fx(n-2) + 3*fx(n-1) + 2*fx(n) for n in range(3,m,3))
        + fx(m))
        
def boole_composite_integral(f,a,b,m=100):
    ''' order 4 Newton-Cotes aproximation over m strips '''
    m = 4*round(m/4)
    h = (b-a)/m
    x = lambda k: a + k*h
    fx = lambda n: f(x(n))
    return (2*h/45)\
        * sum(7*fx(n-4) + 32*fx(n-3) + 12*fx(n-2) + 32*fx(n-1) + 7*fx(n)
        for n in range(4,m,4))
        
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
    xs = [ (0.4+0.9j)**n for n in range(order) ]
    product = lambda ys: reduce(mul, ys, 1)
    for i in range(n):
        for i in range(order):
            xs[i] -= f(xs[i]) / product(xs[i] - y for y in xs if y is not xs[i])
    return xs
    
if __name__ == '__main__':
    from math import *
    g = lambda x: log(5*x)
    print ('True value ~= 1.995732273553990993435223576142540775676601622989028201540')
    print ('trapezium rule:', trapezoidal_composite_integral(g, 1,2, 1000))
    print ('simpson\'s rule:', simpson_composite_integral(g, 1,2, 1000))
    print ('simpson\'s 3/8 rule:', simpson38_composite_integral(g, 1,2, 1000))
    print ('boole\'s rule:', boole_composite_integral(g, 1,2, 1000))
    print ('romberg integration: {:.25f}'.format(romberg_integral(g, 1,2, 10,10)))
    f = lambda x: x**2 - x - 6
    print ('roots:', durand_kerner_roots(f, 2, 10))
