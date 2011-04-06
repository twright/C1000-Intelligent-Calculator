#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

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