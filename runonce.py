#!/usr/bin/env python
# python 2/3 compatibility imports
from __future__ import print_function
# from __future__ import unicode_literals
# we alias the raw_input function for python 3 compatibility
try:
    input = raw_input
except:
    pass
import os,sys,re,csv, subprocess, time, platform, logging, traceback, socket
VER = 0
LOGGING_FORMAT = '[%(asctime)-15s] %(message)s'

logging.basicConfig(filename='/home/cdnlab-gnp/gnp-logs/runonce_%s.log'%socket.gethostname(), level='DEBUG', format=LOGGING_FORMAT) 
try:
    rhdl = open('/home/cdnlab-gnp/gnp-logs/runonce_%s.lock'%socket.gethostname(), 'r') 
    cur_ver = int(rhdl.read().strip())
    if cur_ver >= VER:
        exit(0)
except SystemExit:
    exit(0)
except:
    logging.exception(''.join(traceback.format_exception(*sys.exc_info())))
    pass
os.system('/usr/bin/mysql -u root -paQcy7j2CSHYhDB8E cdnlab < /home/cdnlab-gnp/gnp-deploy/import-nodes.sql')

logging.info('Run at version %d.' % VER)
whdl = open('/home/cdnlab-gnp/gnp-logs/runonce_%s.lock'%socket.gethostname(), 'w')
print(VER, file=whdl)
whdl.close()
logging.info('Lock of version %d is saved.' % VER)