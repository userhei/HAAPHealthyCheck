import datetime
import configparser
import os
print(os.getcwd())
import module
from module.source import functionTimeNow


strTimeNow = functionTimeNow.GetTimeNow()

objReadConfig = configparser.ConfigParser(allow_no_value=True)
objReadConfig.read('Conf.ini')

objReadConfig.set('GlobalSetting', 'TimeNow', strTimeNow)
objReadConfig.write(open('Conf.ini', "w"))