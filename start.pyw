#!/usr/bin/env python
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from PyQt4 import QtCore, QtGui, uic

from simpleui import CalculatorForm as SimpleUiForm
from advancedui import CalculatorForm as AdvancedUiForm
from webstart import Form as WebUiForm

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.ui = uic.loadUi('start.ui', self)

    @QtCore.pyqtSlot()
    def on_btn_simple_pressed(self):
        simpleui.show()
        self.hide()

    @QtCore.pyqtSlot()
    def on_btn_advanced_pressed(self):
        advancedui.show()
        self.hide()

    @QtCore.pyqtSlot()
    def on_btn_web_pressed(self):
        webui.show()
        webui.webui.start()
        self.hide()


if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    simpleui = SimpleUiForm()
    advancedui = AdvancedUiForm()
    webui = WebUiForm()
    form = Form()
    form.show()
    sys.exit(app.exec_())
