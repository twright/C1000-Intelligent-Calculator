#!/usr/bin/env python3.1

from decimal import Decimal, getcontext
from cas import *
from ntypes import *
from yeanpypa import *
getcontext.prec = 3

class Parser():
    number = Word(digit)

