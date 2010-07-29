#!/usr/bin/env python3.1

from decimal import Decimal
from functools import reduce
from numbers import Number
from copy import deepcopy

from .core import handle_type, Integer, Algebra

class Expression(Algebra):
    pass


class Polynomial(Expression):
    def __init__(self, *a):
        self.terms = list(a)
        self._sort_terms()

    def __str__(self):
        self._sort_terms()
        result = str(self.terms[0])
        for t in self.terms[1:]:
            result += ((' + ' + str(t) if t.coefficient > 0
                else ' - ' + str(t)[1:]) if abs(t.coefficient) != 0 else '')
        return result

    def simplify(self):
        self._sort_terms()
        ans = Polynomial()
        ans.terms += [ self.terms[0] ]
        for i in range(1,len(self.terms)):
            if self.terms[i].factors != ans.terms[-1].factors:
                ans.terms += [ self.terms[i] ]
            else:
                ans.terms[-1].coefficient += self.terms[i].coefficient
        return ans
        
    def _sort_terms(self):
        # This function should ensure the enternal state of the polynomial is
        # correct
    
        ''' Sort terms in a half conventional / half arbitrary order '''
 #       key = lambda a: 100000 - (5000*len(a.factors)
 #           + max(map(lambda b: b.power, a.factors))
 #           + sum(map(lambda a: ord(a.abscissa), a.factors)))
 #       self.terms.sort(key=key)
        # The terms are thus sorted for nice display and to ensure that
        # identical items will be next to each other
        power = lambda a: a.power
        maxpower = lambda a: max(map(power, a.factors))
        alpha = lambda a: sum(map(lambda b: ord(b.abscissa), a.factors))
        key = lambda a: 0 if len(a.factors) == 0\
            else -1000000000000*maxpower(a) - 100000000*len(a.factors) \
                - 1000*a.coefficient - alpha(a)
        self.terms.sort(key = key)
                
        self.terms = list(filter(lambda a: a.coefficient != 0, self.terms))

    def _convert_other(self, other):
        import cas.univariate as cf
        if isinstance(other, Polynomial):
            return other
        elif isinstance(other, cf.Polynomial):
            conv = lambda a: Term(a.coefficient, Factor(a.abscissa, a.power))
            return Polynomial(*map(conv, other.terms))
        elif isinstance(other, cf.Term):
            return Polynomial(Term(other.coefficient, Factor(other.abscissa,
                other.power)))
        elif isinstance(other, Integer) or isinstance(other, Decimal):
            return Polynomial(Term(other))
        elif isinstance(other, Term):
            return Polynomial(other)
        else:
            return NotImplemented
            
    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        
        ans = Polynomial()
        for i in range(len(self.terms)):
            for j in range(len(other.terms)):
                ans.terms += [ (self.terms[i] * other.terms[j]).simplify() ]
        
        return ans.simplify()
    __rmul__ = __mul__
    
    def __add__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
            
        return Polynomial(*(self.terms + other.terms)).simplify()

class Term(Expression):
    def __init__(self, coefficient, *factors):
        self.coefficient = handle_type(coefficient)
        self.factors = list(factors)
        self.sort_factors()

    def _convert_other(self, other):
        import cas.univariate as cf
        if isinstance(other, Term):
            return other
        elif isinstance(other, int) or isinstance(other, Decimal):
            return Term(other)
        elif isinstance(other, Factor):
            return Term(1, other)
        elif isinstance(other, cf.Term):
            return Term(other.coefficient, Factor(other.abscissa, other.power))
        else:
            return NotImplemented

    def __mul__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other

        return Term(self.coefficient*other.coefficient, *(self.factors + other.factors))
    __rmul__ = __mul__
    
    def __neg__(self):
        ''' Returns the inverse of a term '''
        return Term(-self.coefficient, *self.factors)
        
    def __sub__(self, other):
        return self + (-other)
    
    def __rsub__(self, other):
        return -self + other

    def sort_factors(self):
        self.factors = list(filter(lambda a: a.power > 0, self.factors))
        self.factors.sort(key=lambda f: ord(f.abscissa))
    #    for i in range(len(self.factors) - 1):
     #       if self.factors[i].abscissa == self.factors[i+1].abscissa:
      #          self.factors[i].power += self.factors[i+1].power
       #         self.factors[i+1].abscissa = 'O'
            
    def simplify(self):
        self.sort_factors()
        if len(self.factors) == 0: return self
        c = Term(self.coefficient)
        c.factors = [ deepcopy(self.factors[0]) ]
        for factor in self.factors[1:]:
            if c.factors[-1].abscissa != factor.abscissa:
                c.factors += [ factor ]
            else:
                c.factors[-1].power += factor.power
        return c
        
#        def simplify(self):
#        c = deepcopy(self)
#        i = 0
#        while i < len(c.factors) - 1:
#            if c.factors[i].abscissa == self.factors[i+1].abscissa:
#                c.factors[i].power += self.factors[i+1].power
#                del c.factors[i+1]
#                i += 1
#        return c
            
        
    def __str__(self):
    #    self.sort_factors()
        if self.coefficient == 0: return ''
        if len(self.factors) == 0: return str(+self.coefficient)

        coefficient = '' if self.coefficient == 1\
            else '-' if self.coefficient == -1 else str(+self.coefficient)
        factors = ''.join(map(str, self.factors))
        
        return coefficient + factors
    __repr__  = __str__

    def __add__(self, other):
        other = self._convert_other(other)
        if other == NotImplemented:
            return other
        return Polynomial(self, other)
    __radd__ = __add__

class Factor(Expression):
    def __init__(self, abscissa, power):
        assert isinstance(power, int)
        self.abscissa = abscissa
        self.power = Integer(power)
        
    def __eq__(self, other):
        if isinstance(other, Factor):
            return self.abscissa == other.abscissa and self.power == other.power
        else:
            return NotImplemented

    def __str__(self):
        return self.abscissa + ('^' + str(self.power) if self.power != 1 else '') if self.power != 0 else ''
    __repr__ = __str__
