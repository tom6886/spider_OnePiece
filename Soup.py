import urllib
import urllib.request as request
from bs4 import BeautifulSoup

def get(url):
    req = urllib.request.Request(url=url, headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0',"Accept":"*/*",'Referer':'http://www.google.com'})  
    response = request.urlopen(req)
    html = response.read()
    return BeautifulSoup(html)
