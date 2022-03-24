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
	data_last_hour= getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","300","-1h","LAST")
        data_max_hour=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","300","-1h","MAX")

        line_chart = pygal.DateTimeLine(
                       truncate_label=-1,
                       x_label_rotation=90,
                       width=1200,height=400,
                       x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
        line_chart.title = 'Memory Usage Of '+nodeName+' For Last Hour'

        appendDataSet('Cur ',data_last_hour,line_chart)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Memory_Hourly.svg')

def appendDataSet(metricType,rrdData,chart):
        resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
        timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

	list=rrdData[2]
	list.pop()
	list.pop()
	dataset=getDatasetForMemory(timeLine,list)

	chart.add('Virt Tot. '+metricType,dataset[3],fill=True)
	chart.add('Phys Tot. '+metricType,dataset[1],fill=True)
	chart.add('Phys Mem Used '+metricType,dataset[0],fill=True)
	chart.add('Virt Mem Used '+metricType,dataset[2],fill=True)
	chart.add('Phys Mem Perc. '+metricType,dataset[4],secondary=True)
	chart.add('Virt Mem Perc. '+metricType,dataset[5],secondary=True)

def createDataset(rrdData):
        resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
        timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

        list=rrdData[2]
        list.pop()
        list.pop()
        return getDatasetForMemory(timeLine,list)

def memoryUsage(free,usage):
	return round(totalMemory(free,usage) - free,2)
def totalMemory(free,usage):
	if ((100 - usage)==0):
		return  round((100 * free)/1,2)
	else:
		return round ((100 * free)/(100 - usage))

def getDatasetForMemory(timeLine,list):
	dataset=[]
	pmu=[]
	vmu=[]
	ptot=[]
	vtot=[]
	ppercent=[]
	vpercent=[]

	for i in range(len(timeLine)):
		if (list[i][0]!=None and list[i][1]!=None and list[i][2]!=None and list[i][3]!=None):
			pmu.append((timeLine[i],memoryUsage(list[i][0],list[i][2])/1024))
			vmu.append((timeLine[i],memoryUsage(list[i][1],list[i][3])/1024))
			ptot.append((timeLine[i],totalMemory(list[i][0],list[i][2])/1024))
			vtot.append((timeLine[i],totalMemory(list[i][1],list[i][3])/1024))
			ppercent.append((timeLine[i],round(list[i][2])))
			vpercent.append((timeLine[i],round(list[i][3])))
		else:
			pmu.append((timeLine[i],-1))
			vmu.append((timeLine[i],-1))
			ptot.append((timeLine[i],-1))
			vtot.append((timeLine[i],-1))
			ppercent.append((timeLine[i],-1))
			vpercent.append((timeLine[i],-1))
	dataset.append(pmu)
	dataset.append(ptot)
	dataset.append(vmu)
	dataset.append(vtot)
	dataset.append(ppercent)
	dataset.append(vpercent)
	return dataset
		

def createLastDayGraph(nodeName):
	data_average_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","900","-1d","AVERAGE")
	data_max_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","900","-1d","MAX")
        line_chart = pygal.DateTimeLine(
                       truncate_label=-1,
                       x_label_rotation=90,
                       width=1200,height=400,
                       x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
        line_chart.title = 'Memory Usage Of '+nodeName+' For Last Day'
	dataset_avg=createDataset(data_average_day)
	dataset_max=createDataset(data_max_day)

        line_chart.add('Virt Tot. ',dataset_avg[3],fill=True)
        line_chart.add('Phys Tot. ',dataset_avg[1],fill=True)
        line_chart.add('Phys Mem Used Avg ',dataset_avg[0],fill=True)
        line_chart.add('Virt Mem Used Avg',dataset_avg[2],fill=True)
        line_chart.add('Phys Mem Perc.Avg ',dataset_avg[4],secondary=True)
        line_chart.add('Virt Mem Perc. Avg',dataset_avg[5],secondary=True)
        line_chart.add('Phys Mem Used Max',dataset_max[0],fill=True)
        line_chart.add('Virt Mem Used Max',dataset_max[2],fill=True)
        line_chart.add('Phys Mem Perc.Max ',dataset_max[4],secondary=True)
        line_chart.add('Virt Mem Perc. Max',dataset_max[5],secondary=True)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Memory_Daily.svg')

def createLastWeekGraph(nodeName):
        data_average_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","3600","-1w","AVERAGE")
        data_max_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","3600","-1w","MAX")
        line_chart = pygal.DateTimeLine(
                       truncate_label=-1,
                       x_label_rotation=90,
                       width=1200,height=400,
                       x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
        line_chart.title = 'Memory Usage Of '+nodeName+' For Last Week'
        dataset_avg=createDataset(data_average_day)
        dataset_max=createDataset(data_max_day)

        line_chart.add('Virt Tot. ',dataset_avg[3],fill=True)
        line_chart.add('Phys Tot. ',dataset_avg[1],fill=True)
        line_chart.add('Phys Mem Used Avg ',dataset_avg[0],fill=True)
        line_chart.add('Virt Mem Used Avg',dataset_avg[2],fill=True)
        line_chart.add('Phys Mem Perc.Avg ',dataset_avg[4],secondary=True)
        line_chart.add('Virt Mem Perc. Avg',dataset_avg[5],secondary=True)
        line_chart.add('Phys Mem Used Max',dataset_max[0],fill=True)
        line_chart.add('Virt Mem Used Max',dataset_max[2],fill=True)
        line_chart.add('Phys Mem Perc.Max ',dataset_max[4],secondary=True)
        line_chart.add('Virt Mem Perc. Max',dataset_max[5],secondary=True)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Memory_Weekly.svg')

def createLastMonthGraph(nodeName):
	data_average_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","86400","-1m","AVERAGE")
        data_max_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","86400","-1m","MAX")
        line_chart = pygal.DateTimeLine(
                       truncate_label=-1,
                       x_label_rotation=90,
                       width=1200,height=400,
                       x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
        line_chart.title = 'Memory Usage Of '+nodeName+' For Last Month'
        dataset_avg=createDataset(data_average_day)
        dataset_max=createDataset(data_max_day)

        line_chart.add('Virt Tot. ',dataset_avg[3],fill=True)
        line_chart.add('Phys Tot. ',dataset_avg[1],fill=True)
        line_chart.add('Phys Mem Used Avg ',dataset_avg[0],fill=True)
        line_chart.add('Virt Mem Used Avg',dataset_avg[2],fill=True)
        line_chart.add('Phys Mem Perc.Avg ',dataset_avg[4],secondary=True)
        line_chart.add('Virt Mem Perc. Avg',dataset_avg[5],secondary=True)
        line_chart.add('Phys Mem Used Max',dataset_max[0],fill=True)
        line_chart.add('Virt Mem Used Max',dataset_max[2],fill=True)
        line_chart.add('Phys Mem Perc.Max ',dataset_max[4],secondary=True)
        line_chart.add('Virt Mem Perc. Max',dataset_max[5],secondary=True)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Memory_Monthly.svg')

def createLastYearGraph(nodeName):
        data_average_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","604800","-1y","AVERAGE")
        data_max_day=getDataFromRRDFile('rrdFiles/Memory/'+nodeName+".rrd","604800","-1y","MAX")
        line_chart = pygal.DateTimeLine(
                       truncate_label=-1,
                       x_label_rotation=90,
                       width=1200,height=400,
                       x_value_formatter=lambda dt: dt.strftime('%d-%m-%Y %H:%M')
                )
        line_chart.title = 'Memory Usage Of '+nodeName+' For Last Year'
        dataset_avg=createDataset(data_average_day)
        dataset_max=createDataset(data_max_day)

        line_chart.add('Virt Tot. ',dataset_avg[3],fill=True)
        line_chart.add('Phys Tot. ',dataset_avg[1],fill=True)
        line_chart.add('Phys Mem Used Avg ',dataset_avg[0],fill=True)
        line_chart.add('Virt Mem Used Avg',dataset_avg[2],fill=True)
        line_chart.add('Phys Mem Perc.Avg ',dataset_avg[4],secondary=True)
        line_chart.add('Virt Mem Perc. Avg',dataset_avg[5],secondary=True)
        line_chart.add('Phys Mem Used Max',dataset_max[0],fill=True)
        line_chart.add('Virt Mem Used Max',dataset_max[2],fill=True)
        line_chart.add('Phys Mem Perc.Max ',dataset_max[4],secondary=True)
        line_chart.add('Virt Mem Perc. Max',dataset_max[5],secondary=True)

        line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Memory_Yearly.svg')


def getNodeList():
        nodeList=[]
        for name in glob.iglob('rrdFiles/Memory/*.rrd'):
                parts=name.split("/")
                node=parts[2].replace(" ","").replace(".rrd","").split("_")[0]
                nodeList.append(node)

        return list(set(nodeList))

def createMemoryReport(step):
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
