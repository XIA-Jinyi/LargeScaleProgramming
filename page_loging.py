
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import control
import page_register
import  page_code_loging
import page_error
import page_finishi_loging
from control import *


class WinGUI(Tk):
    """登录界面实现"""
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        """初始化登录界面"""
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_title"] = self.__tk_label_title(self)
        self.widget_dic["tk_label_ID"] = self.__tk_label_ID(self)
        self.widget_dic["tk_label_pw"] = self.__tk_label_pw(self)
        self.widget_dic["tk_input_ID_str"] = self.__tk_input_ID_str(self)
        self.widget_dic["tk_input_pw_str"] = self.__tk_input_pw_str(self)
        self.widget_dic["tk_button_do_register"] = self.__tk_button_do_register(self)
        self.widget_dic["tk_button_do_loging"] = self.__tk_button_do_loging(self)
        self.widget_dic["tk_button_code_loging"] = self.__tk_button_code_loging(self)

    def __win(self):
        """设置登录界面标题"""
        self.title("登录界面")
        # 设置窗口大小、居中
        width = 338
        height = 401
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
        label = Label(parent,text="登录",anchor="center", )
        label.place(x=50, y=40, width=239, height=58)
        return label

    def __tk_label_ID(self,parent):
        """创建登录邮箱标签

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="邮箱",anchor="center", )
        label.place(x=20, y=140, width=50, height=30)
        return label

    #创建登录密码标签
    def __tk_label_pw(self,parent):
        """
        创建登录密码标签

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="密码",anchor="center", )
        label.place(x=20, y=220, width=50, height=30)
        return label

    def __tk_input_ID_str(self,parent):
        """读取登录邮箱输入

        Args:
            parent:所放置的容器

        Returns:
            Entry:邮箱名

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=140, width=221, height=30)
        return ipt

    def __tk_input_pw_str(self,parent):
        """读取登录密码输入

        Args:
            parent:所放置的容器

        Returns:
            Entry：登录密码

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=220, width=220, height=30)
        return ipt

    def __tk_button_do_register(self,parent):
        """创建注册转跳按钮

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        btn = Button(parent, text="注册", takefocus=False,)
        btn.place(x=200, y=310, width=99, height=31)
        return btn

    def __tk_button_do_loging(self,parent):
        """创建登录转跳按钮

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        btn = Button(parent, text="登录", takefocus=False,)
        btn.place(x=40, y=310, width=99, height=31)
        return btn


    def __tk_button_code_loging(self,parent):
        """创建验证码登录标签

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        btn = Button(parent, text="验证码登录", takefocus=False,)
        btn.place(x=40, y=360, width=99, height=31)
        return btn

def close_window(win):
    win.destroy()

def close_after_timeout(win):
    win.after(3000, close_window, win)

class Win(WinGUI):
    """运行页面"""
    def __init__(self):
        super().__init__()
        self.__event_bind()
        self.close_callback = None

    def register(self,evt):
        """注册转跳按钮函数

        Args:
            evt:接收事件对象

        """
        close_after_timeout(win)
        page_register.run()
        #print("转跳注册页面",evt)

    def loging(self,evt):
        """登录转跳按钮函数

        Args:
            evt:接收事件对象

        """
        ID = self.widget_dic["tk_input_ID_str"].get()
        code = self.widget_dic["tk_input_pw_str"].get()
        temp,tmp1 = control.login(ID, code)
        if (temp == 1):
            close_after_timeout(win)
            page_finishi_loging.run()
        else:
            page_error.run()
        #print("登录判定完成",evt)

    def code_loging(self,evt):
        """验证码登录转跳按钮函数

        Args:
            evt:接收事件对象

        """
        close_after_timeout(win)
        page_code_loging.run()
        #print("验证码登录转跳",evt)

    def __event_bind(self):
        """绑定事件处理函数到相应的小部件"""
        self.widget_dic["tk_button_do_register"].bind('<Button-1>',self.register)
        self.widget_dic["tk_button_do_loging"].bind('<Button-1>',self.loging)
        self.widget_dic["tk_button_code_loging"].bind('<Button-1>',self.code_loging)

if __name__ == "__main__":
    control.init()
    win = Win()
    win.mainloop()
