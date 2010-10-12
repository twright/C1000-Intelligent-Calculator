#!/usr/bin/env python3.1
''' A commandline interface. '''

import os
from pyparsing_py3 import ParseException

if os.name == 'posix': import readline
from calculator import Calculator

calc = Calculator()

if __name__ == '__main__':
    # Read any existing history file 
    if os.name == 'posix': 
        try: readline.read_history_file()
        except: pass
        
    print('Welcome to the C1000 Intelligent Calculator')
    print('[ If you are stuck, just type help() ]')

    while True:
        try:
            # Input, evaluate and print command
            print(calc.evaluate(input('>>> ')))
            
            # Write command history
            if os.name == 'posix': readline.write_history_file()
        except SystemExit:
            print('Bye!')
            break
        except KeyError as e:
            print('Symbol not found:', e)
    #    except ParseException as e:
    #        print('Invalid input:', e)
    #    except (ValueError, ZeroDivisionError, TypeError) as e:
    #        print('Math error:', e)
        except KeyboardInterrupt:
            print('Command cancelled.')
  #      except:
  #          print('Invalid operation!')
