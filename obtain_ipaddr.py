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
import os,sys,re,csv, subprocess, time, platform, logging
import mysql.connector


AUTOSAVE_INTERVAL = 30
MYSQL_USER = 'cdnlab_scanner'
MYSQL_PSWD = 'GVL3X94Q5nD29RBh'
MYSQL_DBNAME = 'cdnlab'
num_threads = 30
if len(sys.argv) <= 1:
    trails = 25
else:
    trails = int(sys.argv[1])
    if len(sys.argv) > 2:
        num_threads = int(sys.argv[2])
        if len(sys.argv) > 3:
            AUTOSAVE_INTERVAL = int(sys.argv[3])

logging.basicConfig(filename='/root/cdnlab-gnp/scanner.log', level='DEBUG')

queue = Queue()
regex = re.compile("time(=|<)(\d*)", re.IGNORECASE | re.MULTILINE)
ip_count = 0
buf_lst = []

select = ("SELECT `id`, `ip` FROM `roundtrip` "
         "WHERE `done`=0 "
         "LIMIT 1000")
update = ("UPDATE `roundtrip` SET `done`=%s, `online`=%s, "
            "`min_roundtrip`=%s, `trails`=%s "
          "WHERE `id`=%s")

if platform.system() == 'Windows':
    __ping_count = '-n'
else:
    __ping_count = '-c'

def runCheck(i, host):
    host = str(host)
    shortest_time = -1
    ping_trails = 0
    # Check if the host is alive
    p = subprocess.Popen(['ping', __ping_count, '1', host],
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = False)
    out = p.stdout.read().decode('utf8')
    if len(regex.findall(out)) > 0:
        for match in regex.findall(out):
            ping_trails = ping_trails + 1
            if shortest_time == -1 or shortest_time > int(match[1]):
                shortest_time = int(match[1])
                if match[0] == '<':
                    shortest_time = shortest_time - 1
    else:
        print('[%2d] %s: Offline'%(i, host))
        return None
    # Measure
    p = subprocess.Popen(['ping', __ping_count, str(trails - 1), host],
                        stdin = subprocess.PIPE,
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE,
                        shell = False)
    out = p.stdout.read().decode('utf8')
    if len(regex.findall(out)) > 0:
        for match in regex.findall(out):
            ping_trails = ping_trails + 1
            if shortest_time == -1 or shortest_time > int(match[1]):
                shortest_time = int(match[1])
                if match[0] == '<':
                    shortest_time = shortest_time - 1
    print('[%2d] %s: Reachable (%d ms)'%(i, host, shortest_time))
    logging.info('[%2d] %s: Reachable (%d ms)'%(i, host, shortest_time))
    return [host, shortest_time, ping_trails]
def scanner(i, q):
    global ip_count
    print('[%2d] Thread is started.'%(i))
    logging.info('[%2d] Thread is started.'%(i))
    while True:
        (ip, row_id) = q.get()
        # print('[%2d] get %s'%(i, ip))
        ret = runCheck(i, ip)
        ip_count = ip_count + 1
        
        online = 0
        min_roundtrip = -1
        ping_trails = 0
        
        if ret is not None:
            online = 1
            min_roundtrip, ping_trails = ret[1:]
        buf_lst.append((1, online, min_roundtrip, ping_trails, row_id))
        if ip_count % AUTOSAVE_INTERVAL == 0:
            saveResult()
            print('[%2d] Autosaved at %d'%(i, ip_count))
            logging.info('[%2d] Autosaved at %d'%(i, ip_count))
        q.task_done()
def saveResult():
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
while True:
    print('Add tasks')
    logging.info('Add tasks')
    conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                                   host='localhost', database=MYSQL_DBNAME,
                                   autocommit=True)
    cursor = conn.cursor()
    cursor.execute(select)
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
