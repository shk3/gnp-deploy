#!/bin/bash
mysql -u root -pcdnlab << EOF
	use cdnlab;
	select * from roundtrip into outfile '/root/mydata.csv' fields terminated by ',' optionally enclosed by '"' lines terminated by '\r\n';
EOF

tmpName=hostname
mv /root/mydata.csv /root/mydata_$tmpName.csv

lftp -u root,Iheji2013 sftp://115.28.165.235 <<EOF
	put /root/mydata_$tmpName.csv
EOF


