'''
Created on 2018年11月14日

@author: Tsuru
'''
import urllib.request;


class spider:
    '''
    爬虫工具
    '''
    
    def fetchContent(self, url):
        res = urllib.request.urlopen(url)
        content = res.read()
        content = content.decode('gbk')  # 电影天堂这个编码很奇怪，居然用gbk
        return content
    
    def findDLUrl(self, link):
        url_list = []
        for tag in link.descendants:
            if tag.name == 'a':
                if (tag['href'] != '/html/gndy/dyzz/index.html') & (tag['href'] != '/app.html'):
                    url_list.append(tag['href'])  # 取href的时候和取class的时候又不一样，href的值不是一个数组，不需要再取下标
        return url_list
    
    def findMagnetUrl(self, link):
        for tag in link.descendants:
            if tag.name == 'a':
                href = tag['href']
                if href.startswith('magnet'):
                    return href
