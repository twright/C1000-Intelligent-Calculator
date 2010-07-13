#!/usr/bin/env python3

from decimal import Decimal, getcontext
from sys import exit

from cas import *
from ntypes import nint, hstr
from expr_parser import parse_command
from gnuplot import Gnuplot
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

def plot(f, *between):
    graph = Gnuplot()
    file_name = graph.file_name
    graph.plot_function(f, *between)
    return hstr (
        'Image saved to %s' % file_name,
        r'<img src="' + file_name + '">'
        )

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
        'plot1' : plot,
        'plot3' : plot,
        'test' : lambda: hstr('test', '<b>test</b>'),
        'about' : lambda: hstr('Copyright Tom Wright <tom.tdw@gmail.com>',
            '''<img src="./images/about.png"><br>
            This program was written by Tom Wright <tom.tdw@gmail.com>'''),
        'evaluate2' : lambda a,b: a.evaluate(b),
        'help' : lambda: 'Commands include: solve, diff, integrate',
        'setprecision1' : setPrecision,
        'quit' : exit
    }
    def _evaluate(self, a):
        # print (*a)
        return (self.commands[a[0] + str(len(a)-1)] (*a[1:100]) if len(a) > 1 
            else self.commands[a[0]]())
    def evaluate(self, a):
        return self._evaluate(parse_command(a))
