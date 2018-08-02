#-*- coding:utf-8 -*-
import os
import time
import datetime
import shutil
import sys
import configparser


objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

strFolderName = objReadConfig.get('FolderSetting','collectionfolder')
fltFileRetain = float(objReadConfig.get('RetainSetting','resultfileretain'))
fltFolderRetain = float(objReadConfig.get('RetainSetting','collectfolderretain'))


def functionClean(strFName):        #Fname : File or Folder Name
    fltFileCreateTimeStamp = os.path.getmtime(strFName)
    fltNowTimeStamp = time.time()
    fltDeltaDays = (fltNowTimeStamp - fltFileCreateTimeStamp)/60/60/24

    try:
        if os.path.isfile(strFName) and fltDeltaDays >= fltFileRetain:
            os.remove(strFName)
            return('Delete File: {} '.format(strFName))
        elif os.path.isdir(strFName) and fltDeltaDays >= fltFolderRetain:
            shutil.rmtree(strFName)
            return('Delete Folder: {} '.format(strFName))
    except Exception as e:                                             
        print(e)
        return('Delete Failed With Error: {}'.format(e))

def Clean():
    if os.path.exists(strFolderName):
        intFlagOldFile = 0
        lstFName = list(os.listdir(strFolderName))
        objLogFile = open('{}/collection_{}_Result.log'.format(strFolderName, objReadConfig.get('GlobalSetting','TimeNow')), 'a')
        objLogFile.write('\nDelete Old Colections and Result File ...\n')
        print('\nDelete Old Colections and Result File ...\n')
        for strFname in lstFName:
            strResult = functionClean('{}/{}'.format(strFolderName, strFname))
            if strResult:
                objLogFile.write(strResult + '\n')
                print(strResult)
                intFlagOldFile += 1
            else:
                pass

        if intFlagOldFile == 0:
            objLogFile.write('No file been deleted...\n')
            print('No file been deleted...')
    
        objLogFile.write('\n')
        print('')
    else:
        pass

