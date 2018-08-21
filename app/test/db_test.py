# -*- coding: utf-8 -*-

import sys,time
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
sys.path.append('../../framework')

from mlog.log import mlog
from db.db import MysqlConnPool

def main():
	dbPool = MysqlConnPool(host='127.0.0.1',user='root',passwd='dyb.123',db='mydata')
	dbcon = dbPool.Acquire()
	sql = "select content from joke where id=6"
	row = dbcon.query(sql)
	for x in row:
		mlog.debug(x[0])
	dbPool.Release(dbcon)

if __name__ == '__main__':
	main()