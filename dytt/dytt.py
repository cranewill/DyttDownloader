import urllib.request;
import urllib.parse;
import re;
import bs4;
import sys;
import os;
from spider import spider;
from win32com.client import Dispatch;

'''
Created on 2018年11月14日

@author: Tsuru
'''

if __name__ == '__main__':
    spider = spider()
    
    content = spider.fetchContent("https://www.dytt8.net")
    soup = bs4.BeautifulSoup(content, "html.parser")  # 得到soup
    
    for link in soup.find_all('strong'):
        if (link.string == '2018新片精品'):  # 找到新片区域的标签，以此找到包含所有新片列表的父标签
            className = ''
            while (className != 'co_area2'):
                if (link.name == 'div'):
                    if (link['class'][0] == 'co_area2'):  # 标签的属性(attrs)是一个字典通过key = 'class'取出来的貌似是个数组列表一样的东西，还需要取第一个
                        className = 'co_area2'
                    else :
                        link = link.parent
                else:
                    link = link.parent
            # 这里就拿到了包含所有新片列表的父标签，然后找到需要的下载页面的url
#           pattern = re.compile("<a href='/html/gndy/dyzz/.*?/.*?.html'>.*?</a>")
#           pattern = re.compile("<a href=\"/html/gndy/dyzz/")
#           results = re.findall(pattern, str(link))
#           print(results)
################################################################################################
            url_list = []
            url_list = spider.findDLUrl(link)
#             print(url_list)
            # 这里拿到所有新片的下载页面的url，拼接一下就可以继续抓取
            for url in url_list :
                url = "https://www.dytt8.net" + url
                content = spider.fetchContent(url)
                # 继续解析该页面
                soup = bs4.BeautifulSoup(content, "html.parser")
                movieName = soup.title.string
                print(movieName)
                for tag in soup.find_all(id='Zoom'):
                    if (tag.name == 'div'):
                        magnetUrl = spider.findMagnetUrl(tag)
                
                # 调用迅雷接口方法
                # 1.调用迅雷的代理
#                 thunder = Dispatch('ThunderAgent.Agent64.1') # 64位和32位的区别
                thunder = Dispatch('ThunderAgent.Agent.1')
                thunder.AddTask(magnetUrl, movieName)
                thunder.CommitTasks()
                
                # 2.系统执行exe的方式打开迅雷并传入下载链接
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:1710e389ee578b6e1ec2906d6f1e7dceadc1a53a&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e6%9a%97%e6%95%b0%e6%9d%80%e4%ba%ba.BD.720p.%e9%9f%a9%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:9b9bba10ebce7bfd953e015b25952296a0ec65cc&dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e7%8a%ac%e8%88%8d%e7%9c%9f%e4%ba%ba%e7%89%88.BD.720p.%e6%97%a5%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')
            
