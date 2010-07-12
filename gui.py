#!/usr/bin/env python3

from PyQt4 import QtCore, QtGui

from calculator import Calculator


class Ui_MainWindow():
    def runCommand(self):
      #  try:
        command = self.lineEdit.text()
        output = self.calc.evaluate(command)
        self.textEdit.append(command + '\n')
        if type(output) == str:
            self.textEdit.append(output + '\n')
        else:
            self.textEdit.insertHtml(output.html + '\n<br>\n')
     #   except:
     #       self.textEdit.insertHtml('<b style="color : red">Invalid Command!</b><br>\n<img src="///home/tom/Desktop/Computing%20Project/logo.png">')
    def setupUi(self, MainWindow):
        self.calc = Calculator()
        MainWindow.setObjectName('MainWindow')
        MainWindow.resize(512, 422)

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

        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL("returnPressed()"), self.runCommand)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
