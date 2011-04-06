#!/usr/bin/env python
# coding=utf-8
from __future__ import division, unicode_literals
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

# Standard modules
from decimal import Decimal, getcontext
from functools import reduce, partial
from sys import exit
import random

# Third party modules
import dmath
from pyparsing import *

# Project modules
from cas.core import StrWithHtml, List, handle_type, Symbol,\
    partial_differential, partial_integral, expand, Ln, Sin, Cos, Tan,\
    Algebra
from cas.numeric import Integer, Complex, Real
from cas.matrices import Matrix, identity_matrix, diagonal_matrix
from cas.vectors import Vector
from cas.statistics import nCr, nPr, binomialpdf, binomialcdf,\
    poissonpdf, poissoncdf, normalcdf, factorial
import cas.numerical_methods as nm
from gnuplot import Gnuplot
import help

# The precision for internal working must be greater that for display
# to ensure that results are justified
PREC_OFFSET = 50
getcontext().prec = 3 + PREC_OFFSET


def evalute_between(f, a, b, samples=1000, variable=None):
    ''' Evaluate the function f at samples evenly spaced points for
    variable between a and b '''
    # Convert a and b to Decimals for speed and samples to an int
    a = Decimal(a)
    b = Decimal(b)
    samples = int(samples)

    # Calculate the step width
    step = (b - a) / samples
    # Create a matrix m to contain the values
    m = Matrix(samples, 2)
    # For each value x seperated by step between a and b, add each
    # value x and f(x) to the matrix of results
    i = 0
    while i < samples:
        x = i*step + a
        m[i][0] = x
        try:
            m[i][1] = f(x)
        except:
            m[i][1] = None
        i += 1

    # Return the matrix of results
    return m


def gnuplot(f, *between):
    ''' Plot the function f within the optional limits *between '''
    # Create an instance of the gnuplot class
    graph = Gnuplot()
    # Get the full file name and root_file_name (excluding extension)
    file_name, root_file_name = graph.file_name, graph.root_file_name
    # Plot the function
    graph.plot_function(f, *between)
    # Return a string / html representation of the graph
    return StrWithHtml('Image saved to ' + file_name,
        '''<img src="{}.svg" style="width: 100%" />'''.format(root_file_name))


# Miscellaneous small functions to be used within the calculator
pi = lambda: Real(nm.pi())
pi.__doc__ = ''' An anonymous function to calculate the value of pi
accurate to the current precision '''
radians = lambda x: x*pi()/handle_type(180)
radians.__doc__ = ''' An anonymous function to convert degrees to
radians '''
degrees = lambda x: x*handle_type(180)/pi()
degrees.__doc__ = ''' An anonymous function to convert radians to
degrees '''
wrapped_f = lambda f, g, x: f(x) if isinstance(x, Algebra)\
    else handle_type(g(x))
wrapped_f.__doc__ = ''' An anonymous function to evaluate an instance of
algebra or convert the output of a standard function to the appropriate
type '''
ln = partial(wrapped_f, Ln, dmath.log)
ln.__doc__ = ''' A wrapped version of dmath.log '''
sin = partial(wrapped_f, Sin, dmath.sin)
sin.__doc__ = ''' A wrapped version of dmath.sin '''
cos = partial(wrapped_f, Cos, dmath.cos)
cos.__doc__ = ''' A wrapped version of dmath.sin '''
tan = partial(wrapped_f, Tan, dmath.tan)
tan.__doc__ = ''' A wrapped version of dmath.tan '''


