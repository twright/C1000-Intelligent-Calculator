#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from PyQt4 import QtCore, QtGui, uic

from gui2 import CalculatorForm as SimpleUiForm
from gui import CalculatorForm as AdvancedUiForm
from webstart import Form as WebUiForm

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ui = uic.loadUi('start.ui', self)

    @QtCore.pyqtSlot()
    def on_btn_simple_pressed(self):
        ui = SimpleUiForm()
        # self.hide()
        ui.show()

    @QtCore.pyqtSlot()
    def on_btn_advanced_pressed(self):
        ui = AdvancedUiForm()
        # self.hide()
        ui.show()

    @QtCore.pyqtSlot()
    def on_btn_web_pressed(self):
        ui = WebUiForm()
        ui.show()
        # ui.webui.start()
        # self.hide()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())

