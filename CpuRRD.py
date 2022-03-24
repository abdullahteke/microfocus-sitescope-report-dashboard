#!/usr/bin/python 

import os
import rrdtool

def isRRDFileExist(hostname):
	if os.path.isfile('rrdFiles/Cpu/'+hostname+'.rrd'):
		return True
	else:
		return False

def updateRRDFile(hostname,cpuValue):
	c=str(round(float(cpuValue),2))
	try:
        	ret=rrdtool.update('rrdFiles/Cpu/'+hostname+'.rrd','N:%s' %(c))
        except rrdtool.error,e:
                print e

def createRRDFile(hostname): 
	try:
	        ret = rrdtool.create("rrdFiles/Cpu/"+hostname+".rrd", "--step", "300", "--start", "N",
                       "DS:CPU:GAUGE:600:0:100",
                        "RRA:LAST:0.5:1:2016",
			"RRA:MIN:0.5:1:2016",
			"RRA:MAX:0.5:1:2016",
			"RRA:AVERAGE:0.5:1:2016",
                        "RRA:LAST:0.5:6:672",
			"RRA:MIN:0.5:6:672",
			"RRA:MAX:0.5:6:672",
			"RRA:AVERAGE:0.5:6:672",
                        "RRA:LAST:0.5:12:2160",
			"RRA:MIN:0.5:12:2160",
			"RRA:MAX:0.5:12:2160",
			"RRA:AVERAGE:0.5:12:2160",
                        "RRA:LAST:0.5:288:365",
			"RRA:MIN:0.5:288:365",
			"RRA:MAX:0.5:288:365",
			"RRA:AVERAGE:0.5:288:365")
	except rrdtool.error,e:
        	print e
	
def updateOrCreateCpuRRDFile(monitor):
        serverName=monitor.get('target').replace(".test.local","")
        serverIP=monitor.get('targetIP')
        monTime=int(monitor.get('time'))/1000
        monCnts=monitor.getchildren()
        cpu='-1'

        for cnt in monCnts:
                if (cnt.get('name')=='utilization'):
                        if (cnt.get('value')!='n/a'):
                                cpu=cnt.get('value')

        if (not isRRDFileExist(serverName)):
		createRRDFile(serverName)

	updateRRDFile(serverName,cpu)
