import csv
import datetime
import pmon_logging


def manual_sample(time1, time2):
    #order times
    if time1 > time2:
        tmp = time1
        time1 = time2
        time2 = tmp
    # get sample id for each event
    # note that when time is below range we take the first id
    # and when it exceeds range we take the last id
    s_id1 = pmon_logging.get_sid_by_time(time1)
    s_id2 = pmon_logging.get_sid_by_time(time2)
    if s_id1 == -1 or s_id2 == -1:
        print('You have not logged anything yet, please run in automatic mode')
        return
    # get samples matching our sample ids and find differences
    ps_new = pmon_logging.get_processes_by_sid(s_id1)
    ps_old = pmon_logging.get_processes_by_sid(s_id2)
    
    ps_born = [i for i in ps_old + ps_new if i in ps_new and i not in ps_old]
    ps_died = [i for i in ps_old + ps_new if i in ps_old and i not in ps_new]
    for process in ps_born:
        print(str(process[0]) +" "+  str(process[1]) + " created")
    for process in ps_died:
        print(str(process[0]) +" "+  str(process[1]) + " terminated")
