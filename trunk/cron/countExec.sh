#!/bin/bash
#echo "test2 next_start" >> /home/shane/project/a.txt
#echo $(pwd) >> /home/shane/project/a.txt
read flag < /root/timeflag.conf
if [ $flag -ne "-1" ]; then
	if [ $[ $flag%2 ] -eq '0' ]; then
		echo $[ $flag%2 ]		
		echo "python"
		cd /root/gnp-deploy/cron
		./startRunning.sh
	fi
	echo $flag
    echo $[ $flag+1 ] > /root/timeflag.conf
fi


