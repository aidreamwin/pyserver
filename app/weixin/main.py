# -*- coding: utf-8 -*-

import sys,os,time
sys.path.append('../../framework')

from mlog.log import mlog

from wxpy import *
import threading
import Queue

from joke import JokeInfo
from dbinfo import DBServer

def main():
	# bot = Bot(console_qr=True, cache_path=True)
	# time.sleep(3)
	# bot.enable_puid()
	# fs = bot.friends(update=True)
	# friends = fs
	# admin = friends.search(u'那棵树看起来生',sex=MALE,city="成都")
	# if len(admin)<=0:
	# 	mlog.error(admin)
	# 	return
	
	q_sql = Queue.Queue()
	q_msg = Queue.Queue()
	
	# joke
	joke = JokeInfo(q_sql)
	tjoke = threading.Thread(target=joke.run)
	tjoke.start()

	def printInfo(q_msg):
		try:
			while True:
				msg = q_msg.get()
				if msg!=None:
					# admin.send_msg(msg)
					mlog.debug("send msg:{}".format(msg))
		except Exception as e:
			mlog.error(e)
			dbs.db.close()
			raise e
	tp = threading.Thread(target=printInfo,args=(q_msg,))
	tp.start()

	# db
	dbs = DBServer("db/joke.db",q_sql,q_msg)
	dbs.run()
	


		
if __name__ == '__main__':
	pid = os.getpid()
	try:
		main()
	except Exception as e:
		mlog.error(e)
		os.system("kill -9 {}".format(pid))


