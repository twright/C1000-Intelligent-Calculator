#!/usr/bin/env python3.1
''' This module includes a collection of numerical methods for use in analysis.
This module draws from methods at:
    - http://mathworld.wolfram.com/Newton-CotesFormulas.html
'''
__author__ = 'Thomas Wright <tom.tdw@gmail.com>'
            
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
    
if __name__ == '__main__':
    from math import *
    g = lambda x: log(5*x)
    # True value ~= 1.995732273553990993435223576142540775676601622989028201540
    print ('trapezium rule:', trapezoidal_composite_integral(g, 1,2, 1000))
    print ('simpson\'s rule:', simpson_composite_integral(g, 1,2, 1000))
    print ('simpson\'s 3/8 rule:', simpson38_composite_integral(g, 1,2, 1000))
    print ('boole\'s rule:', boole_composite_integral(g, 1,2, 1000))
    print ('romberg integration: {:.25f}'.format(romberg_integral(g, 1,2, 10,10)))
