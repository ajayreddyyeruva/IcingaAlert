#!/usr/bin/python
import ConfigParser
import MySQLdb
import sys

config = ConfigParser.ConfigParser()
#Path of properties file
config.read('/data/mysql_db.properties')
conn = MySQLdb.connect(config.get('DEV','IP'),config.get('DEV','USER'),config.get('DEV','PASSWORD'),config.get('DEV','DATABASE'))
cursor = conn.cursor()

cursor.execute("select count(*) from information_schema.processlist")
data = cursor.fetchone()
openConnections=data[0]
if openConnections < 90:
    print "Connections are in acceptable limit"
    sys.exit(0)
elif openConnections < 95:
    print "Connections are in warning state"
    sys.exit(1)
else:
    print "Connections are in critical"
    sys.exit(2)