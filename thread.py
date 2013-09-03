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
 
#¿¿¿¿
def get_all_links(page):
    while True:
        url, endpos = get_next_link(page)
        if url == None: 
            break
        elif url.startswith("http"):
            #print "find:" + url
            #urls.append(url)
            crawl_queue.put(url)
            page = page[endpos+1:]
        else:
            page = page[endpos+1:]

class CrawlUrl(threading.Thread):
    """¿¿¿¿¿¿¿html¿¿¿¿¿¿¿"""
    def __init__(self, crawl_queue):
        threading.Thread.__init__(self)
        self.crawl_queue = crawl_queue

    def run(self):
        while True:
            url = self.crawl_queue.get()
            if url not in crawledurl:
                try:
                    print "tocrawl:" + url
                    resp = urllib2.urlopen(url)
                    page= resp.read()
                    get_all_links(page)
                    crawledurl.append(url)
                except:
                    pass
            else:
                pass
            self.crawl_queue.task_done()

    
def main():
    for i in range(30):
        crawlthread = CrawlUrl(crawl_queue)
        crawlthread.setDaemon(True)
        crawlthread.start()

        for url in urls:
            crawl_queue.put(url)

    crawl_queue.join()

if __name__ == "__main__":
    main()
