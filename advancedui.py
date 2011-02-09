#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from PyQt4 import QtCore, QtGui, uic

from calculator import Calculator
from cas.core import StrWithHtml
import help


class CalculatorForm(QtGui.QMainWindow):
    ''' The advanced mode interface '''

    def __init__(self, parent=None):
        super(CalculatorForm, self).__init__(parent)
        uic.loadUi('advancedui.ui', self)
        self.calc = Calculator()

    @QtCore.pyqtSlot()
    def on_input_returnPressed(self):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertHtml('\n<p>\n')
        #try:
        command = str(self.input.text())
        output = self.calc.evaluate(command)
        self.textEdit.append(command)
        if isinstance(output, StrWithHtml):
            self.textEdit.insertHtml('\n<br>\n'
                + output.html + '\n')
        else:
            self.textEdit.append('   ' + str(output))
        # except:
        #     self.textEdit.insertHtml('<br><b style="color : red">'
        #       + 'Invalid Command!</b><br>\n')
        self.textEdit.insertHtml('\n</p>\n')

    @QtCore.pyqtSlot()
    def on_btn_help_clicked(self):
        help.help()


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
