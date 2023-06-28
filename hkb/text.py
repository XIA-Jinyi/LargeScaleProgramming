from PyQt5.QtWidgets import QApplication, QTextEdit, QTextBrowser, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtGui import QTextDocument

def transfer_content():
    # 创建应用程序和窗口
    app = QApplication([])
    window = QWidget()
    layout = QVBoxLayout()
    window.setLayout(layout)

    # 创建QTextEdit和QTextBrowser
    text_edit = QTextEdit()
    text_browser = QTextBrowser()

    # 创建一个按钮并连接到转移函数
    button = QPushButton("转移内容")
    button.clicked.connect(lambda: transfer(text_edit, text_browser))

    # 将小部件添加到布局中
    layout.addWidget(text_edit)
    layout.addWidget(button)
    layout.addWidget(text_browser)

    # 显示窗口
    window.show()
    app.exec()

def transfer(source: QTextEdit, target: QTextBrowser):
    # 获取QTextEdit的文本内容
    text = source.toPlainText()

    # 创建HTML文本
    html = "<html><body>"
    html += "<h1>文本内容</h1>"
    html += "<p>{}</p>".format(text)
    html += "<h1>图片</h1>"
    html += "<img src='buptchat.png'>"
    html += "</body></html>"

    # 将HTML设置为QTextBrowser的内容
    target.setHtml(html)

# 调用函数以展示界面和实现内容转移
transfer_content()
