#-*- coding:utf-8 -*-

from module import moduleConfigTimeNow
from module import moduleTraceAnalyse
from module import moduleGetTrace
from module import moduleSWPortErrorAnalyze
from module import moduleOldFileClean
from module import moduleClearPortError
from module import moduleZipCollections
from module import modulePeriodicCheck

import configparser
import os
import sys

strHelp = '''
        -run            : Run Normally
        -porterrshow    : Run, but Collect PortError only
        -statsclear     : Clear PortError Counter on the SAN Switch
        -zipall         : Zip All non-Zip File
        -check          : Run Periodic Check
        '''

def main():

    if len(sys.argv) == 1 or len(sys.argv) > 2:
        print(strHelp)
        
    elif sys.argv[1] == '-run':
        moduleOldFileClean.Clean()
        moduleGetTrace.GetTrace()
        moduleTraceAnalyse.TraceAnalyze()
        moduleSWPortErrorAnalyze.SWPortErrorAnalyze()
        moduleZipCollections.ZipCollections()

    elif sys.argv[1] == '-porterrshow':
        moduleOldFileClean.Clean()
        moduleSWPortErrorAnalyze.SWPortErrorAnalyze()
        moduleZipCollections.ZipCollections()

    elif sys.argv[1] == '-statsclear':
        moduleClearPortError.ClearPortError()

    elif sys.argv[1] == '-zipall':
    	moduleZipCollections.ZipAll()

    elif sys.argv[1] == '-check':
        modulePeriodicCheck.main()

    else:
        print(strHelp)


main()
    
