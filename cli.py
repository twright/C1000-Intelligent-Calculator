#!/usr/bin/env python
''' A commandline interface. '''
from __future__ import unicode_literals
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

# Standard modules
import os
# Import the readline library for a history of commands if on a unix
# based operating system
if os.name == 'posix':
    import readline

# Third party modules
from pyparsing import ParseException

# Project modules
from calculator import Calculator


calc = Calculator()

if __name__ == '__main__':
    # Read any existing history file
    if os.name == 'posix':
        try:
            readline.read_history_file()
        except:
            pass

    # Print welcome message
    print('Welcome to the C1000 Intelligent Calculator')
    print('[ If you are stuck, just type help() ]')

    # Main loop for user interaction
    while True:
        try:
            # Input, evaluate and print command
            print(calc.evaluate(raw_input('>>> ')))

            # Write command history
            if os.name == 'posix':
                readline.write_history_file()
        except SystemExit:
            # Allow the user to exit on request
            print('Bye!')
            break
        except KeyError as e:
            # Handle functions / constants which cannot be found
            print('Symbol not found:', e)
        except ParseException as e:
            # Handle invalid expressions
            print('Invalid input:', e)
        except (ValueError, ZeroDivisionError, TypeError) as e:
            # Handle mathematical errors
            print('Math error:', e)
        except KeyboardInterrupt:
            # Handle Ctrl+C (cancel command)
            print('Command cancelled.')
        except:
            # Handle generic errors
            print('Invalid operation!')
