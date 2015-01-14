import Soup
import threading
import urllib
import urllib.request as request

class Url():
    def __init__(self,url):
        threading.Thread.__init__(self)
        self.url = url

    def getUrl(self):
        soup = Soup.get(self.url)
        target = soup.select('.newslist_line a')[0].get('href')
        targets.append(target)
        soup_t = Soup.get(target)
        items = []
        for i in soup_t.select('.pagelist a'):
            item = i.get('href')
            if item is not None and item != '#' and item not in items:
                items.append(item)
                targets.append(self.url + item)
        return targets

    def run(self):
        self.getUrl()    

class Get(threading.Thread):
    def __init__(self,target):
        threading.Thread.__init__(self)
        self.target = target

    def getProxy(self):
        soup = Soup.get(self.target)
        for i in str(soup.select('.cont_font p')[0])[3:-4].split('<br/>'):
            proxyList.append(i.strip('\r\n').split('@')[0])

    def run(self):
        self.getProxy()

#检验代理的类
class ProxyCheck(threading.Thread):
    def __init__(self,proxyList):
        threading.Thread.__init__(self)
        self.proxyList = proxyList
        self.timeout = 5
        self.testUrl = "http://www.baidu.com/"
        self.testStr = b"030173"

    def checkProxy(self):
        cookies = request.HTTPCookieProcessor()
        for proxy in self.proxyList:
            proxyHandler = request.ProxyHandler({"http" : r'http://%s' %(proxy)})
            print(r'http://%s' %(proxy))
            opener = request.build_opener(cookies,proxyHandler)
            opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.2; WOW64; rv:22.0) Gecko/20100101 Firefox/22.0')]

            try:
                req = opener.open(self.testUrl, timeout=self.timeout)
                result = req.read()
                pos = result.find(self.testStr)

                if pos > 1:
                    print("%s 通过检测" %proxy)
                    checkedProxyList.append(proxy)
                    #print "ok ip: %s %s %s %s" %(proxy[0],proxy[1],proxy[2],timeused)
                else:
                     continue
            except Exception as e:
                print(e)
                continue

    def run(self):
        self.checkProxy()

if __name__ == "__main__":
    proxyList = []
    getThreads = []
    #添加目标网页
    targets = []
    url = Url('http://www.youdaili.net/Daili/http/')
    targets = url.getUrl()
    print(targets)

#对每个目标网页开启一个线程负责抓取代理
for i in range(len(targets)):
    t = Get(targets[i])
    getThreads.append(t)

for i in range(len(getThreads)):
    getThreads[i].start()

for i in range(len(getThreads)):
    getThreads[i].join()

print('.'*10+"总共抓取了%s个代理" %len(proxyList) +'.'*10)
print('.'*10+"开始过滤代理，请稍候" +'.'*10)

checkThreads = []
checkedProxyList = []
#开启20个线程负责校验，将抓取到的代理分成20份，每个线程校验一份
for i in range(20):
    t = ProxyCheck(proxyList[((len(proxyList)+19)//20) * i:((len(proxyList)+19)//20) * (i+1)])
    checkThreads.append(t)

for i in range(len(checkThreads)):
    checkThreads[i].start()

for i in range(len(checkThreads)):
    checkThreads[i].join()

print('.'*10+"总共有%s个代理通过校验" %(len(checkedProxyList)) +'.'*10)

#持久化
f= open("proxy_list.txt",'w+')
for proxy in checkedProxyList:
    #print("checked proxy is: %s:%s" %(proxy[0],proxy[1]))
    f.write("%s\n"%proxy)
f.close()
