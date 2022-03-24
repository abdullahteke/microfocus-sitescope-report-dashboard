#!/usr/bin/python 

import datetime
import subprocess
from lxml import objectify, etree
import os
import time
import rrdtool
import pygal
import pytz
import glob
import threading

def ping(node):
	subprocess.call(['./createPingReport.py', node])

def cpu(node):
        subprocess.call(['./createCpuReport.py', node])
def memory(node):
	subprocess.call(['./createMemoryReport.py', node])


os.chdir('/opt/scripts/sitescopeReport')

print("Start:")
print(datetime.datetime.now())

threads = []

def getPingNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Ping/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)

        return list(set(nodeList))

def getCpuNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Cpu/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)
        return list(set(nodeList))

def getMemoryNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Memory/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)

        return list(set(nodeList))


fp=getPingNodeList()
fcpu=getCpuNodeList()
fmemory=getMemoryNodeList()


for line in fp:
	t1 = threading.Thread(target=ping, args=(line.strip(),))
        threads.append(t1)
        t1.start()

for line in fcpu:
        t1 = threading.Thread(target=cpu, args=(line.strip(),))
        threads.append(t1)
        t1.start()

for line in fmemory:
        t1 = threading.Thread(target=memory, args=(line.strip(),))
        threads.append(t1)
        t1.start()

		
var=True
while var==True:
        print (threading.activeCount())
        if threading.activeCount()==1: 
                var=False
                print('All tasks has been finished')
        else:
                time.sleep(5)


print("End:")
print(datetime.datetime.now())
