# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')

import Queue
import threading
import time
import event

from mlog.log import mlog

# 事件处理器信息
class EventHandlerInfo(object):
	def __init__(self):
		super(EventHandlerInfo, self).__init__()
		self.Handler = None # EventHandler
		self.Sort = 0



# 事件处理器组
class EventDispatcher(object):
	def __init__(self):
		super(EventDispatcher, self).__init__()
		self.innerHandlers = [] 	# []*EventHandlerInfo  # 处理器集合
		self.asyncEvents = Queue.Queue()   	# chan *AsyncEventInfo # 异步事件,Queue
		self.throttle  = 1     		# int                  # 并发数


	def Sort(self):
		_length = len(self.innerHandlers)
		for i in range(0,_length-1):
			for j in range(0,_length-i-1):
				ih = self.innerHandlers[i]
				jh = self.innerHandlers[j]
				if ih.Sort < jh.Sort:
					self.innerHandlers[i], self.innerHandlers[j] = self.innerHandlers[j], self.innerHandlers[i]
	

	# 添加事件处理器,可控制排序
	# h EventHandler, sortIndex int
	def AddHandler(self,h, sortIndex):
		if h == None:
			raise("处理器不能为空")

		hi = EventHandlerInfo()
		hi.Handler = h
		hi.Sort = sortIndex
		self.innerHandlers.append(hi)

		# 排序
		self.Sort()

	# 添加事件处理器
	def PushHandler(self,h):
		self.AddHandler(h, 0)

	# 遍历处理器
	 # func(int, EventHandler) bool
	def RangeSort(self,f):
		for v in self.innerHandlers:
			ret = f(v.Sort, v.Handler)
			if not ret:
				return

	# 遍历处理器
	# func(EventHandler) bool
	def Range(self,f):
		for v in self.innerHandlers:
			ret = f(v.Handler)

			if not ret:
				return

	# 同步触发事件
	# evt *Event,Return *EventRet
	def OnEvent(self,evt):
		ret = event.NewEventRet()
		try:
			for h in self.innerHandlers:
				goon = h.Handler.OnEvent(evt, ret)
				if not goon:
					break
		except Exception as e:
			mlog.error("触发同步事件{}发生错误{}".format( evt,e))
			raise e
		return ret

	# 异步触发事件
	# evt *Event, callback CallbackFun
	def OnAsyncEvent(self,evt,callback):
		asinfo = AsyncEventInfo()
		asinfo.Evt = evt
		asinfo.Callback = callback
		self.asyncEvents.put(asinfo)


# 异步事件信息
class AsyncEventInfo(object):
	def __init__(self):
		super(AsyncEventInfo, self).__init__()
		self.Evt = None      	# *Event
		self.Callback = None	# CallbackFun


# 创建事件处理器组
def NewEventDispatcher():
	evg = EventDispatcher()
	return evg

# 创建异步事件处理器组
def NewAsyncEventDispatcher(throttle):
	evg = EventDispatcher()
	evg.asyncEvents = Queue.Queue(10000)
	evg.throttle = throttle

	def AsyncEventRun(evg):

		try:
			while True:
				asinfo = evg.asyncEvents.get()
				if asinfo != None:
					ret = evg.OnEvent(asinfo.Evt)
					if asinfo.Callback != None:
						asinfo.Callback(asinfo.Evt, ret)
		except Exception as e:
			mlog.error("AsyncEventDispatcher failed,Info[{}]".format(e))
			raise e
	for i in range(0,throttle):
		# 开启处理异步事件线程
		_th = threading.Thread(target=AsyncEventRun, args=(evg,))
		_th.start()

	return evg