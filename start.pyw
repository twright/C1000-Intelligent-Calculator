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
