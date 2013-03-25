# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
import urllib,urllib2,time,hashlib
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt  
import re
# from django.utils.encoding import smart_str, smart_unicode
import xiaoche
import translate
import huanyi
import weather
import renren

TOKEN = ""

welcome_msg = u"""
欢迎关注「人在北理」校园助手

"""

help_info = u"""
1.发送「校车」或「明天校车」可以查看校车时刻表。
2.发送「环一」或「环1」可以查看环1公交发车时刻。
3.发送「天气」或「空气」可以查看天气预报或空气质量。
4.发送英文单词或句子可以进行翻译。
5.发送「发状态」+「内容」会自动在人人主页发状态。
"""

report_info = u"""
报告bug或有任何建议请发邮件至liamchzh@gmail.com
©Liam  http://liamchzh.com/about
"""

@csrf_exempt
def handleRequest(request):
	if request.method == 'GET':
		response = HttpResponse(checkSignature(request),content_type="text/plain")
		return response
	elif request.method == 'POST':
		response = HttpResponse(responseMsg(request),content_type="application/xml")
		return response
	else:
		return None

def checkSignature(request):
	global TOKEN
	signature = request.GET.get("signature", None)
	timestamp = request.GET.get("timestamp", None)
	nonce = request.GET.get("nonce", None)
	echoStr = request.GET.get("echostr",None)

	token = TOKEN
	tmpList = [token,timestamp,nonce]
	tmpList.sort()
	tmpstr = "%s%s%s" % tuple(tmpList)
	tmpstr = hashlib.sha1(tmpstr).hexdigest()
	if tmpstr == signature:
		return echoStr
	else:
		return None

def responseMsg(request):
    # post_data = smart_str(request.raw_post_data)
    post_data = request.raw_post_data
    msg = paraseMsgXml(post_data)
    content = process(msg['Content'])
    return replyXml(msg, content)

def process(msg):
    if msg == 'Hello2BizUser':
        return welcome_msg+help_info
    elif isinstance(msg, type('string')):
        return translate.translate(msg)
    elif msg == u'校车' or msg == u'明天校车':
        return xiaoche.get_timetable(msg)
    elif msg == u'环一' or msg == u'环1':
        return huanyi.get_timetable()
    elif msg == u'天气':
        return weather.weather()
    elif msg == u'空气':
        return weather.get_airquality()
    elif re.match(u"发状态", msg):
        if msg[3:]:
            return renren.renren_status(msg[3:])
        else:
            return u"请输入状态内容"
    else:
        return u"无法处理请求，请查看使用说明" + help_info + report_info

def paraseMsgXml(raw_msg):  
    root = ET.fromstring(raw_msg)
    msg = {}  
    if root.tag == 'xml':  
        for child in root:  
            msg[child.tag] = (child.text)  
    return msg

def replyXml(recvmsg, replyContent):
    textTpl = """ <xml>
                <ToUserName><![CDATA[%s]]></ToUserName>
                <FromUserName><![CDATA[%s]]></FromUserName> 
                <CreateTime>%s</CreateTime>
                <MsgType><![CDATA[%s]]></MsgType>
                <Content><![CDATA[%s]]></Content>
                <FuncFlag>0</FuncFlag>
                </xml>
                """
    echostr = textTpl % (recvmsg['FromUserName'], recvmsg['ToUserName'], recvmsg['CreateTime'], recvmsg['MsgType'], replyContent)
    return echostr

