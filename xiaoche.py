# -*- coding:utf-8 -*-
import datetime

weekdays_table = u"""
        本部←→良乡(对开)
        6:40
        8:00
        10:10
        12:20
        12:50
        14:30
        16:10
        18:30
        21:40
"""
weekends_table = u"""
        本部—→良乡
        7:30(1辆)
        13:30(1辆)
        20:00(1辆)
        良乡—→本部
        8:30(1辆)
        14:30(1辆)
        21:00(1辆)
"""
holidays_table = u"""
        本部—→良乡
        8:00(1辆)
        20:00(1辆)
        良乡—→本部
        9:00(1辆)
        21:00(1辆)
"""

holidays = [[[2013,04,04],[2013,04,06]]]

def get_timetable(msg):
    if msg == u'校车':
        return timetable(0)
    elif msg == u'明天校车':
        return timetable(1)

def timetable(offset):
    date = datetime.date.today() + datetime.timedelta(days = offset)
    if check(date):
        return u'%s是法定节假日，校车时刻如下：\n' % date + holidays_table
    elif date.weekday() == 5 or date.weekday() == 6:
        return u'%s是周末，校车时刻如下：\n' % date + weekends_table
    else:
        return u'%s校车时刻如下\n' % date + weekdays_table

def check(date):
    for day in holidays:
        print day
        start = datetime.date(day[0][0], day[0][1], day[0][2])
        end = datetime.date(day[1][0], day[1][1], day[1][2])
        if start<=date<=end:
            return True
    return False
