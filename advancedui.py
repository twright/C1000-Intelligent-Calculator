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

# Third party modules
from PyQt4 import QtCore, QtGui, uic

# Project modules
from calculator import Calculator
from cas.core import StrWithHtml
import help


class CalculatorForm(QtGui.QMainWindow):
    ''' The advanced mode interface '''

    def __init__(self, parent=None):
        ''' Initialize the graphical interface '''
        # Initialize the parent class
        super(CalculatorForm, self).__init__(parent)
        # Load the ui file
        uic.loadUi('advancedui.ui', self) # This is probably wrong
        # Create an instance of the calculator
        self.calc = Calculator()

    @QtCore.pyqtSlot()
    def on_input_returnPressed(self):
        ''' An event to handle a press of enter to calculate the
        result '''
        # Move the cursor to the end of the input box
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        # Insert the start of a new paragraph
        self.textEdit.insertHtml('\n<p>\n')
        
        # Catch any errors (i.e. invalid input) and display an error
        # message
        try:
            # Retrieve the command    
            command = str(self.input.text())
            # Evaluate the command
            output = self.calc.evaluate(command)
            
            # Append the command and result to the output box
            self.textEdit.append(command)
            if isinstance(output, StrWithHtml):
                self.textEdit.insertHtml('\n<br>\n'
                    + output.html + '\n')
            else:
                self.textEdit.append('   ' + str(output))
        except:
            self.textEdit.insertHtml('<br><b style="color : red">'
                + 'Invalid Command!</b><br>\n')
        # Insert the end of the paragraph
        self.textEdit.insertHtml('\n</p>\n')

    @QtCore.pyqtSlot()
    def on_btn_help_clicked(self):
        ''' '''
        help.help()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())