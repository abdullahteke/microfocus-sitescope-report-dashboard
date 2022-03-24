#!/usr/bin/python 

import os
import rrdtool


def isRRDFileExist(hostname):
        if os.path.isfile('rrdFiles/Ping/'+hostname+'.rrd'):
                return True
        else:
                return False

def updateRRDFile(hostname,packetGoodValue,rttValue):
	a=str(round(float(packetGoodValue),2))
	b=str(round(float(rttValue),2))

        try:
                ret=rrdtool.update('rrdFiles/Ping/'+hostname+'.rrd','N:%s:%s' %(a,b))
        except rrdtool.error,e:
                print e

def createRRDFile(hostname):
	try:
        	ret = rrdtool.create("rrdFiles/Ping/"+hostname+".rrd", "--step", "300", "--start", "N",
                           "DS:PACKET_LOSS:GAUGE:600:0:100",
                           "DS:RTT_TIME:GAUGE:600:U:U",
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

	except rrdtool.error, e:
		print e

def updateOrCreatePingRRDFile(monitor):
	serverName=monitor.get('target').replace(".test.local","")
	serverIP=monitor.get('targetIP')
	monTime=int(monitor.get('time'))/1000
	monCnts=monitor.getchildren()

	rttValue='-1'
	packetGoodValue='-1'
	
	for cnt in monCnts:
		if (cnt.get('name')=='round trip time'):
			if (cnt.get('quality')=='good'):
				rttValue=cnt.get('value')	
		else:
			packetGoodValue=cnt.get('value')

	if (not isRRDFileExist(serverName)):
                createRRDFile(serverName)

        updateRRDFile(serverName,packetGoodValue,rttValue)
