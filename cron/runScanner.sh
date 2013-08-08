#!/bin/bash
. ~/.bash_profile
cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/obtain_ipaddr.py 25 30 30 1 &
# cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/nslookup_daemon.py 1 10 &