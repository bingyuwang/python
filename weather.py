# -*- coding:utf-8 -*-
import urllib, urllib2
import json

url_hd = 'http://m.weather.com.cn/data/101010200.html'
url_fs = 'http://m.weather.com.cn/data/101011200.html'
urls = [url_hd, url_fs]

url_aqi = 'http://pm25.in/api/querys/aqi_details.json?city=beijing&token=****************'

def weather():
    weather = u""
    for url in urls:
        weather = weather + get_weatherinfo(url)
    return weather
    

def get_weatherinfo(url):
    try:
        rawinfo = urllib2.urlopen(url).read()
        weatherinfo = json.loads(rawinfo)
        weatherinfo = weatherinfo["weatherinfo"]
        content = u"%s, %s, %s\n" % (weatherinfo["city"], weatherinfo["date_y"], weatherinfo["week"]) + u"今天：%s,%s\n" % (weatherinfo["temp1"], weatherinfo["weather1"]) + u"明天：%s,%s\n" % (weatherinfo["temp2"], weatherinfo["weather2"]) + u"后天：%s,%s\n" % (weatherinfo["temp3"], weatherinfo["weather3"])
        return content
    except:
        return u"暂时无法获取天气信息，请稍后再试"


def get_airquality():
    AQI = {"aqi":None, "area":None, "pm2_5":None, "pm10":None, "quality":None, "time_point":None}
    try:
        rawinfo = urllib2.urlopen(url_aqi).read()
        airinfo = json.loads(rawinfo)
        airinfo = airinfo[-1]
        for key in list(airinfo.viewkeys()):
            AQI[key] = airinfo[key]
    except:
        return u"暂时无法获取空气质量详情，请稍后再"
    
    content = u"%s空气质量指数：%s\nPM2.5: %s \t PM10: %s\n空气质量类别为：%s\n 数据来源网络 更新时间 %s" % (AQI["area"], AQI["aqi"], AQI["pm2_5"], AQI["pm10"], AQI["quality"], AQI["time_point"])
    return content
