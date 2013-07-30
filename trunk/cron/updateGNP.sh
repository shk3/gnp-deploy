svn checkout http://gnp-deploy.googlecode.com/svn/trunk/ /home/cdnlab-gnp/gnp-deploy --non-interactive
cd /home/cdnlab-gnp/gnp-logs && svn add *.log --non-interactive -q && svn ci *.log -m "auto upload" --username shk3@monkeyhouse.info --password pu8bq7qu5hB4 --non-interactive -q
cd /home/cdnlab-gnp/gnp-logs && svn add *.lock --non-interactive -q && svn ci *.lock -m "auto upload" --username shk3@monkeyhouse.info --password pu8bq7qu5hB4 --non-interactive -q
cd /home/cdnlab-gnp && python /home/cdnlab-gnp/gnp-deploy/runonce.py