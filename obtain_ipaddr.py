#!/usr/bin/env python
#http://blog.chinaunix.net/uid-21926461-id-3577291.html
#http://lihuipeng.blog.51cto.com/3064864/924890
# python 2/3 compatibility imports
from __future__ import print_function
# from __future__ import unicode_literals
# we alias the raw_input function for python 3 compatibility
try:
    input = raw_input
except:
    pass
    
from threading import Thread
try:
    from queue import Queue
except ImportError:
    from Queue import Queue
from datetime import datetime, timedelta
import os,sys,re,csv, subprocess, time, platform, logging, traceback, socket
import mysql.connector

TERMINATE_MINUTES = 58
AUTOSAVE_INTERVAL = 30
MYSQL_USER = 'cdnlab_scanner'
MYSQL_PSWD = 'GVL3X94Q5nD29RBh'
MYSQL_DBNAME = 'cdnlab'
num_threads = 30
LOGGING_FORMAT = '[%(asctime)-15s]%(levelname)s: %(message)s'
if len(sys.argv) <= 1:
    trails = 25
else:
    trails = int(sys.argv[1])
    if len(sys.argv) > 2:
        num_threads = int(sys.argv[2])
        if len(sys.argv) > 3:
            AUTOSAVE_INTERVAL = int(sys.argv[3])

try:
    if platform.system() == 'Windows':
        logging.basicConfig(filename='scanner_%s.log'%socket.gethostname(), level=logging.WARNING, format=LOGGING_FORMAT)
    else:
        logging.basicConfig(filename='/home/cdnlab-gnp/gnp-logs/scanner_%s.log'%socket.gethostname(), level=logging.WARNING, format=LOGGING_FORMAT)
except:
    pass
terminate_time = datetime.now() + timedelta(minutes=TERMINATE_MINUTES)
cur_hour = datetime.now().hour>>1<<1

queue = Queue()
regex = re.compile("time(=|<)([\d\.]*)", re.IGNORECASE | re.MULTILINE)
ip_count = 0
buf_lst = []

select = ("SELECT `id`, `ip` FROM `roundtrip` "
         "WHERE `done`=0 AND `hour`=%s "
         "LIMIT 1000")
update = ("UPDATE `roundtrip` SET `done`=%s, `online`=%s, "
            "`min_roundtrip`=%s, `trails`=%s, `last_change`=%s, `hour`=%s "
          "WHERE `id`=%s AND `hour`=%s")

if platform.system() == 'Windows':
    __ping_count = '-n'
else:
    __ping_count = '-c'

def runCheck(i, host):
    host = str(host)
    shortest_time = -1
    ping_trails = 0
    # Check if the host is alive
    p = subprocess.Popen(['ping', __ping_count, '3', host],
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = False)
    out = p.stdout.read().decode('utf8')
    if len(regex.findall(out)) > 0:
        for match in regex.findall(out):
            ping_trails = ping_trails + 1
            if shortest_time == -1 or shortest_time > float(match[1]):
                shortest_time = float(match[1])
                if match[0] == '<':
                    shortest_time = 0
    else:
        # print('[%2d] %s: Offline'%(i, host))
        return None
    # Measure
    p = subprocess.Popen(['ping', __ping_count, str(trails - 3), host],
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = False)
    out = p.stdout.read().decode('utf8')
    if len(regex.findall(out)) > 0:
        for match in regex.findall(out):
            ping_trails = ping_trails + 1
            if shortest_time == -1 or shortest_time > float(match[1]):
                shortest_time = float(match[1])
                if match[0] == '<':
                    shortest_time = 0
    # print('[%2d] %s: Reachable (%f ms)'%(i, host, shortest_time))
    logging.debug('[%2d] %s: Reachable (%f ms)'%(i, host, shortest_time))
    return [host, shortest_time, ping_trails]
def scanner(i, q):
    global ip_count, flag
    # print('[%2d] Thread is started.'%(i))
    logging.debug('[%2d] Thread is started.'%(i))
    while True:
        (ip, row_id) = q.get()
        try:
            # print('[%2d] get %s'%(i, ip))
            ret = runCheck(i, ip)
            ip_count = ip_count + 1
            
            online = 0
            min_roundtrip = -1
            ping_trails = 0
            
            if ret is not None:
                online = 1
                min_roundtrip, ping_trails = ret[1:]
            buf_lst.append((1, online, min_roundtrip, ping_trails, datetime.now(), 
                    cur_hour, row_id, cur_hour))
            if ip_count % AUTOSAVE_INTERVAL == 0:
                saveResult()
                # print('[%2d] Autosaved at %d'%(i, ip_count))
                logging.debug('[%2d] Autosaved at %d'%(i, ip_count))
            q.task_done()
        except:
            q.task_done()
            logging.critical('The process is terminated with an exception.', exc_info=True)
            flag = True
        if terminate_time < datetime.now():
            logging.info('Time limitation exceed. ')
            clearQueue(q)
def clearQueue(q):
    logging.debug('Start to clear the queue...')
    while not q.empty():
        q.get()
        q.task_done()
def saveResult():
    logging.debug('Start to save the result...')
    global buf_lst
    conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                                   host='localhost', database=MYSQL_DBNAME,
                                   autocommit=True)
    updater = conn.cursor()
    save_lst = buf_lst
    buf_lst = []
    for row in save_lst:
        updater.execute(update, row)
    conn.commit()
    conn.close()
    
started = False
#Push all tasks
try:
    # print('Scanner is started at %s.' % 
            # (datetime.now().strftime('%m/%d/%y %H:%M:%S')))
    while True:
        # print('Add tasks')
        logging.debug('Add tasks')
        conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                                       host='localhost', database=MYSQL_DBNAME,
                                       autocommit=True)
        cursor = conn.cursor()
        cursor.execute(select, (cur_hour,))
        flag = True
        for row in cursor:
            flag = False
            queue.put((row[1], row[0]))
        #Start workers
        if not started:
            for i in range(num_threads): 
                worker = Thread(target=scanner, args=(i, queue)) 
                worker.setDaemon(True) 
                worker.start() 
                time.sleep(0.1)
            started = True
        queue.join()
        saveResult()
        cursor.close()
        conn.commit()
        conn.close()
        if flag:
            break
        if terminate_time < datetime.now():
            break
    logging.info('The process is done normally.')
    # print('Scanner is done normally.')
except:
    logging.critical('The process is terminated with an exception.', exc_info=True)
    try:
        saveResult()
        logging.info('Results are saved.')
    except:
        pass
    raise sys.exc_info()[1]