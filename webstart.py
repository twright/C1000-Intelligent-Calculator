#!/usr/bin/env python3.1
__author__ = 'Tom Wright <tom.tdw@gmail.com>'

from PyQt4 import QtCore, QtGui, uic
import sys

def WebUiManager():
    form = Form()
    form.show()


class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        from webbrowser import open_new
        from webui import start_webui
        from threading import Thread
        import socket
        QtGui.QDialog.__init__(self,parent)
#        self.ui = Ui_Calculator()
        uic.loadUi('webstart.ui', self)
        address = 'http://' + socket.gethostname() + ':8080/'
        open_new(address)
        self.label.setText('Web Interface running at <a href = "{0}">{0}</a>'.format(address))
        self.webui = Thread(target=start_webui)
        self.webui.setDaemon(1)
#    webui.start()
        
    @QtCore.pyqtSlot()
    def on_btn_stop_pressed(self):
        sys.exit() 

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
#    WebUiManager()
    form = Form()
    form.show()
    form.webui.start()
    sys.exit(app.exec_())

