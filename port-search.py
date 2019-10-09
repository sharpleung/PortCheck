#!/usr/bin/env python
#-*-coding:utf-8-*-
import threading
try:
    import queue
except:
    from Queue import Queue
import sys
import telnetlib
import os
class SearchPort(threading.Thread):
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'	
	def __init__(self,queue):
		threading.Thread.__init__(self)
		self._queue=queue
	def run(self):
		while not self._queue.empty():
			try:
				PortLimit = self._queue.get()
				self.IPPort(PortLimit)
			except Exception as e:
					print(e)
					pass
	def IPPort(self,port):
		tn = telnetlib.Telnet()
		try:
			tn.open(ip,int(port),timeout=1.5)
			sys.stdout.write('\r%s%s\t[%s][Open]\n'%(self.OKGREEN,ip,port))
			with open(filename) as file:
				if port not in file.read():
					f = open(filename,'a+')
					f.write(port+"\n")
					f.close()	
		except Exception as e:
			#sys.stdout.write('\r%s%s\t[%s][Close]\n'%(self.FAIL,ip,port))
			pass
		finally:
			tn.close()
	
def main(threadsnum):
	try:
		Myqueue = Queue()
	except:
		Myqueue = queue.Queue()
	with open("port_dic.txt") as dic:	
		for line in dic:	
			Myqueue.put(line.strip('\n'))
	threads=[]
	threadsCount=int(threadsnum)
	for i in range(threadsCount):
		threads.append(SearchPort(Myqueue))
	for j in threads:
		j.start()
	for j in threads:
		j.join()

	print ('\033[0m'+"The log file is in:"+filename)
if __name__=='__main__':
	if len(sys.argv) != 3:
		print("Enter:python %s ip threads" %(sys.argv[0]))
		print("eg:python port-search.py 127.0.0.1 100")
		sys.exit(-1)
	else:
		print("Find the following port for ip:")
		path="log/"+sys.argv[1]
		filename=path+'/'+sys.argv[1]+".txt"
		isExists=os.path.exists(path)
		if not isExists:
			os.makedirs(path)
		f = open(filename,"w+")
		f.close()
		ip=sys.argv[1]
		main(sys.argv[2])
