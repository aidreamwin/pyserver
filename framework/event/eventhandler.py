# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')
# 事件处理器
class EventHandler(object):
	def __init__(self):
		super(EventHandler, self).__init__()
	# 同步触发事件
	def OnEvent(self,evt,ret):
		pass
	# 处理器名称
	def HandlerName(self):
		pass

# 空的事件处理器
class EmptyEventHandler(EventHandler):
	def __init__(self):
		super(EmptyEventHandler, self).__init__()

def OnEvent(self,evt, ret):
	return True

def HandlerName(self):
	return "EmptyEventHandler"

# 公用的事件处理器
class CommHandler(EventHandler):
	def __init__(self,name,f,evts):
		super(CommHandler, self).__init__()
		self.handerName = name 	#string
		self.handler = f    	#func(evt *Event, ret *EventRet) bool
		self.hookEvts = []
		self.hookEvts.append(evts)

	def OnEvent(self,evt, ret):
		for s in self.hookEvts:
			if s.lower() == evt.Name.lower():
				break
			return True

		return self.handler(evt, ret)

	def HandlerName(self):
		return h.handerName

def NewCommonHandler(name, f, evts):
	ch = CommHandler(name,f,evts)
	return ch
