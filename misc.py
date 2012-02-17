#!/usr/bin/env python
''' Assorted useful functions. '''
from __future__ import unicode_literals
__author__ = 'Tom Wright <tom.tdw@gmail.com>'
# Copyright 2012 Thomas Wright <tom.tdw@gmail.com>
# This file is part of C1000 Intelligent Calculator.
#
# C1000 Intelligent Calculator is free software: you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# C1000 Intelligent Calculator is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General Public License along with
# C1000 Intelligent Calculator.  If not, see <http://www.gnu.org/licenses/>.

# Standard modules
import random
import re
from tempfile import gettempdir

# Initialize the pseudorandom number generator
random.seed()

def gen_file_name(prefix='file', extension=''):
    ''' Generates a random file name in tmp '''
    # Get the path of the temp directory and replace all backslashes
    # with forward slashes for compatibility reasons
    temp = re.sub(r'\\', r'/', gettempdir(), 100)
    # Generate a random file path based upon the temp directory,
    # file extension, 4 random digits and the temp directory
    return '{}/{}-{}{}'.format(temp, prefix,
        str(random.randint(0000, 9999)), extension)

# A list of colours which may be used for highlighting.
colour_list = {
#    'Butter1': '#fce94f',
    'Butter2': '#edd400',
    'Butter3': '#c4a000',
    'Chameleon1': '#8ae234',
    'Chameleon2': '#73d216',
    'Chameleon3': '#4e9a06',
    'Orange1': '#fcaf3e',
    'Orange2': '#f57900',
    'Orange3': '#ce5c00',
    'SkyBlue1': '#729fcf',
    'SkyBlue2': '#3465a4',
    'SkyBlue3': '#204a87',
    'Plum1': '#ad7fa8',
    'Plum2': '#75507b',
    'Plum3': '#5c3566',
    'Chocolate1': '#e9b96e',
    'Chocolate2': '#c17d11',
    'Chocolate3': '#8f5902',
#     'ScarletRed1': '#ef2929',
    'ScarletRed2': '#cc0000',
#     'ScarletRed3': '#a40000',
#     'Aluminium1': '#eeeeec',
#     'Aluminium2': '#d3d7cf',
    'Aluminium3': '#babdb6',
    'Aluminium4': '#888a85',
    'Aluminium5': '#555753',
    'Aluminium6': '#2e3436'}
# Extract the colour hexes into a list
colours = [colour_list[x] for x in colour_list]
# Randomize the order of the list
random.shuffle(colours)


def colour_brackets(s):
    ''' Colourise matching brackets using html tags for the string
    s. '''
    result = ''
    # i tracks how deeply the brackets are nested
    i = 0
    # For each character c in the string s
    for c in s:
        if c == '(':
            # Each time we open a bracket we want to highlight it in the
            # ith colour and increment i
            result += '<b style="color: {}">(</b>'.format(colours[i])
            i += 1
        elif c == ')':
            # Each time we close a bracket we want to decrement i and
            # highlight it in the ith colour. If i is negative we know
            # the brackets are unmatched and highlight the bracket in
            # red.
            i -= 1
            result += '<b style="color: {}">)</b>'.format(colours[i]) \
                if i >= 0\
                else '<b style="background-color: #a40000; color: white">)</b>'
        else:
            # Normal characters should just be appended to the result.
            result += c
    return result
