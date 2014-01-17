#!/bin/bash
mysql -u root -paQcy7j2CSHYhDB8E << EOF
	use cdnlab;
	select * from roundtrip into outfile 'mydata.csv' fields terminated by ',' optionally enclosed by '"' lines terminated by '\r\n';
EOF


mkdir /root/newdata
mv /var/lib/mysql/cdnlab/mydata.csv /root/newdata/mydata_$HOSTNAME.csv

lftp -u root,Iheji2013 sftp://115.28.165.235 <<EOF
	put /root/newdata/mydata_$HOSTNAME.csv
EOF


