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

def getEthList(nodeName):
	ethList=[]
	for name in glob.glob('rrdFiles/Net/'+nodeName+'_*.rrd'):
		#ethList.append(name.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Eth/",""))
		ethList.append(name)
	return ethList

def createLastHourGraph(nodeName):
	ethList=getEthList(nodeName)
	last_rrd_data=[]	
	max_rrd_data=[]

        line_chart = pygal.DateTimeLine(
                truncate_label=-1,
                x_label_rotation=90,
                width=1200,height=400,
                x_value_formatter=lambda dt: dt.strftime('%H:%M')
        )

	for eth in ethList:
		data_last_hour= getDataFromRRDFile(eth,"300","-1h","LAST")	
		data_max_hour=getDataFromRRDFile(eth,"300","-1h","MAX")
		ethName=eth.replace(nodeName+"_","").replace(".rrd","").replace("rrdFiles/Net/","")
		last_rrd_data.append((ethName,data_last_hour))
		max_rrd_data.append((ethName,data_max_hour))
		

	
		
        line_chart.title = 'Int '+ethName +' Usage Of '+nodeName+' For Last Hour'
	for eth in ethList:
		line_chart.add("In.Traff: "+eth,getInTrafDatasetForEth(eth))
		line_chart.add("Out.Traff: "+eth,getOutDatasetForEth(eth))
	line_chart.add("Total Out:",getTotalInTrafDataset(ethList))
	line_chart.add("Total In:",getTotalInTrafDataset(ethList))
		

       	line_chart.render_to_file('/var/www/html/sitescopereports/svgFiles/'+nodeName+'/Eth_Hourly.svg')

def createDataset(ethDataList):
	dataset=[]
	for eth


def appendDataSet(rrdData,chart):
        resolution=rrdData[0][2]
        startTime=rrdData[0][0]+resolution
        endTime=rrdData[0][1]
        timeLine=map(getDateFromTimestamp, range(startTime,endTime,resolution))

        list=rrdData[2]
        list.pop()
        list.pop()
        dataset=getEthDataset(timeLine,list)

def getEthDataset(timeLine,list):
        dataset=[]
	in=[]
	out=[]	

        for i in range(len(timeLine)):
        	in.append((timeLine[i],list[i][0]))
		out.append((timeLine[i],list[i][1]))	

	dataset.append(in)
	dataset.append(out)

        return dataset

def createNetReports(node):
        checkDir(node)
        createLastHourGraph(node)
        createLastDayGraph(node)
        createLastWeekGraph(node)
        createLastMonthGraph(node)
        createLastYearGraph(node)
