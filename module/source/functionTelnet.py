import sys
import os
import re
import telnetlib
import time

#===# For Telnet To MAC Test
#strLoginPrompt = 'login'
#strMainMenuPrompt = 'Password'
#strCLIPrompt = '~'
#strCLIConflictPrompt = 'Another session owns the CLI'

#===# For Telnet To HAAP Engine
strLoginPrompt = 'Enter password'
strMainMenuPrompt = 'Coredump Menu'
strCLIPrompt = 'CLI>'
strCLIConflictPrompt = 'Another session owns the CLI'


def TelnetToEngineAndExecute(strIP, intPort, strPasswd, strCommand):
    objTelnetConnect = telnetlib.Telnet(strIP, intPort)

    objTelnetConnect.read_until(
        strLoginPrompt.encode(encoding="utf-8"), timeout=2)
    objTelnetConnect.write(strPasswd.encode(encoding="utf-8"))
    objTelnetConnect.write(b'\r')

    objTelnetConnect.read_until(
        strMainMenuPrompt.encode(encoding="utf-8"), timeout=2)
    objTelnetConnect.write(b'7')

    strOutPut = objTelnetConnect.read_until(
        strCLIPrompt.encode(encoding="utf-8"), timeout=2)
    if int(strOutPut.find(strCLIPrompt.encode(encoding="utf-8"))) > 0:
        time.sleep(0.25)
    elif int(strOutPut.find(strCLIConflictPrompt.encode(encoding="utf-8"))) > 0:
        objTelnetConnect.write(b'y' + b'\r')
        strOutPut = objTelnetConnect.read_until(strCLIPrompt.encode(encoding="utf-8"), timeout=2)
        if int(strOutPut.find(strCLIPrompt.encode(encoding="utf-8"))) > 0:
            print("------Handle the CLI Succesfully For Engine: " + strIP)
    else:
        print("------Goto the CLI Failed For Engine: " + strIP)
        sys.exit(0)

    objTelnetConnect.write(strCommand.encode(encoding="utf-8") + b'\r')
    strCommandResult = objTelnetConnect.read_until(
        strCLIPrompt.encode(encoding="utf-8"), timeout=10).decode()
    time.sleep(0.5)
    objTelnetConnect.close
    return strCommandResult

