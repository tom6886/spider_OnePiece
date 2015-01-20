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
    def __init__(self,url,lessons):
        threading.Thread.__init__(self)
        self.url = url
        self.timeout = 5
        self.lessons = lessons

    def getSoup(self):
        for i in self.lessons:
            if(i<41):
                self.title = '第%s卷'%i
            else:
                self.title = '第%s话'%i
            print('开始下载%s'%self.title)
            self.num = self.getNum(i)
            d_url = self.url + 'Utility/2/'+self.num+'.js'
            #print(d_url)
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
        dirName = r'F:/image/%s'%self.title
        if(not os.path.isdir(dirName)):
            os.makedirs(dirName)
        #print(str(self.soup))
        for m in re.finditer(r'(/Pic/OnlineComic1/[\w./]+)', str(self.soup)):
            sName = 'F:/image/%s/%s第%s页.jpg'%(self.title,self.title,count)
            if os.path.exists(sName):
                print("%s 已存在，跳过"%sName)
                count += 1
                continue
            print('正在下载%s第%s页, 并保存为%s'%(self.title,count,sName))
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
        print('%s下载完毕'%self.title)

    def getNum(self,i):
        if(i<10):
            return '00%sj'%i
        elif(9 < i < 100):
            return '0%sj'%i
        else:
            return str(i)

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
    import Numbers
    numbers = Numbers.getNumbers()
    hasProxy = os.path.isfile('proxy_list.txt')
    if(not hasProxy):
        print(u'代理文件不存在，开始获取代理')
        import proxyIP

for line in open('proxy_list.txt').readlines():
    proxyList.append(line.strip('\n'))

#开启20个线程负责抓取，每个线程抓取一份
for i in range(20):
    t = CommicGet(url,numbers[((len(numbers)+19)//20) * i:((len(numbers)+19)//20) * (i+1)])
    getThreads.append(t)

for i in range(len(getThreads)):
    getThreads[i].start()

for i in range(len(getThreads)):
    getThreads[i].join()
    

