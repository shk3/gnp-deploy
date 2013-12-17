#!/bin/bash
cd /root
if [ ! -f "starttime.conf" ]; then 
	python /root/gnp-deploy/first.py 
fi
echo "runing Scanner...."
cd /root/gnp-deploy/cron
./runScanner.sh
echo "finish scanner"
