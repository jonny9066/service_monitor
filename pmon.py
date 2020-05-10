import os
import sys
import stat
import pmon_auto
import pmon_manual
import pmon_logging
import platform

current_os = platform.system()
if current_os != 'Linux' and current_os != 'Windows':
    sys.exit("Unsupported system, exiting.")

#check if permissions are correct
files = os.scandir()
for file in files:
    if file.name == 'serviceList.txt' or file.name == 'Status_Log.txt':
        if file.stat().st_mode != 33152:
            print('Permissions of log file have been changed by someone! It might have been modified!')



mode = sys.argv[1]


if mode == '-a':
    # get interval from user
    try:
        interval = int(sys.argv[2])
    except ValueError:
        print("Please supply valid arguments, use -h for usage info")
        sys.exit(1)
    
    pmon_auto.start_monitor(current_os, interval)
elif mode == '-m':
    time1 = pmon_logging.get_user_time_date(sys.argv[2])
    time2 = pmon_logging.get_user_time_date(sys.argv[3])
    pmon_manual.manual_sample(time1, time2)
elif mode == '-h':
    usage = "1) for automatic mode: python3 pmon -a interval\n2) for manual mode: python3 pmon -m event1 event1\n  (event must be in the following format: 'YYYY:MM:DD hh:mm:ss')"
    print(usage)
else:
    print("Please supply valid arguments, use -h for usage info")