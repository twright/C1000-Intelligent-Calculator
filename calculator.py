#!/usr/bin/env python3.1
# coding=utf-8
from __future__ import division, unicode_literals
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from decimal import Decimal, getcontext, localcontext
from functools import reduce, partial
import math
from copy import copy
from sys import exit
import dmath

from cas.core import StrWithHtml, List, handle_type, Symbol,\
    partial_differential, partial_integral, expand, Ln, Sin, Cos, Tan, Algebra
from cas.numeric import Integer, Complex, Real
from cas.matrices import Matrix, identity_matrix, diagonal_matrix
from cas.vectors import Vector
from cas.statistics import nCr, nPr, binomialpdf, binomialcdf, poissonpdf,\
    poissoncdf, normalcdf, factorial
import cas.numerical_methods as nm
#from dmath import log, sin, cos, tan, asin, acos, atan, sinh, cosh, tanh
from gnuplot import Gnuplot
from pyparsing import *
import help

# The precision for internal working must be greater that for display
# to ensure that results are justified
# TODO: replace with a context manager or something more comprehensive
PREC_OFFSET = 50
getcontext().prec = 3 + PREC_OFFSET

def plot(f, *between):
    graph = Gnuplot()
    file_name, root_file_name = graph.file_name, graph.root_file_name
    graph.plot_function(f, *between)
    return StrWithHtml (
        'Image saved to %s' % file_name,
        '''<!--<object data="{0}.svg" type="image/svg+xml" style="width: 100%">-->
            <img src="{0}.png" style="width: 100%" />
        <!-- </object>-->'''.format(root_file_name),
        )

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
    else: return a[0] ** a[1]

def _assign_action(vars, a):
    vars[a[0]] = a[1]
    return a[1]

#PI = Real('3.14159265358979323846264338327950288419716939937510582097494459')
pi = lambda : Real(nm.pi())
radians = lambda x: x*PI/handle_type(180)
degrees = lambda x: x*handle_type(180)/PI
wrapped_f = lambda f, g, x: f(x) if isinstance(x, Algebra) else handle_type(g(x))
ln = partial(wrapped_f, Ln, dmath.log)
sin = partial(wrapped_f, Sin, dmath.sin)
cos = partial(wrapped_f, Cos, dmath.cos)
tan = partial(wrapped_f, Tan, dmath.tan)

#ln = lambda x: Ln(x) if isinstance(x, Algebra) else handle_type(dmath.log(x))

