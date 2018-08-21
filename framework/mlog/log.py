from __future__ import absolute_import

import logging.handlers
import logging,os
import time
 
class Logger:
  def __init__(self, path = './general.log',clevel = logging.DEBUG,Flevel = logging.DEBUG):
    self.logger = logging.getLogger(path)
    self.logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter('%(asctime)s|%(levelname)s|%(filename)s:%(lineno)d|func:%(funcName)s|%(message)s')
    # fmt = logging.Formatter('%(levelname)s|%(filename)s:%(lineno)d|func:%(funcName)s|%(message)s')
    
    sh = logging.StreamHandler()
    sh.setFormatter(fmt)
    sh.setLevel(clevel)
    
    fh = logging.handlers.RotatingFileHandler(path, maxBytes=10*1024, backupCount=1)
    # fh = logging.FileHandler(path)
    fh.encoding="utf-8"
    fh.setFormatter(fmt)
    fh.setLevel(Flevel)
    self.logger.addHandler(sh)
    self.logger.addHandler(fh)

  def getInstance(self):
    return self.logger

# debug,info,warn,error,critical
dir_name = "log"
os.system("mkdir -p {}".format(dir_name))
strTime = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
# nTime = int(time.time()*1000)
path_name = "{}/".format(dir_name) + "{}".format(strTime) + ".log"

mlog = Logger(path=path_name).getInstance()
