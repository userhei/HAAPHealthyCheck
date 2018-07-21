#-*- coding:utf-8 -*-

from __future__ import print_function
import os
import time
import shutil
import codecs
import re
import sys
import configparser
import collections
from collections import OrderedDict
import module
from module.source import classSSH



objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

strSWUserName = objReadConfig.get('SWSetting', 'username')
strSWPasswd = objReadConfig.get('SWSetting', 'password')

oddSWPort = collections.OrderedDict()
for i in objReadConfig.items('SWPorts'):
    oddSWPort[i[0]] = eval(i[1])

lstSANSwitchIPs = list(oddSWPort.keys())
lstSWPorts = list(oddSWPort.values())

strSWPortErrorFolder = objReadConfig.get('FolderSetting','porterrfolder')


def boolPortinLine(intPort, strLine):
    lstLine = strLine.split()
    if (str(intPort) + ':') in lstLine:
        return True
    else:
        return False


def findDataAndErr(intPortNum, lstPortErrLines):
    for portErrLine in lstPortErrLines:
        if boolPortinLine(intPortNum, portErrLine) == True:
            reDataAndErr = re.compile(r'(.*:)((\s+\S+){2})((\s+\S+){6})((\s+\S+){5})(.*)')
            resultDataAndErr = reDataAndErr.match(portErrLine)
            return(resultDataAndErr.group(2).split() +
                   resultDataAndErr.group(6).split())


def SWPortErrorAnalyze():
    try:
        os.mkdir(strSWPortErrorFolder)
    except  FileExistsError as E:
        pass
    os.chdir(strSWPortErrorFolder)

    objPorterrResult = open('../../collection_{}_Result.log'.format(objReadConfig.get('GlobalSetting','TimeNow')), 'a')

    for indexEngineIP in range(len(lstSANSwitchIPs)):
        strPortErrorFileName = 'SW_porterrshow_{}.log'.format(
            lstSANSwitchIPs[indexEngineIP])
        objFilePorterrshow = open(strPortErrorFileName, 'w')

        try:
            objConnectToSANSwitch = classSSH.SSHConnection(
                lstSANSwitchIPs[indexEngineIP], 22, strSWUserName, strSWPasswd)
            objFilePorterrshow.write(
            str(objConnectToSANSwitch.exec_command('porterrshow')).replace('\\n','\r'))
            objFilePorterrshow.close()
            objConnectToSANSwitch.close()
        except Exception as E:
            print('Connect to SAN Switch {} Failed ...'.format(lstSANSwitchIPs[indexEngineIP]))
            continue
        
        objPorterrResult.write(
            '\n' + '{} Error Picked: \n'.format(strPortErrorFileName))
        print('\n' + '{} Error Picked: \n'.format(strPortErrorFileName))
        #tx     rx    encout   discc3   linkfail   losssync   losssig
        objPorterrResult.write(
            'PortID'.center(8) + 'FramTX'.center(8) + 'FramRX'.center(8) + 'encout'.center(8) + 'Discc3'.center(8) + 'LinkFL'.center(8) + 'LossSC'.center(8) + 'LossSG' + '\n')
        print('PortID'.center(8) + 'FramTX'.center(8) + 'FramRX'.center(8) + 'encout'.center(8) + 'Discc3'.center(8) + 'LinkFL'.center(8) + 'LossSC'.center(8) + 'LossSG')
        

        if '3.6' in sys.version.split(' ')[0]:
            lstPortErrLines = codecs.open(strPortErrorFileName).readlines()
        elif '3.4' in sys.version.split(' ')[0]:
            lstPortErrLines = open(strPortErrorFileName).readlines()
        elif '2.7' in sys.version.split(' ')[0]:
            lstPortErrLines = open(strPortErrorFileName).readlines()

        for intPortNum in lstSWPorts[indexEngineIP]:
            lstErrInfo = findDataAndErr(intPortNum, lstPortErrLines)
            objPorterrResult.write(str(intPortNum).center(8))
            print(str(intPortNum).center(8), end='')
            for strErrorCount in lstErrInfo:
                objPorterrResult.write(strErrorCount.center(8))
                print(strErrorCount.center(8), end='')
            objPorterrResult.write('\n')
            print('')
    objPorterrResult.close()
    os.chdir('../../../')
