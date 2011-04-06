#!/usr/bin/env python
# coding=utf-8
''' A module containing code relating to Matrices. '''
from __future__ import division
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

# Standard modules
from functools import reduce
from copy import deepcopy
from decimal import Decimal

# Project modules
from cas.core import Algebra, Product, Symbol, expand
from cas.numeric import Integer

def identity_matrix(n):
    ''' Create an n*n identity matrix I(n) e.g. I(2) = [[1,0],[0,1]] '''
    # Create our new matrix a (whose entries will be defaulted to 0)
    a = Matrix(n,n)
    for i in range(n):
        # Set every entry on the first diagonal to 1
        a.values[i][i] = Integer(1)
    # Return our matrix a
    return a

def diagonal_matrix(*xs):
    ''' Create a diagonal matrix with elements xs on the first diagonal '''
    # Create our new matrix whose diagonal matches xs in length.
    n = len(xs)
    a = Matrix(n, n)
    for i, x in enumerate(xs):
        # Set every ith entry on the first diagonal to the ith element of xs.
        a[i][i] = x
    return a

class Matrix(Algebra):
    ''' A class to represent a matrix (2D array) '''
    def __init__(self, *a):
        ''' Initiate the the matrix based on the tuple of arguments a '''
        if len(a) == 2 and isinstance(a[0], int) and isinstance(a[1], int)\
            and a[0] >= 1 and a[0] >= 1:
            # If passed an order create a zero matrix of that order.
            self.__rows, self.__cols = a
            self.__values = [ [ Integer(0) for j in range(self.__cols) ]
                for i in range(self.__rows) ]
        elif len(a) == 1 and reduce(lambda a, b: a == b, map(len, a)):
            # If passed a multidimensional list with equal length rows,
            # use that for initial values.
            self.__values = list(a[0])
            self.__rows = len(self.__values)
            self.__cols = len(self.__values[0])
            # Check the multidimensional list passed is valid
            for row in self.__values:
                if len(row) != self.__cols:
                    raise ValueError('All rows of a matrix must be of equal'
                        + 'length')
        else:
            raise ValueError()

    def __getitem__(self, i):
        return self.__values[i]

    def trace(self):
        return sum(self.__values[i][i] for i in range(self.order()[0]))

    def order(self):
        ''' Return a tuple representing the order of the matrix '''
        return (self.__rows, self.__cols)

    def row(self, i):
        ''' Return a list representing one row '''
        return self.__values[i]

    def col(self, j):
        ''' Return a list representing one column. '''
        r = []
        for row in self.__values:
            r += [ row[j] ]
        return r

    def transpose(self):
        ''' Return a copy with rows and columns swapped. '''
        ans = Matrix(self.__cols, self.__rows)
        for i in range(self.__cols):
            for j in range(self.__rows):
                ans.values[i][j] = self.__values[j][i]
        return ans

    def map_to_all(self, f):
        ''' Apply a function to each value in the matrix '''
        return Matrix(list(map(lambda a: list(map(f, a)), self.__values)))

    def __neg__(self):
        return self.map_to_all(lambda a: -a)

    def __add__(self, other):
        ''' Add two matrices '''
        if isinstance(other, Matrix) and self.order() == other.order():
            # The result will be of the same order as self and other
            result = Matrix(*self.order())
            for i in range(self.__rows):
                for j in range(self.__cols):
                    # Each element of the result is the sum of the
                    # corresponding elements of self and other.
                    result.values[i][j]\
                        = self.__values[i][j] + other.values[i][j]
            return result
        else:
            return NotImplemented
    __radd__ = __add__

    def __sub__(self, other):
        return self + -other

    def __eq__(self, other):
        ''' If two matrices orders and elements are equal, they are equal '''
        if isinstance(other, Matrix):
            if self.order() != other.order():
                return False
            for i in range(self.__rows):
                for j in range(self.__cols):
                    if self[i][j] != other[i][j]:
                        return False
            return True
        else:
            return NotImplemented

    def minor(self, i, j):
        ''' Return a matrix after removing one col and rowumn '''
        r = self.transpose()
        del r.values[j]
        r.rows -= 1
        r = r.transpose()
        del r.values[i]
        r.rows -= 1
        return r

    def determinant(self, row=0):
        ''' The determinant of a 1*1 matrix is trivial and those for square
        matrices can be derived recursively from it. '''
        if self.__rows == self.__cols == 1:
            return self[0][0]
        elif self.__rows == self.__cols:
            ans = Integer(0)
            i = row;
            for j in range(self.__cols):
                ans += Integer(-1) ** j * self.__values[i][j]\
                    * self.minor(i,j).determinant()
            return ans
        else:
            raise ValueError('This matrix is not square')

    def adjgate(self):
        # adj(A)ij = (-1)^(i+j)*det[A(j|i)]
        if self.__rows != self.__cols:
            raise ValueError('This matrix is not square')

        ans = Matrix(*self.order())
        for i in range(self.order()[0]):
            for j in range(self.order()[1]):
                ans.values[i][j] = Integer(-1)**(i+j)\
                    * self.minor(j,i).determinant()
        return ans

    def eigenvalues(self):
        ''' The Eigenvalues of a matrix are defined as the roots of its
        characteristic polynomial. '''
        return self.characteristic_polynomial().roots()

    def __mul__(self, other):
        ''' Implement multiplication by Matrices or scalars '''
        if isinstance(other, Matrix):
            if self.__cols == other.rows:
                # If A = (𝛂ij)[l·m] and B = (𝛃ij)[m·n]
                # then AB is defined as the matrix C = (𝛄ij)[l·m]
                # such that 𝛄ij = 𝛂i1𝛃1j + 𝛂i2𝛃2j + ... + 𝛂im𝛃mj
                # For obvious reasons, this algorithm's complexity should 
                # increase at around O(n^3)
                r = Matrix(self.__rows, other.cols)
                for i in range(self.__rows):
                    for j in range(other.cols):
                        for k in range(len(self.row(i))):
                            r.values[i][j] += self.row(i)[k] * other.col(j)[k]
                return r
            else:
                return NotImplemented
        else:
            return self.map_to_all(lambda a: a*other)

    def __rmul__(self, other):
        ''' Matrix multiplication is not communicative so rely on the
        multiplication function of other. '''
        if isinstance(other, Matrix):
            return other.__mul__(self)
        else:
            return self.map_to_all(lambda a: other*a)

    def __str__(self):
        ''' Return a string representation. '''
        p = lambda a: +a if isinstance(a, Decimal) else a
        p.__doc__ = ''' Normalize a class if it is a subclass of decimal. '''
        s = lambda a: '[' + ', '.join(map(s, a)) + ']' if isinstance(a, list)\
            else str(p(a))
        s.__doc__ = ''' Recursively convert a multidimensional list to a
        string. '''
        return s(self.__values)

    def _scale_row(self, row, factor):
        ''' Multiply all elements in a row by a constant factor '''
        for j in range(self.__cols):
            self.__values[row][j] *= factor

    def _swap_rows(self, a, b):
        ''' Swap two rows of a matrix '''
        self.__values[a], self.__values[b] = self.__values[b], self.__values[a]

    def _scale_add_rows(self, a, b, factor):
        ''' Multiply each value in row a by a constant factor and add to
        row b '''
        for j in range(self.__cols):
            self.__values[b][j] += factor * self.__values[a][j]

    def LU_decomposition(self):
        ''' Split a square matrix into an upper and lower triangle matrix '''
        n = self.order()[0]
        L = identity_matrix(n); U = deepcopy(self)

        # Perform Gaussian elimination to find L and U
        for j in range(n):
            for i in range(j + 1, n):
                scale = U.values[i][j] / U.values[j][j]
                L.values[i][j] = scale
                U._scale_add_rows(j, i, -scale)

        return Product(L, U)

    def characteristic_polynomial(self):
        ''' The polynomial equations whose roots represent the eigenvalues
        of the matrix. '''
        # Note that some define the characteristic polynomial of a matrix as
        # the determinant of the product of abscissa and identity matrix
        # minus the matrix i.e. the inverse of this form.
        return expand((self - Symbol('x') 
            * identity_matrix(self.order()[0])).determinant())

    def inverse(self):
        ''' Calculate the matrix inverse using Gauss-Jordan elimination. '''
        # This method is not numerically stable so rounding errors may occur.
        # It will also break in the case of divide by zero
        # By inspection, the complexity grows at around O(n^3)

        if self.__rows != self.__cols:
            raise ValueError('Only square matrices may be inverted.')

        if self.determinant() == 0:
            raise ValueError('This matrix is singular!')

        scale = 0; n = self.__rows

        # A and B represent halves of an augmented matrix
        A = deepcopy(self)
        B = identity_matrix(n)

        # For each column or iteration
        for j in range(n):
            # Attempt to swap rows if the pivot is zero.
            if A.values[j][j] == 0:
                # For every row after the current
                for i in range(j+1,n+1):
                    # If the coresponding value is non-zero, swap and continue
                    if A.values[i][j] != 0:
                        A._swap_rows(i,j)
                        B._swap_rows(i,j)
                        break
                    # If when the final row is reached, no rows have been 
                    # swapped, the Matrix is singular.
                    elif i == n:
                        raise ValueError('This matrix is singular!')

            # Divide both halves by the pivot to gain 1 of the identity matrix.
            scale = Integer(1) / A.values[j][j]
            A._scale_row(j, scale)
            B._scale_row(j, scale)

            # For each other row
            for i in range(n):
                if i != j:
                    # Subtract by a multiple of row 1 to make 0 for identity
                    scale = - A.values[i][j]
                    A._scale_add_rows(j, i, scale)
                    B._scale_add_rows(j, i, scale)

        # By this stage A should be an identity matrix and B the inverse matrix
        return B

    def __repr__(self):
        ''' An string representing the matrix in python code. '''
        return 'Matrix(' + str(self) + ')'
