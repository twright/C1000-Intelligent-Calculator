#!/usr/bin/env python3.1
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from PyQt4 import QtCore, QtGui, uic

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
#        self.ui = Ui_Calculator()
        uic.loadUi('start.ui', self)
    #    self.ui.__init__(self)

    @QtCore.pyqtSlot()
    def on_btn_simple_pressed(self):
        from gui2 import CalculatorForm
        ui = CalculatorForm()
        self.hide()
        ui.show()

    @QtCore.pyqtSlot()
    def on_btn_advanced_pressed(self):
        from gui import CalculatorForm
        ui = CalculatorForm()
        self.hide()
        ui.show()

    @QtCore.pyqtSlot()
    def on_btn_web_pressed(self):
        from webstart import Form
        form = Form()
        form.show()
#        WebUiManager()
#        self.hide()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

