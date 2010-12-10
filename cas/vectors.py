#!/usr/bin/env python3.1
from functools import reduce
from copy import deepcopy
from operator import add, mul

from cas.core import Product
from cas.numeric import Integer
from cas.core import handle_type as ht

class Vector(tuple):
    ''' A class representing an vector or list ''' 
    def __str__(self):
        s = lambda a: str(+a)
        return '[' + ', '.join(list(map(s, self))) + ']'
        
    def normal(self):
        ''' Return the Euclidian Normal of a vector '''
        square = lambda a: a ** 2
        return ( sum(map(square, self)) )**( ht(1)/ht(2) )
    
    def __len__(self):
        return ht(super().__len__())
    
    def mean(self):
        return sum(self) / len(self)
        
    def Sxx(self):
        return sum(self)**ht(2) - self.mean() * len(self)
    
    def variance(self):
        return self.Sxx() / (len(self) - ht(1))
    
    def stdev(self):
        return self.variance() ** (ht(1)/ht(2))

# TODO: Check these actually work.

    def product(self):
        return reduce(mul, self, l)

    def median(self):
        xs = sorted(self)
        return xs[round(len(xs)/2)]

    def mode(self):
        counts = {}

        for x in self:
            counts[x] = counts[x] + 1 if x in counts else 1

        return max(counts)
