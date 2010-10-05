#!/usr/bin/env python3.1
from functools import reduce
from copy import deepcopy
from decimal import Decimal
from operator import add

from .core import Integer, Product, handle_type

class Vector(tuple):
    ''' A class representing an vector ''' 
    def __str__(self):
        s = lambda a: str(+a)
        return '[' + ', '.join(list(map(s, self))) + ']'
        
    def normal(self):
        ''' Return the normal of a vector '''
        square = lambda a: a ** 2
        half = Decimal(1) / Decimal(2)
        return ( sum(map(square, self)) )**(half)
