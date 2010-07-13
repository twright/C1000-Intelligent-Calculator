#!/usr/bin/env python3

from PyQt4 import QtCore, QtGui


from calculator import Calculator
from ntypes import hstr


class Ui_MainWindow():
    def runCommand(self):
        self.textEdit.moveCursor(QtGui.QTextCursor.End)
    #    self.textEdit.selectAll()
        self.textEdit.insertHtml('\n<p>\n')
        #try:
        command = self.lineEdit.text()
        output = self.calc.evaluate(command)
        self.textEdit.append(command)
        if type(output) == hstr:
            self.textEdit.insertHtml('\n<br>\n' + output.html + '\n')
        else:
            self.textEdit.append('   ' + str(output))
       # except:
       #     self.textEdit.insertHtml('<br><b style="color : red">Invalid Command!</b><br>\n')
        self.textEdit.insertHtml('\n</p>\n')
    def setupUi(self, MainWindow):
        self.calc = Calculator()
        MainWindow.setObjectName('MainWindow')
        MainWindow.setFixedSize(512, 422)

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(0, 70, 512, 351))

        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(0, 0, 512, 61))
        font = QtGui.QFont()
        font.setFamily("Inconsolata")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.textEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("returnPressed()"),
            self.runCommand)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
