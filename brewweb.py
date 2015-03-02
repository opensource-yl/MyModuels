import urllib
import sys,time, socket
import re
from bs4 import BeautifulSoup
import chardet
import urllib2


###################################################
#This is a small web crawler, designed to scratch build infos from brewweb,
#and result to a list with all buildinfos. Help yourself and feel free to recreate it.
###################################################
###################################################
#Configure your project which you want to monitor, such as: libguestfs, rhel-guest-image, rhevm, rhevh, and so on,
#it must be a real project which exists and can be searched on brewweb.
PackageName='rhel-guest-image'
####################################################

####################################################
#This is brewweb search web url. Do not change it.
BrewServer='https://brewweb.devel.redhat.com/search?match=glob&type=package&'
URL=BrewServer+'terms='+PackageName
print URL
#eg: https://brewweb.devel.redhat.com/search?match=glob&type=package&terms=rhel-guest-image
####################################################
####################################################
#Global variant.
html=''
####################################################

def GetPageInfo(url):
    global html
    try:
        Headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Connection': 'keep-alive'}
        #Headers is needed to make this crawler works as the browser. To find your user agent, open this link:
        #http://whatsmyuseragent.com/
        req = urllib2.Request(url, headers=Headers)
        content = urllib2.urlopen(req,timeout=10).read()

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
    return html
def ScratchBuildInfo(self):
    BuildList=[]
    SOUP = BeautifulSoup(self)
    BuildListSoup=SOUP.find_all('tr')
    for Build in BuildListSoup:
        if Build.find_all('th', attrs={"id":"buildlist"}):
            Soup=Build
            break
    BuildInfos=Soup.find_all('tr', attrs={"class":re.compile('row')})
    for BuildInfo in BuildInfos:
        BuildNames = BuildInfo.find_all('td')
        BuildDict={}
        BuildDict["BuildName"] = BuildNames[0].a.contents
        BuildDict["BuildUser"] = BuildNames[1].a.contents
        BuildDict["BuildTime"] = BuildNames[2].contents
        BuildDict["BuildStatus"] = BuildNames[3]['class']
        BuildList.append(BuildDict)

    return BuildList

BuildList=[]
BuildDict={}
PackageInfo=GetPageInfo(URL)
BuildLists=ScratchBuildInfo(PackageInfo)

#for i in BuildLists: print i
#{'BuildName': [u'rhel-guest-image-7.1-20150224.0.el7'], 'BuildUser': [u'rbarry'], 'BuildTime': [u'2015-02-24 12:26:03'], 'BuildStatus': ['complete']}
#{'BuildName': [u'rhel-guest-image-7.1-20150224.0'], 'BuildUser': [u'rbarry'], 'BuildTime': [u'2015-02-24 09:34:16'], 'BuildStatus': ['complete']}
#{'BuildName': [u'rhel-guest-image-7.1-20150223.0.el7'], 'BuildUser': [u'rbarry'], 'BuildTime': [u'2015-02-23 14:43:45'], 'BuildStatus': ['complete']}
#...
