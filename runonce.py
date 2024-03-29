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
VER = 15

LOGGING_FORMAT = '[%(asctime)-15s] %(message)s'

try:
    logging.basicConfig(filename='/root/gnp-logs/runonce_%s.log'%socket.gethostname(), level=logging.INFO, format=LOGGING_FORMAT) 
except:
    pass
try:
    rhdl = open('/root/runonce.lock', 'r') 
    cur_ver = int(rhdl.read().strip())
    if cur_ver >= VER:
        exit(0)
    print('Runonce script ver %d start...' % VER)
    logging.info('Run at version %d.' % VER)
        
    # Backup database
    #if os.system('/usr/bin/mysqldump -u root -pcdnlab cdnlab | /bin/gzip > /root/export-cdn.sql.gz') != 0:
    if os.system('/usr/bin/mysqldump -u root -paQcy7j2CSHYhDB8E cdnlab | /bin/gzip > /root/export-cdn.sql.gz') != 0:
        logging.critical('Backup database failed...')
        exit(0)
    # Import data
    if os.system('gunzip <  /root/gnp-deploy/roundtrip.sql.gz | /usr/bin/mysql -u root -paQcy7j2CSHYhDB8E cdnlab') != 0:
    #if os.system('gunzip < /root/gnp-deploy/roundtrip.sql.gz | /usr/bin/mysql -u root -pcdnlab cdnlab') != 0:
        logging.critical('Import database failed...')
        exit(0)

    # # Clear log file
    # os.system('rm -f /home/cdnlab-gnp/gnp-logs/*.log')

    whdl = open('/root/runonce.lock', 'w')
    print(VER, file=whdl)
    whdl.close()
    logging.info('Lock of version %d is saved.' % VER)
    print('Runonce script is terminated normally.')
    # # Kill all processes of `cdnlab-gnp`
    # os.system('pkill -ucdnlab-gnp')

except SystemExit:
    exit(0)
except:
    logging.exception(''.join(traceback.format_exception(*sys.exc_info())))
    pass
