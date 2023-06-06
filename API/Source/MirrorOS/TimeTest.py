import time
import sys
from API.Exception import TimeServerNotFoundException as TimeServerNotFoundException
from datetime import timedelta
from API import NTP

try:
    startTime = NTP.get_ntp_time_datetime("ntp.nict.jp")
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