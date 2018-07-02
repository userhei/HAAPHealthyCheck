# import os,shutil,time,getpass

from module import moduleConfigTimeNow
from module import moduleTraceAnalyse
from module import moduleGetTrace
from module import moduleSWPortErrorAnalyze

import configparser
import os



# ======= Setting ======= #
# intTelnetPort = 23
# intFTPPort = 21
# strPasswd = ''
# strSWPasswd ''

# ======= Get Password ======= #
# if not strPasswd:
#     strPasswd = getpass.getpass(prompt='Please Input Your Engine Password: ', stream=None)

# if not strPasswd:
#     strSWPasswd = getpass.getpass(prompt='Please Input Your SANSwitch Password: ', stream=None)

#

# ======= Port List of SANSwitch ======= #



# ======= List of SANSwitchIPs ======= #

# lstSANSwitchIPs = ['192.168.1.1','192.168.1.2']

#获取到所有SAN交换机的PortErrorShow，并以引擎地址保存文件


# objReadConfig = configparser.ConfigParser(allow_no_value=True)
# objReadConfig.read('Conf.ini')

# print(objReadConfig.get('GlobalSetting', 'TimeNow'))

def main():
    moduleGetTrace.GetTrace()
    moduleTraceAnalyse.TraceAnalyze()
    moduleSWPortErrorAnalyze.SWPortErrorAnalyze()

main()
    