#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

# Standard modules
from PyQt4 import QtCore, QtGui, uic
import re

# Project modules
from calculator import Calculator
import help


class CalculatorForm(QtGui.QMainWindow):
    ''' The simple interface '''

    def __init__(self, parent=None):
        ''' Initialize the interface. '''
        super(type(self), self).__init__(parent)
        uic.loadUi('simpleui.ui', self)
        self.calc = Calculator()

    def _command(self):
        ''' Return the user's command. '''
        return str(self.input.text())

    def _append(self, text):
        ''' Append text to the command entry box. '''
        # Retrieve the current command
        cmd = self._command()
        if re.match(r'[ ()]', cmd[-1]):
            # If the command ends with a space just append text.
            self.input.setText(cmd + text)
        else:
            # Otherwise append a space followed by text.
            self.input.setText(cmd + ' ' + text)

    def _append_digit(self, digit):
        # Retrieve the current command
        cmd = self._command()
        if len(cmd) == 0:
            # If the command is of zero length, just replace it with
            # digit.
            self.input.setText(digit)
        elif re.match(r'^([^a-z][a-z]|.*[0-9\.^ (])$', self._comma):
            # If the commands ends with a digit or and opening bracket,
            # just append the digit.
            self.input.setText(cmd + digit)
        else:
            # Otherwise append a space followed by digit.
            self.input.setText(cmd + ' ' + digit)

    # Event handlers for the buttons

    @QtCore.pyqtSlot()
    def on_btn_help_clicked(self):
        help.help()

    @QtCore.pyqtSlot()
    def on_input_returnPressed(self):
        output = re.sub(r'^= ', '', self.calc.evaluate(self._command()))
        self.input.setText(output)

    @QtCore.pyqtSlot()
    def on_btn_eval_clicked(self):
        output = re.sub(r'^= ', '', self.calc.evaluate(self._command()))
        self.input.setText(output)

    @QtCore.pyqtSlot()
    def on_btn_0_clicked(self):
        self._append_digit('0')

    @QtCore.pyqtSlot()
    def on_btn_1_clicked(self):
        self._append_digit('1')

    @QtCore.pyqtSlot()
    def on_btn_2_clicked(self):
        self._append_digit('2')

    @QtCore.pyqtSlot()
    def on_btn_3_clicked(self):
        self._append_digit('3')

    @QtCore.pyqtSlot()
    def on_btn_4_clicked(self):
        self._append_digit('4')

    @QtCore.pyqtSlot()
    def on_btn_5_clicked(self):
        self._append_digit('5')

    @QtCore.pyqtSlot()
    def on_btn_6_clicked(self):
        self._append_digit('6')

    @QtCore.pyqtSlot()
    def on_btn_7_clicked(self):
        self._append_digit('7')

    @QtCore.pyqtSlot()
    def on_btn_8_clicked(self):
        self._append_digit('8')

    @QtCore.pyqtSlot()
    def on_btn_9_clicked(self):
        self._append_digit('9')

    @QtCore.pyqtSlot()
    def on_btn_mantissa_clicked(self):
        self._append_digit('.')

    @QtCore.pyqtSlot()
    def on_btn_x_clicked(self):
        self._append_digit('x')

    @QtCore.pyqtSlot()
    def on_btn_i_clicked(self):
        self._append_digit('i')

    @QtCore.pyqtSlot()
    def on_btn_add_clicked(self):
        self._append('+')

    @QtCore.pyqtSlot()
    def on_btn_sub_clicked(self):
        self._append('-')

    @QtCore.pyqtSlot()
    def on_btn_mul_clicked(self):
        self._append('*')

    @QtCore.pyqtSlot()
    def on_btn_div_clicked(self):
        self._append('/')

    @QtCore.pyqtSlot()
    def on_btn_index_clicked(self):
        self._append_digit('^')

    @QtCore.pyqtSlot()
    def on_btn_left_bracket_clicked(self):
        self._append('(')

    @QtCore.pyqtSlot()
    def on_btn_right_bracket_clicked(self):
        self._append_digit(')')

    @QtCore.pyqtSlot()
    def on_btn_logax_clicked(self):
        self._append('log(a, x)')

    @QtCore.pyqtSlot()
    def on_btn_log_clicked(self):
        self._append('log')

    @QtCore.pyqtSlot()
    def on_btn_ln_clicked(self):
        self._append('ln')

    @QtCore.pyqtSlot()
    def on_btn_del_clicked(self):
        self.input.setText('')

    @QtCore.pyqtSlot()
    def on_btn_sin_clicked(self):
        self._append('sin')

    @QtCore.pyqtSlot()
    def on_btn_arcsin_clicked(self):
        self._append('arcsin')

    @QtCore.pyqtSlot()
    def on_btn_cos_clicked(self):
        self._append('cos')

    @QtCore.pyqtSlot()
    def on_btn_arccos_clicked(self):
        self._append('arccos')

    @QtCore.pyqtSlot()
    def on_btn_tan_clicked(self):
        self._append('tan')

    @QtCore.pyqtSlot()
    def on_btn_arctan_clicked(self):
        self._append('arctan')

    @QtCore.pyqtSlot()
    def on_btn_pi_clicked(self):
        self._append('pi')

    @QtCore.pyqtSlot()
    def on_btn_e_clicked(self):
        self._append('e')

    @QtCore.pyqtSlot()
    def on_btn_clear_clicked(self):
        self.input.setText('')

    @QtCore.pyqtSlot()
    def on_btn_fact_clicked(self):
        self._append_digit('!')

    @QtCore.pyqtSlot()
    def on_btn_factors_clicked(self):
        self._append('factors')

    @QtCore.pyqtSlot()
    def on_btn_abs_clicked(self):
        self._append('|')


if __name__ == '__main__':
    import sys

    app = QtGui.QApplication(sys.argv)
    calculator = CalculatorForm()
    calculator.show()
    sys.exit(app.exec_())
