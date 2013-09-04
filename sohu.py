# coding:utf-8

import urllib2
import socket
import Queue
import threading
import sys
import datetime

# 已经爬过的链接和不需要爬的链接
crawledurl = []
filterurl = ["javascript:void(0);", "#", "javascript:;", "javascript:window.scrollTo(0,0);"]

crawl_queue = Queue.Queue()

def get_next_link(page):
    """找到下一个href，提取链接"""
    start_link = page.find("href=")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    if url in filterurl:
        url = "/"
    return url, end_quote
 
def get_all_links(page, baseurl):
    """获取整个页面的链接"""
    while True:
        url, endpos = get_next_link(page)
        if url == None: 
            break
        elif url.startswith("http"):
            crawl_queue.put(url)
            page = page[endpos+1:]
        else:
            crawl_queue.put(baseurl[:-1]+url)
            page = page[endpos+1:]

def write_log(error, url):
    """把错误信息写入日志"""
    ferror = open("log.txt", "a")
    ferror.write(error+" ")
    ferror.write(str(datetime.datetime.now())+" ")
    ferror.write(url+'\n')
    ferror.close()

def check_link(url):
    """分析链接"""
    crawledurl.append(url)
    try:
        resp = urllib2.urlopen(url, timeout=5)
    except urllib2.HTTPError,e:
        write_log("HTTPError:"+str(e.code), url)
    except urllib2.URLError,e:
        write_log("URLError:"+str(e.reason), url)
    except socket.timeout:
        write_log("TiemoutError:", url)
    except:
        write_log("UnkonwError:", url)
    else:
        page = resp.read()
        get_all_links(page, url)

class CrawlUrl(threading.Thread):
    def __init__(self, crawl_queue):
        threading.Thread.__init__(self)
        self.crawl_queue = crawl_queue

    def run(self):
        while True:
            url = self.crawl_queue.get()
            if url not in crawledurl:
                check_link(url)
            self.crawl_queue.task_done()

def main():
    for i in range(10):
        crawlthread = CrawlUrl(crawl_queue)
        crawlthread.setDaemon(True)
        crawlthread.start()

        url = "http://m.sohu.com/"
        crawl_queue.put(url)

    crawl_queue.join()

if __name__ == "__main__":
    main()

