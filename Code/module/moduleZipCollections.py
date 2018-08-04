import os
import time
import datetime
import shutil
import sys
import configparser
import module
from module.source import functionZipFile

objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

strFolderName = objReadConfig.get('FolderSetting','collectionfolder')
strTimeNowFromConf = objReadConfig.get('GlobalSetting','TimeNow')

def ZipCollections():
    if os.path.exists(strFolderName):

        os.chdir(strFolderName)

        functionZipFile.ZipFilesOrDirs('Zip_{}.zip'.format(strTimeNowFromConf),\
            'collection_{}'.format(strTimeNowFromConf),\
            'collection_{}_Result.log'.format(strTimeNowFromConf))

    else:
        pass

def ZipAll():
    if os.path.exists(strFolderName):
        lstFName = list(os.listdir(strFolderName))

        for intIndex in range(len(lstFName))[::-1]:
            if lstFName[intIndex].endswith('.zip'):
                lstFName.remove(lstFName[intIndex])

        os.chdir(strFolderName)

        functionZipFile.ZipFilesOrDirs('ZipAll_{}.zip'.format(strTimeNowFromConf),*lstFName)
        print('All Collections file and Result file Store in {}/{}'.format(strFolderName,'ZipAll_{}.zip'.format(strTimeNowFromConf)))
    else:
        pass