#-*- coding:utf-8 -*-

import os
import datetime
import shutil
import re
import time
import configparser
import getpass
from collections import OrderedDict
import module
from module.source import classFTP
from module.source import functionTelnet
from module.source import functionTimeNow


objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

lstEngineIPs = list(i[0] for i in objReadConfig.items('Engines'))
intTraceLevel = int(objReadConfig.get('TraceSetting','TraceLevel'))
intTelnetPort = int(objReadConfig.get('EngineSetting','TelnetPort'))
intFTPPort = int(objReadConfig.get('EngineSetting','FTPPort'))

strHAAPPasswd = objReadConfig.get('EngineSetting','HAAPPassword')
if strHAAPPasswd:
    strHAAPPasswd = strHAAPPasswd
else:
    strHAAPPasswd = getpass.getpass(
        prompt='Please Input Your Engine Password: ', stream=None)


strTimeNow = functionTimeNow.GetTimeNow()


def GetoddTraceCommand(intTraceLevel):
    oddTraceCommand = OrderedDict()
    if intTraceLevel == 1 or intTraceLevel == 2 or intTraceLevel == 3:
        oddTraceCommand['Trace'] = 'ftpprep trace'
        if intTraceLevel == 2 or intTraceLevel == 3:
            oddTraceCommand['Primary'] = 'ftpprep coredump primary all'
            if intTraceLevel == 3:
                oddTraceCommand['Secondary'] = 'ftpprep coredump secondary all'
        return oddTraceCommand
    else:
        print('Error: Trace Level Must Be 1,2,3')
        return 'Trace Level Must Be 1,2,3'


def FindTraceName(strResultOut):
    reFindTraceFileName = r'(ftp_data_\d{8}_\d{6}.txt)'
    objResult = re.search(reFindTraceFileName, strResultOut)
    try:
        return (objResult.group(1))
    except AttributeError as E:
        # print(E)
        return 'Trace File Create Failed...'


def GetTrace():

    strWorkDir = '{}/collection_{}'.format(objReadConfig.get('FolderSetting','collectionfolder'),\
        objReadConfig.get('GlobalSetting', 'TimeNow'))
    os.makedirs(strWorkDir)
    os.chdir(strWorkDir)

    strLocalTraceFolder = objReadConfig.get('FolderSetting','TraceFolder')
    try:
        os.mkdir(strLocalTraceFolder)
    except WindowsError as E:
        pass

    oddTraceCommand = GetoddTraceCommand(intTraceLevel)
    if isinstance(oddTraceCommand, OrderedDict):
        lstTraceCommand = list(oddTraceCommand.values())
        lstTraceDescribe = list(oddTraceCommand.keys())
    else:
        print('Please Check the Trace Level Setting')

    for strEngineIP in lstEngineIPs:

        try:
            objFTPToEngine = classFTP.FTPConnect(
                strEngineIP, intFTPPort, 'adminftp', strHAAPPasswd)
            for i in range(len(lstTraceDescribe)):
                strOutputTraceName = functionTelnet.TelnetToEngineAndExecute(
                    strEngineIP, intTelnetPort, strHAAPPasswd, lstTraceCommand[i])
                strTraceFileName = FindTraceName(strOutputTraceName)
                if strTraceFileName.startswith('ftp_data'):
                    strLocalFileName = 'Trace_{}_{}_{}.log'.format(
                        strEngineIP, lstTraceDescribe[i], strTimeNow)
                    objFTPToEngine.GetFile(
                        'mbtrace', strLocalTraceFolder, strTraceFileName, strLocalFileName)
                    print('\nGet Trace {} Completely For {}'.format(lstTraceDescribe[i],strEngineIP))
                elif strTraceFileName.startswith('Trace'):
                    print('{} Create Failed For {}'.format(lstTraceDescribe[i],strEngineIP))
        except Exception as E:
            print('Connect to Engine {} Failed ...'.format(strEngineIP))
            continue

        
