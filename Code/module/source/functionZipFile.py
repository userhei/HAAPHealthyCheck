import os
import zipfile
import shutil


def ZipFilesOrDirs(strZipFileName,*lstFName):

    lstFileName = []
    for strFName in lstFName:
        if os.path.isfile(strFName):
            lstFileName.append(strFName)
        elif os.path.isdir(strFName):
            for strRoot, lstDirs, lstFiles in os.walk(strFName):
                for strFileName in lstFiles:
                    lstFileName.append(os.path.join(strRoot, strFileName))
    objZipFileWrite = zipfile.ZipFile(strZipFileName, 'w', zipfile.zlib.DEFLATED)
    for strFullFileName in lstFileName:
        objZipFileWrite.write(strFullFileName)

    objZipFileWrite.close()


def CheckZipFileAndDelete(strZipFileName,*lstFName):
    objZipFileRead = zipfile.ZipFile(strZipFileName, 'r')
    if objZipFileRead.testzip() == None:
        print('Zip File {} Test OK, Now Delete All Source File And Folder...'.format(strZipFileName))
        for strFName in lstFName:
            if os.path.isfile(strFName):
                os.remove(strFName)
            elif os.path.isdir(strFName):
                shutil.rmtree(strFName)
    else:
        pass


# ZipFilesOrDirs('strZipFileName.zip','classSSH.py','classSSH321.py')

