# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

import time

import json
import requests
from wxpy import *
import sqlite3
import random
from mlog.log import mlog

bot = Bot(console_qr=True, cache_path=True)
bot.enable_puid()

commands = []
class command(object):
	"""docstring for command"""
	def __init__(self,func,name,loop=False,time=3):
		super(command, self).__init__()
		self.time = time
		self.loop = loop
		self.func = func
		self.name = name

def test():
	conn = sqlite3.connect('db/joke.db')
	c = conn.cursor()

	for _ in range(2):
		_id = random.randint(0, 15)
		sql = "select content from joke where id=%d;" % _id
		mlog.debug("sql[{}]".format(sql))
		
		x = c.execute(sql)

		result = bot.friends().search(u'那棵树看起来生',sex=MALE,city="成都")
		my_friend = result[0]
		mlog.debug(my_friend.puid)

		for row in x:
		    mlog.debug(row)
		    my_friend.send_msg(row[0])
		time.sleep(3)
	    
	conn.close()

commands.append(command(test,"joke"))