#-*- coding:utf-8 -*-

import datetime
import configparser

def GetTimeNow():
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-7]
    time_now = time_now.replace(' ', '-')
    strTimeNow = time_now.replace(':', '-')
    return strTimeNow
