
from tkinter import *
from tkinter.ttk import *
from typing import Dict
import control
import page_error
import page_finishi_loging
from control import *

class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_title"] = self.__tk_label_title(self)
        self.widget_dic["tk_label_ID"] = self.__tk_label_ID(self)
        self.widget_dic["tk_input_ID_str"] = self.__tk_input_ID_str(self)
        self.widget_dic["tk_button_do_register"] = self.__tk_button_do_register(self)
        self.widget_dic["tk_label_code"] = self.__tk_label_code(self)
        self.widget_dic["tk_input_code_str"] = self.__tk_input_code_str(self)
        self.widget_dic["tk_button_get_code"] = self.__tk_button_get_code(self)

    def __win(self):
        self.title("验证码登录")
        # 设置窗口大小、居中
        width = 338
        height = 401
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        geometry = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
        self.geometry(geometry)
        self.resizable(width=False, height=False)

        # 自动隐藏滚动条
    def scrollbar_autohide(self,bar,widget):
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
        label = Label(parent,text="验证码登录",anchor="center", )
        label.place(x=50, y=40, width=239, height=58)
        return label

    def __tk_label_ID(self,parent):
        label = Label(parent,text="邮箱",anchor="center", )
        label.place(x=20, y=150, width=50, height=30)
        return label

    def __tk_input_ID_str(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=100, y=150, width=221, height=30)
        return ipt

    def __tk_button_do_register(self,parent):
        btn = Button(parent, text="登录", takefocus=False,)
        btn.place(x=120, y=340, width=99, height=31)
        return btn

    def __tk_label_code(self,parent):
        label = Label(parent,text="验证码",anchor="center", )
        label.place(x=20, y=240, width=50, height=30)
        return label

    def __tk_input_code_str(self,parent):
        ipt = Entry(parent, )
        ipt.place(x=100, y=240, width=138, height=30)
        return ipt

    def __tk_button_get_code(self,parent):
        btn = Button(parent, text="获取验证码", takefocus=False,)
        btn.place(x=240, y=240, width=82, height=30)
        return btn

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def register(self,evt):
        ID = self.widget_dic["tk_input_ID_str"].get()
        code = self.widget_dic["tk_input_code_str"].get()
        control.get_verify(code)
        temp,tmp1=control.login(ID,'')
        #print(tmp1)
        if(temp==1):
            self.destroy()
            page_finishi_loging.run()
        else:
            page_error.run()
        #print("判断密码完成",evt)
        
    def get_code(self,evt):
        ID = self.widget_dic["tk_input_ID_str"].get()
        if control.send_verify_code(ID) == 0:
            tkinter.messagebox.showerror(message='邮箱输入有误！')
        #print("已发送验证码",evt)
        
    def __event_bind(self):
        self.widget_dic["tk_button_do_register"].bind('<Button-1>',self.register)
        self.widget_dic["tk_button_get_code"].bind('<Button-1>',self.get_code)
        
def run():
    win = Win()
    win.mainloop()
