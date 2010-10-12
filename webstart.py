#!/usr/bin/env python3.1

from PyQt4 import QtCore, QtGui, uic

class Form(QtGui.QDialog):
    def __init__(self, parent=None):
        from webui import start_webui
        from webbrowser import open_new
        import socket
        from threading import Thread
        super().__init__(parent)
#        self.ui = Ui_Calculator()
        uic.loadUi('webstart.ui', self)
        open_new('http://localhost:8080/')
        ip = '127.0.0.1'
#        ip = [ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] 
#            if not ip.startswith("127.")][0]
        self.label.setText('Web Interface running at <a href = "{0}">{0}</a>'.format('http://' + ip + ':8080/'))
        self.__webui = Thread(target=start_webui)
        self.__webui.setDaemon(1)
        self.__webui.start()
    #    self.ui.__init__(self)
        
    @QtCore.pyqtSlot()
    def on_btn_stop_pressed(self):
        import sys
        sys.exit()
        
if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    form = Form()
    form.show()
    sys.exit(app.exec_())
