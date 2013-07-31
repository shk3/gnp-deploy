#!/bin/bash
. ~/.bash_profile
cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/obtain_ipaddr.py 100 30 10 &
