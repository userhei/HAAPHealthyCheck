#-*- coding:utf-8 -*-

import os
import datetime
import shutil
import re
import time
import configparser
import getpass
import module
from module.source import functionHAAPExcute


objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

lstEngineIPs = list(i[0] for i in objReadConfig.items('Engines'))
intTelnetPort = int(objReadConfig.get('EngineSetting','TelnetPort'))
strCollectionFolder = objReadConfig.get('FolderSetting','collectionfolder')
strTimeNowFromConf = objReadConfig.get('GlobalSetting','TimeNow')
lstCheckCommand = list(i[0] for i in objReadConfig.items('PeriodicCheckCommand'))

strHAAPPasswd = objReadConfig.get('EngineSetting','HAAPPassword')
if strHAAPPasswd:
    strHAAPPasswd = strHAAPPasswd
else:
    strHAAPPasswd = getpass.getpass(
        prompt = 'Please Input Your Engine Password: ', stream = None)


def Excute(*lstCommand):

    strWorkDir = '{}/PeriodicCheck_{}'.format(strCollectionFolder,strTimeNowFromConf)
    try:
        os.makedirs(strWorkDir)
    except WindowsError as E:
        pass
    os.chdir(strWorkDir)

    for strEngineIP in lstEngineIPs:
        objCheckResultFile = open('Engine_{}_ChechResult.log'.format(strEngineIP), 'a')
        try:
            strOutPutResult = functionHAAPExcute.HAAPExecute(strEngineIP, intTelnetPort, strHAAPPasswd, *lstCommand)
            objCheckResultFile.write(strOutPutResult)
        except Exception as E:
            print('Connect to Engine {} Failed ...'.format(strEngineIP))
            continue
        objCheckResultFile.close
        print('Engine {} Check completely, Result saved in {}'.format(strEngineIP,strWorkDir))

def main():
    Excute(*lstCheckCommand)
