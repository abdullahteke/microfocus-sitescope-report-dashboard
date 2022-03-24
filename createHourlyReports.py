#!/usr/bin/python 

import datetime
import subprocess
from lxml import objectify, etree
import os
import time
import rrdtool
import pygal
from reportFunctions import *
import pytz
import glob
import threading
from createPingReport import *
from createCpuReport import *
from createMemoryReport import *

def createHourlyReports(metricType):
	if (metricType=='Ping'):
		createPingReport('h')
	elif(metricType=='Cpu'):
		createCpuReport('h')
	elif(metricType=='Memory'):
		createMemoryReport('h')
	
	
os.chdir('/opt/scripts/sitescopeReport')

print("Start:")
print(datetime.datetime.now())
threads=[]

t1 = threading.Thread(target=createHourlyReports, args=('Ping',))
threads.append(t1)
t1.start()

t2 = threading.Thread(target=createHourlyReports, args=('Cpu',))
threads.append(t2)
t2.start()

t3 = threading.Thread(target=createHourlyReports, args=('Memory',))
threads.append(t3)
t3.start()

print("End:")
print(datetime.datetime.now())
