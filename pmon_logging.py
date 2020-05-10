import csv
import datetime
import sys
import logging
import os
import stat
from pmon_settings import *

class pmon_logger:

    def __init__(self, name, log_file, level=logging.INFO):
        formatter = logging.Formatter('%(asctime)s'+log_delim+'%(message)s')
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)   

        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.addHandler(handler)
    
    # logs sample to serviceList
    def log_serviceList(self,processes, sample_id):
        for process in processes:
            self.logger.info(str(process[0]) +log_delim+ str(process[1])+log_delim+str(sample_id))
    
    # logs changes to statusLog
    def log_Status_Log(self, processes, what, ask_print):
        for process in processes:
            if  ask_print == True:
                print(str(process[0]) +" "+  str(process[1])+" "+ what)
            self.logger.info(str(process[0]) +log_delim+  str(process[1])+log_delim + what)




def get_log_time_date(dt):
    #2020-05-08 16:32:50,506 1 init 0
    return datetime.datetime.strptime(dt[:-4], '%Y-%m-%d %H:%M:%S')

def get_user_time_date(dt):
    #2020-05-08 16:32:50,506 1 init 0
    try:
        dtobj = datetime.datetime.strptime(dt, '%Y-%m-%d %H:%M:%S')
        return dtobj
    except ValueError:
        print("Bad time input format, exiting.")
        sys.exit(1)

# tnd is a dimedate object
def get_sid_by_time(tnd):
    sid = -1
    try:
        csv_file = open('serviceList.txt', 'r')
        csv_reader = csv.reader(csv_file, delimiter=log_delim)
        row = ""
        for row in csv_reader:
            rowtime = get_log_time_date(row[0])
            if tnd < rowtime and sid == -1:
                sid = row[3]
        # sid will be -1 if the time we got is greater than any available
        # note that row is now the last row
        if sid == -1 and row != "":
            sid = row[3]
        return sid
    except FileNotFoundError:
        return sid
# returns last sid, returns 0 if no log yet
def get_last_sid():
    sid = 0
    try:
        csv_file = open('serviceList.txt', 'r')
        csv_reader = csv.reader(csv_file, delimiter=log_delim)
        row = ""
        for row in csv_reader:
            pass
        if row != "":
            sid = row[3]
        return sid
    except FileNotFoundError:
        return sid

def get_processes_by_sid(sid):
    # must be string for comparison to work
    sid = str(sid)
    try:
        processes = []
        csv_file = open('serviceList.txt', 'r')
        csv_reader = csv.reader(csv_file, delimiter=log_delim)
        for row in csv_reader:
            if row[3] == sid:
                processes.append([row[1], row[2]])
        return processes
    except FileNotFoundError:
        return []

    