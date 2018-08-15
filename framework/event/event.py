# -*- coding: utf-8 -*-

import sys
if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

# 事件结果
class EventRet(object):

	SINGLERESULTKEYMAME = "result"
	SINGLEARGSKEYNAME   = "arg"

	def __init__(self):
		super(EventRet, self).__init__()
		self.Ret = {}
		self.Error = None

	# 结果是否有错误
	def HasError(self):
		return self.Error != None

	# 是否空的结果
	def IsEmpty(self):
		return self.Ret == None or len(self.Ret) == 0

	def mustNotEmpty(self):
		if self.Ret == None:
			raise("Ret is empty.")

	# 从结果中获取字符串
	def GetString(self,key):
		self.mustNotEmpty()

		rt = self.Ret[key]
		return str(rt)

	# 从结果中获取int
	def GetInt(self,key):
		self.mustNotEmpty()

		rt = self.Ret[key]
		return int(rt)

	# 从结果中获取float32
	def GetFloat(self,key):
		self.mustNotEmpty()

		rt = self.Ret[key]
		return float(rt)	

	# 获取bool值
	def GetBool(self,key):
		self.mustNotEmpty()

		rt = self.Ret[key]
		return bool(rt)

	# 获取Ret值
	def GetRet(self,key):
		self.mustNotEmpty()

		rt = self.Ret[key]
		return rt
	
	# 设置结果 value: interface{}
	def SetResult(self,key, value):
		self.mustNotEmpty()

		self.Ret[key] = value

	# 设置单一结果，用于返回结果只有一个值的情况
	def SetSingleResult(self,value):
		self.SetResult(SINGLERESULTKEYMAME, value)

	# 获取单一结果
	def GetSingleResult(self):
		return self.Ret[SINGLERESULTKEYMAME]

	# 结果转变为字符串
	def ToString(self):
		if self.HasError():
			return "{}".format(self.Error)

		retstr = ""
		for _, v in self.Ret:
			retstr += str(v) + "."

		return retstr

# 事件
class Event(object):
	def __init__(self,name,args):
		super(Event, self).__init__()
		self.Name = name      # 事件名称 string
		self.Args = args  	  # 事件参数 EventArgs

	def GetSingleArgValue(self):
		return self.Args[SINGLEARGSKEYNAME]

	# 获取string参数
	def GetString(self,key):
		rt = self.Args[key]
		return str(rt)

	# 获取int参数
	def GetInt(self,key):
		rt = self.Args[key]
		return int(rt)

	# 获取float32参数
	def GetFloat(self,key):
		rt = self.Args[key]
		return float(rt)

	# 获取bool参数
	def GetBool(self,key):
		rt = self.Args[key]
		return bool(rt)

# 创建事件参数
def NewEventArgs():
	args = {}
	return args

# 创建事件结果
def NewEventRet():
	ret = EventRet()
	return ret