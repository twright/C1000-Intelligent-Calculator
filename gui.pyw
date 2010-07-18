#!/usr/bin/env python3.1

from PyQt4 import QtCore, QtGui

from gui_ui import Ui_Calculator
from calculator import Calculator
from cas_core import hstr

class CalculatorForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(CalculatorForm,self).__init__(parent)
        self.ui = Ui_Calculator()
        self.ui.setupUi(self)
        self.calc = Calculator()

    @QtCore.pyqtSlot()
    def on_lineEdit_returnPressed(self):
        self.ui.textEdit.moveCursor(QtGui.QTextCursor.End)
        self.ui.textEdit.insertHtml('\n<p>\n')
        #try:
        command = self.ui.lineEdit.text()
        output = self.calc.evaluate(command)
        self.ui.textEdit.append(command)
        if type(output) == StrWithHtml:
            self.ui.textEdit.insertHtml('\n<br>\n'
                + output.html + '\n')
        else:
            self.ui.textEdit.append('   ' + str(output))
       # except:
       #     self.textEdit.insertHtml('<br><b style="color : red">Invalid Command!</b><br>\n')self.calc = Calculator()
        self.ui.textEdit.insertHtml('\n</p>\n')


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
