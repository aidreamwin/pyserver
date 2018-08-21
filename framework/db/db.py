# -*- coding: utf-8 -*-
import time
import sqlite3
import pymysql
import threading

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

class MysqlDB(MyDBConnect):
	def __init__(self, conn):
		super(MysqlDB, self).__init__()
		self._conn = conn
		self._c = conn.cursor()
		self._isConnect = True

	def query(self,sql):
		try:
			self._c.execute(sql)
		except Exception as e:
			mlog.error("query error[{}]".format(e))
			return None
		mlog.debug("query sql[{}] success.".format(sql))
		return self._c.fetchall()
		

# 连接池
class MysqlConnPool(object):
	def __init__(self,host,user,passwd,db,port=3306,charset='utf8',poolSize=1):
		super(MysqlConnPool, self).__init__()
		self.conns = []
		self.poolSize = poolSize
		self.mutex = threading.Lock()
		self.currentSize = 0
		self.host = host
		self.user = user
		self.passwd = passwd
		self.db = db
		self.port = port
		self.charset = charset
		self.init()

	def init(self):
		for x in range(self.poolSize):
			conn = pymysql.connect(host=self.host, port=self.port, user=self.user, \
			passwd=self.passwd, db=self.db, charset=self.charset)
			dbcon = MysqlDB(conn)
			self.conns.append(dbcon)
		mlog.debug("init db pool[%d] success." % self.poolSize)
	# 获取连接
	def Acquire(self):
		self.mutex.acquire()
		try:
			if len(self.conns) > 0:
				mlog.info("从池中获取连接,当前连接池数量:%d", len(self.conns))
				dbcon = self.conns[0]
				self.conns = self.conns[1:]
				return dbcon

			mlog.info("创建新连接,当前连接池数量0")
			self.currentSize+=1
			conn = pymysql.connect(host=self.host, port=self.port, user=self.user, \
			passwd=self.passwd, db=self.db, charset=self.charset)

			dbcon = MysqlDB(conn)
			return dbcon

		except Exception as e:
			raise e
		finally:
			self.mutex.release()

	# 释放连接
	def Release(self,dbcon):
		self.mutex.acquire()
		try:
			if self.currentSize >= self.poolSize:
				self.currentSize-=1
				dbcon.close()
				mlog.info("关闭连接,当前连接池数量:%d", len(self.conns))
			else:
				self.conns.append(dbcon)
				mlog.info("释放连接,当前连接池数量:%d", len(self.conns))
		except Exception as e:
			raise e	
		finally:
			self.mutex.release()


		
