#-*- coding:utf-8 -*-

from module import moduleConfigTimeNow
from module import moduleTraceAnalyse
from module import moduleGetTrace
from module import moduleSWPortErrorAnalyze
from module import moduleOldFileClean
from module import moduleClearPortError

import configparser
import os
import sys


def main():

    if len(sys.argv) == 1:
        print('''
        -run        : Run Normally
        -statsclear : Clear PortError Counter on the SAN Switch
            ''')
    elif sys.argv[1] == '-run':
        moduleOldFileClean.Clean()
        moduleGetTrace.GetTrace()
        moduleTraceAnalyse.TraceAnalyze()
        moduleSWPortErrorAnalyze.SWPortErrorAnalyze()

    elif sys.argv[1] == '-statsclear':
        moduleClearPortError.ClearPortError()

    else:
        print('''
            -run        : Run Normally
            -statsclear : Clear PortError Counter on the SAN Switch
            ''')


main()
    
