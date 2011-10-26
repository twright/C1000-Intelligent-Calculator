#!/usr/bin/env python3

from distutils.core import setup  
from distutils.extension import Extension  
from Cython.Distutils import build_ext  
  
setup(  
  name = 'algorithms',  
  ext_modules=[  
    Extension('sorting_c', ['sorting_c.pyx'])  
    ],  
  cmdclass = {'build_ext': build_ext}  
)  

