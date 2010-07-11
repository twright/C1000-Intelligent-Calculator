#!/usr/bin/env python3

from decimal import Decimal, getcontext

from pyparsing_py3 import *

from cas import *
from ntypes import nint, handle_type

getcontext.prec = 3

def compose_poly(a):
    y = Polynomial('x')
    y.terms = list(a)
    y.sort_terms()
    return y

def pt(a):
    if len(a) == 1: return a[0]
    elif a[0] == '+': return a[1]
    elif a[0] == '-': return a[1].invert()

def ft(a):
    ''' term (n*)x(^m) '''
    if type(a[0]) != str: n = a[0]
    else: n = 1  
    if type(a[-1]) != str: m = a[-1]
    else: m = 1
    return Term(n, 'x', m)

# Start of BFN for parser
uint = Word(nums)
uint.setParseAction(lambda a: nint(a[0]))
ufloat = Word(nums) + '.' + Word(nums)
ufloat.setParseAction(lambda a: Decimal(''.join(a)))
unum = ufloat | uint
variable = Word(alphas, max=1)
sign = Word('+-', max=1)

numterm = unum + Suppress(Empty())
numterm.setParseAction(lambda a: Term(a[0],'x',0))
fullterm = Optional(unum + Optional(Suppress('*'))) + variable \
    + Optional(Suppress('^') + uint)
fullterm.setParseAction(ft)
baseterm = numterm ^ fullterm
firstterm = Optional(sign) + baseterm
firstterm.setParseAction(pt)
term = sign + baseterm
term.setParseAction(pt)

poly = firstterm + ZeroOrMore(term)
poly.setParseAction(compose_poly)

equality = poly + Suppress('=') + poly
equality.setParseAction(lambda a: Equality(*a))

action = Word(alphas)
qualifier = ('between' + unum + ',' + unum) | ('at' + unum)
command = action + Optional((poly ^ equality) + Optional(qualifier)) + StringEnd() 
# End of BFN

def parsePoly(a):
    return poly.parseString(a)[0]

def parseCommand(a):
    return command.parseString(a)
