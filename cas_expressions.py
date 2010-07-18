#!/usr/bin/env python3.1

from decimal import Decimal
from functools import reduce

from cas_core import handle_type, Integer

class Expression():
    def __add__(self, other):
        if other == 0:
            return self
        else:
            return NotImplemented
    __radd__ = __add__

    def __sub__(self, other):
        if other == 0:
            return self
        else:
            return NotImplemented
    __rsub__ = __sub__

    def __mul__(self, other):
        if other == 1:
            return self
        elif other == 0:
            return 0
        else:
            return NotImplemented
    __rmul__ = __mul__


class Polynomial(Expression):
    def __init__(self, *a):
        self.terms = list(a)

    def __str__(self):
        result = str(self.terms[0])
        for t in self.terms[1:]:
            result += (' + ' + str(t) if t.coefficient > 1
                else ' - ' + str(t)[1:]) if t.coefficient != 0 else ''
        return result

    def simplify(self):
        pass

    def _convert_other(self, other):
        if isinstance(other, Integer) or isinstance(other, Decimal):
            return Polynomial(Term(other))
        elif isinstance(other, term):
            return Polynomial(other)
        else:
            return NotImplemented


class Term(Expression):
    def __init__(self, coefficient, *factors):
        self.coefficient = handle_type(coefficient)
        self.factors = list(factors)
        self.sort_factors()

    def _convert_other(self, other):
        if isinstance(other, Integer) or isinstance(other, Decimal):
            return Term(other)
        elif isinstance(other, Factor):
            return Term(1, other)
        else:
            return NotImplemented

    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other

        return Term(self.coefficient*other.coefficient, *(self.factors + other.factors))
    __rmul__ = __mul__

    def sort_factors(self):
        self.factors.sort(key=lambda f: f.power)

    def __str__(self):
        self.sort_factors()
        return (str(self.coefficient) if abs(self.coefficient) != 1 else '')\
            + (reduce(lambda a,b: a+b, map(str, self.factors)) 
            if len(self.factors) else '') if self.coefficient != 0 else ''

    def __add__(self, other):
        return Polynomial(self, self._convert_other(other))
    __radd__ = __add__


class Factor(Expression):
    def __init__(self, abscissa, power):
        assert isinstance(power, int)
        self.abscissa = abscissa
        self.power = Integer(power)

    def __str__(self):
        return self.abscissa + ('^' + str(self.power) if self.power != 1 else '') if self.power != 0 else ''
