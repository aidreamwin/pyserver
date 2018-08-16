# -*- coding: utf-8 -*-

import random,time

class JokeInfo(object):
	def __init__(self, query_queue):
		super(JokeInfo, self).__init__()
		self.query = query_queue
		self.sql = "select id,content from joke where id=%d"
		# self.sql = "select id,content from joke LIMIT 1;"

	def run(self):
		while True:
			sql_dict = {}
			_id = random.randint(0, 50)
			sql = self.sql % _id
			sql_dict["joke"] = sql
			self.query.put(sql_dict)
			time.sleep(60)
			

		