class Calculator():
    ''' An object providing an interactive, text driven, calculator. '''
    def __init__(self):
        # An array
        self.functions = {
        # Logaritms
            'ln' : ln,
            'log' : lambda a, b=10: dmath.log(a,b),
        # Trianometric Functions
            'sin' : lambda x: handle_type(sin(x)),
            'cos' : lambda x: handle_type(cos(x)),
            'tan' : lambda x: handle_type(tan(x)),
            'arcsin' : lambda x: handle_type(dmath.asin(x)),
            'arccos' : lambda x: handle_type(dmath.acos(x)),
            'arctan' : lambda x: handle_type(dmath.atan(x)),
            'sinh' : lambda x: handle_type(dmath.sinh(x)),
            'cosh' : lambda x: handle_type(dmath.cosh(x)),
            'tanh' : lambda x: handle_type(dmath.tanh(x)),
            'arcsinh' : lambda z: handle_type(log(z + (Integer(1)
                + z**Integer(2))**Real('0.5'))),
            'arccosh' : lambda z: handle_type(log(z + (z + Integer(1))**Real('0.5')
                * (z - Integer(1))**Real('0.5'))),
            'arctanh' : lambda z: handle_type(log(Integer(1) + z)
                - log(Integer(1) - z))/Integer(2),
            'degrees' : lambda x: handle_type(degrees(x)),
        # Statistics
            'nCr' : nCr,
            'nPr' : nPr,
            'binomialpdf' : binomialpdf,
            'binomialcdf' : binomialcdf,
            'poissonpdf' : poissonpdf,
            'poissoncdf' : poissoncdf,
            'normalcdf' : normalcdf,
            'mean' : lambda a: a.mean(),
            'median' : lambda a: a.median(),
            'mode' : lambda a: a.mode(),
            'variance' : lambda a: a.variance(),
            'stdev' : lambda a: a.stdev(),
            'sxx' : lambda a: a.Sxx(),
        # Manipulation of functions
            'expand' : expand,
            'differentiate' : lambda a,b=Symbol('x'): partial_differential(a,b),
            'integrate' : lambda y, a, b, x=Symbol('x'): partial_integral(y,x)\
                if len(l) == 0 \
                else partial_integral(y,x).limit(a, b, variable=x),
            'romberg' : lambda f,a,b,*n: f.romberg_integral(a,b,*n),
            'trapeziumrule' : lambda f,a,b,*n: f.trapezoidal_integral(a,b,*n),
            'simpsonrule' : lambda f,a,b,*n: f.simpson_integral(a,b,*n),
            'roots' : lambda a, n=1000: List(*list(a.roots(n))),
            'maxima' : lambda a, n=100: List(*a.maxima(n)),
            'minima' : lambda a, n=100: List(*a.minima(n)),
        # Vectors
            'norm' : lambda a: a.norm(),
        # Matrices
            'transpose' : lambda a: a.transpose(),
            'order' : lambda a: '{}×{}'.format(*a.order()),
            'eval' : lambda a,b,c=None: a(b,variable=c),
            'identity' : identity_matrix,
            'diag' : diagonal_matrix,
            'inv' : lambda a: a.inverse(),
            'invert' : lambda a: a.inverse(),
            'decompose' : lambda a: a.LU_decomposition(),
            'trace' : lambda a: a.trace(),
            'poly' : lambda a: a.characteristic_polynomial(),
            'adj' : lambda a: a.adjgate(),
            'zero' : Matrix,
            'minor': lambda a, b, c: a.minor(b, c),
            'det' : lambda a: a.determinant(),
            'eigenvalues' : lambda a: List(*a.eigenvalues()),
        # Complex Numbers
            're' : lambda a: a.real,
            'im' : lambda a: a.imag,
            'arg' : lambda a: a.argument(),
            'conj' : lambda a: a.conjugate(),
        # Misc
            'yum' : pi,
            'factorial' : factorial,
            'factors' : lambda a: a.factors(),
            'decimal' : lambda a: Decimal(a) if not isinstance(a, List) else List(*list(map(Decimal, a))),
            'complex' : lambda a: complex(a) if not isinstance(a, List) else List(*list(map(complex, a))),
            'round' : lambda a: handle_type(round),
            'list' : lambda a: str(list(a)),
            'plot' : plot,
            'type' : lambda a: str(type(a)),
            'setprec' : self.set_precision,
            'setexact' : self.set_exact,
            'about' : lambda: StrWithHtml('Copyright Tom Wright <tom.tdw@gmail.com>',
                '''<img src="./images/about.png" />
                <br>This program was written by Tom Wright <tom.tdw@gmail.com>'''),
            'help' : help.help,
            'quit' : exit,
        }

        self.post_functions = {
            '!' : factorial,
            'degs' : radians #lambda a: Real.from_float(math.radians(a))
        }

        self.consts = {
            'pi' : pi(),
            'g' : Real('9.81'),
            'h' : Real('6.62606896e-34'),
            'F' : Real('96485.3399'),
            'I' : Integer(1),
        #    'E' : e(),
        }

        self.objects = { 'ans' : Integer(0) }

    def set_exact(self):
        ''' Tell the calculator to toggle the use of exact answers and return
        the previous answer in the new form. '''
        Real.exact_form = not Real.exact_form
        return self.objects['ans']

    def set_precision(self, a):
        ''' Set the number of significant figures to display, adjust the internal
        precision and return the previous answer in the new form. '''
        assert a >= 0
        getcontext().prec = int(a) + PREC_OFFSET
        return self.objects['ans']

    def grammar(self):
        ''' A top-down recursive parser for handling algebraic expressions. '''
        # Start of BFN for parser

        # Forward declarations for recursive definitions
        expr = Forward(); factor = Forward(); aterm = Forward()
        atom = Forward(); aexpr = Forward(); expr = Forward()
        const = Forward(); func = Forward()

        # Rules for the parsing of numbers
        uint = Word(nums)
        uint.setParseAction(lambda a: Integer(a[0]))
        ufloat = Word(nums) + '.' + Word(nums)
        ufloat.setParseAction(lambda a: Real(''.join(a)))
        ucomplex = (Literal('i') | Literal('j')) + NotAny(func | const)
        ucomplex.setParseAction(lambda a: Complex(1j))
        unum = ufloat ^ uint ^ ucomplex
        sign = Word('+-', max=1)
        num = Optional(sign) + unum
        num.setParseAction(_sign_action)

        # Rules for algebraic data types
        variable = reduce(lambda a,b: a | b, map(Literal, srange('[a-z]'))) \
        + NotAny(func | const)
        variable.setParseAction(lambda a: Symbol(a[0]))
        obj = 'ans' | Word(srange('[A-Z]'), max=1)
        obj.setParseAction(lambda a: self.objects[a[0]])
        vector = Suppress('[') + delimitedList(NotAny('[') + atom) + Suppress(']')
        vector.setParseAction(lambda a: Vector(a))
        matrix = Suppress('[') + delimitedList(vector) + Suppress(']')
        matrix.setParseAction(lambda a: Matrix(list(map(list,a))))

        # Rules for composite algebraic expressions
        exp = Literal("^") | Literal("**")
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
        norm = Suppress('||') + expr + Suppress('||')
        norm.setParseAction(lambda a: a[0].norm())
        atom << (Suppress('(') + expr + Suppress(')') | Suppress('$') + expr
            | const | vector | matrix | obj | num | variable | norm | aabs | func)
        factor << (atom ^ post_func) + Optional(Suppress(exp) + factor)
        factor.setParseAction(_factor_action)
        aterm << factor + Optional((mul | FollowedBy(Literal('(') | Literal('[') | variable | obj)) + aterm)
        aterm.setParseAction(_aterm_action)
        expr << aterm + ZeroOrMore(add + aterm)
        expr.setParseAction(_expr_action)

        # Rules for variable assignments
        assign = Word(srange('[A-Z]')) + Suppress(':=') + expr
        assign.setParseAction(lambda a: _assign_action(self.objects, a))

        command = Forward()
        command << (assign | expr) # + StringEnd()
        # End of BFN
        return command

    def evaluate(self, command):
        ''' Return the result of an algebraic expression '''
        # Parse and evaluate command
        a = self.grammar().parseString(command)

        # Assign answer variable to expression
        self.objects['ans'] = a[0]

        # Set resolution for display and print results
        Real.prec_offset = PREC_OFFSET
        if isinstance(a[0], Decimal):
            return '= ' + str(+a[0])
        elif isinstance(a[0], str):
            return '= ' + a[0]
        elif isinstance(a[0], StrWithHtml):
            return a[0]
        elif (len(a) == 1) or (type(a[0]) == int) or (type(a[0]) == float):
            return '= ' + str(a[0])

