#!/usr/bin/env python
''' This module implements various methods for statistics. '''
from __future__ import division
__author__ = 'Thomas Wright <tom.tdw@gmail.com>'

# Third party modules
from dmath import e, pi

# Project modules
from .core import handle_type as ht
from .numerical_methods import romberg_integral

# Calculate constants
e = ht(e())
pi = ht(pi())

def factorial(x):
    ''' An iterative factorial function. '''
    if x < 0 or not isinstance(x, int):
        raise ValueError('The factorial of negative numbers in not defined')
    ans = x.__class__(1)
    while x > 0:
        ans *= x
        x -= 1
    return ans
    # return x * factorial(x - 1) if x > 0 else 1

def nCr(n, r):
    ''' n combinations of r. '''
    return factorial(n) / ( factorial(r) * factorial(n - r) )
    
def nPr(n, r):
    ''' n permutations of r. '''
    return factorial(n) / factorial(r)
    
def binomialpdf(n, p, r):
    ''' Binomial probability density function. '''
    return nCr(n,r) * p**r * (n.__class__(1)-p)**(n-r)

def binomialcdf(n, p, r):
    ''' Binomial cumulative probability density function. '''
    if r < 0:
        return ht(0)
    if r >= 0:
        return binomialpdf(n, p, r) + binomialcdf(n, p, r - r.__class__(1))

def poissonpdf(t, r):
    ''' Poisson probability density function. '''
    return e**(-t) * t**r / factorial(r)
    
def poissoncdf(t, r):
    ''' Poisson cumulative probability density function. '''
    if r < 0:
        return r.__class__(0)
    if r >= 0:
        return poissonpdf(t, r) + poissoncdf(t, r - r.__class__(1))
        
def normalcdf(x):
    ''' Normal cumulative probability density function. '''
    f = lambda x: (2*pi*e**(x**2))**(-1/2)
    return ht(0.5 + romberg_integral(f, 0, x, 5,5))
