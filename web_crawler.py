#-*- encoding:utf-8 -*-
import urllib2
 
def get_page(url):
    try:
        return urllib2.urlopen(url).read()
    except:
        return ""

def get_next_target(page):
    start_link = page.find('href=')
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    print url
    return url, end_quote
 
def get_all_links(page):
    links = [] #�����ҵ���Links
    while True:
        url, endpos = get_next_target(page)
        if url == None: #url == None, ˵��û�������ˣ��˳�ѭ��
            break
        elif url.startswith("http"):
            links.append(url) #�ҵ�url����ӵ�index
            page = page[endpos+1:]
        else:
            page = page[endpos+1:]
    return links
 
index = [] #��Źؼ��ֺ�����
 
def add_to_index(index, keyword, url):
    for entry in index:
        if entry[0] == keyword:
            entry[1].append(url)
            return
        index.append([keyword,[url]])
 
def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
        return []
 
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)
 
def crawl_web(seed):
    tocrawl = [seed] #û��������
    crawled = []     #�Ѿ�������
    while tocrawl:
        page = tocrawl.pop()
        print "ready to craw "+page
        if page not in crawled:
            content = get_page(page)
            #add_page_to_index(index, page, content)
            tocrawl = tocrawl + get_all_links(content)
            crawled.append(page)
    return crawled
 
if __name__ == '__main__':
    crawl_web('http://bitren.com')

