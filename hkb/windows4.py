# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'windows_3.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1091, 593)
        MainWindow.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.user = QtWidgets.QFrame(self.centralwidget)
        self.user.setMaximumSize(QtCore.QSize(50, 16777215))
        self.user.setStyleSheet("QFrame{\n"
"    background-color:rgb(46, 46, 46)\n"
"}\n"
"")
        self.user.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.user.setFrameShadow(QtWidgets.QFrame.Raised)
        self.user.setLineWidth(10)
        self.user.setObjectName("user")
        self.horizontalLayout.addWidget(self.user)
        self.send = QtWidgets.QFrame(self.centralwidget)
        self.send.setStyleSheet("QFrame{\n"
"    background-color:rgb(245, 245, 245)\n"
"}")
        self.send.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.send.setFrameShadow(QtWidgets.QFrame.Raised)
        self.send.setLineWidth(10)
        self.send.setObjectName("send")
        self.friend_list = QtWidgets.QFrame(self.send)
        self.friend_list.setGeometry(QtCore.QRect(0, 50, 211, 721))
        self.friend_list.setStyleSheet("QFrame{\n"
"    background-color:rgb(234, 232, 231)\n"
"}")
        self.friend_list.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.friend_list.setFrameShadow(QtWidgets.QFrame.Plain)
        self.friend_list.setLineWidth(10)
        self.friend_list.setObjectName("friend_list")
        self.search = QtWidgets.QFrame(self.send)
        self.search.setGeometry(QtCore.QRect(0, 0, 211, 51))
        self.search.setStyleSheet("QFrame{\n"
"    background-color:rgb(247,247,247);\n"
"}")
        self.search.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.search.setFrameShadow(QtWidgets.QFrame.Raised)
        self.search.setObjectName("search")
        self.add = QtWidgets.QPushButton(self.search)
        self.add.setGeometry(QtCore.QRect(180, 10, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        self.add.setFont(font)
        self.add.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.add.setStyleSheet("QPushButton {\n"
"    background-color: rgb(226, 226, 226);\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(210, 210, 210);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"}\n"
"")
        self.add.setObjectName("add")
        self.search_edit = QtWidgets.QTextEdit(self.search)
        self.search_edit.setGeometry(QtCore.QRect(10, 10, 151, 21))
        self.search_edit.setStyleSheet("QTextEdit {\n"
"    background-color: rgb(226, 226, 226); /* 设置背景颜色 */\n"
"    color: rgb(129,129,129); /* 设置文本颜色 */\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: black;\n"
"}")
        self.search_edit.setObjectName("search_edit")
        self.comm = QtWidgets.QFrame(self.send)
        self.comm.setGeometry(QtCore.QRect(210, 50, 881, 431))
        self.comm.setStyleSheet("QFrame{\n"
"    background-color:rgb(245, 245, 245);\n"
"    border-bottom: 0.5px solid lightgrey;\n"
"}")
        self.comm.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.comm.setFrameShadow(QtWidgets.QFrame.Raised)
        self.comm.setObjectName("comm")
        self.textEdit = QtWidgets.QTextEdit(self.send)
        self.textEdit.setGeometry(QtCore.QRect(210, 480, 881, 271))
        self.textEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.textEdit.setStyleSheet("QTextEdit {\n"
"    background-color: rgb(245,245,245);  /* 设置背景颜色 */\n"
"    color: black;  /* 设置文本颜色 */\n"
"}")
        self.textEdit.setObjectName("textEdit")
        self.friend_info = QtWidgets.QFrame(self.send)
        self.friend_info.setGeometry(QtCore.QRect(210, 0, 881, 51))
        self.friend_info.setStyleSheet("QFrame{\n"
"    background-color:rgb(245, 245, 245);\n"
"    border-bottom: 0.5px solid lightgrey;\n"
"}")
        self.friend_info.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.friend_info.setFrameShadow(QtWidgets.QFrame.Raised)
        self.friend_info.setObjectName("friend_info")
        self.remove = QtWidgets.QPushButton(self.friend_info)
        self.remove.setGeometry(QtCore.QRect(800, 10, 21, 21))
        font = QtGui.QFont()
        font.setFamily("Microsoft Sans Serif")
        self.remove.setFont(font)
        self.remove.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.remove.setStyleSheet("QPushButton {\n"
"    background-color: rgb(226, 226, 226);\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(210, 210, 210);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"}\n"
"")
        self.remove.setObjectName("remove")
        self.Send = QtWidgets.QPushButton(self.send)
        self.Send.setGeometry(QtCore.QRect(950, 550, 81, 31))
        self.Send.setStyleSheet("QPushButton {\n"
"    background-color: rgb(233, 233, 233);\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    color:rgb(7,193,96);\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: rgb(210, 210, 210);\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    border-style: inset;\n"
"}\n"
"")
        self.Send.setObjectName("Send")
        self.horizontalLayout.addWidget(self.send)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.add.setText(_translate("MainWindow", "+"))
        self.search_edit.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><meta charset=\"utf-8\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"hr { height: 1px; border-width: 0; }\n"
"li.unchecked::marker { content: \"\\2610\"; }\n"
"li.checked::marker { content: \"\\2612\"; }\n"
"</style></head><body style=\" font-family:\'Microsoft YaHei UI\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.remove.setText(_translate("MainWindow", "-"))
        self.Send.setText(_translate("MainWindow", "Send"))
