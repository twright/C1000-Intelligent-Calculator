#!/usr/bin/env python3.1

from decimal import Decimal, getcontext
import sys

from pyparsing_py3 import *
from dmath import *

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
    #return Term(n, 'x', m)
    return Polynomial('x',n,m)

def sign_action(a):
    ''' Generates a number based on an optional sign and number '''
    if len(a) == 1: return a[0]
    elif len(a) == 2: return int(a[0] + '1') * a[1]

def aterm_action(a):
    if len(a) == 1: return a[0]
    elif a[1] == '*': return a[0] * a[2]
    elif a[1] == '/': return a[0] / a[2]

def expr_action(a):
    if len(a) == 1: return a[0]
    elif a[1] == '+': return a[0] + a[2]
    elif a[1] == '-': return a[0] - a[2]

def expr_action2(a):
    result = a[0]
    for i in range(1,len(a),2):
        if a[i] == '+': result += a[i+1]
        if a[i] == '-': result -= a[i+1]
    return result


def factor_action(a):
    if len(a) == 1: return a[0]
    elif a[1] == '^': return a[0] ** a[2]

def factorial(a):
    assert (a > 0)
    if a == 1:
        return 1
    elif a > 1:
        return a * factorial(a - 1)

functions = {
    'ln' : log,
    'log' : lambda a, b=10: log(a,b),
    'sin' : sin,
    'cos' : cos,
    'tan' : tan,
    'arcsin' : asin,
    'arccos' : acos,
    'arctan' : atan,
    'sinh' : sinh,
    'cosh' : cosh,
    'tanh' : tanh,
    'arcsinh' : lambda z: log(z + sqrt(1 + z**2)),
    'arccosh' : lambda z: log(z + sqrt(z + 1)*sqrt(z - 1)),
    'arctanh' : lambda z: (log(1 + z) - log(1 - z))/2,
    'factorial' : factorial,
    'degrees' : degrees,
    'nCr' : lambda n,r: factorial(n) / (factorial(n - r) * factorial(r)),
    'nPr' : lambda n,r: factorial(n) / factorial(r),
    'round' : round,
    'quit' : sys.exit,
}

post_functions = {
    '!' : factorial,
    'degs' : radians
}

consts = {
    'pi' : Decimal('3.14159265358979846264338327950288419716939937510582097494'),
    'g' : Decimal('9.81'),
    'h' : Decimal('6.62606896e-34'),
    'e' : e(),
}

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

nx = Optional(num) + Suppress('x')
nx.setParseAction(lambda a: Polynomial('x', a[0] if len(a) != 0 else 1, 1))

poly = firstterm + ZeroOrMore(term)
poly.setParseAction(compose_poly)

equality = poly + Suppress('=') + poly
equality.setParseAction(lambda a: Equality(*a))

expr = Forward(); factor = Forward(); aterm = Forward()
atom = Forward()
exp = Literal("^")
mul = Literal("*") | Literal("/")
add = Literal("+") | Literal("-")
func = Word(alphas) + (atom | Suppress('(') + Optional(delimitedList(expr)) + Suppress(')'))
func.setParseAction(lambda a: functions[a[0]] (*a[1:]))
post_func = atom + (Literal('degs') | '!')
post_func.setParseAction(lambda a: post_functions[a[1]] (a[0]))
const = Literal('pi') | 'e' | 'g' | 'h'
const.setParseAction(lambda a: consts[''.join(a)])
aabs = Suppress('|') + expr + Suppress('|')
aabs.setParseAction(lambda a: abs(a[0]))
atom << (Suppress('(') + expr + Suppress(')') | Suppress('$') + expr 
    | fullterm | num | aabs | func | const)
factor << (atom ^ post_func) + Optional(exp + factor)
factor.setParseAction(factor_action)
aterm << factor + Optional(mul + aterm)
aterm.setParseAction(aterm_action)
#expr << aterm + Optional(add + expr)
#expr << Optional(expr + add) + aterm
expr << aterm + ZeroOrMore(add + aterm)
expr.setParseAction(expr_action2)

action = Word(alphas)
qualifier = Suppress(':') + delimitedList(num)
command = (expr ^ (action + Optional(poly ^ equality) + Optional(qualifier)))
# End of BFN

def parse_poly(a):
    return poly.parseString(a)[0]

def parse_command(a):
    return command.parseString(a)
