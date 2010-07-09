#!/usr/bin/env python3.1
from cas import *
import unittest

class Polynomial(unittest.TestCase):
    def setUp(self):
        self.y = polynomial('y',1,1,2,3,4,5)  
    def test_evaluate(self):
        ''' Evaluate works for sample values '''
        xys = ((3,'1029'),(0,'0'),(1,'7'),(.1,'0.102'),(-4,'-4228'))
        for a, b in xys:
            self.assertEqual(str(self.y.evaluate(a)), b)

if __name__ == '__main__':
    unittest.main()
