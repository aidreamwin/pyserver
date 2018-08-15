# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() != 'utf-8':
	reload(sys)
	sys.setdefaultencoding('utf-8')
import threading
import time

import eventhandler
import event
from mlog.log import mlog


EVTNAME_TIMERFUNC     = "timerfunc" # 事件名称
EVTArgsName_TimerFunc = "timerinfo" # 参数名称

TimerStatus_Stop = 0
TimerStatus_Run  = 1

TimerType_Timer  = 0
TimerType_Ticker = 1

# 延迟执行一次的函数
class TimerFunc(object):
	def __init__(self):
		super(TimerFunc, self).__init__()
		self.WaitSeconds = 0     		#int32     # 延迟时间
		self.Func = None             	#func()    # 处理函数
		self.Status = TimerStatus_Run	#int       # 状态
		self.Loop = False             	#bool      # 是否循环执行
		self.Name = ""             		#string    # 名称
		self.BeginTime = time.time()	#time.Time # 开始时间
		self.TimerType =0       		#int       # timer类型

	# 执行延迟函数
	def Exec(self):
		try:
			if self.Status == TimerStatus_Run:
				self.Func()
		except Exception as e:
			mlog.error("Exec failed,Info[{}]".format(e))
			raise e
		
	# 消耗的秒数
	def ElapsedSeconds(self):
		return int32(time.Now() - (self.BeginTime).Seconds())

	def Stop(self):
		self.Status = TimerStatus_Stop

	def IsStop(self):
		return self.Status == TimerStatus_Stop

# 延迟函数管理器
class TimerFuncManager(object):
	def __init__(self):
		super(TimerFuncManager, self).__init__()
		self.evtDispatcher = None 	#*EventDispatcher
		self.timerFuncs = {}    	#map[string]*TimerFunc

	def NewTimer(self,wait, f):
		return self.NewNamedTimer(wait, f, "")

	# 创建一个timer
	def NewNamedTimer(self,wait, f , timername):
		return self.NewNamedMilliSecTimer(wait, f, timername)

	def NewMilliSecTimer(self,wait, f):
		return self.NewNamedMilliSecTimer(wait, f, "")

	# 创建一个毫秒级的timer
	def NewNamedMilliSecTimer(self,wait, f , timername):
		tf = TimerFunc()
		tf.WaitSeconds = wait
		tf.Loop = False
		tf.Status = TimerStatus_Run
		tf.Func = f
		tf.Name = timername
		tf.BeginTime = time.time()
		tf.TimerType = TimerType_Timer

		def SleepPublishTimerFuncEvent(wait,tf):
			time.sleep(wait)
			self.publishTimerFuncEvent(tf)

		_th = threading.Thread(target=SleepPublishTimerFuncEvent, args=(wait,tf,))
		_th.start()

		if timername != "":
			self.timerFuncs[timername] = tf
			mlog.info("create timerfunc %s" % timername)

		return tf

	def NewTicker(self, wait, f):
		return self.NewNamedTicker(wait, f, "")

	# 创建一个 tick
	def NewNamedTicker(self,wait, f, timername):
		return self.NewNamedMilliSecTicker(wait, f, timername)

	def NewMilliSecTicker(self,wait,f):
		return self.NewNamedMilliSecTicker(wait, f, "")

	# 创建一个毫秒级的 tick
	def NewNamedMilliSecTicker(self,wait, f, timername):
		tf = TimerFunc()
		tf.WaitSeconds = wait
		tf.Loop = True
		tf.Status = TimerStatus_Run
		tf.Func = f
		tf.Name = timername
		tf.BeginTime = time.time()
		tf.TimerType = TimerType_Ticker

		def SleepPublishTimerFuncEvent(wait,tf):
			while True:
				time.sleep(wait)

				if tf.Status == TimerStatus_Stop:
					break
				self.publishTimerFuncEvent(tf)

		_th = threading.Thread(target=SleepPublishTimerFuncEvent, args=(wait,tf,))
		_th.start()

		if timername != "":
			self.timerFuncs[timername] = tf

		return tf

	# 获取延迟函数
	def GetTimerFunc(self,timername):
		tf = self.timerFuncs.get(timername)
		if tf == None:
			return None

		return tf

	# 移除timer
	def RemoveTimer(self,timername):
		tf = self.timerFuncs.get(timername)
		if tf == None:
			return None

		tf.Status = TimerStatus_Stop

		del self.timerFuncs[timername]

		return tf

	def publishTimerFuncEvent(self,tf):
		self.evtDispatcher.OnAsyncEvent(newTimerFuncEvent(tf),None)

	def registerTimeFuncEvtHandler(self):
		def _f(evt, evtret):
			tf = getTimerFuncEventArg(evt.Args)
			try:
				tf.Exec()
			except Exception as e:
				mlog.error("registerTimeFuncEvtHandler failed,Info[{}]".format(e))
				raise e
			# 移除命名的timer
			if tf.TimerType == TimerType_Timer and tf.Name != "":
				self.RemoveTimer(tf.Name)
			return True

		h = eventhandler.NewCommonHandler("timerfunc", _f, EVTNAME_TIMERFUNC)

		self.evtDispatcher.PushHandler(h)

# 创建延迟函数管理器对象
def NewTimerFuncManager(evtDispatcher):
	tfm = TimerFuncManager()
	tfm.evtDispatcher = evtDispatcher
	
	tfm.registerTimeFuncEvtHandler()

	return tfm

# 创建延迟函数事件
def newTimerFuncEvent(tf):
	evt = event.Event(EVTNAME_TIMERFUNC,event.NewEventArgs())
	evt.Args[EVTArgsName_TimerFunc] = tf

	return evt

# 获取延迟函数事件参数
def getTimerFuncEventArg(evtArgs):
	return evtArgs[EVTArgsName_TimerFunc]
