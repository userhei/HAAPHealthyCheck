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


def ClearPortError():

    for indexEngineIP in range(len(lstSANSwitchIPs)):
        try:
            objConnectToSANSwitch = classSSH.SSHConnection(
                lstSANSwitchIPs[indexEngineIP], 22, strSWUserName, strSWPasswd)
            for strPortNum in lstSWPorts[indexEngineIP]:
                objConnectToSANSwitch.exec_command('statsclear {}'.format(str(strPortNum)))
        except Exception as E:
            print('Connect to SAN Switch {} Failed ...'.format(lstSANSwitchIPs[indexEngineIP]))
            continue

    objConnectToSANSwitch.close()

# ClearPortError()