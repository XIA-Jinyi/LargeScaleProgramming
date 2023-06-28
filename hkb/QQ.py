from PyQt5 import QtCore, QtGui, QtWidgets
from socket import *
import json
import sys
from chat import Ui_Dialog


class Ui_Login(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_Login, self).__init__()
        self.cancel = QtWidgets.QPushButton(self)
        self.Login = QtWidgets.QPushButton(self)
        self.password = QtWidgets.QLineEdit(self)
        self.account = QtWidgets.QLineEdit(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("Dialog")
        self.resize(332, 239)
        self.setMaximumSize(QtCore.QSize(332, 239))

        self.account.setGeometry(QtCore.QRect(80, 60, 197, 37))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)

        self.account.setFont(font)
        self.account.setInputMethodHints(QtCore.Qt.ImhNone)
        self.account.setText("")
        self.account.setObjectName("account")

        self.password.setGeometry(QtCore.QRect(80, 96, 197, 37))
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        password_font = QtGui.QFont()
        password_font.setFamily("宋体")
        password_font.setPointSize(12)
        password_font.setBold(True)
        password_font.setWeight(75)
        self.password.setFont(password_font)

        self.Login.setGeometry(QtCore.QRect(100, 170, 139, 32))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.Login.setFont(font)
        self.Login.setAutoFillBackground(False)
        self.Login.setObjectName("Login")
        self.Login.clicked.connect(self._login)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(10, 66, 51, 21))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(10, 106, 61, 31))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.radioButton = QtWidgets.QRadioButton(self)
        self.radioButton.setGeometry(QtCore.QRect(80, 140, 89, 16))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self)
        self.radioButton_2.setGeometry(QtCore.QRect(190, 140, 89, 16))
        self.radioButton_2.setObjectName("radioButton_2")

        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(0, 216, 64, 23))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.reg_account)

        self.cancel.setGeometry(QtCore.QRect(300, 0, 31, 21))
        self.cancel.setObjectName("cancel")
        self.cancel.clicked.connect(self._close)

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(10, 10, 31, 21))
        font = QtGui.QFont()
        font.setFamily("Aharoni")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "聊天登录"))
        self.cancel.setText(_translate("Dialog", "X"))
        self.Login.setText(_translate("Dialog", "登录"))
        self.label.setText(_translate("Dialog", "账号："))
        self.label_2.setText(_translate("Dialog", "密码："))
        self.radioButton.setText(_translate("Dialog", "记住密码"))
        self.radioButton_2.setText(_translate("Dialog", "找回密码"))
        self.pushButton_2.setText(_translate("Dialog", "注册账号"))
        self.label_3.setText(_translate("Dialog", "登录"))
        self.account.setPlaceholderText("请输入账号")
        self.password.setPlaceholderText("请输入密码")
        self.Login.setStyleSheet("background-color: #99FF99")
        self.pushButton_2.setStyleSheet("background-color:silver")
        self.cancel.setStyleSheet("background-color: #880000 ")

    def _login(self):
        get_account = self.account.text()
        get_password = self.password.text()
        if get_account is "" or get_password is "":
            QtWidgets.QMessageBox.warning(self, '警告', '密码账号错误',
                                          QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                                          QtWidgets.QMessageBox.Yes)

        else:
            login_data = {"type": "login", "id": get_account, "password": get_password}
            send_data = json.dumps(login_data)
            try:
                socket_client = socket(AF_INET, SOCK_STREAM)
                socket_client.connect(('127.0.0.1', 8848))
                socket_client.send(send_data.encode())
                self.chat_ui = Ui_Dialog(client=socket_client, account=get_account)
                self.chat_ui.show()
                self.close()
            except OSError:
                print("网络超时，请重新尝试")
            finally:
                pass

    def reg_account(self):
        self.close()

    def _close(self):
        self.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    w = Ui_Login()
    w.show()
    sys.exit(app.exec_())