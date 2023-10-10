import sys
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from windows_final import *
from enum import Enum
from control import *
from Model import *
import control
import functools
from PyQt5 import QtCore, QtGui, QtWidgets


class BuptChat(QMainWindow, Ui_MainWindow):
    updateFriendList = QtCore.pyqtSignal()
    clearTextBrowser = QtCore.pyqtSignal()
    setFriendName = QtCore.pyqtSignal()

    def __init__(self, username):
        super().__init__()
        self.setupUi(self)
        self.username = username

        # 这个add_friend_status用于判断是否可以加好友
        self.add_friend_status = 1
        self.message = ""
        self.sender_name = ""
        self.updateFriendList.connect(self.front_update_friend_ls)
        self.clearTextBrowser.connect(self.textBrowser.clear)
        self.setFriendName.connect(lambda: self.friend_name.setText(''))

        self.chatObject = ''
        self.add.clicked.connect(self.showMessageBox)
        self.pushButton.clicked.connect(self.front_update_friend_new_ls)
        self.Send.clicked.connect(self.transfer)
        self.Send.clicked.connect(self.textBrowser.raise_)
        self.remove.clicked.connect(self.deleteMessageBox)
        self.button_lst = []
        self.accept_lst = []
        self.refuse_lst = []

        self.chatlayout = QGridLayout()
        self.friend_list.setLayout(self.chatlayout)
        self.layout = QGridLayout()
        self.rqwindow.setLayout(self.layout)
        self.initUI()

    def createButton(self, friend):
        if friend.status == 1:
            status = '在线'
        else:
            status = '离线'
            return 0
        btn = QtWidgets.QPushButton(f"{friend.username}({status})\n{friend.email}", self.friend_list)
        btn.setObjectName(friend.email)
        btn.clicked.connect(lambda: self.set_chatObject(friend.email))
        btn.clicked.connect(lambda: self.set_friend_name(friend.username))
        btn.clicked.connect(lambda: self.chatwindow(friend.email))
        return btn

    def front_update_friend_ls(self):
        #print("front_called")
        y = 0
        for i in reversed(range(self.chatlayout.count())):
            self.chatlayout.itemAt(i).widget().setParent(None)
        self.chatlayout.setSpacing(10)

        for i, friend in enumerate(control.friend_ls):
            #print(friend.email)
            btn = self.createButton(friend)
            if (btn == 0):
                continue
            btn.setGeometry(0, y, 180, 50)
            btn.setFixedSize(180, 50)
            self.chatlayout.addWidget(btn, i, 0, Qt.AlignTop)
            y = y + btn.height()

    def front_update_friend_new_ls(self):
        self.friend_name.setText("好友申请表")
        y = 0
        for i in reversed(range(self.layout.count())):  # Clear the layout
            widget_to_remove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for i in range(len(control.friend_new_ls)):
            acp = QPushButton(f'接受√', self.rqwindow)
            acp.clicked.connect(lambda _, i=i: ctrl_confirm_add_friend(control.friend_new_ls[i].email))
            self.accept_lst.append(acp)
            ref = QPushButton('拒绝×', self.rqwindow)
            ref.clicked.connect(lambda _, i=i: self.del_add_friend(control.friend_new_ls[i].email))
            self.refuse_lst.append(ref)
            rqlabel = QLabel(control.friend_new_ls[i].username + '(' + control.friend_new_ls[i].email + ')',
                             self.rqwindow)
            self.layout.addWidget(rqlabel, y, 0, Qt.AlignLeft | Qt.AlignTop)
            self.layout.addWidget(self.accept_lst[i], y, 50, Qt.AlignLeft | Qt.AlignTop)
            self.layout.addWidget(self.refuse_lst[i], y, 80, Qt.AlignLeft | Qt.AlignTop)
            y += 1
        self.rqwindow.raise_()

    def get_search_editText(self):
        '''
        返回search_edit里的email
        '''
        return self.search_edit.text

    def chatwindow(self, email):
        '''
        显示message到聊天窗口,让textBrowser至于顶层
        '''
        self.textBrowser.clear()
        self.set_chatObject(email)
        text = get_message(email)
        #print(text)
        if (text != ''):
            string = text.split('$')
            for i in range(len(string)):
                result = string[i].split('<')
                if result[0] == control.client_account:
                    result[0] = '我'
                else:
                    for friend in control.friend_ls:
                        if friend.email == result[0]:
                            result[0] = friend.username
                self.textBrowser.append(result[0] + ':' + '\n' + result[1])
        self.textBrowser.raise_()

    def confirm_add_friend(self, tar_email):
        '''
        确定添加好友
        '''
        for i in range(len(control.friend_new_ls)):
            if control.friend_new_ls[i].email == tar_email:
                # Check if the user is already in friend_ls
                if not any(friend.email == tar_email for friend in control.friend_ls):
                    control.friend_ls.append(control.friend_new_ls[i])
                del control.friend_new_ls[i]
                break
        self.front_update_friend_new_ls()  # Update new friend list
        self.front_update_friend_ls()  # Update friend list

    def set_friend_name(self, name):
        self.friend_name.setText(name)

    def del_add_friend(self, tar_email):
        '''
        确定删除好友
        '''
        for i in range(len(control.friend_new_ls)):
            if control.friend_new_ls[i].email == tar_email:
                del control.friend_new_ls[i]
                break
        self.front_update_friend_new_ls()  # Update new friend list
        self.front_update_friend_ls()  # Update friend list

    def initUI(self):
        """
        初始化用户界面的方法
        """
        self.setWindowTitle('buptchat')
        self.setWindowIcon(QIcon('buptchat.png'))
        # self.front_update_friend_ls()
        self.show()

    def closeEvent(self, event):
        reply = QMessageBox.question(self, '退出确认',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def showMessageBox(self):
        # print('1')
        text = self.search_edit.toPlainText()
        # print(text)
        self.add_friend_status = request_add_friend(text)
        # print(self.add_friend_status)
        if self.add_friend_status == 1:
            QMessageBox.information(self, 'Message', "好友申请发送成功")
        else:
            QMessageBox.information(self, 'Message', "该用户不存在")

    def deleteMessageBox(self):
        reply = QMessageBox.question(self, 'Warning', '确认删除此好友吗?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            delete_friend(self.chatObject)
            # self.textBrowser.clear()
            # self.front_update_friend_ls()
            # self.friend_name.setText(' ')
        else:
            pass

    def remove_friend(self, friend_email):
        control.friend_ls = [friend for friend in control.friend_ls if friend.email != friend_email]

    def set_username(self, new_username):
        self.username = new_username

    def set_chatObject(self, chatObject):
        self.chatObject = chatObject


    def set_add_friend_status(self, add_friend_status):
        self.add_friend_status = add_friend_status

    def set_message(self, sender_name, new_message):
        self.sender_name = sender_name
        self.message = new_message

    def update_textBrowser(self, content):
        self.textBrowser.append(content)

    def transfer(self):
        text = self.textEdit.toHtml()
        build_message(self.textEdit.toPlainText())
        #print('after_build')
        send_message(self.chatObject)
        #print('after_send')
        self.textBrowser.append(f"<b>{self.username}:</b> {text}")
        self.textEdit.clear()

    def receive_message(self, sender_name, message):
        self.set_message(sender_name, message)
        self.update_textBrowser()

    def update_textBrowser(self):
        content = f"<b>{self.sender_name}:</b><br />{self.message}"
        self.textBrowser.append(content)

    def get_friend_request(self):
        self.search_edit.toPlainText()
