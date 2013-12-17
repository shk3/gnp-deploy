svn checkout http://gnp-deploy.googlecode.com/svn/trunk/ /root/gnp-deploy --non-interactive -q
cd /root/gnp-logs && svn add *.log -q && svn ci *.log -m "auto upload" --username shk3@monkeyhouse.info --password pu8bq7qu5hB4 --non-interactive -q
chmod -R u+x /root/gnp-deploy/cron
cd /root && python /root/gnp-deploy/runonce.py