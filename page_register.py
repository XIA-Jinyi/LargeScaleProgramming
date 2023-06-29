
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import page_error
import page_finishi_loging
import control
import page_finish_register
import page_test_rergister
from control import *

class WinGUI(Tk):
    """注册页面实现"""
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        """初始化注册页面"""
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_title"] = self.__tk_label_title(self)
        self.widget_dic["tk_label_ID"] = self.__tk_label_ID(self)
        self.widget_dic["tk_label_pw"] = self.__tk_label_pw(self)
        self.widget_dic["tk_input_ID_str"] = self.__tk_input_ID_str(self)
        self.widget_dic["tk_input_pw_str"] = self.__tk_input_pw_str(self)
        self.widget_dic["tk_button_do_register"] = self.__tk_button_do_register(self)
        self.widget_dic["tk_label_code"] = self.__tk_label_code(self)
        self.widget_dic["tk_input_code_str"] = self.__tk_input_code_str(self)
        self.widget_dic["tk_label_repw"] = self.__tk_label_repw(self)
        self.widget_dic["tk_input_repw_str"] = self.__tk_input_repw_str(self)
        self.widget_dic["tk_button_get_code"] = self.__tk_button_get_code(self)
        self.widget_dic["tk_label_name"] = self.__tk_label_name(self)
        self.widget_dic["tk_input_name_str"] = self.__tk_input_name_str(self)

    def __win(self):
        """设置登录界面标题"""
        self.title("注册页面")
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
        label = Label(parent,text="注册",anchor="center", )
        label.place(x=50, y=10, width=239, height=58)
        return label

    def __tk_label_ID(self,parent):
        """创建登录邮箱标签

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="邮箱",anchor="center", )
        label.place(x=20, y=90, width=50, height=30)
        return label

    def __tk_label_pw(self,parent):
        """
        创建登录密码标签

        Args:
            parent:所放置的容器

        Returns:
            Lable:标签对象

        """
        label = Label(parent,text="密码",anchor="center", )
        label.place(x=20, y=190, width=50, height=30)
        return label

    def __tk_input_ID_str(self,parent):
        """读取登录邮箱输入

        Args:
            parent:所放置的容器

        Returns:
            Entry:邮箱名

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=90, width=221, height=30)
        return ipt

    def __tk_input_pw_str(self,parent):
        """读取登录密码输入

        Args:
            parent:所放置的容器

        Returns:
            Entry：登录密码

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=190, width=220, height=30)
        return ipt

    #创建登录确认密码标签
    def __tk_label_repw(self,parent):
        """创建登录确认密码标签

        Args:
            parent:所放置的容器

        Returns:
            Lable：标签

        """
        label = Label(parent,text="确认密码",anchor="center", )
        label.place(x=20, y=240, width=50, height=30)
        return label

    def __tk_input_repw_str(self,parent):
        """读取登录密码验证输入

        Args:
            parent:所放置的容器

        Returns:
            Entry：登录密码

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=240, width=218, height=30)
        return ipt

    def __tk_button_do_register(self,parent):
        """创建注册转跳按钮

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        btn = Button(parent, text="注册", takefocus=False,)
        btn.place(x=120, y=340, width=99, height=31)
        return btn

    def __tk_label_code(self,parent):
        """创建验证码标签

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        label = Label(parent,text="验证码",anchor="center", )
        label.place(x=20, y=290, width=50, height=30)
        return label

    def __tk_input_code_str(self,parent):
        """读取验证码输入

        Args:
            parent:所放置的容器

        Returns:
            Entry：登录密码

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=290, width=138, height=30)
        return ipt

    def __tk_button_get_code(self,parent):
        """创建获取验证码转跳按钮

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        btn = Button(parent, text="获取验证码", takefocus=False,)
        btn.place(x=239, y=290, width=82, height=30)
        return btn

    def __tk_label_name(self,parent):
        """创建昵称标签

        Args:
            parent:所放置的容器

        Returns:
            Button：按钮

        """
        label = Label(parent,text="昵称",anchor="center", )
        label.place(x=20, y=140, width=50, height=30)
        return label

    def __tk_input_name_str(self,parent):
        """读取昵称输入

        Args:
            parent:所放置的容器

        Returns:
            Entry：登录密码

        """
        ipt = Entry(parent, )
        ipt.place(x=100, y=140, width=221, height=30)
        return ipt

def close_window(win):
    win.destroy()

def close_after_timeout(win):
    win.after(3000, close_window, win)

class Win(WinGUI):
    """运行页面"""
    def __init__(self):
        super().__init__()
        self.__event_bind()

    #注册转跳按钮函数
    def register(self,evt):
        """注册转跳按钮函数

        Args:
            evt:接收事件对象

        """
        ID = self.widget_dic["tk_input_ID_str"].get()
        name = self.widget_dic["tk_input_name_str"].get()
        pw = self.widget_dic["tk_input_pw_str"].get()
        repw = self.widget_dic["tk_input_repw_str"].get()
        code = self.widget_dic["tk_input_code_str"].get()
        if repw!=pw:
        #if page_test_rergister.validate_inputs(ID, name, pw, repw, code):
            page_error.run()
        else:
            #print('2')
            control.get_verify(code)
            temp,temp1=control.register(ID, name, pw)
            #print(temp)
            if (temp==1):
                self.destroy()
                page_finishi_loging.run()
            else:
                page_error.run()
        #print("注册验证完成")

    #获取验证码转跳按钮函数
    def get_code(self, evt):
        """获取验证码按钮函数

        Args:
            evt:接收事件对象

        """
        ID = self.widget_dic["tk_input_ID_str"].get()
        if control.send_verify_code(ID) == 0:
            tkinter.messagebox.showerror(message='邮箱输入有误！')
        #print("已发送验证码", evt)

    def __event_bind(self):
        """绑定事件处理函数到相应的小部件"""
        self.widget_dic["tk_button_do_register"].bind('<Button-1>', self.register)
        self.widget_dic["tk_button_get_code"].bind('<Button-1>', self.get_code)

def run():
    """实现运行"""
    win = Win()
    win.mainloop()

'''
if __name__ == "__main__":
    win = Win()
    win.mainloop()
'''
