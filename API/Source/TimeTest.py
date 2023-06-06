import Function
import time
import sys
import Exception.TimeServerNotFoundException as TimeServerNotFoundException
from datetime import timedelta

try:
    startTime = Function.get_ntp_time_datetime("ntp.nict.jp")
except TimeServerNotFoundException as e:
    print(e)
    sys.exit()

if startTime.year <= 1999:
    print ("Error:Could not connect to NTP server")
    sys.exit()
else:
    while True:
        time.sleep(1)
        startTime = startTime + timedelta(seconds = 1)
        print(f'\r{startTime}', end='')
        sys.stdout.flush()