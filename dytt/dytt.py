# coding=utf-8

'''
Created on 2018年11月14日

@author: Tsuru
'''

import os;
import bs4;
from spider import spider;

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
            url_map = spider.findDLUrl(link)
            
            print('''
                    　　　　　        ;* *:;,,　　　　　,;**:;, 
                    　　　　　　　　　;*　　 *:;,.,.,.,,;*　　*;, 
     电影天堂近期热门     　    　　,:*　　　　　　　　 　　  : :、 
                    　　　　　　　,:* ／ 　　　　　＼ 　 ::::::::*,　
                    　　　　　　 :*　 ●　　　　 ●　　　　  :::::i. 
                    　　　　　　 i　 ***　(_人＿)　**** * 　　 :::::i 
                    　　　　　 　 :　 　 　　　　　　　　　　:::::i 
     Tsuru             　　　　   `:,、 　　　　 　 　　 ::::::::: /
     ver.1.0.1        　　　　　   ,:*　　　　　　　 : ::::::::::::‘:、
            ''')
            for _id in url_map.keys() :
                print('(' + _id + '):' + url_map[_id][0])
            print('\n输入对应编号下载对应电影，可连续输入多个编号，或者输入星号（*）下载全部')
            command = input('调用迅雷API可能不响应等情况，可能出现下载任务创建失败的情况，重试几次应该就好了 -。-\n')
            if command == '*' :
                # 这里拿到所有新片的下载页面的url，拼接一下就可以继续抓取
                for u_id in url_map.keys() :
                    urlList = url_map[u_id]
                    url = "https://www.dytt8.net" + urlList[1]
                    spider.download(url)
            else :
                err = False
                for u_id in list(command):
                    if u_id in url_map.keys():
                        url = url_map[u_id][1]
                        url = "https://www.dytt8.net" + url
                        spider.download(url)
                    else :
                        err = True
                if err :
                    print('检查到输入编号中可能有错误，请核对')
                    
                os.system('pause')
                break
                    
