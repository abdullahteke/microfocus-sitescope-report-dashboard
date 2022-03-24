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
import sys

os.chdir('/opt/scripts/sitescopeReport')

def checkDir(hostname):
	if not os.path.exists('/var/www/html/sitescopereports/svgFiles/'+hostname):
    		os.makedirs('/var/www/html/sitescopereports/svgFiles/'+hostname)

def createLastHourGraph(nodeName):
	data_last_hour= getDataFromRRDFile('rrdFiles/Ping/'+nodeName+".rrd","300","-1h","LAST")	
	line_chart = pygal.DateTimeLine(
		truncate_label=-1,
		x_label_rotation=90,
		width=1200,height=400,
		x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))

	line_chart.title = 'Availability Of '+nodeName+' For Last Hour'
	#line_chart.x_labels = map(getDateFromTimestamp, range(startTime,endTime,resolution))

	appendDataSet('Cur.',data_last_hour,line_chart)

	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Ping_Hourly.svg')

def appendDataSet(metricType,rrdData,chart):
	resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
	timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

	list=rrdData[2]
	list.pop()
	list.pop()
	
	dataset=getPingDataSet(timeLine,list)
	chart.add('GoodPacket '+metricType,dataset[0],allow_interruptions=True,fill=True)
	chart.add('RTT Time'+metricType,dataset[1],allow_interruptions=True,fill=True)

def getPingDataSet(timeLine,list):
	dataset=[]
	gpck=[]
	rtt=[]
	for i in range(len(timeLine)):
		if (list[i][0]==None):
			gpck.append((timeLine[i],-1))
		else:
    			gpck.append((timeLine[i],list[i][0]))
		if (list[i][1]==None):
			rtt.append((timeLine[i], -1))
		else:
			rtt.append((timeLine[i], list[i][1]))

	dataset.append(gpck)
	dataset.append(rtt)
	return dataset
			 
def createLastDayGraph(nodeName):
	data_last_day=getDataFromRRDFile('rrdFiles/Ping/'+nodeName+".rrd","900","-1d","LAST")
	

	line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
		x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'),
                width=1200,height=400)
        line_chart.title = 'Availability Of '+nodeName+' For Last Day'

        appendDataSet('Cur ',data_last_day,line_chart)

	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Ping_Daily.svg')
	
def createLastWeekGraph(nodeName):
        data_last_week=getDataFromRRDFile('rrdFiles/Ping/'+nodeName+".rrd","3600","-1w","LAST")

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
		x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))
	
        line_chart.title = 'Availability Of '+nodeName+' For Last Week'

        appendDataSet('Cur ',data_last_week,line_chart)
	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Ping_Weekly.svg')

def createLastMonthGraph(nodeName):
        data_last_month=getDataFromRRDFile('rrdFiles/Ping/'+nodeName+".rrd","86400","-1m","LAST")
	
        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
		x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))

        line_chart.title = 'Availability Of '+nodeName+' For Last Month'

        appendDataSet('Cur ',data_last_month,line_chart)
        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Ping_Monthly.svg')



def createLastYearGraph(nodeName):
        data_last_year=getDataFromRRDFile('rrdFiles/Ping/'+nodeName+".rrd","604800","-1y","LAST")
	

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
		x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))

        line_chart.title = 'Availability Of '+nodeName+' For Last Year'

        appendDataSet('Cur ',data_last_year,line_chart)
        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Ping_Yearly.svg')

def getNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Ping/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)

        return list(set(nodeList))

def createPingReport(step):
        threads=[]
        nodeList=getNodeList()

        for node in nodeList:
                checkDir(node)
                if (step=='h'):
                        t = threading.Thread(target=createLastHourGraph, args=(node.strip(),))
                elif(step=='d'):
                        t = threading.Thread(target=createLastDayGraph, args=(node.strip(),))
                elif(step=='w'):
                        t = threading.Thread(target=createLastWeekGraph, args=(node.strip(),))
                elif(step=='m'):
                        t= threading.Thread(target=createLastMonthGraph, args=(node.strip(),))
                else:
                        t=threading.Thread(target=createLastYearGraph, args=(node.strip(),))

        	threads.append(t)
        	t.start()

def test(step):
        nodeList=getNodeList()

        for node in nodeList:
                checkDir(node)

                if (step=='h'):
                        createLastHourGraph(node)
                elif(step=='d'):
                        createLastDayGraph(node)
                elif(step=='w'):
                        createLastWeekGraph(node)
                elif(step=='m'):
                        createLastMonthGraph(node)
                else:
                        createLastYearGraph(node)

threads=[]
node=sys.argv[1]
t1 = threading.Thread(target=createLastHourGraph, args=(node.strip(),))
t2 = threading.Thread(target=createLastDayGraph, args=(node.strip(),))
t3 = threading.Thread(target=createLastWeekGraph, args=(node.strip(),))
t4 = threading.Thread(target=createLastMonthGraph, args=(node.strip(),))
t5 = threading.Thread(target=createLastYearGraph, args=(node.strip(),))

threads.append(t1)
threads.append(t2)
threads.append(t3)
threads.append(t4)
threads.append(t5)

t1.start()
t2.start()
t3.start()
t4.start()
t5.start()


