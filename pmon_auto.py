import csv
import pmon_logging
import psutil
import time
import sys


def start_monitor(current_os, interval):
    # create new logger objects
    service_list_logger = pmon_logging.pmon_logger('svclist', 'serviceList.txt')
    status_logger = pmon_logging.pmon_logger('statlog', 'Status_Log.txt')

    #pick up where we left off: get last sample and processes from last sample_id
    sample_id = int(pmon_logging.get_last_sid())
    ps_old = pmon_logging.get_processes_by_sid(sample_id)
    sample_id += 1
    try:
        while True:
            # list to store our services
            ps_new = []
            if current_os == 'Linux':
                for process in psutil.process_iter():
                    # we discern daemons by checking whether they are linked to a terminal
                    if process.terminal() is None:
                        ps_new.append([str(process.pid), process.name()])
                        
            else: #must be windows
                for process in psutil.win_service_iter():
                    ps_new.append([str(process.pid()), process.name()])
            #take difference between old and new lists
            ps_born = [i for i in ps_old + ps_new if i in ps_new and i not in ps_old]
            ps_died = [i for i in ps_old + ps_new if i in ps_old and i not in ps_new]


            #logging and printing
            service_list_logger.log_serviceList(ps_new, sample_id)
            status_logger.log_Status_Log(ps_born, 'created', True)
            status_logger.log_Status_Log(ps_died, 'terminated', True)
            
            #iteration
            ps_old = ps_new
            sample_id += 1
            time.sleep(interval)
    except KeyboardInterrupt:
        print('Program terminated by user.')
        
        