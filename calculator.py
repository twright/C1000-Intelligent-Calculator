#!/usr/bin/env python3.1

from decimal import Decimal, getcontext
from sys import exit

from pyparsing_py3 import *
from dmath import *

from cas import *
from ntypes import nint, hstr
# from expr_parser import parse_command
from gnuplot import Gnuplot
getcontext().prec = 3

def print_complex(a):
    r, i = Decimal().from_float(a.real).normalize(),\
        Decimal().from_float(a.imag).normalize()
    if abs(r) < Decimal('0.001') and abs(i) < Decimal('0.001'): return '0'
    elif abs(i) < Decimal('0.001'): return str(r)
    elif abs(r) < Decimal('0.001'): return str(i) + 'j'
    else: return str(r) + ('-' if i < 0 else '+') + str(abs(i)) + 'j'

def set_precision(a): 
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
        for t in a:
            if isinstance(t,str): abscissa = t
        return Term(n, abscissa, m)
        # return Polynomial('x',n,m)

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
        'differentiate' : lambda a: a.differential(),
        'integrate' : lambda *a: a[0].integral() if len(a) == 1 else a[0].integral().limit(a[1],a[2]),
        'trapeziumrule' : lambda a,b,c,n=100: str(a.trapezoidal_integral(b,c,n)),
        'nintegrate' : lambda a,b,c,n=100: str(a.numerical_integral(b,c,n)),
        'solve' : lambda a, n=100: a.abscissa + ' = ' + ' or '.join(map(print_complex,
            a.roots(n))),
        'plot' : plot,
        'evaluate' : lambda a,b: a.evaluate(b),
        'setprecision' : set_precision,
        'about' : lambda: hstr('Copyright Tom Wright <tom.tdw@gmail.com>',
            '''<img src="./images/about.png"><br>
            This program was written by Tom Wright <tom.tdw@gmail.com>'''),
        'help' : lambda: 'Commands include: solve, diff, integrate',
        'quit' : exit,
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
    fullterm = Optional(unum + Optional(Suppress('*'))) + variable\
        + Optional(Suppress('^') + uint)
    fullterm.setParseAction(full_term_action)
    baseterm = numterm ^ fullterm
    firstterm = Optional(sign) + baseterm
    firstterm.setParseAction(signed_term_action)
    term = sign + baseterm
    term.setParseAction(signed_term_action)

    poly = firstterm + ZeroOrMore(term)
    poly.setParseAction(compose_poly)

    expr = Forward(); factor = Forward(); aterm = Forward()
    atom = Forward(); aexpr = Forward(); expr = Forward()

    equality = aexpr + Suppress('=') + aexpr
    equality.setParseAction(lambda a: Equality(*a))

    exp = Literal("^")
    mul = Literal("*") | Literal("/")
    add = Literal("+") | Literal("-")
    func = Word(alphas) + (atom | Suppress('(') + Optional(delimitedList(expr)) + Suppress(')'))
    func.setParseAction(lambda a: Calculator.functions[a[0]] (*a[1:]))
    post_func = atom + (Literal('degs') | '!')
    post_func.setParseAction(lambda a: Calculator.post_functions[a[1]] (a[0]))
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
    aexpr << aterm + ZeroOrMore(add + aterm)
    aexpr.setParseAction(expr_action2)
    expr << (aexpr + NotAny('=') | equality)

    command = Forward()
    action = Word(alphas)
    qualifier = Suppress(':') + delimitedList(num)
    # command = (expr ^ (action + Optional(poly ^ equality) + Optional(qualifier)))
    command << expr
    # End of BFN

    def _evaluate(self, a):
        # print (*a)
        if isinstance(a[0], Decimal):
            return '= ' + str(a[0].normalize())
        elif (len(a) == 1) or (type(a[0]) == int) or (type(a[0]) == float):
            return a[0]
        else:
            return (self.commands[a[0] + str(len(a)-1)] (*a[1:100]) if len(a) > 1 else self.commands[a[0]]())

    def evaluate(self, a):
        return self._evaluate(self.command.parseString(a))
