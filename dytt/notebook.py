'''
Created on 2018年11月26日

@author: Administrator
'''
from tkinter import *;
from tkinter import ttk;


if __name__ == '__main__':
    root = Tk()
    mainTabCtrl = ttk.Notebook(root)
    mainTabCtrl.place(relx = 0.001, rely = 0.071, relwidth = 0.887, relheight = 0.876)
    aTab = Frame(mainTabCtrl)
    mainTabCtrl.add(aTab , text = "A")
    bTab = Frame(mainTabCtrl)
    mainTabCtrl.add(bTab , text = "B")
    root.mainloop()