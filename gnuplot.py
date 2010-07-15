#!/usr/bin/env python3.1
import os
import random
from tempfile import gettempdir
import re
random.seed()

def gen_file_name():
    ''' Generates a random file name in tmp '''
    return re.sub(r'\\', r'/',
        (gettempdir() + '\\plot-%s.svg' % str(random.randint(1000,9999)))
        [2 if os.name == 'nt' else None:], 100)

class Gnuplot:
    def __init__(self, *f):
        # Locate and open a session with gnuplot
        if os.name == 'posix': self.session = os.popen("gnuplot","w")
        else: self.session = os.popen("gnuplot\\binary\\gnuplot.exe","w")
        
        # Set file name if specified or use a file in tmp
        if len(f) == 1: self.file_name = str(*f)
        else: self.file_name = gen_file_name()

        # Set gnuplot to output to png, at the correct size
        # and to the correct file
        self.send('set term svg enhanced size 400, 400')
        self.send('set output "%s"' % self.file_name)

    #    self.send('set font "consolas"')
    #    self.send('set enhanced')
    #    self.send('set nocrop')
    #    self.send('set size 60,50')

        # Specify appearance options
        self.send("set xlabel 'x'")
        self.send("set ylabel 'y'")
        self.send("unset key")
        self.send('set grid')

    def __del__(self):
        self.session.close()

    def send(self, cmd):
        self.session.write(cmd + '\n')
        self.session.flush()

    def plot(self, f):
        self.send('plot ' + f)

    def plot_function(self, f, *limits):
        s = f.as_gnuplot_expression()
        if len(limits) == 0:
            self.plot(s)
        elif len(limits) == 2:
            self.plot('[%s:%s] ' % limits + s)
        else:
            raise ValueError('Two limits required')

    def replot(self):
        self.send('set terminal png')
        self.send('set output "%s"' % self.file_name)
        self.send('replot')
