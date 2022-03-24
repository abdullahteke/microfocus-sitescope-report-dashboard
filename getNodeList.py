#!/usr/bin/python 

import os
import time
import rrdtool
import pygal
import glob
import threading
from createPingReport import *

os.chdir('/opt/scripts/sitescopeReport')

def checkDir(hostname):
	if not os.path.exists('/var/www/html/sitescopereports/svgFiles/'+hostname):
    		os.makedirs('/var/www/html/sitescopereports/svgFiles/'+hostname)

def getNodeList(metric):
	nodeList=[]
	for name in glob.iglob('rrdFiles/'+metric+'/*.rrd'):
		parts=name.split("/")
		node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
		nodeList.append(node)
	
	return list(set(nodeList))

def createReportsForNode(nodeName,metric):
	createPingReports(nodeName)

threads=[]	

pingNodeList=getNodeList('Ping')


for pingNode in pingNodeList:
	t = threading.Thread(target=createPingReports, args=(pingNode.strip(),))
        threads.append(t)
        t.start()

cpuNodeList=getNodeList('Cpu')

for cpuNode in cpuNodeList:
        t = threading.Thread(target=createCpuReports, args=(cpuNode.strip(),))
        threads.append(t)
        t.start()

var=True
while var==True:
        print (threading.activeCount())
        if threading.activeCount()==1:
                var=False
                print('All tasks has been finished')
        else:
                time.sleep(5)
