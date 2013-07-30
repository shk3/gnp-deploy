import mysql.connector, os, sys
from IPy import IP
MYSQL_USER = 'scanner_admin'
MYSQL_PSWD = 'vVshFqqhJpHcJT5F'
MYSQL_DBNAME = 'cdnlab'

if len(sys.argv) <= 1:
    remote_host = input("Host: ")
else:
    remote_host = sys.argv[1]

conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                               host=remote_host, database=MYSQL_DBNAME)
select = ("SELECT `ip`, `min_roundtrip`, `trails` FROM `roundtrip` "
         "WHERE `done`=1 AND `online`=1")
cursor = conn.cursor()
updater = conn.cursor()
cursor.execute(select)
while True:
    flag = False
    for row in cursor.fetchmany(20):
        flag = True
        ip = IP(row[0]).strNormal()
        print('%s\t%7.3f\t%3d'%(ip, row[1], row[2]))
    if not flag:
        break
    os.system('pause')
cursor.close()
conn.commit()
conn.close()