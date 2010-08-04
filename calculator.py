#!/usr/bin/env python3.1

from decimal import Decimal, getcontext, localcontext
from functools import reduce
import math
from copy import copy
from sys import exit

from cas.core import StrWithHtml, Integer, print_complex, List
from cas.matrices import Matrix, identity_matrix, diagonal_matrix
from cas.vectors import Vector
import cas.univariate as cf
from dmath import *
from gnuplot import Gnuplot
from pyparsing_py3 import *

# The precision for internal working must be greater that for display
# to ensure that results are justified
PREC_OFFSET = 25
getcontext().prec = 3 + PREC_OFFSET

def set_precision(a): 
    assert a >= 0
    getcontext().prec = int(a) + PREC_OFFSET
    return 'Done!'

def plot(f, *between):
    graph = Gnuplot()
    file_name = graph.file_name
    graph.send("set xlabel '%s'" % f.abscissa)
    graph.plot_function(f, *between)
    return StrWithHtml (
        'Image saved to %s' % file_name,
        r'<img src="' + file_name + '">'
        )

def _full_term_action(a):
    ''' Generates a term from the parse output '''
    # term (n)x(^m)
    n = a[0] if type(a[0]) != str else 1
    m = a[-1] if type(a[-1]) != str else 1
    for t in a:
        if isinstance(t,str): abscissa = t
    return cf.Term(n, abscissa, m)
    # return Polynomial('x',n,m)

def _sign_action(a):
    ''' Generates a number based on an optional sign and number '''
    if len(a) == 1: return a[0]
    elif len(a) == 2: return int(a[0] + '1') * a[1]

def _aterm_action(a):
    if len(a) == 1: return a[0]
    elif len(a) == 2: return a[0] * a[1]
    elif a[1] == '*': return a[0] * a[2]
    elif a[1] == '/': return a[0] / a[2]

def _expr_action(a):
    result = a[0]#Integer(0)
#    b = list(a)
#    if not isinstance(a[0], str):
#        b = [ '+' ] + b
    for i in range(1,len(a),2):
        if a[i] == '+': result += a[i+1]
        if a[i] == '-': result -= a[i+1]
    return result

def _factor_action(a):
    if len(a) == 1: return a[0]
    elif a[1] == '^': return a[0] ** a[2]

def _assign_action(vars, a):
    vars[a[0]] = a[1]
    return 'Done!'

def factorial(a):
    ''' A recursive factorial function '''
    assert (a >= 0)
    if a == 1:
        return 1
    elif a > 1:
        return a * factorial(a - 1)

