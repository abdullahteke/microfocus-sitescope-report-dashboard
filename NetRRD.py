#!/usr/bin/python 

import os
import rrdtool
import re

def isRRDFileExist(hostname,ethname):
        if os.path.isfile('rrdFiles/Net/'+hostname+'_'+ethname+'.rrd'):
                return True
        else:
                return False

def updateRRDFile(hostname,ethname,inTraff,outTraff):
        try:
                ret=rrdtool.update('rrdFiles/Net/'+hostname+'_'+ethname+'.rrd','N:%s:%s' %(round(float(inTraff),2),round(float(outTraff),2)))
        except rrdtool.error,e:
                print e


def createRRDFile(hostname,eth): 
        try:
                ret = rrdtool.create("rrdFiles/Net/"+hostname+"_"+eth+".rrd", "--step", "300", "--start", "N",
                        "DS:IN_TRAFFIC:GAUGE:600:U:U",
			"DS:OUT_TRAFFIC:GAUGE:600:U:U",
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



def updateOrCreateNetRRDFile(monitor):
        serverName=monitor.get('target').replace(".test.local","")
        serverIP=monitor.get('targetIP')
        monTime=int(monitor.get('time'))/1000
        monCnts=monitor.getchildren()
	interfaces=[]
	ethName=''
	
	if (monitor.get('type')=='Unix Resources'):
		
		for cnt in monCnts:
			trafficValue='-1'
			tmpInt=[]

			match=re.search(r".*\\.*\\(ReceiveBytes|TransmitBytes)",cnt.get('name'))
			if match:
				intName,type=re.search(r".*\\(.*)\\(ReceiveBytes|TransmitBytes)",cnt.get('name')).groups()
				ethName=intName.replace(" ","_")
				tmpInt.append(ethName)
				trafficValue=cnt.get('value').replace(",",".").replace("n/a",'-1')

				if (type=='ReceiveBytes'):
					tmpInt.append('IN')
				else:
					tmpInt.append('OUT')
				tmpInt.append(trafficValue)

				interfaces.append(tmpInt)
	else:
        	for cnt in monCnts:
                        trafficValue='-1'
                        tmpInt=[]

                        match=re.search(r".*\\.*\\(Bytes Received/sec|Bytes Sent/sec)",cnt.get('name'))
                        if match:
                                intName,type=re.search(r".*\\(.*)\\(Bytes Received/sec|Bytes Sent/sec)",cnt.get('name')).groups()
                                ethName=intName.replace(" ","_")
                                tmpInt.append(ethName)
                                trafficValue=cnt.get('value').replace(",",".").replace("n/a",'-1')
				
                                if (type=='Bytes Received/sec'):
                                        tmpInt.append('IN')
                                else:
                                        tmpInt.append('OUT')
                                tmpInt.append(trafficValue)

                                interfaces.append(tmpInt)


	updateOrCreateNetRRDFiles(serverName,interfaces)	

def updateOrCreateNetRRDFiles(serverName,interfaces):
	cnt=0
	intName=''
	inTraff=''
	outTraff=''

	for interface in sorted(interfaces):
		if (len(interface) > 0):
			if (cnt==0):
				intName=interface[0]
				inTraff=interface[2]
				cnt=cnt+1
			elif (cnt==1):
				outTraff=interface[2]
				if (not isRRDFileExist(serverName,intName)):
					createRRDFile(serverName,intName)
				updateRRDFile(serverName,intName,inTraff,outTraff)

				cnt=0
					

