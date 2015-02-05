#coding:utf-8
#!/usr/bin/python
import urllib
import sys,time, socket, random
import re
from bs4 import BeautifulSoup
import chardet
import urllib2
html = ''
reload(sys)
sys.setdefaultencoding( "utf-8" )
def GetPageInfo(url):
    global html
    try:
        Headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:17.0) Gecko/20130329 Firefox/17.0',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Connection': 'keep-alive'}
        req = urllib2.Request(url, headers=Headers)
        content = urllib2.urlopen(req,timeout=2).read()

    except urllib2.HTTPError:
        print 'HTTPError'
        html='None'
        return html
    except (socket.timeout, urllib2.URLError):
        print 'TIMEOUT'
        html='None'
        return html
    typeEncode = sys.getfilesystemencoding()
    infoencode = chardet.detect(content).get('encoding','utf-8')
    html = content.decode(infoencode,'ignore').encode(typeEncode)

def ScratchMovies(self):
    SOUP = BeautifulSoup(self)
    global MOVIE_CLASS
    global MOVIE_NAME
    global MOVIE_FEN
    global MOVIE_TYPE
    try:
        MOVIE_NAME = SOUP.title.contents[0]
        MOVIE_NAME = MOVIE_NAME.split()[0]
    except AttributeError:
        MOVIE_NAME = 'None'
        MOVIE_CLASS = 'None'
        MOVIE_FEN = 'None'
        return 2
    try :
        MOVIE_FEN = SOUP.find('strong', attrs={"class":"ll rating_num", "property":"v:average"}).contents[0].strip()
        if MOVIE_FEN == '': MOVIE_FEN='None_proporty_yet'
    except IndexError:
        MOVIE_FEN = 'None_property_yet'
    except AttributeError:
        try:
            MOVIE_FEN = SOUP.find('strong', attrs={"class":"ll rating_num ", "property":"v:average"}).contents[0].strip()
        except AttributeError:
            MOVIE_FEN = 'None_property_yet'

    try:
        MOVIE_CLASS = SOUP.find('div', attrs={"class":"nav-logo"}).contents[1].contents[0]
        if MOVIE_CLASS == u"豆瓣电影" :
            try:
                MOVIE_TYPE = SOUP.find('span', attrs={"class":"rec"}).a['data-type']
            except AttributeError:
                MOVIE_TYPE = "None"
    except AttributeError:
        MOVIE_CLASS = "NO_CLASS"


#QUNA = 'http://movie.douban.com/subject/1842121'
count=25835265
Doban_Url='http://movie.douban.com/subject/'

while count>0:
    URL=Doban_Url+str(count)
    print "Running %s" %count
    #print URL
    count -= 1
    GetPageInfo(URL)
    if html=='None':continue
    html = html.decode('utf8')
    ScratchMovies(html)
    if MOVIE_NAME == 'None':continue
    MOVIE='%(URL)s %(MOVIE_CLASS)s %(MOVIE_NAME)s %(MOVIE_FEN)s' %vars()
    print MOVIE
    if MOVIE_CLASS == u"豆瓣电影":
        f=open('MyMovies', 'a')
        f.write('%s\n' %MOVIE)
        f.close()
        if (MOVIE_FEN != 'None_property_yet') and (MOVIE_TYPE == u'电影'):
            print MOVIE_FEN
            Proporty = float(MOVIE_FEN)
            if Proporty >= 8.0:
                f=open('GreatMovies', 'a')
                f.write('%s\n' %MOVIE)
                f.close()

    elif MOVIE_CLASS == u"豆瓣读书":
        f=open('MyBooks', 'a')
        f.write('%s\n' %MOVIE)
        f.close()
    else:
        f=open('MyMusics', 'a')
        f.write('%s\n' %MOVIE)
        f.close()
    SleepTime = random.randint(2,5)
    time.sleep(SleepTime)