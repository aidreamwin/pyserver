# 事件命令
class EventCmd(object):
	def __init__(self, evtdispatcher):
		super(EventCmd, self).__init__()
		self.evtdispatcher = evtdispatcher

	def Name(self):
		return "event"

	def Help(self):
		return "事件处理器.usage:event stat/event listhandler"

	# args []string
	def Exec(self,args):
		if len(args) == 0:
			return "error,seeref usage"

		evtname = args[0]

		if evtname =="stat":
			etype = "async"
			if self.evtdispatcher.asyncEvents == None:
				etype = "sync"

			return "hander:%d,type:%s" % (len(self.evtdispatcher.innerHandlers), etype)
		elif evtname == "listhandler":
			_str = ""
			for _, h in self.evtdispatcher.innerHandlers:
				_str += h.Handler.HandlerName()
				_str += ","

			return _str
		else:
			return "error,seeref usage."

# 创建事件命令对象
def NewEventCmd(evtdispatcher):
	cmd = EventCmd(evtdispatcher)
	return cmd