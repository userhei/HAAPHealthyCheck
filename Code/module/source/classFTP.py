#-*- coding:utf-8 -*-

from ftplib import FTP


class FTPConnect(object):
    def __init__(self, strIP, intPort, strUserName, strPasswd):
        self._host = strIP
        self._port = intPort
        self._username = strUserName
        self._password = strPasswd
        self._connect()

    def _connect(self):

        ftp = FTP()
        try:
            ftp.connect(self._host, self._port)
        except TimeoutError as E:
            print('\nFTP Connect to {} Failed'.format(self._host))
        try:
            ftp.login(self._username, self._password)
        except Exception as E:
            print(E)
        return ftp

    def GetFile(self, strRemoteFolder, strLocalFolder, strRemoteFileName,\
    	strLocalFileName, FTPtype='bin', intBufSize = 1024):
        ftp = self._connect()
        # print(ftp.getwelcome())
        ftp.cwd(strRemoteFolder)
        objOpenLocalFile = open(strLocalFolder + '/' + strLocalFileName, "wb")

        if FTPtype == 'bin':
            ftp.retrbinary('RETR {}'.format(strRemoteFileName),
                           objOpenLocalFile.write)
        elif FTPtype == 'asc':
            ftp.retrlines('RETR {}'.format(strRemoteFileName),
                          objOpenLocalFile.write)

        objOpenLocalFile.close()
        ftp.close()

    def PutFile(self, strRemoteFolder, strLocalFolder, strRemoteFileName,\
    	strLocalFileName, FTPtype='bin', intBufSize = 1024):
        ftp = self._connect()
        # print(ftp.getwelcome())
        ftp.cwd(strRemoteFolder)
        objOpenLocalFile = open(strLocalFolder + '/' + strLocalFileName, 'rb')

        if FTPtype == 'bin':
            ftp.storbinary('STOR {}'.format(strRemoteFileName),
                           objOpenLocalFile, intBufSize)
        elif FTPtype == 'asc':
            ftp.storlines('STOR {}'.format(
                strRemoteFileName), objOpenLocalFile)

        ftp.set_debuglevel(0)
        objOpenLocalFile.close()
        ftp.close()
