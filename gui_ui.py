# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui.ui'
#
# Created: Tue Jul 20 19:42:52 2010
#      by: PyQt4 UI code generator 4.7.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Calculator(object):
    def setupUi(self, Calculator):
        Calculator.setObjectName("Calculator")
        Calculator.resize(512, 422)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icon.xpm"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Calculator.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(Calculator)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setMinimumSize(QtCore.QSize(0, 70))
        font = QtGui.QFont()
        font.setFamily("Inconsolata")
        font.setPointSize(14)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Inconsolata")
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setAutoFillBackground(False)
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        Calculator.setCentralWidget(self.centralwidget)

        self.retranslateUi(Calculator)
        QtCore.QMetaObject.connectSlotsByName(Calculator)

    def retranslateUi(self, Calculator):
        Calculator.setWindowTitle(QtGui.QApplication.translate("Calculator", "Calculator", None, QtGui.QApplication.UnicodeUTF8))
        self.textEdit.setHtml(QtGui.QApplication.translate("Calculator", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Inconsolata\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Calculator = QtGui.QMainWindow()
    ui = Ui_Calculator()
    ui.setupUi(Calculator)
    Calculator.show()
    sys.exit(app.exec_())

