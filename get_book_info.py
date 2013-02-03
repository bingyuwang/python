# -*- coding:utf-8 -*-
import urllib2
import json

book_url = "http://book.douban.com/subject/"
api_headurl = "https://api.douban.com/v2/book/"
def get_info(url):
    if url.startswith(book_url):
        book_id = url[31:-1]
        api_url = api_headurl + book_id
        get_json(api_url)
    else:
        pass

def get_json(url):
    book_json = urllib2.urlopen(url).read()
    book_data = json.loads(book_json)
    print book_data["rating"]["average"],book_data["author"][0],book_data["title"],book_data["alt"]

if __name__ == "__main__":
    get_info("http://book.douban.com/subject/20472637/")
