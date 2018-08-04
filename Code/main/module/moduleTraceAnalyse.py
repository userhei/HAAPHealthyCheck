#-*- coding:utf-8 -*-

import re
import sys
import os
import codecs
import xlwt
import collections
import time
import configparser


objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

oddHAAPErrorDict = collections.OrderedDict()
for i in objReadConfig.items('TraceRegular'):
    oddHAAPErrorDict[i[0]] = eval(i[1])

strLocalTraceFolder = objReadConfig.get('FolderSetting','TraceFolder')


def ReadFile(fileName):
    with open(fileName, 'r+') as fileContent: # Python 3 :, encoding='UTF-8', errors='ignore'
        strTrace = fileContent.read()
    return strTrace.strip().replace('\ufeff', '')

def HAAPTraceAnalysing(lstTraceFiles):	#输入参数是一个列表
	
	objLogFile = open('../../collection_{}_Result.log'.format(objReadConfig.get('GlobalSetting','TimeNow')), 'w')
	objLogFile.write("TraceAnalyze Result @ {} ...".format(objReadConfig.get('GlobalSetting','TimeNow')) + '\n\n')

	intErrFlag = 0
	for strFileName in lstTraceFiles:
		if (lambda i:i.startswith('Trace_'))(strFileName):
			print('\n{}  Analysing ...'.format(strFileName))
			objLogFile.write('\n{}  Analysing ...'.format(strFileName) + '\n')
			openExcel = xlwt.Workbook() #创建工作簿
			for strErrType in oddHAAPErrorDict.keys():
				reErrInfo = re.compile(oddHAAPErrorDict[strErrType])
				tupInlstFindAll = reErrInfo.findall(ReadFile(strFileName))
				if len(tupInlstFindAll) > 0:
					print("  ***  {} Times of {} Error Found...".format((len(tupInlstFindAll) + 1),strErrType))
					objLogFile.write("   ***  {} Times of {} Error Found...\r".format((len(tupInlstFindAll) + 1),strErrType))
					strSheetName = strErrType
					objSheet = openExcel.add_sheet(strSheetName) #需要覆盖的话加“,cell_overwrite_ok=True”
					for x in range(len(tupInlstFindAll)):
						for y in range(len(tupInlstFindAll[x])):
							objSheet.write(x,y,tupInlstFindAll[x][y].strip().replace("\n",'',1))
					intErrFlag += 1
				else:
					# print("--- No {} Error in {}".format(strErrType,strFileName))
					pass
				reErrInfo = None
			else:
				pass
			if intErrFlag > 0:
				openExcel.save('TraceAnalyse_' + strFileName + '.xls')	#保存工作簿
			else:
				print("--- No Error in {}".format(strFileName))
				objLogFile.write("--- No Error in {}\r".format(strFileName))
			intErrFlag = 0
	objLogFile.close()

def TraceAnalyze():
    lstTraceFileNames = os.listdir(strLocalTraceFolder)
    os.chdir(strLocalTraceFolder)
    HAAPTraceAnalysing(lstTraceFileNames)
    os.chdir('../')
