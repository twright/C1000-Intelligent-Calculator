#!/usr/bin/env python3.1
''' A module containing code relating to Matrices. '''
from functools import reduce
from copy import deepcopy
from decimal import Decimal

from .core import Integer, Product
import cas.univariate as cf

def identity_matrix(n):
    ''' Create an n*n identity matrix I(n) e.g. [[1,0],[0,1]] '''
    a = Matrix(n,n)
    for i in range(n):
        a.values[i][i] = Integer(1)
    return a
    
def diagonal_matrix(*a):
    ''' Create a diagonal matrix with elements from arguments '''
    n = len(a)
    ans = Matrix(n, n)
    for i, item in enumerate(a):
        ans[i][i] = item
    return ans

class Matrix():
    ''' A class to represent a matrix (2D array) '''
    def __init__(self, *a):
        ''' Initiate the the matrix based on ... '''
        if len(a) == 2 and isinstance(a[0], int) and isinstance(a[1], int)\
            and a[0] >= 1 and a[0] >= 1:
            ''' If passed an order create a zero matrix of that order '''
            self.rows, self.cols = a
            self.values = [ [ Integer(0) for j in range(self.cols) ]
                for i in range(self.rows) ]
        elif len(a)==1 and reduce(lambda a,b: a==b, map(len, a)):
            ''' If passed a multidimensional list with equal length rows,
            use that for initial values '''
            self.values = list(a[0])
            self.rows = len(self.values)
            self.cols = len(self.values[0])
            for row in self.values:
                if len(row) != self.cols:
                    raise ValueError('All rows of a matrix must be of equal length')
        else:
            raise ValueError()
                
    def __getitem__(self, i):
        return self.values[i]

    def trace(self):
        return sum(self.values[i][i] for i in range(self.order()[0]))
    
    def order(self):
        ''' Return a tuple representing the order of the matrix '''
        return (self.rows, self.cols)
        
    def row(self, i):
        ''' Return a list representing one rowumn '''
        return self.values[i]
        
    def col(self, j):
        ''' Return a list representing one col '''
        r = []
        for row in self.values:
            r += [ row[j] ]
        return r
        
    def transpose(self):
        ''' Return a copy with rows and columns swapped. '''
        ans = Matrix(self.cols, self.rows)
        for i in range(self.cols):
            for j in range(self.rows):
                ans.values[i][j] = self.values[j][i]
        return ans
                
    def map_to_all(self, f):
        ''' Apply a function to each value in the matrix '''
        return Matrix(list(map(lambda a: list(map(f, a)), self.values)))
                
    def __neg__(self):
        return self.map_to_all(lambda a: -a)
                
    def __add__(self, other):
        ''' Add two matrices '''
        if isinstance(other, Matrix) and self.order() == other.order():
            result = Matrix(*self.order())
            for i in range(self.rows):
                for j in range(self.cols):
                    result.values[i][j] = self.values[i][j] + other.values[i][j]
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
            for i in range(self.rows):
                for j in range(self.cols):
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
        ''' The determinant of a 1*1 matrix is trivial and those for square matrices
        can be derived recursively from it. '''
        if self.rows == self.cols == 1:
            return self[0][0]
        elif self.rows == self.cols:
            ans = Integer(0)
            i = row;
            for j in range(self.cols):
                ans += Integer(-1) ** j * self.values[i][j] * self.minor(i,j).determinant()
            return ans
        else:
            raise ValueError('This matrix is not square')
            
    def adjgate(self):
        # adj(A)ij = (-1)^(i+j)*det[A(j|i)] 
        if self.rows != self.cols:
            raise ValueError('This matrix is not square')
        
        ans = Matrix(*self.order())
        for i in range(self.order()[0]):
            for j in range(self.order()[1]):
                ans.values[i][j] = Integer(-1)**(i+j) * self.minor(j,i).determinant()
        return ans
        
    def eigenvalues(self):
        return self.characteristic_polynomial().roots()
            
    def __mul__(self, other):
        ''' Implement multiplication by Matrices or scalars '''
        if isinstance(other, Matrix):
            if self.cols == other.rows:
                # If A = (𝛂ij)[l×m] and B = (𝛃ij)[m×n]
                # then AB is defined as the matrix C = (𝛄ij)[l×m]
                # such that 𝛄ij = 𝛂i1𝛃1j + 𝛂i2𝛃2j + ... + 𝛂im𝛃mj
                # For obvious reasons, this algorithm's complexity should increase
                # at around O(n^3)
                r = Matrix(self.rows, other.cols)
                for i in range(self.rows):
                    for j in range(other.cols):
                        for k in range(len(self.row(i))):
                            r.values[i][j] += self.row(i)[k] * other.col(j)[k]
                return r
            else:
                return NotImplemented
        else:
            return self.map_to_all(lambda a: a*other)
            
    def __rmul__(self, other):
        ''' Matrix multiplication is not communicative so rely on other function '''
        if isinstance(other, Matrix):
            return other.__mul__(self)
        else:
            return self.map_to_all(lambda a: other*a)
        
    def __str__(self):
        ''' Return a string representation '''
        p = lambda a: +a if isinstance(a, Decimal) else a
        # Recursively convert a multidimensional list to a string
        s = lambda a: '[' + ', '.join(map(s, a)) + ']' if isinstance(a, list)\
            else str(p(a))
        return s(self.values)
        
    def _scale_row(self, row, factor):
        ''' Multiply all elements in a row by a constant factor '''
        for j in range(self.cols):
            self.values[row][j] *= factor
    
