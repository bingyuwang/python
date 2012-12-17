# -*- encoding:utf-8 -*-
from xml.dom import minidom
import urllib2

rss = 'http://www.guokr.com/rss/'
##rss = 'http://www.bitren.com/'

def get_xml(url):
    return urllib2.urlopen(url).read()

def main():
    xmldoc = get_xml(rss)
    print xmldoc
    
    xmldoc = unicode(xmldoc, "utf-8")
##    grammarNode = xmldoc.firstChild
##    print grammarNode
##    xmldoc = xmldoc.encode('gb2312')
##    print xmldoc

if __name__ == '__main__':
    main()