class Calculator(object):
    ''' An object providing an interactive, text driven, calculator. '''

    def __init__(self):
        # An array of accessible functions
        self.functions = {
        # Logarithms
            'ln': ln,
            'log': lambda a, b=10: dmath.log(a, b),
        # Trigonometric Functions
            'sin': lambda x: handle_type(sin(x)),
            'cos': lambda x: handle_type(cos(x)),
            'tan': lambda x: handle_type(tan(x)),
            'arcsin': lambda x: handle_type(dmath.asin(x)),
            'arccos': lambda x: handle_type(dmath.acos(x)),
            'arctan': lambda x: handle_type(dmath.atan(x)),
            'sinh': lambda x: handle_type(dmath.sinh(x)),
            'cosh': lambda x: handle_type(dmath.cosh(x)),
            'tanh': lambda x: handle_type(dmath.tanh(x)),
            'arcsinh': lambda z: handle_type(log(z + (Integer(1)
                + z**Integer(2))**Real('0.5'))),
            'arccosh': lambda z: ht(log(z + (z + Integer(1))**Real('0.5')
                * (z - Integer(1))**Real('0.5'))),
            'arctanh': lambda z: handle_type(log(Integer(1) + z)
                - log(Integer(1) - z))/Integer(2),
            'degrees': lambda x: handle_type(degrees(x)),
        # Statistics
            'nCr': nCr,
            'nPr': nPr,
            'binomialpdf': binomialpdf,
            'binomialcdf': binomialcdf,
            'poissonpdf': poissonpdf,
            'poissoncdf': poissoncdf,
            'normalcdf': normalcdf,
            'mean': lambda a: a.mean(),
            'median': lambda a: a.median(),
            'mode': lambda a: a.mode(),
            'variance': lambda a: a.variance(),
            'stdev': lambda a: a.stdev(),
            'sxx': lambda a: a.Sxx(),
        # Manipulation of functions
            'expand': expand,
            'differentiate': lambda a, b=Symbol('x'):\
                partial_differential(a, b),
            'integrate': lambda y, a=None, b=None, x=Symbol('x'):\
                partial_integral(y, x) if a == None or b == None \
                else partial_integral(y, x).limit(a, b, variable=x),
            'romberg': lambda f, a, b, *n: f.romberg_integral(a, b, *n),
            'trapeziumrule': lambda f, a, b, *n:\
                f.trapezoidal_integral(a, b, *n),
            'simpsonrule': lambda f, a, b, *n: f.simpson_integral(a, b, *n),
            'roots': lambda a, n=1000: List(*list(a.roots(n))),
            'maxima': lambda a, n=100: List(*a.maxima(n)),
            'minima': lambda a, n=100: List(*a.minima(n)),
        # Vectors
            'norm': lambda a: a.norm(),
        # Matrices
            'transpose': lambda a: a.transpose(),
            'order': lambda a: '{}×{}'.format(*a.order()),
            'eval': lambda a, b, c=None: a(b, variable=c),
            'identity': identity_matrix,
            'diag': diagonal_matrix,
            'inv': lambda a: a.inverse(),
            'invert': lambda a: a.inverse(),
            'decompose': lambda a: a.LU_decomposition(),
            'trace': lambda a: a.trace(),
            'poly': lambda a: a.characteristic_polynomial(),
            'adj': lambda a: a.adjgate(),
            'zero': Matrix,
            'minor': lambda a, b, c: a.minor(b, c),
            'det': lambda a: a.determinant(),
            'eigenvalues': lambda a: List(*a.eigenvalues()),
        # Complex Numbers
            're': lambda a: a.real,
            'im': lambda a: a.imag,
            'arg': lambda a: a.argument(),
            'conj': lambda a: a.conjugate(),
        # Misc
            'yum': pi,
            'plot': lambda f, a=-10, b=10: StrWithHtml('testing...',
                '''<canvas id="{0}" onclick="new CartesianPlot('{0}').simplePlot('{1}',{2},{3})" width="600" height="600">{4}</canvas>'''.format('graph-'
                    + str(random.randint(1, 1000)), f, a, b, gnuplot(f, a, b).html)),
            'polarplot': lambda f, a=-pi(), b=pi(): StrWithHtml('testing...',
                '''<canvas id="{0}" onclick="new PolarPlot('{0}').simplePlot('{1}',{2},{3})" width="600" height="600"></canvas>'''.format('graph-'
                    + str(random.randint(1, 1000)), f, a, b)),
            'testcanvas': lambda: StrWithHtml('testing...',
                '''<canvas id="testcanvas" width="600" height="600"></canvas>'''),
            'evalbetween': evalute_between,
            'factorial': factorial,
            'factors': lambda a: a.factors(),
            'decimal': lambda a: Decimal(a) if not isinstance(a, List)\
               else List(*list(map(Decimal, a))),
            'complex': lambda a: complex(a) if not isinstance(a, List)\
               else List(*list(map(complex, a))),
            'round': lambda a: handle_type(round),
            'list': lambda a: str(list(a)),
            'gnuplot': gnuplot,
            'type': lambda a: str(type(a)),
            'typelist': lambda b: ', '.join(map(lambda a: str(type(a)), b)),
            'typematrix': lambda c: '; '.join(map(lambda b:
                ', '.join(map(lambda a: str(type(a)), b)), c)),
            'setprec': self.set_precision,
            'setexact': self.set_exact,
            'about': lambda:\
                StrWithHtml('Copyright Tom Wright <tom.tdw@gmail.com>',
                '''<img src="./images/about.png" />
                <br>This program was written by Tom Wright
                 <tom.tdw@gmail.com>'''),
            'help': help.help,
            'quit': exit,
        }

        # An array of accessible post functions
        self.post_functions = {
            '!': factorial,
            'degs': radians
        }

        # An array of standard constants
        self.consts = {
            'pi': pi(),
            'g': Real('9.81'),
            'h': Real('6.62606896e-34'),
        }

        # An array of miscellaneous internal variables such as ans
        # which stores the previous result
        self.objects = {'ans': Integer(0)}

    def set_exact(self):
        ''' Tell the calculator to toggle the use of exact answers and
        return the previous answer in the new form. '''
        Real.exact_form = not Real.exact_form
        return self.objects['ans']

    def set_precision(self, a):
        ''' Set the number of significant figures to display, adjust the
        internal precision and return the previous answer in the new form. '''
        assert isinstance(a, int)
        assert a >= 0
        getcontext().prec = int(a) + PREC_OFFSET
        return self.objects['ans']

    def grammar(self):
        ''' A top-down recursive parser for handling algebraic expressions. '''

        # Start of BFN for parser
        # See design section in project report

        # Forward declarations for recursive definitions
        expr = Forward(); factor = Forward(); aterm = Forward()
        atom = Forward(); aexpr = Forward(); expr = Forward()
        const = Forward(); func = Forward()

        # Rules for the parsing of numbers
        uint = Word(nums)
        ufloat = Word(nums) + '.' + Word(nums)
        ucomplex = (Literal('i') | Literal('j')) + NotAny(func | const)
        unum = ufloat ^ uint ^ ucomplex
        sign = Word('+-', max=1)
        num = Optional(sign) + unum

        # Rules for algebraic data types
        variable = reduce(lambda a, b: a | b, map(Literal, srange('[a-z]')))\
        + NotAny(func | const)
        obj = 'ans' | Word(srange('[A-Z]'), max=1)
        vector = Suppress('[') + delimitedList(NotAny('[') + atom)\
            + Suppress(']')
        matrix = Suppress('[') + delimitedList(vector) + Suppress(']')

        # Rules for composite algebraic expressions
        exp = Literal("^") | Literal("**")
        mul = Literal("*") | Literal("/")
        add = Literal("+") | Literal("-")
        func << Word(srange('[a-zA-Z]')) + (atom | Suppress('(')\
            + Optional(delimitedList(expr)) + Suppress(')'))
        post_func = atom + (Literal('degs') | '!')
        const << (Literal('pi'))
        aabs = Suppress('|') + expr + Suppress('|')
        norm = Suppress('||') + expr + Suppress('||')
        atom << (Suppress('(') + expr + Suppress(')') | Suppress('$') + expr
            | const | vector | matrix | obj | num | variable | norm | aabs
            | func)
        factor << (atom ^ post_func) + Optional(Suppress(exp) + factor)
        aterm << factor + Optional((mul | FollowedBy(Literal('(')
            | Literal('[') | variable | obj)) + aterm)
        expr << aterm + ZeroOrMore(add + aterm)


        # Rules for variable assignments
        assign = Word(srange('[A-Z]')) + Suppress(':=') + expr

        command = Forward()
        command << (assign | expr) # + StringEnd()
        # End of BFN
        
        # Start of parser actions

        def _sign_action(a):
            ''' Generates a number based on an optional sign and number '''
            if len(a) == 1:
                return a[0]
            elif len(a) == 2:
                return int(a[0] + '1') * a[1]

        def _aterm_action(a):
            if len(a) == 1:
                return a[0]
            elif len(a) == 2:
                return a[0] * a[1]
            elif a[1] == '*':
                return a[0] * a[2]
            elif a[1] == '/':
                return a[0] / a[2]

        def _expr_action(a):
            result = a[0]
            for i in range(1, len(a), 2):
                if a[i] == '+':
                    result += a[i+1]
                if a[i] == '-':
                    result -= a[i+1]
            return result

        def _factor_action(a):
            if len(a) == 1:
                return a[0]
            else:
                return a[0] ** a[1]

        def _assign_action(vars, a):
            vars[a[0]] = a[1]
            return a[1]

        uint.setParseAction(lambda a: Integer(a[0]))
        ufloat.setParseAction(lambda a: Real(''.join(a)))
        ucomplex.setParseAction(lambda a: Complex(1j))
        num.setParseAction(_sign_action)
        variable.setParseAction(lambda a: Symbol(a[0]))
        obj.setParseAction(lambda a: self.objects[a[0]])
        matrix.setParseAction(lambda a: Matrix(list(map(list, a))))
        vector.setParseAction(lambda a: Vector(a))
        func.setParseAction(lambda a: self.functions[a[0]] (*a[1:]))
        post_func.setParseAction(lambda a: self.post_functions[a[1]] (a[0]))
        const.setParseAction(lambda a: self.consts[''.join(a)])
        aabs.setParseAction(lambda a: abs(a[0]))
        norm.setParseAction(lambda a: a[0].norm())
        factor.setParseAction(_factor_action)
        aterm.setParseAction(_aterm_action)
        expr.setParseAction(_expr_action)    
        assign.setParseAction(lambda a: _assign_action(self.objects, a))
    
        # End of parser actions
        
        # Return an algebraic or numeric containing the evaluated
        # expression
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
        elif (len(a) == 1) or isinstance(a[0], (int, float)):
            return '= ' + str(a[0])
