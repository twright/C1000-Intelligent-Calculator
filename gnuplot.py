#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

import os
from misc import gen_file_name


class Gnuplot(object):
    ''' An object respresenting a graph drawn via gnuplot. '''

    def __init__(self, *f):
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
        if format == 'svg':
            self.send('set term svg enhanced size 400, 400')
        elif format == 'png':
            self.send('set term png enhanced size 1000, 1000')
        self.file_name = self.root_file_name + '.' + format
        self.send('set output "{}"'.format(self.file_name))

    def set_size(self, x, y):
        self.send('set size {}, {}'.format(x, y))

    def __del__(self):
        self.session.close()

    def send(self, cmd):
        self.session.write(cmd + '\n')
        self.session.flush()

    def plot(self, f):
        for format in ['svg', 'png']:
            self.set_format(format)
            self.send('plot ' + f)

    def plot_function(self, f, *limits):
        s = f.as_gnuplot_expression()
        if len(limits) == 0:
            self.plot(s)
        elif len(limits) == 2:
            a, b = limits
            self.plot('[{}:{}] {}'.format(a, b, s))
        else:
            raise ValueError('Two limits required')

    def replot(self):
        self.send('replot')
