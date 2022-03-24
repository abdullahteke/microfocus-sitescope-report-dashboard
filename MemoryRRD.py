#!/usr/bin/python 

import os
import rrdtool

def isRRDFileExist(hostname):
        if os.path.isfile('rrdFiles/Memory/'+hostname+'.rrd'):
                return True
        else:
                return False

def updateRRDFile(hostname,pmf,vmf,pmu,vmu):
        try:
		ret=rrdtool.update('rrdFiles/Memory/'+hostname+'.rrd','N:%s:%s:%s:%s' %(round(float(pmf),2),round(float(vmf),2),round(float(pmu),2),round(float(vmu),2)))
        except rrdtool.error,e:
                print e

def createRRDFile(hostname):
	try:
        	ret = rrdtool.create("rrdFiles/Memory/"+hostname+".rrd", "--step", "300", "--start", "N",
                                "DS:PYHS_MEM_FREE:GAUGE:600:U:U",
                                "DS:VIRT_MEM_FREE:GAUGE:600:U:U",
                                "DS:PYHS_MEM_USG:GAUGE:600:0:100",
                                "DS:VIRT_MEM_USG:GAUGE:600:0:100",
                                "RRA:LAST:0.5:1:2016",
				"RRA:MAX:0.5:1:2016",
				"RRA:MIN:0.5:1:2016",
				"RRA:AVERAGE:0.5:1:2016",
                                "RRA:LAST:0.5:6:672",
				"RRA:MAX:0.5:6:672",
				"RRA:MIN:0.5:6:672",
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
	
def updateOrCreateMemoryRRDFile(monitor):
        serverName=monitor.get('target').replace(".test.local","")
        serverIP=monitor.get('targetIP')
        monCnts=monitor.getchildren()
	
	pyhsicalMemFree='-1'
	virtualMemFree='-1'
	pyhsicalMemUsage='-1'
	virtualMemUsage='-1'

        for cnt in monCnts:
		if (cnt.get('value')!="n/a"):
                	if (cnt.get('name')=='physical memory MB free'):
                                pyhsicalMemFree=cnt.get('value')
                	elif (cnt.get('name')=='swap space MB free') or (cnt.get('name')=='virtual memory MB free'):
                        	virtualMemFree=cnt.get('value')
			elif (cnt.get('name')=='physical memory used %'):
				pyhsicalMemUsage=cnt.get('value')
			elif (cnt.get('name')=='swap space used %') or (cnt.get('name')=='virtual memory used %'):
				virtualMemUsage=cnt.get('value')
			
        if (not isRRDFileExist(serverName)):
                createRRDFile(serverName)

        updateRRDFile(serverName,pyhsicalMemFree,virtualMemFree,pyhsicalMemUsage,virtualMemUsage)

