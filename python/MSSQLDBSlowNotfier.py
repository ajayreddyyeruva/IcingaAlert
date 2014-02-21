#!/usr/bin/python
import pymssql
import timeit
import ConfigParser
import sys
from functools import wraps
import errno
import os
import signal
import time

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

config = ConfigParser.ConfigParser()
#Path of properties file
config.read('/usr/lib/nagios/libexec/db.properties')
conn = pymssql.connect(host=config.get('DEV','IP'),user=config.get('DEV','USER'),password=config.get('DEV','PASSWORD'),database=config.get('DEV','DATABASE'))
cursor = conn.cursor()

@timeout(2)
def executeSP():
	print("Executing SP")
#	time.sleep(2)
	cursor.callproc(config.get('DEV','SP_NAME'), (config.get('DEV','USER'),config.get('DEV','PASSWORD'),))
	for row in cursor:
		print row

try:
	executionTime=timeit.timeit("executeSP()", setup="from __main__ import executeSP",number=5)
except TimeoutError:
	executionTime=15
conn.close()
print executionTime
if executionTime < 5:
	sys.exit(0)
elif executionTime < 10:
	sys.exit(1)
else:
	sys.exit(2)
