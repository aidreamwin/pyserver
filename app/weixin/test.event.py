# -*- coding: utf-8 -*-

import sys,time
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
sys.path.append('../../framework')

from mlog.log import mlog
from event.timerfunc import NewTimerFuncManager
from event.eventdispatcher import NewAsyncEventDispatcher

from function import commands

def main():
	dispatcher = NewAsyncEventDispatcher(1)
	timer = NewTimerFuncManager(dispatcher)

	timerInfo = {}
	for fn in commands:
		if fn.loop:
			t = timer.NewNamedTicker(fn.time,fn.func,fn.name)
		else:
			t = timer.NewNamedTimer(fn.time,fn.func,fn.name)
		timerInfo[fn.name] = t
	while True:
		time.sleep(10)
		mlog.info("main loop...")
		pass

if __name__ == '__main__':
	main()