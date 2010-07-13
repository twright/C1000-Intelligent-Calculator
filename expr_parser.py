#!/usr/bin/env python3

from decimal import Decimal, getcontext

from pyparsing_py3 import *

from cas import *
from ntypes import nint, handle_type

getcontext().prec = 3

def compose_poly(a):
    y = Polynomial('x')
    y.terms = list(a)
    y.sort_terms()
    return y

def signed_term_action(a):
    ''' Generates a term based on a term and sign '''
    if len(a) == 1: return a[0]
    elif a[0] == '+': return a[1]
    elif a[0] == '-': return a[1].invert()

def full_term_action(a):
    ''' Generates a term from the parse output '''
    # term (n)x(^m)
    n = a[0] if type(a[0]) != str else 1
    m = a[-1] if type(a[-1]) != str else 1
    return Term(n, 'x', m)

def sign_action(a):
    ''' Generates a number based on an optional sign and number '''
    if len(a) == 1: return a[0]
    elif len(a) == 2: return int(a[0] + '1') * a[1]

# Start of BFN for parser
uint = Word(nums)
uint.setParseAction(lambda a: nint(a[0]))
ufloat = Word(nums) + '.' + Word(nums)
ufloat.setParseAction(lambda a: Decimal(''.join(a)))
unum = ufloat ^ uint
sign = Word('+-', max=1)
num = Optional(sign) + unum
num.setParseAction(sign_action)
variable = Word(alphas, max=1)

numterm = unum + Suppress(Empty())
numterm.setParseAction(lambda a: Term(a[0],'x',0))
fullterm = Optional(unum + Optional(Suppress('*'))) + 'x' \
    + Optional(Suppress('^') + uint)
fullterm.setParseAction(full_term_action)
baseterm = numterm ^ fullterm
firstterm = Optional(sign) + baseterm
firstterm.setParseAction(signed_term_action)
term = sign + baseterm
term.setParseAction(signed_term_action)

poly = firstterm + ZeroOrMore(term)
poly.setParseAction(compose_poly)

equality = poly + Suppress('=') + poly
equality.setParseAction(lambda a: Equality(*a))

action = Word(alphas)
qualifier = Suppress(':') + delimitedList(num)
command = action + Optional(poly ^ equality) + Optional(qualifier) + StringEnd() 
# End of BFN

def parse_poly(a):
    return poly.parseString(a)[0]

def parse_command(a):
    return command.parseString(a)
