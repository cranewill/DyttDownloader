# coding=utf-8

'''
Created on 2018年11月14日

@author: Tsuru
'''
import urllib.request;
import bs4;
import traceback;
from win32com.client import Dispatch;


class spider:
    '''
    爬虫工具
    '''
    
    def fetchContent(self, url, logger):
        '''
            取到网站页面
        '''
        try:
            res = urllib.request.urlopen(url)
            content = res.read()
            content = content.decode('gbk')  # 电影天堂这个编码很奇怪，居然用gbk
        except Exception:
            logger.error(traceback.format_exc())
            return 'error'
        else:
            return content
    
    def getHotPart(self, soup, logger):
        '''
        找到热门板块
        '''
        try:
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
                    return link
        except Exception:
            logger.error(traceback.format_exc())
    
    def findDLUrl(self, link, logger):
        '''
            返回下载链接形式：[[name, url], [name, url], ..]
        '''
        try:
            url_list = []
            i = 0
            for tag in link.descendants:
                if tag.name == 'a':
                    if (tag['href'] != '/html/gndy/dyzz/index.html') & (tag['href'] != '/app.html'):
                        url_pair = []
                        url_pair.append(tag.string)
                        url_pair.append(tag['href'])  # 取href的时候和取class的时候又不一样，href的属性不是一个数组，不需要再取下标
                        url_list.append(url_pair)
                        i = i + 1
            return url_list
        except Exception:
            logger.error(traceback.format_exc())
    
    def findMagnetUrl(self, link, logger):
        '''
        找到磁力链接地址
        '''
        try:
            for tag in link.descendants:
                if tag.name == 'a':
                    href = tag['href']
                    if href.startswith('magnet'):
                        return href
        except Exception:
            logger.error(traceback.format_exc())

    def download(self, link, logger):
        '''
        开始下载任务
        '''
        try:
            content = self.fetchContent(link, logger)
            # 继续解析该页面
            soup = bs4.BeautifulSoup(content, "html.parser")
            movieName = soup.title.string
            logger.info('遭遇Boss:' + movieName)
            for tag in soup.find_all(id='Zoom'):
                if (tag.name == 'div'):
                    magnetUrl = self.findMagnetUrl(tag, logger)
                    break
            # 调用迅雷接口方法
            # 1.调用迅雷的代理
    #       thunder = Dispatch('ThunderAgent.Agent64.1') # 64位和32位的区别
            thunder = Dispatch('ThunderAgent.Agent.1')
            thunder.AddTask(magnetUrl, movieName)
            thunder.CommitTasks()
            logger.info("Boss战结束!")
        # 2.系统执行exe的方式打开迅雷并传入下载链接
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:1710e389ee578b6e1ec2906d6f1e7dceadc1a53a&amp;dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e6%9a%97%e6%95%b0%e6%9d%80%e4%ba%ba.BD.720p.%e9%9f%a9%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')
#                 os.execl("D:\Softwares\Program\Thunder.exe", '-StartType:DesktopIcon', 'magnet:?xt=urn:btih:9b9bba10ebce7bfd953e015b25952296a0ec65cc&dn=%e9%98%b3%e5%85%89%e7%94%b5%e5%bd%b1www.ygdy8.com.%e7%8a%ac%e8%88%8d%e7%9c%9f%e4%ba%ba%e7%89%88.BD.720p.%e6%97%a5%e8%af%ad%e4%b8%ad%e5%ad%97.mkv')
        except Exception:
            logger.error(traceback.format_exc())
