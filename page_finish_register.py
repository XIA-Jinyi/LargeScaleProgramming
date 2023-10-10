
from tkinter import *
from tkinter.ttk import *
from typing import Dict
from buptchat import *

class WinGUI(Tk):
    """注册成功反馈页面实现"""
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        """初始化页面"""
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_title"] = self.__tk_label_title(self)
        self.widget_dic["tk_label_content"] = self.__tk_label_content(self)

    def __win(self):
        """设置登录界面标题"""
        self.title("注册成功")
        # 设置窗口大小、居中
        width = 319
        height = 161
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

    def scrollbar_autohide(self,bar,widget):
        """自动隐藏滚动条"""
        self.__scrollbar_hide(bar,widget)
        widget.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        bar.bind("<Enter>", lambda e: self.__scrollbar_show(bar,widget))
        widget.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
        bar.bind("<Leave>", lambda e: self.__scrollbar_hide(bar,widget))
    
    def __scrollbar_show(self,bar,widget):
        bar.lift(widget)

    def __scrollbar_hide(self,bar,widget):
        bar.lower(widget)
        
    def __tk_label_title(self,parent):
        """创建标题

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="注册成功",anchor="center", )
        label.place(x=40, y=10, width=239, height=58)
        return label

    def __tk_label_content(self,parent):
        """创建内容

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="注册已完成，即将自动登录！",anchor="center", )
        label.place(x=40, y=80, width=239, height=59)
        return label

class Win(WinGUI):
    """运行页面"""
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def __event_bind(self):
        """绑定事件处理函数到相应的小部件"""
        pass

def close_window(win):
    win.destroy()

def close_after_timeout(win):
    win.after(3000, close_window, win)

def run():
    """实现运行"""
    win = Win()
    close_after_timeout(win)  # 在win.mainloop()之前调用定时关闭函数
    win.mainloop()

    app = QApplication(sys.argv)
    bupt_chat=BuptChat('kb', '1429099037@qq.com')
    init_after_login(bupt_chat)
    sys.exit(app.exec_())