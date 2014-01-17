#!/bin/bash
mysql -u root -pcdnlab << EOF
	use cdnlab;
	select * from roundtrip into outfile 'mydata.csv' fields terminated by ',' optionally enclosed by '"' lines terminated by '\r\n';
EOF

tmpName=hostname
mkdir /root/newdata
mv /var/lib/mysql/cdnlab/mydata.csv /root/newdata/mydata_$tmpName.csv

lftp -u root,Iheji2013 sftp://115.28.165.235 <<EOF
	lcd /root/newdata
	put *
EOF


