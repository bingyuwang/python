# Create your views here.
# -*- coding: utf-8 -*-
from django.http import HttpResponse
import urllib,urllib2,time,hashlib
import xml.etree.ElementTree as ET
from django.views.decorators.csrf import csrf_exempt  
# from django.utils.encoding import smart_str, smart_unicode
import xiaoche


TOKEN = "***"

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
    if msg == u'校车' or msg == u'明天校车':
        return xiaoche.get_timetable(msg)
    else:
        return msg

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
