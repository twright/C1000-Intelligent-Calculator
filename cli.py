#!/usr/bin/env python3.1

import os

if os.name == 'posix': import readline
import pyparsing_py3
from calculator import Calculator

calc = Calculator()

if __name__ == '__main__':

    # Read any existing history file 
    if os.name == 'posix': 
        try: readline.read_history_file()
        except: pass

    while True:
        try:
            # Input, evaluate and print command
            print(calc.evaluate(input('>>> ')))
            
            # Write command history
            if os.name == 'posix': readline.write_history_file()
        except SystemExit:
            print('Bye!')
            break
        except KeyError:
            print('Command not found!')
        except pyparsing_py3.ParseException:
            print('Invalid input!')
        except KeyboardInterrupt:
            print('Command cancelled.')
        except:
            print('Invalid operation!')
