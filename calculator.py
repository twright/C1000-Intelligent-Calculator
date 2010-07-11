#!/usr/bin/env python3

from decimal import Decimal, getcontext
from sys import exit

from cas import *
from ntypes import nint
from parser import parseCommand

getcontext.prec = 3

def print_complex(a):
    r, i = Decimal().from_float(a.real).normalize(),\
        Decimal().from_float(a.imag).normalize()
    if abs(r) < Decimal('0.001') and abs(i) < Decimal('0.001'): return '0'
    elif abs(i) < Decimal('0.001'): return str(r)
    elif abs(r) < Decimal('0.001'): return str(i) + 'j'
    else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'j'

class Calculator():
    commands = {
        'diff' : lambda a: str(a.differential()),
        'integrate' : lambda a: str(a.integral()),
        'solve' : lambda a: 'x = ' + ' or '.join(map(print_complex,
            a.roots())),
        'help' : lambda: 'Commands include: solve, diff, integrate',
        'quit' : exit
    }
    def _evaluate(self, a):
        return (self.commands[a[0]] (*a[1:100]) if len(a) > 1 
            else self.commands[a[0]]())
    def evaluate(self, a):
        return self._evaluate(parseCommand(a))
