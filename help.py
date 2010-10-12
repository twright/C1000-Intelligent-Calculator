docs = ["""C1000 Intelligent Calculator

Welcome to the C1000 Intelligent Calculator. The C1000 provides all of the
functionality of a normal calculator plus many nice extras and advanced features
to make your life easier.

You can just type an equation in below to get the answer or find out more about
specific topics:
 1 : Basic calculation (GCSE,C1,C2)
 2 : Trigonometric functions (GCSE,C2,FP2)
 3 : Functions and equations (GCSE,C1,C2,C3,FP1)
 4 : Calculus (C2,C3,C4)
 5 : Vectors (C4)
 6 : Complex numbers (FP1)
 7 : Matrices (FP1,FP2)
 8 : Statistics (GCSE,S1,S2)

 (type help <number> to get help on a topic)""",
"""1 : Basic calculation (GCSE,C1,C2)

To perform a calculation, just enter it into the calculator's command box and
press the enter key to get the result.

We can start with simple arithmetic:
    >>> 1 + 2
    = 3
    >>> 4 - 2
    = 2
    >>> 4*2
    = 27/2
    >>> 1/3 + 1/2
    = 5/6
    >>> (2 + 3) * 4
    = 20
As you can see, fractions are treated correctly so results will be given in
exact form where possible.

We can also use powers with the '^' symbol (x^(1/2) = √x):
    >>> 5^2
    = 25
    >>> 5^3
    = 125
    >>> 25^(1/2)
    = 5
    >>> 5^(1/2)
    = 5^(1/2)
You will notice that the last result was given in exact form; to get it as a
decimal you can either use 'setexact()' to switch between using exact form and
decimals or the decimal function to convert a single result:
    >>> 5^(1/2)
    = 5^(1/2)
    >>> decimal (5^(1/2))
    = 2.24
    >>> setexact()
    = 2.24
    >>> 7^(1/3)
    = 1.91
Note that decimal values are given to 3 significant figures by default (as most
exam-boards require), but you can set how many are displayed with the setprec
function.
    >>> 5^(1/2)
    = 2.24
    >>> setprec 10
    = 2.236067977

To store answers for future use, the calculator provides upto 26 variable named
A to Z (they must be capitalised), as well as the ans variable which stores the
result of the previous calculation. You may use := to change a variable and refer to
it at any time by name:
    >>> 1/2
    = 1/2
    >>> ans - 1/3
    = 1/6
    >>> A := 5
    = 5
    >>> A^2 - A
    = 20""",
"""2 : Trigonometric functions (GCSE,C2,FP2)

The calculator will allow you to calculate all of the common trigonometric
functions:
    >>> sin 1
    = 0.841
    >>> cos 1
    = 0.540
    >>> tan 1
    = 1.56
However you must be aware that if you enter an angle without units, IT WILL BE
TAKEN AS RADIANS. To specific an angle is in degrees, just write degs after it:
    >>> sin (5 degs)
    = 0.0872
Note that whenever, exact answers will be given:
    >>> sin (pi/6)
    = 1/2
    >>> cos (pi/6)
    = 3^(1/2)/2
    >>> tan (pi/6)
    = 3^(1/2)/3

You may also use inverse trigonometric functions:
    >>> arcsin 1
    = pi/2
    >>> arccos 1
    = 0
    >>> arctan 1
    = pi/4
The values of these functions are also GIVEN IN RADIANS. To get them in degrees,
you can use the degrees function:
    >>> degrees (arcsin 1)
    = 90
    >>> degrees (arccos 1)
    = 0
    >>> degrees (arctan 1)
    = 45
    
Hyperbolic trigonometric functions are also supported:
    >>> sinh 1
    = 1.18
    >>> cosh 1
    = 1.54
    >>> tanh 1
    = 0.762
along with their inverses:
    >>> arcsinh 1
    = 0.881
    >>> arccosh 1
    = 0""",
"""3 : Solving equations (GCSE,C1)""",
"""4 : Calculus (C2,C3,C4)""",
"""5 : Vectors (C4)""",
"""6 : Complex numbers (FP1)""",
"""7 : Matrices (FP1,FP2)

The calculator allows your to directly enter matrices:
    >>> [[1,2],[3,4]]
    = [[1, 2], [3, 4]]
    >>> [[1,2],[3,4],[5,6]]
    = [[1, 2], [3, 4], [5, 6]]
You can also create an n by n identity matrix:
    >>> identity 3
    = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]

Matrices may be added:
    >>> [[2,3],[5,1]] + [[4,5],[2,1]]
    = [[6, 8], [7, 2]]
subtracted:
    >>> [[2,3],[5,1]] - [[4,5],[2,1]]
    = [[-2, -2], [3, 0]]
and multiplied:
    >>> [[2,3],[5,1]] * [[4,5],[2,1]]
    = [[14, 13], [22, 26]]
    >>> 7 * [[2,3],[5,1]]
    = [[14, 21], [35, 7]]
    >>> [[2,3],[5,1]] * identity 2
    = [[2, 3], [5, 1]]

You can calculate a matrix's determinant:
    >>> det [[1,5,2],[2,3,1],[2,4,1]]
    = 3
the inverse:
    >>> inv [[1,5,2],[2,3,1],[2,4,1]]
    = [[1/3, 1, 1/3], [0, -1, 1], [2/3, 2, 7/3]]
the characteristic polynomial:
    >>> poly [[1,5,2],[2,3,1],[2,4,1]]
    = -x^3 + 5x^2 + 11x + 3
the eigenvalues:
    >>> eigenvalues [[1,5,2],[2,3,1],[2,4,1]]
    = 6.71, -1.38, -0.323""",
"""8 : Statistics (GCSE,S1,S2)

The calculator supports a variety of functions useful for statistics.

We can use basic functions such as nCr:
    >>> nCr (5,2)
    = 10
and nPr:
    >>> nPr (5,2)
    = 60

We can also calculate probabilities from various distributions.
To calculate P(X = 3) where X ~ B(20, 0.3):
    >>> binomialpdf(20, 0.3, 3)
    = 0.0716
for P(X <= 3):
    >>> binomialcdf(20, 0.3, 3)
    = 0.107
and for P(X >= 3):
    >>> 1 - binomialcdf(20, 0.3, 2)
    = 0.965
To calculate P(X = 3) where X ~ P(6):
    >>> poissonpdf(6, 3)
    = 0.0892
for P(X <= 3):
    >>> poissoncdf(6, 3)
    = 0.151
and for P(X >= 3)
    >>> 1 - poissoncdf(6, 2)
    = 0.938
For standardised normal cumulative probabilities such as P(X < 2):
    >>> normalcdf(2)
    = 0.977"""
]

def help(n=0):
    return docs[n]
