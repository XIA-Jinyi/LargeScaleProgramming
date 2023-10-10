import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication, Qt
from windows_11 import *
from enum import Enum
from control import *
from Model import *
import control
from PyQt5 import QtCore, QtGui, QtWidgets


def del_add_friend(tar_email):
    for i in range(len(control.friend_new_ls)):
        if control.friend_new_ls[i].email == tar_email:
            del control.friend_new_ls[i]
            break
    for i in range(len(control.friend_new_ls)):
        # print(control.friend_new_ls[i].email)
        pass

'''
control.friend_ls = [User() for _ in range(2)]
for i in range(2):
    control.friend_ls[i].email = '1257820962@qq.com'
    control.friend_ls[i].username = '111'
    control.friend_ls[i].status = '1'

control.friend_ls[0].email = '1257820962@qq.com'
control.friend_ls[1].email = '1429099037@qq.com'

control.friend_ls[0].username = '张宇轩'
control.friend_ls[1].username = '黄凯博'

control.friend_ls[0].status = 0
control.friend_ls[1].status = 1

control.friend_new_ls = [User() for _ in range(3)]
for i in range(3):
    control.friend_new_ls[i].email = '1257820962@qq.com'
    control.friend_new_ls[i].username = '111'
    control.friend_new_ls[i].status = '1'

control.friend_new_ls[0].email = 'first@qq.com'
control.friend_new_ls[1].email = 'second@qq.com'
control.friend_new_ls[2].email = 'third@qq.com'

control.friend_new_ls[0].username = '张宇轩'
control.friend_new_ls[1].username = '黄凯博'
control.friend_new_ls[2].username = 'hgl'

control.friend_new_ls[0].status = 0
control.friend_new_ls[1].status = 1
control.friend_new_ls[2].status = 1
'''

class Example(QMainWindow, Ui_MainWindow):
    def __init__(self, username, email):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.email = email
        self.add_friend_status = 1
        self.message = ""
        self.sender_name = ""

        self.chatObject = ""
        self.add.clicked.connect(self.showMessageBox)
        self.pushButton.clicked.connect(self.front_update_friend_new_ls)
        self.Send.clicked.connect(self.transfer)
        self.Send.clicked.connect(self.textBrowser.raise_)
        self.button_lst = []
        self.accept_lst = []
        self.refuse_lst = []
        update_front_entity(self)

        self.chatlayout = QGridLayout()
        self.friend_list.setLayout(self.chatlayout)
        self.layout = QGridLayout()
        self.rqwindow.setLayout(self.layout)
        self.initUI()

    def front_update_friend_ls(self):
        y = 0
        for i in reversed(range(self.chatlayout.count())):
            self.chatlayout.itemAt(i).widget().setParent(None)
        self.chatlayout.setSpacing(10)


        for i, friend in enumerate(control.friend_ls):
            btn = QPushButton(f"{friend.username}\n{friend.email}", self.friend_list)
            btn.setObjectName(friend.email)
            btn.clicked.connect(self.chatwindow)
            btn.setGeometry(0, y,180, 50)
            btn.setFixedSize(180, 50)
            self.chatlayout.addWidget(btn, i, 0, Qt.AlignTop)
            y = y + btn.height()

    def front_update_friend_new_ls(self):
        y = 0
        for i in reversed(range(self.layout.count())):  # Clear the layout
            widget_to_remove = self.layout.itemAt(i).widget()
            self.layout.removeWidget(widget_to_remove)
            widget_to_remove.setParent(None)

        for i in range(len(control.friend_new_ls)):
            acp = QPushButton(f'接受√', self.rqwindow)
            acp.clicked.connect(lambda _, i=i: self.confirm_add_friend(control.friend_new_ls[i].email))
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

    def chatwindow(self):
        text=get_message(control.friend_ls[i].email)
        string=text.split('$')
        for i in range(string):
            result=string[i].split('<')
            self.textBrowser.setPlainText(result)
        #self.textBrowser.setPlainText("Hello, World!")
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
        self.front_update_friend_ls()
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
        if self.add_friend_status == 1:
            QMessageBox.information(self, 'Message', "好友申请发送成功")
        else:
            QMessageBox.information(self, 'Message', "该用户不存在")

    def set_username(self, new_username):
        self.username = new_username

    def set_chatObject(self, chatObject):
        self.chatObject = chatObject

    def set_email(self, email):
        self.email = email

    def set_add_friend_status(self, add_friend_status):
        self.add_friend_status = add_friend_status

    def set_message(self, sender_name, new_message):
        self.sender_name = sender_name
        self.message = new_message


    def transfer(self):
        text = self.textEdit.toHtml()
        self.textBrowser.append(f"<b>{self.username}:</b> {text}")
        self.textEdit.clear()

    def receive_message(self, sender_name, message):
        self.set_message(sender_name, message)
        content = f"<b>{self.sender_name}:</b><br />{self.message}"
        self.textBrowser.append(content)

        

    def get_friend_request(self):
        self.search_edit.toPlainText()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example('kb', '1429099037@qq.com')
    control.init_after_login(ex)
    ex.receive_message(sender_name='xjy', message="kb")
    sys.exit(app.exec_())
