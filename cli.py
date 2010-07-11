#!/usr/bin/env python3

import os
import readline
from calculator import Calculator

calc = Calculator()

if __name__ == '__main__':

    # Read any existing history file  
    try: readline.read_history_file()
    except: pass

    while True:
        try:
            # Input, evaluate and print command
            print(calc.evaluate(input('>>> ')))
            
            # Write command history
            readline.write_history_file()
        except SystemExit:
            print('Bye!')
            break
     #   except:
     #       print('Invalid command!')
