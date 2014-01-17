#!/bin/bash
rm -rf gnp-deploy
tac /etc/crontab | sed 1,3d |tac > /root/testcrontab
unalias cp
unalias rm
cp testcrontab /etc/crontab
rm /root/starttime.conf
echo "-1" > /root/timeflag.conf

echo "second run 3" >> /root/setup.log

#check out the src from svn
svn checkout http://gnp-deploy.googlecode.com/svn/trunk/ /root/gnp-deploy --non-interactive -q

chmod -R u+x /root/gnp-deploy/cron

echo "*/30 * * * * root /root/gnp-deploy/cron/updateGNP.sh" >> /etc/crontab
echo "*/10 * * * * root /root/gnp-deploy/cron/countExec.sh" >> /etc/crontab
echo "50 16 17 1 * root /root/gnp-deploy/cron/startCount.sh" >> /etc/crontab

yum -y install lftp


echo "second time all finished" >> /root/setup.log
