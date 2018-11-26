# coding=utf-8

'''
Created on 2018年11月14日

@author: Tsuru
'''
import os;
import bs4;
import wmi;
import base64;
from spider import spider;
from tkinter import *;
from PIL import Image, ImageTk;
from crane import img as craneImg;
from log import Log;

def selectAll():
    global allSelected  # 在python的函数中和全局同名的变量，如果你有修改变量的值就会变成局部变量，所以需要加上global关键字代表引用已有的全局变量
    global logger
    if allSelected == False:
        logger.debug("全选任务")
        for wiget in checkWigetList:
            wiget.select()
        allSelected = True
    else:
        logger.debug("取消全选")
        for wiget in checkWigetList:
            wiget.deselect()
        allSelected = False

        
def download():
    global logger
    none = True
    logger.info("地下城探索开始!")
    for i in range (0, len(checkStateList)):
        if checkStateList[i].get() == 1:  # 因为是Intvar，所以需要通过get()方法取值
            pair = url_list[i]
            url = "https://www.dytt8.net" + str(pair[1])
            logger.info("进入目标地区: " + url)
            spider.download(url, logger)
            none = False
    if none :
        logger.info("未选中至少一个任务")

if __name__ == '__main__':
    logger = Log()
    logger.info("MOVIE CRANE VER.2.0.2")
    logger.info("正在搜寻任务...")
    wmInfo = wmi.WMI()
    sys = wmInfo.Win32_OperatingSystem()[0]
    logger.info("自身装备信息:")
    logger.info(sys.Caption + "---" + sys.BuildNumber + "---" + sys.OSArchitecture)
    ############################################################################# 初始化
    row = 0
    allSelected = False
    checkStateList = []
    checkWigetList = []
    
    root = Tk()
    root.geometry('1050x650')  # 这里不是*而是英文的x...
    root.resizable(0, 0)
    root.title("Movie Crane ver.2.0.1")
    Label(root, text="Movie Crane", font=('Consola', 30), justify=LEFT).pack(side=TOP, pady=20)
    
    ############################################################################# 通过bs4得到热门板块列表
    spider = spider()
    logger.info("地下城区域: https://www.dytt8.net")
    content = spider.fetchContent("https://www.dytt8.net", logger)
    soup = bs4.BeautifulSoup(content, "html.parser")  # 得到soup
    hotPart = spider.getHotPart(soup, logger)  # 得到热门板块
    url_list = spider.findDLUrl(hotPart, logger)  # 得到近期热门链接的列表
    logger.info("找到目标地下城任务手册!")
    ############################################################################# UI显示
    mainFrm = Frame(root)
    topFrm = Frame(mainFrm)
    listFrm = Frame(topFrm)
    buttonFrm = Frame(topFrm)
    buttomFrm = Frame(mainFrm)
    for pair in url_list:
        checked = IntVar()
        checkStateList.append(checked)
        wight = Checkbutton(listFrm, text=pair[0], font=('Arial', 10), variable=checked)
        checkWigetList.append(wight)
        wight.pack(side=TOP, anchor=W)
        row = row + 1
    
    logger.info("正在地下城手册上签名...")
    tmpImg = open('tmp.jpg', 'wb+') # 临时文件用来保存jpg文件
    tmpImg.write(base64.b64decode(craneImg))
    tmpImg.close()
    
    logoSrc = Image.open("tmp.jpg")  # 加载图片,tkinter只支持gif，所以需要引入pillow包来加载png和jpg图片
    logo = ImageTk.PhotoImage(logoSrc)
    Label(buttonFrm, image=logo).pack(side=TOP, pady=10)
    
    os.remove("tmp.jpg")    # 删除临时图片
    logger.info("签名完毕!")
    
    Button(buttonFrm, text="全    选/取   消", width=25, command=selectAll).pack(side=TOP, pady=30)
    Button(buttonFrm, text="下       载", width=25, command=download).pack(side=TOP, pady=30)
    Label(buttomFrm, text="*调用迅雷API可能不响应等情况，建议下载最新版迅雷，并在下载前先打开迅雷 -。-    ——By Tsuru", font=('Arial', 10)).pack(side=RIGHT, anchor=SE)
    listFrm.pack(side=LEFT, padx=60)
    buttonFrm.pack(side=RIGHT, padx=60)
    topFrm.pack(side=TOP)
    buttomFrm.pack(side=BOTTOM, pady=20)
    mainFrm.pack()
    logger.info("任务收集完毕!")
    mainloop()
