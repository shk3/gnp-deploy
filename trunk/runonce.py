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
VER = 5
LOGGING_FORMAT = '[%(asctime)-15s] %(message)s'

try:
    logging.basicConfig(filename='/home/cdnlab-gnp/gnp-logs/runonce_%s.log'%socket.gethostname(), level='DEBUG', format=LOGGING_FORMAT) 
except:
    pass
try:
    rhdl = open('/home/cdnlab-gnp/runonce_%s.lock'%socket.gethostname(), 'r') 
    cur_ver = int(rhdl.read().strip())
    if cur_ver >= VER:
        exit(0)
except SystemExit:
    exit(0)
except:
    logging.exception(''.join(traceback.format_exception(*sys.exc_info())))
    pass
print('Runonce script ver %d start...' % VER)
    
# os.system('rm -fR /home/cdnlab-gnp/gnp-logs')
# if os.system('svn checkout https://gnp-deploy.googlecode.com/svn/branches/logs/%s /home/cdnlab-gnp/gnp-logs --username shk3@monkeyhouse.info --password pu8bq7qu5hB4'%socket.gethostname()) != 0:
    # exit(0)
os.system('/usr/bin/mysql -u root -paQcy7j2CSHYhDB8E cdnlab < /home/cdnlab-gnp/gnp-deploy/import-nodes.sql >> /home/cdnlab-gnp/gnp-logs/mysql_%s.log'%socket.gethostname())

logging.info('Run at version %d.' % VER)
whdl = open('/home/cdnlab-gnp/runonce_%s.lock'%socket.gethostname(), 'w')
print(VER, file=whdl)
whdl.close()
logging.info('Lock of version %d is saved.' % VER)
print('Runonce script is terminated normally.')
# os.system('pkill -ucdnlab-gnp')