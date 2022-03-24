#!/usr/bin/python 

import os
import rrdtool
import re

def isRRDFileExist(hostname,disk):
        if os.path.isfile('rrdFiles/Disk/'+hostname+'_'+disk+'.rrd'):
                return True
        else:
                return False
def clearDiskName(st):
        tmp=st.replace("[","").replace("]","").replace("(","").replace(")","")
        if (tmp=='/'):
                tmp='root'
                return tmp
        else:
                return tmp.replace("/","_")

def updateOrCreateDiskRRDFile(monitor):
        serverName=monitor.get('target').replace(".test.local","")
        serverIP=monitor.get('targetIP')
        monTime=int(monitor.get('time'))/1000
        monCnts=monitor.getchildren()
	disks=[]
	
	for cnt in monCnts:	
		match=re.search(r".*/.*/.*/(percent full|MB total|MB free)",cnt.get('name'))
		tmpDisk=[]
	
		if (match):
			diskName,type=re.search(r".*/.*/.*(\[.*\]|\(.*\)).*/(percent full|MB total|MB free)",cnt.get('name')).groups()	
			tmpDisk.append(diskName)	
			tmpDisk.append(type)

			if (cnt.get('value')=='n/a'):
				tmpDisk.append('-1')
			else:
				tmpDisk.append(cnt.get('value'))
			
		disks.append(tmpDisk)			

	updateRRDDiskFile(serverName,disks)

def updateRRDDiskFile(serverName,disks):
	i=''
	diskName=''
	free='-1'
	tot='-1'
	percent='-1'
	cnt=0
	for disk in sorted(disks):
		if (len(disk)>0):
			if (cnt==0):
				diskName= disk[0]
				free=disk[2]
				cnt=cnt+1
			elif (cnt==1):
				tot=disk[2]
				cnt=cnt+1
			elif (cnt==2):	
				percent=disk[2]
				if (not isRRDFileExist(serverName,clearDiskName(diskName))):
					createRRDFile(serverName,clearDiskName(diskName))
				updateRRDFile(serverName,clearDiskName(diskName),free,tot,percent)
				cnt=0
	
def createRRDFile(serverName,diskName):
        try:
                ret = rrdtool.create("rrdFiles/Disk/"+serverName+"_"+diskName+".rrd", "--step", "300", "--start", "N",
                                "DS:DISK_FREE:GAUGE:600:U:U",
                                "DS:DISK_TOTAL:GAUGE:600:U:U",
                                "DS:DISK_PERCENT:GAUGE:600:0:100",
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
def updateRRDFile(serverName,diskName,free,tot,percent):
	new_free=str(round(float(free),2))
	new_tot=str(round(float(tot),2))
	new_perc=str(round(float(percent),2))
	
        try:
                ret=rrdtool.update('rrdFiles/Disk/'+serverName+"_"+diskName+'.rrd','N:%s:%s:%s' %(new_free,new_tot,new_perc))
        except rrdtool.error,e:
                print e
