#-*-coding:utf-8-*-
from tkinter import Tk
from tkinter import Button, Label, Entry, Message, Frame
from tkinter import messagebox
from tkinter import StringVar
import datetime

class Application(Frame):
    '''GUI 基类'''

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.createWidget()

    def createWidget(self):
        '''创建组件'''
        self.label01 = Label(self, text="用户名")
        self.label01.pack()

        name = StringVar()
        self.entry01 = Entry(self, textvariable=name)
        self.entry01.pack()

        self.label02 = Label(self, text="密码")
        self.label02.pack()

        password = StringVar()
        self.entry02 = Entry(self, textvariable=password, show="*")
        self.entry02.pack()

        self.button = Button(self, text="login", command=self.login)
        self.button.pack()

    def login(self):
        '''Button 响应'''
        messagebox.showinfo("登录成功","%s" % self.entry01.get())

if __name__ == '__main__':
    root = Tk()
    root.geometry("400x300+200+200")
    app = Application(root)
    root.mainloop()