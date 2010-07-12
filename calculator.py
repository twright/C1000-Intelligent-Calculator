#!/usr/bin/env python3

from decimal import Decimal, getcontext
from sys import exit

from cas import *
from ntypes import nint
from parser import parseCommand
getcontext().prec = 3

def print_complex(a):
    r, i = Decimal().from_float(a.real).normalize(),\
        Decimal().from_float(a.imag).normalize()
    if abs(r) < Decimal('0.001') and abs(i) < Decimal('0.001'): return '0'
    elif abs(i) < Decimal('0.001'): return str(r)
    elif abs(r) < Decimal('0.001'): return str(i) + 'j'
    else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'j'

def setPrecision(a): 
    getcontext().prec = int(a)
    return 'Done!'

class Calculator():
    commands = {
        'diff1' : lambda a: str(a.differential()),
        'integrate1' : lambda a: str(a.integral()),
        'integrate3' : lambda a,b,c: str(a.integral().limit(b,c)),
        'trapeziumrule3' : lambda a,b,c: str(a.trapezoidal_integral(b,c)),
        'trapeziumrule4' : lambda a,b,c,n: str(a.trapezoidal_integral(b,c,n)),
        'nintegrate3' : lambda a,b,c: str(a.numerical_integral(b,c)),
        'nintegrate4' : lambda a,b,c,n: str(a.numerical_integral(b,c,n)),
        'solve1' : lambda a: 'x = ' + ' or '.join(map(print_complex,
            a.roots())),
        'solve2' : lambda a,n: 'x = ' + ' or '.join(map(print_complex,
            a.roots(n))),
        'evaluate2' : lambda a,b: a.evaluate(b),
        'help' : lambda: 'Commands include: solve, diff, integrate',
        'setprecision1' : setPrecision,
        'quit' : exit
    }
    def _evaluate(self, a):
        return (self.commands[a[0] + str(len(a)-1)] (*a[1:100]) if len(a) > 1 
            else self.commands[a[0]]())
    def evaluate(self, a):
        return self._evaluate(parseCommand(a))
