from __future__ import print_function
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
import os, sys, subprocess, time, platform, logging, traceback, socket, errno
import mysql.connector

# python fetch_cdn.py [num_threads=1] [autosave=10]
    

TERMINATE_MINUTES = 55
AUTOSAVE_INTERVAL = 10
MYSQL_USER = 'cdnlab_scanner'
MYSQL_PSWD = 'GVL3X94Q5nD29RBh'
MYSQL_DBNAME = 'cdnlab'
num_threads = 1
LOGGING_FORMAT = '[%(asctime)-15s]%(levelname)s: %(message)s'
if len(sys.argv) > 1:
    num_threads = int(sys.argv[1])
    if len(sys.argv) > 2:
        AUTOSAVE_INTERVAL = int(sys.argv[2])

try:
    if platform.system() == 'Windows':
        logging.basicConfig(filename='nslookup_%s.log'%socket.gethostname(), level=logging.WARNING, format=LOGGING_FORMAT)
    else:
        logging.basicConfig(filename='/home/cdnlab-gnp/gnp-logs/nslookup_%s.log'%socket.gethostname(), level=logging.WARNING, format=LOGGING_FORMAT)
except:
    pass
terminate_time = datetime.now() + timedelta(minutes=TERMINATE_MINUTES)
cur_hour = datetime.now().hour

queue = Queue()
dom_count = 0
buf_lst = []

select = ("SELECT `id`, `domain`, `carrier` FROM `cdn_tasks` "
         "WHERE `done`=0 AND `hour`=%s "
         "LIMIT 1000")
update = ("UPDATE `cdn_tasks` SET `done`=%s "
          "WHERE `id`=%s")
insert = ("INSERT IGNORE INTO `cdn_ips` "
          "SET `ip`=inet_aton(%s), `carrier`=%s, `timestamp`=%s")

def runCheck(i, host):
    host = str(host)
    
    try:
        result = socket.gethostbyname_ex(host)
    except (socket.gaierror, herror) as e:
        logging.warning('[%2d] An error occurs when handling the runCheck: %s' % (i, str(e)))
        return []
        # Issues: Some possible errors can be prevented.
        # Possible: socket.gaierror: [Errno 11004] getaddrinfo failed
        # socket.gaierror: [Errno -3] Temporary failure in name resolution
    for item in result[2]:   
        logging.debug('[%2d] %s: %s'%(i, host, item))
    return result[2]
def nslookup(i, q):
    global dom_count, flag
    logging.debug('[%2d] Thread is started.'%(i))
    while True:
        (domain, row_id, carrier) = q.get()
        try:
            ips = runCheck(i, domain)
            dom_count = dom_count + 1
            
            # print(ips)
            buf_lst.append((1, row_id, ips, carrier, datetime.now()))
            if dom_count % AUTOSAVE_INTERVAL == 0:
                saveResult()
                logging.debug('[%2d] Autosaved at %d'%(i, dom_count))
            q.task_done()
        except:
            q.task_done()
            logging.critical('[%2d] The job %d is terminated with an exception.'%(i, row_id), exc_info=True)
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
        for ip in row[2]:
            updater.execute(insert, (ip, row[3], row[4]))
        updater.execute(update, row[0 : 2])
    conn.commit()
    conn.close()
    
started = False
#Push all tasks
try:
    while True:
        logging.debug('Add tasks')
        conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                                       host='localhost', database=MYSQL_DBNAME,
                                       autocommit=True)
        cursor = conn.cursor()
        cursor.execute(select, (cur_hour,))
        flag = True
        for row in cursor:
            flag = False
            queue.put((row[1], row[0], row[2]))
        #Start workers
        if not started:
            for i in range(num_threads): 
                worker = Thread(target=nslookup, args=(i, queue)) 
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
except:
    logging.critical('The process is terminated with an exception.', exc_info=True)
    try:
        saveResult()
        logging.info('Results are saved.')
    except:
        pass
    raise sys.exc_info()[1]