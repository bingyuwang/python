# coding:utf-8

import urllib2
import Queue
import threading

urls = ["http://m.sohu.com/"]
crawledurl = []

crawl_queue = Queue.Queue()

def get_next_link(page):
    start_link = page.find("href=")
    if start_link == -1:
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote
 
def get_all_links(page, baseurl):
    while True:
        url, endpos = get_next_link(page)
        if url == None: 
            break
        elif url.startswith("http"):
            #urls.append(url)
            #print "http:"+ url
            crawl_queue.put(url)
            page = page[endpos+1:]
        elif url.startswith("javascript"):
            pass
        else:
            crawl_queue.put(baseurl[:-1]+url)
            page = page[endpos+1:]

def write_log(error, url):
    ferror = open("log.txt", "a")
    ferror.write(error)
    ferror.write(url+'\n')
    ferror.close()

def check_link(url):
    """
    f = open("urls.txt", "a")
    f.write(url)
    f.close()
    """
    try:
        resp = urllib2.urlopen(url, timeout=5)
    except urllib2.HTTPError,e:
        write_log("HTTPError", url)
    except urllib2.URLError,e:
        write_log("URLError", url)
    except:
        print "timeout:" + url
        write_log("unknow", url)
    else:
        print "check:" + url
        page = resp.read()
        get_all_links(page, url)
        crawledurl.append(url)

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

        for url in urls:
            crawl_queue.put(url)

    crawl_queue.join()

if __name__ == "__main__":
    main()

