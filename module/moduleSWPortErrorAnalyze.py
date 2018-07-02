import os
import time
import shutil
import codecs
import re
import collections
from collections import OrderedDict
import module
from module.source import classSSH
import configparser



objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

strSWUserName = objReadConfig.get('SWSetting', 'username')
strSWPasswd = objReadConfig.get('SWSetting', 'password')

oddSWPort = collections.OrderedDict()
for i in objReadConfig.items('SWPorts'):
    oddSWPort[i[0]] = eval(i[1])

lstSANSwitchIPs = list(oddSWPort.keys())
lstSWPorts = list(oddSWPort.values())

strSWPortErrorFolder = './SWPortErrorCollected'


def boolPortinLine(intPort, strLine):
    lstLine = strLine.split()
    if (str(intPort) + ':') in lstLine:
        return True
    else:
        return False


def findDataAndErr(intPortNum, lstPortErrLines):
    for portErrLine in lstPortErrLines:
        if boolPortinLine(intPortNum, portErrLine) == True:
            reDataAndErr = re.compile(
                r'(.*:)(\s+\S+\s+\S+)(\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+)(\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+)(.*)')
            # reDataAndErr = re.compile(
                # r'(.*:)((\s+\S+){2})((\s+\S)+{6})((\s+\S)+{5})(.*)')
            resultDataAndErr = reDataAndErr.match(portErrLine)
            return(resultDataAndErr.group(2).split() +
                   resultDataAndErr.group(4).split())


def SWPortErrorAnalyze():
    print(os.getcwd())
    print(os.getcwd())

    try:
        os.mkdir(strSWPortErrorFolder)
    except  FileExistsError as E:
        pass
    os.chdir(strSWPortErrorFolder)
    objPorterrResult = open('../../Result_{}.log'.format(objReadConfig.get('GlobalSetting','TimeNow')), 'a')

    for indexEngineIP in range(len(lstSANSwitchIPs)):
        strPortErrorFileName = 'SW_PorterrShow_{}.log'.format(
            lstSANSwitchIPs[indexEngineIP])
        objFilePorterrshow = open(strPortErrorFileName, 'w')
        objConnectToSANSwitch = classSSH.SSHConnection(
            lstSANSwitchIPs[indexEngineIP], 22, strSWUserName, strSWPasswd)
        print(str(objConnectToSANSwitch.exec_command(u'switchshow')))
        # print(str(objConnectToSANSwitch.exec_command('porterrshow')).replace('\n','\r'))
        objFilePorterrshow.write(
            str(objConnectToSANSwitch.exec_command('porterrshow')).replace('\\n','\r'))
        objFilePorterrshow.close()
        objConnectToSANSwitch.close()

        objPorterrResult.write(
            '{} Error Show: \n'.format(strPortErrorFileName) + '\n')
        #tx     rx    encout   discc3   linkfail   losssync   losssig
        objPorterrResult.write(
            'PortID' + '\t' + 'FramTX' + '\t' + 'FramRX' + '\t' + 'encout' + '\t' + 'Discc3' + '\t' + 'LinkFL' + '\t' + 'LossSC' + '\t' + 'LossSG' + '\n')
        lstPortErrLines = codecs.open(strPortErrorFileName).readlines()
        for intPortNum in lstSWPorts[indexEngineIP]:
            lstErrInfo = findDataAndErr(intPortNum, lstPortErrLines)
            objPorterrResult.write('{}\t'.format(str(intPortNum)))
            for strErrorCount in lstErrInfo:
                objPorterrResult.write(
                    '{}\t'.format(strErrorCount))
                print('{}'.format(strErrorCount), end='\t')
            objPorterrResult.write('\n')
            print('\n')
    objPorterrResult.close()
    os.chdir('../')
