#!/usr/bin/env python
''' Display help '''
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

# Standard modules
from webbrowser import open_new


def help():
    ''' Open the user manual using the default web browser. '''
    open_new("./help/index.html")
