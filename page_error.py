
from tkinter import *
from tkinter.ttk import *
from typing import Dict

class WinGUI(Tk):
    widget_dic: Dict[str, Widget] = {}
    def __init__(self):
        super().__init__()
        self.__win()
        self.widget_dic["tk_label_title"] = self.__tk_label_title(self)
        self.widget_dic["tk_label_content"] = self.__tk_label_content(self)

    def __win(self):
        self.title("error")
        # 设置窗口大小、居中
        width = 319
        height = 161
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
        label = Label(parent,text="出现错误！",anchor="center", )
        label.place(x=40, y=10, width=239, height=58)
        return label

    def __tk_label_content(self,parent):
        label = Label(parent,text="***请检查您的输入信息***",anchor="center", )
        label.place(x=40, y=80, width=239, height=59)
        return label

class Win(WinGUI):
    def __init__(self):
        super().__init__()
        self.__event_bind()

    def __event_bind(self):
        pass
        
def run():
    win = Win()
    win.mainloop()
