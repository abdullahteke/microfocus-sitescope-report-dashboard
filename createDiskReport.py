#!/usr/bin/python 

import datetime
import subprocess
from lxml import objectify, etree
import os
import time
import rrdtool
import pygal
from reportFunctions import *
import glob

os.chdir('/opt/scripts/sitescopeReport')

def checkDir(hostname):
	if not os.path.exists('/var/www/html/sitescopereports/svgFiles/'+hostname):
    		os.makedirs('/var/www/html/sitescopereports/svgFiles/'+hostname)

def getDiskList(nodeName):
	diskList=[]
	for name in glob.glob('rrdFiles/Disk/'+nodeName+'_*.rrd'):
		#diskList.append(name.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/",""))
		diskList.append(name)
	return diskList
def createLastHourGraph(nodeName):
	diskList=getDiskList(nodeName)
	for disk in diskList:
		data_last_hour= getDataFromRRDFile(disk,"300","-1h","LAST")	
		data_max_hour=getDataFromRRDFile(disk,"300","-1h","MAX")
		diskName=disk.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/","")
	
		line_chart = pygal.DateTimeLine(
                	truncate_label=-1,
                	x_label_rotation=90,
                	width=1200,height=400,
                	x_value_formatter=lambda dt: dt.strftime('%H:%M')
		)
        	line_chart.title = 'Disk '+diskName +' Usage Of '+nodeName+' For Last Hour'

        	appendDataSet('Cur ',data_last_hour,line_chart)

        	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Disk_'+diskName+'_Hourly.svg')


def appendDataSet(metricType,rrdData,chart):
        resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
        timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

        list=rrdData[2]
        list.pop()
        list.pop()
        dataset=getDiskDataset(timeLine,list)
        chart.add('Disk Total '+metricType,dataset[0],fill=True)
	chart.add('Disk Usage '+metricType,dataset[1],fill=True)
	chart.add('Disk Usage Percent:'+metricType,dataset[2],secondary=True)

def getDiskDataset(timeLine,list):
        dataset=[]
	total_disk=[]
	usagePercent=[]	
	diskUsage=[]
        for i in range(len(timeLine)):
                total_disk.append((timeLine[i],list[i][1]))
		if (list[i][2]!=None):
			usagePercent.append((timeLine[i],list[i][2]))
		else:
			usagePercent.append((timeLine[i],0))
		if (list[i][1]!=None and list[i][0]!=None):	
			diskUsage.append((timeLine[i],list[i][1]-list[i][0]))
		else:
			diskUsage.append((timeLine[i],None))
	dataset.append(total_disk)
	dataset.append(diskUsage)
	dataset.append(usagePercent)

        return dataset
def createLastDayGraph(nodeName):
	
        diskList=getDiskList(nodeName)
        for disk in diskList:
                data_average_hour= getDataFromRRDFile(disk,"900","-1d","LAST")
                data_max_hour=getDataFromRRDFile(disk,"900","-1d","MAX")
                diskName=disk.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/","")

                line_chart = pygal.DateTimeLine(
                        truncate_label=-1,
                        x_label_rotation=90,
                        width=1200,height=400,
                        x_value_formatter=lambda dt: dt.strftime('%H:%M')
                )
                line_chart.title = 'Disk '+diskName +' Usage Of '+nodeName+' For Last Day'

		appendDataSet('Max ',data_average_hour,line_chart)
                appendDataSet('Cur ',data_max_hour,line_chart)


                line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Disk_'+diskName+'_Daily.svg')


def createLastWeekGraph(nodeName):
        diskList=getDiskList(nodeName)
        for disk in diskList:
                data_average_hour= getDataFromRRDFile(disk,"3600","-1w","LAST")
                data_max_hour=getDataFromRRDFile(disk,"3600","-1w","MAX")
                diskName=disk.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/","")

                line_chart = pygal.DateTimeLine(
                        truncate_label=-1,
                        x_label_rotation=90,
                        width=1200,height=400,
                        x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
                line_chart.title = 'Disk '+diskName +' Usage Of '+nodeName+' For Last Week'

                appendDataSet('Max ',data_average_hour,line_chart)
                appendDataSet('Cur ',data_max_hour,line_chart)


                line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Disk_'+diskName+'_Weekly.svg')

def createLastMonthGraph(nodeName):
        diskList=getDiskList(nodeName)
        for disk in diskList:
                data_average_hour= getDataFromRRDFile(disk,"86400","-1m","LAST")
                data_max_hour=getDataFromRRDFile(disk,"86400","-1m","MAX")
                diskName=disk.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/","")

                line_chart = pygal.DateTimeLine(
                        truncate_label=-1,
                        x_label_rotation=90,
                        width=1200,height=400,
                        x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
                line_chart.title = 'Disk '+diskName +' Usage Of '+nodeName+' For Last Month'

                appendDataSet('Max ',data_average_hour,line_chart)
                appendDataSet('Cur ',data_max_hour,line_chart)


                line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Disk_'+diskName+'_Montly.svg')



def createLastYearGraph(nodeName):
        diskList=getDiskList(nodeName)
        for disk in diskList:
                data_average_hour= getDataFromRRDFile(disk,"604800","-1y","LAST")
                data_max_hour=getDataFromRRDFile(disk,"604800","-1y","MAX")
                diskName=disk.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Disk/","")

                line_chart = pygal.DateTimeLine(
                        truncate_label=-1,
                        x_label_rotation=90,
                        width=1200,height=400,
                        x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
                line_chart.title = 'Disk '+diskName +' Usage Of '+nodeName+' For Last Year'

                appendDataSet('Max ',data_average_hour,line_chart)
                appendDataSet('Cur ',data_max_hour,line_chart)


                line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Disk_'+diskName+'_Yearly.svg')

	
def createDiskReports(node):
        checkDir(node)
        createLastHourGraph(node)
        createLastDayGraph(node)
        createLastWeekGraph(node)
        createLastMonthGraph(node)
        createLastYearGraph(node)
