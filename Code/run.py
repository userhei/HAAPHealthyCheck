import os
import time
import sys
import sched 
import configparser

objReadConfig = configparser.ConfigParser(allow_no_value = True)
objReadConfig.read('Conf.ini')

intSecInterval = int(objReadConfig.get('runsetting','interval'))
command = 'main'

def Running(interval, command): 
    print('TimeNow:{}'.format(time.strftime('%Y-%m-%d %X',time.localtime())))

    os.system(command)

    objSchedule = sched.scheduler(time.time, time.sleep)

    objSchedule.enter(intSecInterval, 0, Running, (intSecInterval, command))
    objSchedule.run()

while True:
    try:
        Running(intSecInterval, command)
    except KeyboardInterrupt:
        sys.exit()