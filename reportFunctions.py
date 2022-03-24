#!/usr/bin/python 

import datetime
import os
import time
import rrdtool
import pytz
from pytz import timezone


os.chdir('/opt/scripts/sitescopeReport')

def getDataFromRRDFile(rrdFile,resolution,startTime,metricType):

	try:
		data= rrdtool.fetch(rrdFile,
                     metricType,
                     "-r",
                     resolution,
                    "-s",
	             startTime
                     )
		return data
	except rrdtool.error, e:
                        print e	

def getDateHour(timestamp):
	return datetime.datetime.fromtimestamp(timestamp).strftime('%d-%m-%Y %H:%M')

def getDateFromTimestamp(timestamp):

	return timestamp+10800 
	
        #return datetime.datetime.fromtimestamp(timestamp)

def getDataset(index,data):
	dset=[]
	for d in data:
		dset.append(d[index])	
	return dset

def getDatasetForMemory(list,type):
        dset=[]
	
        for d in list:
		if (type=='pmu'):
			a=100.0-double(list[2])
                dset.append(d[index])
        return dset

	
