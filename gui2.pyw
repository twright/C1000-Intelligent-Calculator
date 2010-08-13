#!/usr/bin/env python3.1

from PyQt4 import QtCore, QtGui, uic
import re

from gui_ui import Ui_Calculator
from calculator import Calculator
from cas.core import StrWithHtml

class CalculatorForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
#        self.ui = Ui_Calculator()
        uic.loadUi('gui2.ui', self)
    #    self.ui.__init__(self)
        self.calc = Calculator()

    def _command(self):
        return self.input.text()

    def _append(self, a):
        cmd = self._command()
        if len(cmd) == 0:
            self.input.setText(a)
        elif cmd[-1] == ' ':
            self.input.setText(cmd + a)
        else:
            self.input.setText(cmd + ' ' + a)

    @QtCore.pyqtSlot()
    def on_input_returnPressed(self):
        output = re.sub(r'^= ', '', self.calc.evaluate(self._command()))
        self.input.setText(output)

    @QtCore.pyqtSlot()
    def on_btn_eval_clicked(self):
        output = re.sub(r'^= ', '', self.calc.evaluate(self._command()))
        self.input.setText(output)

    @QtCore.pyqtSlot()
    def on_btn_0_clicked(self): self._append('0')
    @QtCore.pyqtSlot()
    def on_btn_1_clicked(self): self._append('1')
    @QtCore.pyqtSlot()
    def on_btn_2_clicked(self): self._append('2')
    @QtCore.pyqtSlot()
    def on_btn_3_clicked(self): self._append('3')
    @QtCore.pyqtSlot()
    def on_btn_4_clicked(self): self._append('4')
    @QtCore.pyqtSlot()
    def on_btn_5_clicked(self): self._append('5')
    @QtCore.pyqtSlot()
    def on_btn_6_clicked(self): self._append('6')
    @QtCore.pyqtSlot()
    def on_btn_7_clicked(self): self._append('7')
    @QtCore.pyqtSlot()
    def on_btn_8_clicked(self): self._append('8')
    @QtCore.pyqtSlot()
    def on_btn_9_clicked(self): self._append('9')
    @QtCore.pyqtSlot()
    def on_btn_add_clicked(self): self._append('+')
    @QtCore.pyqtSlot()
    def on_btn_sub_clicked(self): self._append('-')
    @QtCore.pyqtSlot()
    def on_btn_mul_clicked(self): self._append('*')
    @QtCore.pyqtSlot()
    def on_btn_div_clicked(self): self._append('/')
    @QtCore.pyqtSlot()
    def on_btn_index_clicked(self): self._append('^')
    @QtCore.pyqtSlot()
    def on_btn_left_bracket_clicked(self): self._append('(')
    @QtCore.pyqtSlot()
    def on_btn_right_bracket_clicked(self): self._append(')')
    @QtCore.pyqtSlot()
    def on_btn_logax_clicked(self): self._append('log(a, x)')
    @QtCore.pyqtSlot()
    def on_btn_log_clicked(self): self._append('log')
    @QtCore.pyqtSlot()
    def on_btn_ln_clicked(self): self._append('ln')
    @QtCore.pyqtSlot()
    def on_btn_del_clicked(self): self.input.setText('')
    @QtCore.pyqtSlot()
    def on_btn_sin_clicked(self): self._append('sin')
    @QtCore.pyqtSlot()
    def on_btn_arcsin_clicked(self): self._append('arcsin')
    @QtCore.pyqtSlot()
    def on_btn_cos_clicked(self): self._append('cos')
    @QtCore.pyqtSlot()
    def on_btn_arccos_clicked(self): self._append('arccos')
    @QtCore.pyqtSlot()
    def on_btn_tan_clicked(self): self._append('tan')
    @QtCore.pyqtSlot()
    def on_btn_arctan_clicked(self): self._append('arctan')
    @QtCore.pyqtSlot()
    def on_btn_pi_clicked(self): self._append('pi')
    @QtCore.pyqtSlot()
    def on_btn_e_clicked(self): self._append('e')
    @QtCore.pyqtSlot()
    def on_btn_i_clicked(self): self._append('i')
    


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
