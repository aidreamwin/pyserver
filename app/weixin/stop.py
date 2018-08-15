import os,argparse

def stop(_str):
	if _str=="":
		return

	cmd = "ps -ef|grep '%s'|grep -v grep|grep -v 'python stop.py'|awk '{print $2}'" % (_str)
	print_cmd = "ps -ef|grep '%s'|grep -v grep|grep -v 'python stop.py'" % (_str)
	os.system(print_cmd)
	print("run: %s" % cmd)
	result = os.popen(cmd).read()
	if result=='' or result==None:
		print("run: %s empty."%cmd)
		return
	result = result.strip()
	result = result.split("\n")
	for pid in result:
		kill_cmd="kill -9 {}".format(pid)
		print("run: %s" % kill_cmd)
		
		nRet = os.system(kill_cmd)
		if nRet!=0:
			print("run: {} failed.".format(kill_cmd))
			return
		print("run: {} success.".format(kill_cmd))

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("--program", default="hhhhhhtttttt",\
        type=str, help="program name")
	args = parser.parse_args()
	stop(args.program)