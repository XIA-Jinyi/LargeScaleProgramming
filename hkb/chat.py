import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from windows7 import *


class BuptChat(QMainWindow, Ui_MainWindow):
    def __init__(self, username, email):
        super().__init__()
        self.setupUi(self)
        self.username = username
        self.email = email
        self.add_friend_status = 1
        self.message = ""
        self.sender_name = ""
        self.Send.clicked.connect(self.transfer)
        self.add.clicked.connect(self.showMessageBox)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("buptchat")
        self.setWindowIcon(QIcon('buptchat.png'))
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

    def set_email(self, email):
        self.email = email

    def set_add_friend_status(self, add_friend_status):
        self.add_friend_status = add_friend_status

    def set_message(self, sender_name, new_message):
        self.sender_name = sender_name
        self.message = new_message

    def update_textBrowser(self, content):
        self.textBrowser.append(content)

    def transfer(self):
        text = self.textEdit.toHtml()
        self.textBrowser.append(f"<b>{self.username}:</b> {text}")
        self.textEdit.clear()

    def receive_message(self, sender_name, message):
        self.sender_name = sender_name
        self.message = message
        self.update_textBrowser()

    def update_textBrowser(self):
        if self.message['type'] == 'text':
            content = f"<b>{self.sender_name}:</b>\n{self.message['content']}"
            self.textBrowser.append(content)
        elif self.message['type'] == 'image':
            image_path = self.message['path']
            content = f"<b>{self.sender_name}:</b>"
            self.textBrowser.append(content)
            self.display_image(image_path)

    def display_image(self, image_path):
        # 将图片以HTML格式插入textBrowser
        self.textBrowser.append(f"<b>{self.sender_name}:</b>")
        self.textBrowser.append(f"<img src='{image_path}' width='200' height='200'>")




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BuptChat('kb', '1429099037@qq.com')

    # 创建包含图片信息的字典
    image_message = {
        'type': 'image',
        'path': 'buptchat.png'
    }

    ex.receive_message(sender_name='xjy', message=image_message)
    sys.exit(app.exec_())

# if (self.message != ''):
#     self.update_textBrowser(f"<b>{self.sender}:</b>\n \n{self.message}")  # 将message变量内容添加到textBrowser
#     self.message = ""  # 清空message变量