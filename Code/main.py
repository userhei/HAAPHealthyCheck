#-*- coding:utf-8 -*-

from module import moduleConfigTimeNow
from module import moduleTraceAnalyse
from module import moduleGetTrace
from module import moduleSWPortErrorAnalyze
from module import moduleOldFileClean
from module import moduleClearPortError
from module import moduleZipCollections

import configparser
import os
import sys

strHelp = '''
        -run        : Run Normally
        -statsclear : Clear PortError Counter on the SAN Switch
        -zipall 	: Zip All Collections and Result File
        '''

def main():

    if len(sys.argv) == 1:
        print(strHelp)
    elif sys.argv[1] == '-run':
        moduleOldFileClean.Clean()
        moduleGetTrace.GetTrace()
        moduleTraceAnalyse.TraceAnalyze()
        moduleSWPortErrorAnalyze.SWPortErrorAnalyze()
        moduleZipCollections.ZipCollections()

    elif sys.argv[1] == '-statsclear':
        moduleClearPortError.ClearPortError()

    elif sys.argv[1] == '-zipall':
    	moduleZipCollections.ZipAll()

    else:
        print(strHelp)


main()
    
