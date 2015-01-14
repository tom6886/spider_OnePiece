import urllib
import urllib.request as request
import re
import zipfile  
import glob  
import os
import threading
import random
from bs4 import BeautifulSoup

proxyList = []

class CommicGet(threading.Thread):
    def __init__(self,url,lesson):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = 5
        self.lesson = lesson

    def getSoup(self):
        print('开始下载第'+str(self.lesson)+'话')
        self.num = self.getNum()
        d_url = self.url + 'Utility/2/'+self.num+'j.js'
        #req = urllib.request.Request(url=d_url, headers=headers)  
        #response = request.urlopen(req)
        while(True):
            self.getProxy()
            try:
                html = self.opener.open(d_url,timeout=self.timeout).read()
                break
            except Exception as e:
                print(e)
                print('连接出错，更换代理')
        soup = BeautifulSoup(html)
        self.soup = soup
        self.getJpg()

    def getJpg(self):
        count = 1
        dirName = r'F:/image/第%s话'%self.lesson
        if(not os.path.isdir(dirName)):
            os.makedirs(dirName)
        for m in re.finditer(r'(/Pic/OnlineComic1/[\w./]+.jpg)', str(self.soup)):       
            sName = 'F:/image/第'+str(self.lesson)+'话/第' + str(self.lesson) + '话第'+str(count)+'页.jpg'
            if os.path.exists(sName):
                print("%s 已存在，跳过"%sName)
                count += 1
                continue
            print('正在下载第'+str(self.lesson)+'话第'+str(count)+'页, 并保存为'+sName)
            while(True):
                try:
                    page = self.opener.open(self.url+str(m.group(1)),timeout=self.timeout).read()
                    break
                except Exception as e:
                    self.getProxy()
                    print(e)
                    print('连接出错，更换代理')
            #page = request.urlopen(url+str(m.group(1))).read()
            with open(sName,'wb') as file:
                file.write(page)
            file.close()
            count += 1
        print('第'+str(self.lesson)+'话下载完毕')

    def getNum(self):
        if(i<10):
            return '00' + str(self.lesson)
        if(9<i<100):
            return '0' + str(self.lesson)
        if(99<i<1000):
            return str(self.lesson)

    def getProxy(self):
        cookies = request.HTTPCookieProcessor()
        proxy = random.choice(proxyList)
        proxyHandler = request.ProxyHandler({"http" : r'http://%s' %proxy})
        opener = request.build_opener(cookies,proxyHandler)
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]
        self.opener = opener
        try:
            req = opener.open(self.url).read()
        except Exception as e:
            self.getProxy()
        print('获取代理 '+proxy)    

    def run(self):
        self.getSoup()
                
if __name__ == '__main__':
    getThreads = []
    url = 'http://comic.sfacg.com/'
    begin = int(input(u'请输入开始的回数：\n'))
    end = int(input(u'请输入结束的回数：\n'))
    hasProxy = os.path.isfile('proxy_list.txt')
    if(not hasProxy):
        print(u'代理文件不存在，开始获取代理')
        import proxyIP

for line in open('proxy_list.txt').readlines():
    proxyList.append(line.strip('\n'))

#为每一话开启一个线程负责抓取
for i in range(begin,end+1):
    t = CommicGet(url,i)
    getThreads.append(t)

for i in range(len(getThreads)):
    getThreads[i].start()

for i in range(len(getThreads)):
    getThreads[i].join()
    