#    def _swap_rows(self, r1, r2):
#        self.values[r1], self.values[r2] = self.values[r2], self.values[r1]
        
    def _scale_add_rows(self, a, b, factor):
        ''' Multiply each value in row a by a constant factor and add to row b '''
        for j in range(self.cols):
            self.values[b][j] += factor * self.values[a][j]
            
    def LU_decomposition(self):
        ''' Split a square matrix into an upper and lower triangle matrix '''
        n = self.order()[0]
        L = identity_matrix(n); U = deepcopy(self)
            
        # Perform naive Gaussian elimination to find L and U
        for j in range(n):
            for i in range(j+1,n):
                scale = U.values[i][j] / U.values[j][j]
                L.values[i][j] = scale
                U._scale_add_rows(j, i, -scale)
                
        return Product(L, U)
        
    def characteristic_polynomial(self):
        # Note that some define the characteristic polynomial of a matrix as
        # the determinant of the product of abscissa and identity matrix 
        # minus the matrix i.e. the inverse of this form
        return (self - cf.Term(1,'x',1) * identity_matrix(self.order()[0])
            ).determinant()
            
    def inverse(self):
        ''' Calculate the matrix inverse using Gauss-Jordan elimination. '''
        # This method is not numerically stable so rounding errors may occur.
        # It will also break in the case of divide by zero
        # By inspection, the complexity grows at around O(n^3)
        
        if self.rows != self.cols:
            raise ValueError('Only square matrices may be inverted.')
            
        if self.determinant() == 0:
            raise ValueError('This matrix is singular!')
        
        scale = 0; n = self.rows
        
        # A and B represent halves of an augmented matrix
        A = deepcopy(self)
        B = identity_matrix(n)
        
        # For each column or iteration
        for j in range(n):
            # The non-pivoted version of the algorithm cannot handle zeros
            if A.values[j][j] == 0:
                raise ValueError('This matrix cannot be inverted!')
        
            # Divide both halves by the pivot to gain to 1 of the identity matrix
            scale = Integer(1) / A.values[j][j]
            A._scale_row(j, scale)
            B._scale_row(j, scale)
            
            # For each other row
            for i in range(n):
                if i != j:
                    # Subtract by a multiple of the 1st row to make 0 for identity
                    scale = - A.values[i][j] # / A.values[j][j]
                    A._scale_add_rows(j, i, scale)
                    B._scale_add_rows(j, i, scale)
              
        # By this stage A should be an identity matrix, and B the inverse matrix
        return B
        
        '''
        More complex version derived from http://social.msdn.microsoft.com/forums/en-US/csharpgeneral/thread/6f4d2574-48f9-42d0-8ad4-73aaeb986304
        for c in range(n):
            if abs(A.values[c][c]) > 0.01:
                print(A.values[c][c])
                for r in range(c + 1, n):
                    if abs(A.values[r][c]) > 0.01:
                        A._swap_rows(c, r)
                        B._swap_rows(c, r)
                        break
                    if r > n:
                        raise ValueError('This matrix is singular')
                scale = 1.0 / A.values[c][c]
                A._scale_row(c, scale)
                B._scale_row(c, scale)
                
                for r in range(n):
                    if r != c:
                        scale = -A.values[r][c]
                        A._scale_add_rows(c, r, scale)
                        B._scale_add_rows(c, r, scale)
        print (A, B)
    '''
        
    def __repr__(self):
        return 'Matrix(' + str(self) + ')'
    
if __name__ == '__main__':
    print (Matrix([[1,2],[3,4]]).adjgate())
