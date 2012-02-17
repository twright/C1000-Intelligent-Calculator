#!/usr/bin/env python
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
import os

# Project modules
from misc import gen_file_name


class Gnuplot(object):
    ''' An object representing a graph drawn via gnuplot. '''

    def __init__(self, *f):
        ''' Initialize the plot '''
        # Locate and open a session with gnuplot
        if os.name == 'posix':
            self.session = os.popen('gnuplot', 'w')
        else:
            self.session = os.popen(r'gnuplot\binary\gnuplot.exe', 'w')

        # Set file name if specified or use a file in tmp
        if len(f) == 1:
            self.file_name = str(*f)
        else:
            self.root_file_name = gen_file_name('plot')

        # Set gnuplot to output to png, at the correct size
        # and to the correct file
        self.set_format('svg')

        # Specify appearance options
        self.send('set samples 1000')
        self.send('set xlabel "x"')
        self.send('set ylabel "y"')
        self.send('unset key')
        self.send('set grid')

    def set_format(self, format):
        ''' Set the file format of the output. '''
        if format == 'svg':
            # Set the default options for svg
            self.send('set term svg enhanced size 400, 400')
        elif format == 'png':
            # Set the default options for png
            self.send('set term png enhanced size 1000, 1000')
        # Set the filename based upon the extension
        self.file_name = self.root_file_name + '.' + format
        self.send('set output "{}"'.format(self.file_name))

    def __del__(self):
        ''' On deletion close the session with gnuplot. '''
        self.session.close()

    def send(self, cmd):
        ''' Send a command to gnuplot. '''
        self.session.write(cmd + '\n')
        self.session.flush()

    def plot(self, f):
        ''' Plot a function f (given in a standard string format) in a
        variety of formats. '''
        for format in ['svg', 'png']:
            self.set_format(format)
            self.send('plot ' + f)

    def plot_function(self, f, *limits):
        ''' Plot a function f (an instance of Algebra) within optional
        limits. '''
        # Convert the function 
        function_string = f.as_gnuplot_expression()
        if len(limits) == 0:
            # If there are no limits, just pass the string to plot.
            self.plot(function_string)
        elif len(limits) == 2:
            # If there are 2 limits, pass them and the string to plot.
            a, b = limits
            self.plot('[{}:{}] {}'.format(a, b, function_string))
        else:
            # Otherwise show an error as the wrong number of limits
            # must have been given.
            raise ValueError('Two limits required')

    def replot(self):
        ''' Update the graph. '''
        self.send('replot')
