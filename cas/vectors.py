#!/usr/bin/env python
from __future__ import division
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from operator import add, mul

from cas.core import Algebra
from cas.core import handle_type as ht


class Vector(tuple, Algebra):
    ''' A class representing an vector or list '''

    def __str__(self):
        s = lambda a: str(+a)
        return '[' + ', '.join(list(map(s, self))) + ']'

    def __add__(self, other):
        return self.__class__(map(add, self, other))
    __radd__ = __add__

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __neg__(self):
        return self.__class__(map(lambda a: -a, self))

    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return sum(map(mul, self, other))
        else:
            return self.__class__(map(lambda a: a * other, self))
    __rmul__ = __mul__

    def norm(self):
        ''' Return the Euclidian Norm of a vector '''
        square = lambda a: a ** 2
        return sum(map(square, self))**ht('0.5')

    def __len__(self):
        return ht(super(type(self), self).__len__())

    def mean(self):
        return sum(self) / len(self)

    def Sxx(self):
        return sum(self)**ht(2) - self.mean() * len(self)

    def variance(self):
        return self.Sxx() / (len(self) - ht(1))

    def stdev(self):
        return self.variance() ** ht('0.5')

    def product(self):
        return reduce(mul, self, ht(1))

    def median(self):
        xs = sorted(self)
        midpoint = round(len(xs)/2)
        return xs[midpoint] if len(xs) % 2\
            else ht(xs[midpoint] + xs[midpoint-1]) / ht(2)

    def mode(self):
        counts = {}

        for x in self:
            counts[x] = counts[x] + 1 if x in counts else 1

        return max(counts)
