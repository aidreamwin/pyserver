# -*- coding: utf-8 -*-

import sys,os,time
sys.path.append('../../framework')

from mlog.log import mlog

from wxpy import *
import threading
import Queue

from joke import JokeInfo
from dbinfo import DBServer

def dealmsg(friend,q_msg):
	try:
		while True:
			msg = q_msg.get()
			if msg!=None:
				mlog.info("send msg:%s" % (msg))
				friend.send(msg)
	except Exception as e:
		mlog.error(e)
		raise e

def heart(q_msg):
	while True:
		strTime = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
		q_msg.put("TIME[%s]" % strTime)
		time.sleep(60*30)


def main():
	bot = Bot(console_qr=True, cache_path=True)
	time.sleep(3)
	# bot.enable_puid()
	fs = bot.friends(update=True)
	friends = fs
	# admin = friends.search(u'那棵树看起来生',sex=MALE,city="成都")
	admin = friends.search(u'那棵树看起来生')
	if len(admin)<=0:
		mlog.error(admin)
		return
	
	q_sql = Queue.Queue()
	q_msg = Queue.Queue()
	
	# joke
	joke = JokeInfo(q_sql)
	tjoke = threading.Thread(target=joke.run)
	tjoke.start()

	tp = threading.Thread(target=dealmsg,args=(admin[0],q_msg,))
	tp.start()

	th = threading.Thread(target=heart,args=(q_msg,))
	th.start()

	# db
	dbs = DBServer("db/joke.db",q_sql,q_msg)
	dbs.run()
	
		
if __name__ == '__main__':
	pid = os.getpid()
	try:
		main()
	except Exception as e:
		mlog.error(e)
		time.sleep(2)
		os.system("kill -9 {}".format(pid))


