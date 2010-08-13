#!/usr/bin/env python3.1

from PyQt4 import QtCore, QtGui, uic

from gui_ui import Ui_Calculator
from calculator import Calculator
from cas.core import StrWithHtml

class CalculatorForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
#        self.ui = Ui_Calculator()
        uic.loadUi('gui.ui', self)
    #    self.ui.__init__(self)
        self.calc = Calculator()

    @QtCore.pyqtSlot()
    def on_lineEdit_returnPressed(self):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.textEdit.insertHtml('\n<p>\n')
        #try:
        command = self.lineEdit.text()
        output = self.calc.evaluate(command)
        self.textEdit.append(command)
        if type(output) == StrWithHtml:
            self.textEdit.insertHtml('\n<br>\n'
                + output.html + '\n')
        else:
            self.textEdit.append('   ' + str(output))
       # except:
       #     self.textEdit.insertHtml('<br><b style="color : red">Invalid Command!</b><br>\n')self.calc = Calculator()
        self.textEdit.insertHtml('\n</p>\n')


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
