#!/usr/bin/python
import urllib
import sys
import re
from bs4 import BeautifulSoup
import chardet
import urllib2
html = ''
def GetPageInfo(url):
    global html
    req = urllib2.Request(url)
    content = urllib2.urlopen(req).read()
    typeEncode = sys.getfilesystemencoding()
    infoencode = chardet.detect(content).get('encoding','utf-8')
    html = content.decode(infoencode,'ignore').encode(typeEncode)
DYTT = 'http://www.dytt.net/shieryuejingdiandapian/list_18_1.html'
DYTT8 = 'http://www.ygdy8.net/html/gndy/dyzz/index.html'
DOUBAN = 'http://movie.douban.com/'
JIZHAN = 'http://movie.douban.com/subject/20388223/'
XINGJI = 'http://movie.douban.com/subject/24745500/'
QUNA = 'http://movie.douban.com/subject/1842121'
GetPageInfo(QUNA)
html=html.decode('utf8')
#print html
SOUP = BeautifulSoup(html)
MOVIE_NAME = SOUP.title.contents[0]
try :
    MOVIE_FEN = SOUP.find('strong', attrs={"class":"ll rating_num", "property":"v:average"}).contents[0]
except AttributeError:
    MOVIE_FEN = 'None'
MOVIE_CLASS = SOUP.find('div', attrs={"class":"nav-logo"}).contents[1].contents[0]
#MOVIE_NAME = MOVIE_NAME.decode('utf8')
MOVIE_NAME = MOVIE_NAME.split()[0]
print MOVIE_NAME
print MOVIE_CLASS
print MOVIE_FEN
print "%(MOVIE_CLASS)s  %(MOVIE_NAME)s" %vars()


#LIST=re.findall('<a href="(/\w+/\d+/\d+/\d+.html)" class="ulink" title="(.*)">', html)
#LIST2=[('http://www.dytt.net'+x, y) for (x,y) in LIST ]
#print LIST2[0][0], LIST[0][1]
