# -*- coding: utf-8 -*-
from db.db import SqliteDB

class DBServer(object):
	def __init__(self,db_path, queue,q_msg):
		super(DBServer, self).__init__()
		self.queue = queue
		self.db = SqliteDB(db_path)
		self.q_msg = q_msg

	def run(self):
		while True:
			sql_dict = self.queue.get()
			if sql_dict==None:
				continue
			for _type,_sql in sql_dict.items():
				result = self.db.execute(_sql)
				print(result)
				if _type=="joke":
					for raw in result:
						# print(raw)
						self.q_msg.put(raw[1])


		