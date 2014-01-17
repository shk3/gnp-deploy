#!/bin/bash
#echo "test2 next_start" >> /home/shane/project/a.txt
#echo $(pwd) >> /home/shane/project/a.txt
read flag < /root/timeflag.conf
if [ $flag -ne "-1" ]; then
	cd /root/gnp-deploy/cron
	./runScanner.sh
	if [ $flag -gt "145" ]; then
		/root/gnp-deploy/cron/uploader.sh
	echo $[ $flag+1 ] > /root/timeflag.conf
fi


