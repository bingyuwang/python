# -*- coding:utf-8 -*-
import urllib
import urllib2
import cookielib

def chaxun():
    cj = cookielib.LWPCookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)

##
##    data = urllib2.urlopen(url)
##    f = open('chaxun.txt','w')
##    f.write(data.read())
##    print cj._cookies.values()
##    
    log_url = 'http://bitpt.cn/login.php'#post_url
    login_info = {
        'cookie_time' : 86400,
        'password' : 'Xpd3eksa',
        'submitbutton': '提交',
        'username' : 'LAMPARD'}
    req = urllib2.Request(
        log_url,
        urllib.urlencode(login_info))
    resp = urllib2.urlopen(req)
    resp1 = urllib2.urlopen('http://bitpt.cn/takelogin.php')
    print resp.read()#读取返回信息
    print resp1.read()
    
if __name__ == '__main__':
    chaxun()
