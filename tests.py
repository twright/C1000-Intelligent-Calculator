#!/usr/bin/env python3.1
from cas_functions import *
from cas_core import *
from decimal import Decimal
import unittest
from calculator import *

class Parsing(unittest.TestCase):
    polys = ['3x^3 - 5', '18x^7 - 2.7x', '18x^7 - 2.7x',
        'x^5 + 6x^3 - x', 'x^7 + 2.5x^4 + 1', 'x^3 - 2x^2 - 24x - 30']
    def test_polys(self):
        ''' Once parsed, each polynomial is converted to a string and
        compareed with the input '''
        for a in self.polys:
            self.assertEqual(a, str(Calculator().grammar().parseString(a)[0]))

class Calculations(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_solve(self):
        ''' Test the solver works correctly '''
        self.assertEqual(self.calc.evaluate('solve (x^2 - 2x - 15)'),
            'x = 5 or -3')
        self.assertEqual(self.calc.evaluate('solve (x^3 - 19x - 30)'),
            'x = 5 or -3 or -2')
        self.assertEqual(self.calc.evaluate('solve (x^3 + 3x^2 - 6x - 8)'),
            'x = 2 or -4 or -1')

    def test_basic_maths(self):
        ''' Test that basic calculator functionality works '''
        pass


if __name__ == '__main__':
    unittest.main()
