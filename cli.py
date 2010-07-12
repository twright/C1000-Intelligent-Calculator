#!/usr/bin/env python3

import os
import readline
import os
import pyparsing_py3
from calculator import Calculator

calc = Calculator()

if __name__ == '__main__':

    # Read any existing history file 
    if os.name == 'posix': readline.read_history_file()

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
            print('Command canceled.')
#        except:
#            print('Invalid operation!')
