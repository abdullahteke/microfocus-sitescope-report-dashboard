#!/usr/bin/python 

import datetime
import subprocess
from lxml import objectify, etree
import os
import time
import rrdtool
import pygal
from reportFunctions import *
import threading
import glob
import sys

os.chdir('/opt/scripts/sitescopeReport')

def checkDir(hostname):
	if not os.path.exists('/var/www/html/sitescopereports/svgFiles/'+hostname):
    		os.makedirs('/var/www/html/sitescopereports/svgFiles/'+hostname)

def createLastHourGraph(nodeName):
	data_last_hour= getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","300","-1h","LAST")	
	data_average_hour=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","300","-1h","AVERAGE")	
	data_min_hour=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","300","-1h","MIN")
	data_max_hour=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","300","-1h","MAX")

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))	

	line_chart.title = 'CPU Utilization Of '+nodeName+' For Last Hour'
	appendDataSet('Cur ',data_last_hour,line_chart)
	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Cpu_Hourly.svg')

def appendDataSet(metricType,rrdData,chart):
        resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
        timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

	list=rrdData[2]
	list.pop()
	list.pop()
	dataset=getCPUDataset(timeLine,list)
	chart.add('Utilization '+metricType,dataset,fill=True)

def getCPUDataset(timeLine,list):
        dataset=[]
        for i in range(len(timeLine)):
		if (list[i][0]!=None):
                	dataset.append((timeLine[i],round(list[i][0],2)))
		else:
			dataset.append((timeLine[i],-1))

        return dataset
	
def createLastDayGraph(nodeName):
	data_last_day=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","900","-1d","LAST")
	data_average_day=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","900","-1d","AVERAGE")
	data_min_day=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","900","-1d","MIN")
	data_max_day=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","900","-1d","MAX")

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))
	
        line_chart.title = 'CPU Utilization Of '+nodeName+' For Last Day'

        appendDataSet('Avg ',data_average_day,line_chart)

	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Cpu_Daily.svg')
	
def createLastWeekGraph(nodeName):
        data_last_week=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","3600","-1w","LAST")
        data_average_week=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","3600","-1w","AVERAGE")
        data_min_week=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","3600","-1w","MIN")
        data_max_week=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","3600","-1w","MAX")


        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))

        line_chart.title = 'CPU Utilization Of '+nodeName+' For Last Week'
	appendDataSet('Max ',data_max_week,line_chart)
        appendDataSet('Avg ',data_average_week,line_chart)
	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Cpu_Weekly.svg')

def createLastMonthGraph(nodeName):
        data_last_month=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","86400","-1m","LAST")
        data_average_month=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","86400","-1m","AVERAGE")
        data_min_month=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","86400","-1m","MIN")
        data_max_month=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","86400","-1m","MAX")
	

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))
        line_chart.title = 'CPU Utilization Of '+nodeName+' For Last Month'
	
	appendDataSet('Max ',data_max_month,line_chart)
        appendDataSet('Avg ',data_average_month,line_chart)
        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Cpu_Monthly.svg')



def createLastYearGraph(nodeName):
        data_last_year=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","604800","-1y","LAST")
        data_average_year=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","604800","-1y","AVERAGE")
        data_min_year=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","604800","-1y","MIN")
        data_max_year=getDataFromRRDFile('rrdFiles/Cpu/'+nodeName+".rrd","604800","-1y","MAX")


        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M'))

        line_chart.title = 'CPU Utilization Of '+nodeName+' For Last Year'
	appendDataSet('Max ',data_max_year,line_chart)
        appendDataSet('Avg ',data_average_year,line_chart)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Cpu_Yearly.svg')

def getNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Cpu/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)
        return list(set(nodeList))


def createCpuReport(step):
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
		print node

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

