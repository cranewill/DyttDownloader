# coding=utf-8

'''
Created on 2018年11月14日

@author: Tsuru
'''
import urllib.request;
import bs4;
from win32com.client import Dispatch;


class spider:
    '''
    爬虫工具
    '''
    
    def fetchContent(self, url):
        '''
            取到网站页面
        '''
        res = urllib.request.urlopen(url)
        content = res.read()
        content = content.decode('gbk')  # 电影天堂这个编码很奇怪，居然用gbk
        return content
    
    def findDLUrl(self, link):
        '''
            返回下载链接形式：{1:[name, url], 2:[name, url], ...}
        '''
        id_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        url_dict = {}
        i = 1
        for tag in link.descendants:
            if tag.name == 'a':
                if (tag['href'] != '/html/gndy/dyzz/index.html') & (tag['href'] != '/app.html'):
                    url_list = []
                    url_list.append(tag.string)
                    url_list.append(tag['href'])  # 取href的时候和取class的时候又不一样，href的属性不是一个数组，不需要再取下标
                    url_dict[id_list[i - 1]] = url_list
                    i = i + 1
        return url_dict
    
    def findMagnetUrl(self, link):
        '''
        找到磁力链接地址
        '''    
        for tag in link.descendants:
            if tag.name == 'a':
                href = tag['href']
                if href.startswith('magnet'):
                    return href
    
    def download(self, link):
        '''
        开始下载任务
        '''     
        content = self.fetchContent(link)
        # 继续解析该页面
        soup = bs4.BeautifulSoup(content, "html.parser")
        movieName = soup.title.string
        print('创建迅雷任务:' + movieName)
        for tag in soup.find_all(id='Zoom'):
            if (tag.name == 'div'):
                magnetUrl = self.findMagnetUrl(tag)
                break
        # 调用迅雷接口方法
        # 1.调用迅雷的代理
#       thunder = Dispatch('ThunderAgent.Agent64.1') # 64位和32位的区别
        thunder = Dispatch('ThunderAgent.Agent.1')
        thunder.AddTask(magnetUrl, movieName)
        thunder.CommitTasks()
        # 2.系统执行exe的方式打开迅雷并传入下载链接
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:1710e389ee578b6e1ec2906d6f1e7dceadc1a53a&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e6%9a%97%e6%95%b0%e6%9d%80%e4%ba%ba.BD.720p.%e9%9f%a9%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:9b9bba10ebce7bfd953e015b25952296a0ec65cc&dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e7%8a%ac%e8%88%8d%e7%9c%9f%e4%ba%ba%e7%89%88.BD.720p.%e6%97%a5%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')

