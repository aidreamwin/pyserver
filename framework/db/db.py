# -*- coding: utf-8 -*-
import time
import sqlite3

from mlog.log import mlog

class MyDBConnect(object):
	def __init__(self):
		super(MyDBConnect, self).__init__()
		self._conn = None
		self._c = None
		self._isConnect = False

	def commit(self):
		try:
			tmp = self._conn.commit()
		except Exception as e:
			raise e
		mlog.debug("commit sql success[{}].".format(tmp))

	def execute(self,sql):
		try:
			tmp = self._c.execute(sql)
		except Exception as e:
			mlog.error("execute error[{}]".format(e))
			return None
		mlog.debug("execute sql[{}] success.".format(sql))
		return tmp

	def rollback(self):
		self._conn.rollback()

	def close(self):
		self._conn.close()

	def status(self):
		return self._isConnect

	def reconnect(self):
		for _ in range(3):
			self.connect()
			if self._isConnect:
				mlog.debug("reconnect success.")
				break
			mlog.error("reconnect failed,sleep...")
			time.sleep(5)

	def connect(self):
		pass

class SqliteDB(MyDBConnect):
	def __init__(self, path_db):
		super(SqliteDB, self).__init__()
		self._path_db = path_db
		self.connect()
		
	def connect(self):
		try:
			self._conn = sqlite3.connect(self._path_db)
			self._c = self._conn.cursor()
		except Exception as e:
			self._isConnect = False
			mlog.error("connect sqlite failed[{}].".format(e))

		self._isConnect = True
		
		if self._isConnect:
			mlog.debug("connect sqlite success.")
		


def test():
	db = SqliteDB("test.db")
	# sql = "CREATE TABLE joke (id INT PRIMARY KEY NOT NULL,content TEXT NOT NULL);"
	# for x in range(10):
	# 	sql = "insert into joke (id,content) values (%d,'hello_%d')" % (x,x)
	# 	db.execute(sql)
	# db.commit()
	sql = "select * from joke;"
	result = db.execute(sql)
	for row in result:
		mlog.debug(row)
	db.close()

if __name__ == '__main__':
	test()
			



	
		
