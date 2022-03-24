#!/usr/bin/python 

from SOAPpy import WSDL
import datetime
import subprocess
from lxml import objectify, etree
import os
import time
import rrdtool
from PingRRD import *
from CpuRRD import *
from MemoryRRD import *
from NetRRD import *
from DiskRRD import *
from M2Crypto import SSL



def getNowTime():
	d=datetime.datetime.now().strftime('%s')
	d_in_ms = int(d)*1000
	return str(d_in_ms)

def get5MinBefore():
	now = datetime.datetime.now()
	now_minus = now-datetime.timedelta(minutes = 5)
	d=now_minus.strftime('%s')
	d_in_ms=int(d)*1000
	return str(d_in_ms)

def getMonitorStatus():

	fl=open('result.gz','w')
	#WSDL.Config.SSL.key_file = 'sitescopeServer.local'

	# WSDbfetch WSDL URL.
	wsdlUrl = 'https://sitescopeServer.local:8443/SiteScope/services/APIDataAcquisitionImpl?wsdl'
	namespace = 'http://sitescopeServer.local'

	query=[get5MinBefore(),getNowTime(),'','','','Memory#,#Ping#,#Disk#,#Cpu#,#Network Interface','']
	username='administrator'
	password='admin'

	# Create a service proxy from the WSDL.
	dbfetchSrv = WSDL.Proxy(wsdlUrl,namespace)

	# Perform the query.
	result = dbfetchSrv.getData(query,username,password)
	fl.write(result)
	fl.close()

def parseResult():
	tree=etree.parse('result.xml')
	root=tree.getroot()
	for monitor in root.findall('.//monitor'):
		if (monitor.get('name')=='Ping'):
			updateOrCreatePingRRDFile(monitor)
		elif (monitor.get('name')=='Disk'):
			updateOrCreateDiskRRDFile(monitor)
		elif (monitor.get('name')=='Cpu'):
			updateOrCreateCpuRRDFile(monitor)
		elif (monitor.get('name')=='Network Interface'):
			updateOrCreateNetRRDFile(monitor)
		elif (monitor.get('name')=='Memory'):
			updateOrCreateMemoryRRDFile(monitor)

os.chdir('/opt/scripts/sitescopeReport')

if os.path.isfile('result.xml'):
                os.unlink('result.xml')

getMonitorStatus() 
subprocess.call(["gunzip", "result.gz"])
subprocess.call(["mv", "result", "result.xml"])
parseResult()

