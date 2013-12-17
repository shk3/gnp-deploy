#!/bin/bash
#cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/obtain_ipaddr.py 25 30 30 2 &
# cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/nslookup_daemon.py 1 10 &
cd /root/gnp-deploy
python obtain_ipaddr.py 20 30 30 40
