#!/usr/bin/env python3.1
''' Test the functionality of core cas functions like type handling,
the nint datatype and hstr's (html strings) '''

import unittest
from decimal import Decimal

from cas_core import *

class HandlingTypes(unittest.TestCase):
    vals = [(3.4,Decimal), (1,Integer), ('3.4',Decimal), ('4',Integer)]
    def test_handle_type(self):
        ''' Test that handle type assigns sample values the
        correct type'''
        for a, b in self.vals:
            self.assertEqual(type(handle_type(a)), b)

class NInts(unittest.TestCase):
    def test_division(self):
        ''' Dividing integers should result in either a decimal
        or integer, depending on common factors '''
        vals = [(3,4,Decimal('0.75')),(8,4,2)]
        for a,b,c in vals:
            self.assertEqual(Integer(a) / Integer(b), c)

    def test_addition(self):
        ''' Test addition works correctly for sample values '''
        vals = [(Integer(1),Integer(2),Integer(3)),
            (Integer(1),int(2),Integer(3)), (int(3),Integer(2),Integer(5)),
            (Integer(4),Decimal('2.1'),Decimal('6.1'))]
        for a,b,c in vals:
            self.assertEqual(a + b, c)
            self.assertEqual(type(a+b),type(c))

    def test_subtraction(self):
        ''' Test subtraction works correctly for sample values '''
        vals = [(Integer(1),Integer(2),Integer(-1)),
            (Integer(1),int(2),Integer(-1)), (int(3),Integer(2),Integer(1)),
            (Integer(4),Decimal('2.1'),Decimal('1.9'))]
        for a,b,c in vals:
            self.assertEqual(a - b, c)
            self.assertEqual(type(a-b),type(c))

    def test_multiplication(self):
        ''' Test multiplication works correctly for sample
        values '''
        vals = [(Integer(1),Integer(2),Integer(2)),
            (Integer(1),int(2),Integer(2)), (int(3),Integer(2),Integer(6)),
            (Integer(4),Decimal('2.1'),Decimal('8.4'))]
        for a,b,c in vals:
            self.assertEqual(a * b, c)
            self.assertEqual(type(a*b),type(c))

class Constants(unittest.TestCase):
    def test_equality(self):
        ''' Constants should be equal any number '''
        vals = (2, Decimal('5.6'), -2, 0, Decimal('Inf'))
        for x in vals:
            self.assertEqual(x, Constant())

if __name__ == '__main__':
    unittest.main()
