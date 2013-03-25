# -*- coding:utf-8 -*-

#from sgmllib import SGMLParser
import sys,urllib2,urllib,cookielib
import json

ID = ""
tok = ""
rtk = ""

user = ''
password = ''
domain = 'renren.com'

def renren_status(msg):
    msg = msg.encode("utf-8")
    try:
        login()
        return post(msg)
    except:
        return u"出现异常，请稍后再试"        
        
def login():
    try:
        cookie=cookielib.CookieJar()
        cookieProc=urllib2.HTTPCookieProcessor(cookie)
    except:
        raise
    else:
        opener=urllib2.build_opener(cookieProc)
        urllib2.install_opener(opener)
    login_url='http://www.renren.com/PLogin.do'
    postdata={
              'email': user,
              'password': password,
              'domain': domain  
              }
    req = urllib2.Request(
                        login_url,
                        urllib.urlencode(postdata)            
                        )
        
    account_data = urllib2.urlopen(req).read()
    """
    global ID, tok, rtk
    idPos = account_data.index("'id':'")
    ID = account_data[idPos+6:idPos+15]
    tokPos = account_data.index("get_check:'")
    tok = account_data[tokPos+11:tokPos+21]
    rtkPos = account_data.index("get_check_x:'")
    rtk = account_data[rtkPos+13:rtkPos+21]
    print ID, tok, rtk
    """
    
def post(content):
    global ID, tok, rtk
    post_url='http://shell.renren.com/'+ID+'/status'
    postdata={
          'content':content,
          'hostid':ID,
          'requestToken':tok,
          '_rtk':rtk,
          'channel':'renren',
          }
    req = urllib2.Request(
                        post_url,
                        urllib.urlencode(postdata)            
                        )
    post_req = urllib2.urlopen(req).read()
    post_req = json.loads(post_req)
    if post_req.has_key("updateStatusId"):
        return u"发状态成功，内容会在「人在北理」人人主页上显示"
    else:
        return u"发状态失败，请稍后再试"
