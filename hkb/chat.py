import sys
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, \
    QDesktopWidget, QToolTip, QPushButton, QMessageBox, QLabel
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import QCoreApplication
from windows_4 import *
from enum import Enum
from control import *

# app = QApplication([])

# friend_ls = []
friend_ls = [User() for _ in range(2)]
friend_ls[0].email = '1257820962@qq.com'
friend_ls[1].email = '1429099037@qq.com'

friend_ls[0].username = '张宇轩'
friend_ls[1].username = '黄凯博'

friend_ls[0].status = 0
friend_ls[1].status = 1

friend_new_ls = [User() for _ in range(2)]
friend_new_ls[0].email = '1257820962@qq.com'
friend_new_ls[1].email = '1429099037@qq.com'

friend_new_ls[0].username = '张宇轩'
friend_new_ls[1].username = '黄凯博'

friend_new_ls[0].status = 0
friend_new_ls[1].status = 1


# for i in range(len(friend_ls)):
#            print(i)
#           print(friend_ls[i].email)
class Example(QMainWindow, Ui_MainWindow):
    def __init__(self, username, email):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.email = email
        self.add_friend_status = 1
        self.add.clicked.connect(self.showMessageBox)
        self.pushButton.clicked.connect(self.front_update_friend_new_ls)
        self.initUI()

        # self.add.clicked.connect(self.front_update_friend_new_ls)

    def front_update_friend_ls(self):
        y = 0
        for i in range(len(friend_ls)):
            button = QPushButton(friend_ls[i].username + '\n' + friend_ls[i].email, self.friend_list)  # 这里是按钮的父类
            button.setGeometry(0, y, 211, 51)
            y += 50

    def front_update_friend_new_ls(self):
        y = 0

        for i in range(len(friend_new_ls)):
            print('1')
            label = QLabel(friend_new_ls[i].username + '(' + friend_new_ls[i].email + ')', self.comm)  # 这里是按钮的父类
            label.setGeometry(0, y, 570, 51)
            accept = QPushButton('接受√', label)  #
            accept.setGeometry(360, 15, 75, 23)
            refuse = QPushButton('拒绝×', label)  #
            refuse.setGeometry(470, 15, 75, 23)
            y += 50
            # self.show( )

    def initUI(self):
        """
        初始化用户界面的方法
        """

        self.setWindowTitle("buptchat")
        self.setWindowIcon(QIcon('chat.png'))
        self.front_update_friend_ls()
        # self.pushButton.clicked.connect(self.front_update_friend_new_ls)
        # self.front_update_friend_new_ls()
        self.show()

        # 显示窗口部件

    def setTooltipFont(self):
        """
        设置工具提示的字体
        """
        QToolTip.setFont(QFont('SansSerif', 10))

    def createButton(self):
        """
        创建按钮，并设置按钮的图标、工具提示等属性
        """
        btn = QPushButton('', self)
        btn.setToolTip(f'用户名: {self.username}\n邮箱: {self.email}')
        btn.setIcon(QIcon('icon.png'))
        btn.setIconSize(btn.size())
        btn.resize(btn.sizeHint())

    def center_and_resize(self):
        """
        图形界面设置，实现界面为屏幕1/4，并居中显示
        设置屏幕标题为"用户名"
        """
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width() // 2, screen.height() // 2)
        self.move(screen.width() // 4, screen.height() // 4)

    def set_username(self, new_username):
        """
        修改用户名的方法
        """
        self.username = new_username
        # 更新用户名属性

        self.setWindowTitle(self.username)
        # 更新窗口标题为新的用户名

    def closeEvent(self, event):

        reply = QMessageBox.question(self, '退出确认',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def set_email(self, email):
        """
        设置邮箱的方法
        """
        self.email = email
        # 更新邮箱属性

    def set_add_friend_status(self, add_friend_status):
        """
        设置好友申请请求
        """
        self.add_friend_status = add_friend_status

    def showMessageBox(self):
        if self.add_friend_status == 1:
            QMessageBox.information(self, 'Message', "好友申请发送成功")
        else:
            QMessageBox.information(self, 'Message', "该用户不存在")

    # def front_update_friend_new_ls(self):


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example('kb', '1429099037@qq.com')
    sys.exit(app.exec_())