class Calculator():
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
        'factors' : lambda a: a.factors(),
        'degrees' : degrees,
        'nCr' : lambda n,r: factorial(n) / (factorial(n - r) * factorial(r)),
        'nPr' : lambda n,r: factorial(n) / factorial(r),
        'round' : round,
        'differentiate' : lambda a: a.differential(),
        'integrate' : lambda *a: a[0].integral() if len(a) == 1 else a[0].integral().limit(a[1],a[2]),
        'romberg' : lambda f,a,b,*n: f.romberg_integral(a,b,*n),
        'trapeziumrule' : lambda f,a,b,*n: f.trapezoidal_integral(a,b,*n),
        'simpsonrule' : lambda f,a,b,*n: f.simpson_integral(a,b,*n),
        'solve' : lambda a, n=100: List(*a.roots(n)),
        #a.abscissa + ' = ' + ' or '.join(map(print_complex, a.roots(n))),
        'abscissa' : lambda a: a.abscissa,
        'maxima' : lambda a, n=100: List(*a.maxima(n)),
        'minima' : lambda a, n=100: List(*a.minima(n)),
        'simplify' : lambda expr: expr.simplify(),
        'plot' : plot,
        'transpose' : lambda a: a.transpose(),
        'order' : lambda a: '{}×{}'.format(*a.order()),
        'eval' : lambda a,b: a.evaluate(b),
        'identity' : identity_matrix,
        'diag' : diagonal_matrix,
        'inv' : lambda a: a.inverse(),
        'decompose' : lambda a: a.LU_decomposition(),
        'trace' : lambda a: a.trace(),
        'poly' : lambda a: a.characteristic_polynomial(),
        'adj' : lambda a: a.adjgate(),
        'zero' : Matrix,
        'minor': lambda a, b, c: a.minor(b, c),
        'det' : lambda a: a.determinant(),
        'normal' : lambda a: a.normal(),
        'eigenvalues' : lambda a: List(*a.eigenvalues()),
        'type' : lambda a: str(type(a)),
        'setprecision' : set_precision,
        'about' : lambda: StrWithHtml('Copyright Tom Wright <tom.tdw@gmail.com>',
            '''<img src="./images/about.png">
            <br>This program was written by Tom Wright <tom.tdw@gmail.com>'''),
        'help' : lambda: 'Commands include: solve, diff, integrate',
        'quit' : exit,
    }

    post_functions = {
        '!' : factorial,
        'degs' : radians #lambda a: Decimal.from_float(math.radians(a))
    }

    consts = {
        'pi' : Decimal('3.14159265358979846264338327950288419716939937510582097494'),
        'g' : Decimal('9.81'),
        'h' : Decimal('6.62606896e-34'),
        'F' : Decimal('96485.3399'),
        'I' : Integer(1),
        'E' : e(),
    }

    objects = { 'ans' : Integer(0) }

    def grammar(self):
        # Start of BFN for parser
        expr = Forward(); factor = Forward(); aterm = Forward()
        atom = Forward(); aexpr = Forward(); expr = Forward()
        const = Forward(); func = Forward()

        uint = Word(nums)
        uint.setParseAction(lambda a: Integer(a[0]))
        ufloat = Word(nums) + '.' + Word(nums)
        ufloat.setParseAction(lambda a: Decimal(''.join(a)))
        unum = ufloat ^ uint
        sign = Word('+-', max=1)
        num = Optional(sign) + unum
        num.setParseAction(_sign_action)
        variable = reduce(lambda a,b: a | b, map(Literal, srange('[a-z]'))) \
        + NotAny(func | const)
        variable.setParseAction(lambda a: cf.Term(1, a[0], 1))
        obj = 'ans' | Word(srange('[A-Z]'), max=1)
        obj.setParseAction(lambda a: self.objects[a[0]])
        vector = Suppress('[') + delimitedList(NotAny('[') + atom) + Suppress(']')
        vector.setParseAction(lambda a: Vector(a))
        matrix = Suppress('[') + delimitedList(vector) + Suppress(']')
        matrix.setParseAction(lambda a: Matrix(list(map(list,a))))

        equality = aexpr + Suppress('=') + aexpr
        equality.setParseAction(lambda a: cf.Equality(*a))

        exp = Literal("^")
        mul = Literal("*") | Literal("/")
        add = Literal("+") | Literal("-")
        func << Word(srange('[a-zA-Z]')) + (atom | Suppress('(') + Optional(delimitedList(expr)) + Suppress(')'))
        func.setParseAction(lambda a: self.functions[a[0]] (*a[1:]))
        post_func = atom + (Literal('degs') | '!')
        post_func.setParseAction(lambda a: self.post_functions[a[1]] (a[0]))
        const << (Literal('pi'))
        const.setParseAction(lambda a: self.consts[''.join(a)])
        aabs = Suppress('|') + expr + Suppress('|')
        aabs.setParseAction(lambda a: abs(a[0]))
        atom << (Suppress('(') + expr + Suppress(')') | Suppress('$') + expr
            | const | vector | matrix | obj | variable | num | aabs | func)
        factor << (atom ^ post_func) + Optional(exp + factor)
        factor.setParseAction(_factor_action)
        aterm << factor + Optional((mul | FollowedBy(Literal('(') | variable | obj)) + aterm)
        aterm.setParseAction(_aterm_action)
        aexpr << aterm + ZeroOrMore(add + aterm)
        aexpr.setParseAction(_expr_action)
        expr << (aexpr + NotAny('=') | equality)

        assign = Word(srange('[A-Z]')) + Suppress(':=') + expr
        assign.setParseAction(lambda a: _assign_action(self.objects, a))

        command = Forward()
        command << (assign | expr) # + StringEnd()
        # End of BFN
        return command

    def evaluate(self, command):
        # Parse and evaluate command
        a = self.grammar().parseString(command)
        
        # Assign answer variable to expression
        self.objects['ans'] = a[0]
        
        # Set resolution for display and print results
        with localcontext(): 
            getcontext().prec -= PREC_OFFSET
            if isinstance(a[0], Decimal):
                return '= ' + str(+a[0])
            elif isinstance(a[0], str):
                return '= ' + a[0]
            elif isinstance(a[0], StrWithHtml):
                return a[0]
            elif (len(a) == 1) or (type(a[0]) == int) or (type(a[0]) == float):
                return '= ' + str(a[0])
