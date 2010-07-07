#!/usr/bin/env python3.1

import math
from decimal import *

# Set precision for numbers
getcontext().prec = 3

def attempt_decimal_convert (a, ints=0):
    '''
    >>> print(attempt_decimal_convert(4))
    4
    >>> print(attempt_decimal_convert(4.5))
    4.5
    >>> print(attempt_decimal_convert(4.534534534534))
    4.534534534534
    >>> print(attempt_decimal_convert(1.1))
    1.1
    >>> print(attempt_decimal_convert(-1.1))
    -1.1
    >>> print(attempt_decimal_convert(0))
    0
    '''
    if ints and type(a) == type(1): return Decimal(a)
    if type(a) == type(1.1): return Decimal(repr(a))
    else: return a
    
def smart_division (a,b):
    ''' Calculate a / b, returning an integer or a decimal
    >>> print(smart_division(3,4))
    0.75
    >>> print(smart_division(4,4))
    1
    >>> print(smart_division(0,4))
    0
    >>> print(smart_division(7,-3))
    -2.33
    >>> print(smart_division(-7,3))
    -2.33
    '''
    return (a // b, attempt_decimal_convert(a,1) / attempt_decimal_convert (b,1))\
        [a % b != 0]
        
variables = {'pi' : Decimal('3.14159265358979'), 'e' : Decimal(repr(math.e))}
    
def nv (a):
    if type(a) == num: return nv(a.value())
    else: return a
        
class num:
    ''' A class for storing integers or aribitrary precision decimals
     - Passing it an integer will store that integer
     - Passing it a float or similar will store a Decimal
     - Integers will be converted to decimals when neccessary
    '''
    def __init__(self, a, nonint=0):
        if nonint and type(a) == type(1): self.x = Decimal(a)
        elif type(a) == type(1.1): self.x = Decimal(repr(a))
        elif a in variables: self.x = a
        else: self.x = a
    def value(self):
        if self.x in variables: return variables[self.x]
        else: return self.x
    def __truediv__(a, b):
        '''
        >>> print(num(3)/num(4))
        0.75
        >>> print(num(4)/num(4))
        1
        >>> print(num(0)/num(4))
        0
        >>> print(num(7)/num(-3))
        -2.33
        >>> print(num(-7)/num(3))
        -2.33
        '''
        return (nv(a) // nv(b), Decimal(repr(nv(a))) / Decimal(repr(nv(b))))\
            [nv(a) % nv(b) != 0]
    def __hash__(self): return hash(self.value())
    def __abs__(self): return num(abs(self.value()))
    def __add__(a,b): return num(nv(a) + nv(b))
    def __eq__(a,b):
        '''
        >>> print(num(-7)==num(3))
        False
        >>> print(num(3)==num(3))
        True
        '''
        return nv(a) == nv(b)
    def __ge__(a,b): 
        return nv(a) >= nv(b)
    def __gt__(a,b): 
        '''
        >>> print(num(1.1)>num(1))
        True
        >>> print(num(0.9)>num(1))
        False
        '''
        return nv(a) > nv(b)
    def __pow__(a,b): return num(nv(a) ** nv(b))
    def __le__(a,b): return nv(a) <= nv(b)
    def __lt__(a,b): return nv(a) < nv(b)
    def __mul__(a,b): return num(nv(a) * nv(b))
    def __sub__(a,b): return num(nv(a) - nv(b))
    def __str__(self): return str(self.x)
    def __repr__(self): return 'num(\'' + str(self.x) + '\')'
    __radd__ = __add__; __rmul__=__mul__; __rmul__ = __mul__; __rsub__ = __sub__
    __rpow__ = __pow__

class function:
    ''' A class to hold arbitrary algebraic functions '''
    def __init__(self,var):
        self.var = var
    def evaluate(n): pass
    # TODO: Add numberic differentiation and integration here
    def differential(): pass
    def integral(): pass
    def limit(self,lower,upper):
        '''
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print (y.integral().limit(1,2))
        51.0
        '''
        return self.evaluate(upper) - self.evaluate(lower)

class term(function):
    ''' A class holding a polynomial term
    >>> y = term(4,'t',5.57); print (y)
    4*t^5.57
    >>> y = term(4.45345,'t',5.57); print (y)
    4.45345*t^5.57
    >>> y = term(4,'t',3); print (y)
    4*t^3
    >>> y = term(4,'t',3); print (y.integral().differential())
    4*t^3
    >>> y = term(4,'t',-3); print (y)
    4*t^-3
    >>> y = term(-3.4,'t',-3); print (y)
    -3.4*t^-3
    >>> y = term(0,'t',-3); print (y)
    <BLANKLINE>
    >>> y = term(7,'t',0); print (y)
    7
    >>> y = term(7,'t',1); print (y)
    7*t
    >>> y = term(1,'t',1); print (y)
    t
    >>> y = term(1,'t',0); print (y)
    1
    '''
    def __init__(self, coefficient, var, power):
        self.coefficient = num(coefficient)
        self.power = num(power)
        function.__init__(self, var)
    def __str__(self):
        ''' Output the term nicely via assorted logic '''
        if self.coefficient == 0: return ''
        else: return \
            ('', str(self.coefficient))[self.coefficient != 1 or self.power == 0] \
            + ('', '*')[self.coefficient != 1 and self.power != 0] \
            + ('', self.var)[self.power != 0] \
            + ('', '^' + str(self.power))[0 != self.power != 1]
    def sign(self):
        ''' Return 0, 1 or -1 depending on the sign of the coefficient
        >>> y = term(0,'t',3); print (y.sign())
        0
        >>> y = term(-5,'t',3); print (y.sign())
        -1
        >>> y = term(16.5,'t',3); print (y.sign())
        1
        '''
        return (0, 1, -1)[(self.coefficient > 0) + 2*(self.coefficient < 0)]
    def __abs__(self):
        ''' Return a version of the term, with the coefficient positive 
        >>> y = term(-16.5,'t',3); print (abs(y))
        16.5*t^3
        >>> y = term(12.5,'t',3); print (abs(y))
        12.5*t^3
        '''
        return term(abs(self.coefficient), self.var, self.power)
    def differential(self):
        '''
        >>> y = term(4,'t',3); print (y.differential())
        12*t^2
        '''
        return term(self.coefficient * self.power, self.var, self.power - 1)
    def integral(self):
        '''
        >>> y = term(4,'t',3); print (y.integral())
        t^4
        '''
        return term(self.coefficient/(self.power + 1), self.var, self.power + 1)
    def evaluate(self,x):
        ''' Returns the value of the term for x
        >>> y = term (3, 'x', 2)
        >>> print(y.evaluate(5))
        75
        >>> print(y.evaluate(4.5))
        60.6
        >>> print(y.evaluate(0))
        0
        >>> print(y.evaluate(-4))
        48
        '''
        return self.coefficient * num(x) ** self.power

class polynomial(function):
    ''' A class representing a polynomial '''
    def __init__(self, var, *nums):
        function.__init__(self, var)
        self.terms = [ term(a, var, b) for (a,b) in zip (nums[::2], nums[1::2]) ]
    def __str__(self):
        ''' A list comprehension to combine the terms of the polynomial
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('f(y) =',y);
        f(y) = y + 2*y^3 + 4*y^5
        '''
        if len(self.terms) > 1:
            return ' '.join([str(self.terms[0])] + [('+', '-')[a.sign() == -1] \
                + ' ' + str(abs(a)) for a in self.terms[1:] if a.sign() != 0])
        elif len(self.terms) == 1:
            return str(self.terms[0])
        else:
            return ''
    def map_to_terms(self,f):
        ''' Allows list proccessing of terms '''
        y = polynomial(self.var)
        y.terms = list(map(f, self.terms))
        return y
    def differential(self):
        ''' Calculate the differential of 
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('f`(y) =',y.differential())
        f`(y) = 1 + 6*y^2 + 20*y^4
        '''
        f = lambda x: x.differential()
        return (self.map_to_terms(f))
    def integral(self):
        ''' Calculate the indefinite integral of the expression
         - Integrate each term
         - Return a polynomial object based on the new terms
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print ('∫ f(y) dy =',y.integral(),'+ c')
        ∫ f(y) dy = 0.5*y^2 + 0.5*y^4 + 0.667*y^6 + c
        '''
        f = lambda x: x.integral()
        return (self.map_to_terms(f))
    def append(self, coefficient, power):
        ''' Add a term to the polynomial
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> y.append(3.141, 666)
        >>> print(y)
        y + 2*y^3 + 4*y^5 + 3.14*y^666
        '''
        self.terms += [ term(coefficient, self.var, power) ]
    def evaluate(self, x):
        ''' Return the value of f(x)
         - Evalute each term
         - Sum them
        >>> y = polynomial('y',1,1,2,3,4,5)
        >>> print (y.evaluate(3))
        1029
        >>> print (y.evaluate(0))
        0
        >>> print (y.evaluate(1))
        7
        >>> print (y.evaluate(.1))
        0.102
        >>> print (y.evaluate(-4))
        -4228
        '''
        g = lambda a: a.evaluate(x)
        return sum(map(g, self.terms))

if __name__ == '__main__':
    import doctest
    getcontext().prec = 3
    doctest.testmod()
