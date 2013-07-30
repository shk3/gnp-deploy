from __future__ import print_function
try:
    input = raw_input
except:
    pass
    
import mysql.connector, os
MYSQL_USER = 'cdnlab_scanner'
MYSQL_PSWD = 'GVL3X94Q5nD29RBh'
MYSQL_DBNAME = 'cdnlab'
conn = mysql.connector.connect(user=MYSQL_USER, password=MYSQL_PSWD,
                               host='localhost', database=MYSQL_DBNAME)
select = ("SELECT `ip`, `min_roundtrip`, `trails` FROM `roundtrip` "
         "WHERE `done`=1 AND `online`=1")
cursor = conn.cursor()
updater = conn.cursor()
cursor.execute(select)
while True:
    flag = False
    for row in cursor.fetchmany(20):
        flag = True
        ip = row[0]
        print('%s\t%4d\t%3d'%(ip, row[1], row[2]))
    if not flag:
        break
    os.system('pause')
cursor.close()
conn.commit()
conn.close()