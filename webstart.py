#!/usr/bin/env python3.1
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
import sys


class Form(QtGui.QDialog):
    ''' A form to manager the server '''

    def __init__(self, parent=None):
        from webbrowser import open_new
        from webui import start_webui
        from threading import Thread
        import socket
        super(Form, self).__init__(parent)
        uic.loadUi('webstart.ui', self)
        address = 'http://' + socket.gethostname() + ':8080/'
        #open_new(address)
        self.label.setText('Web Interface running at'
            + ' <a href = "{0}">{0}</a>'.format(address))
        self.webui = Thread(target=start_webui)
        self.webui.setDaemon(1)

    @QtCore.pyqtSlot()
    def on_btn_stop_pressed(self):
        sys.exit()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    form.webui.start()
    sys.exit(app.exec_())
