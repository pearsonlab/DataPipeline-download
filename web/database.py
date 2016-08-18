#!/usr/bin/env python
from __future__ import print_function

import json
import urllib
import boto3
import datetime
import pymysql
import logging
import rds_config
import sys
import boto3
import os.path
import os
import queryDynamo

s3BucketEDF = rds_config.s3BucketEDF
localFolder = rds_config.localFolder

def rds_handler():
    #rds settings
    rds_host = rds_config.rds_host
    name = rds_config.db_username
    password = rds_config.db_password
    db_name = rds_config.db_name
    port = rds_config.port

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logging.basicConfig()

    print('Loading function')

    #RDS connection stuff
    server_address = (rds_host, port)
    try:
        conn = pymysql.connect(rds_host, user=name, passwd=password, db=db_name, connect_timeout=5)
    except:
        logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
        sys.exit()

    logger.info("SUCCESS: Connection to RDS mysql instance succeeded")
    # dateRange()

    ch = "="
    for i in range(0,5):
        ch = ch+"="
        print(ch, end='')
    print("")
    return conn

# download using time range
def timeRange(start, stop):
    rds_handler()
    conn = rds_handler()
    with conn.cursor() as cur:
        cur = conn.cursor()
        query = ("SELECT ObjectKey, StartTime, StopTime FROM edfPatientInfo WHERE StartTime >= %s AND StopTime <= %s")
        cur.execute(query, (start, stop))
        data = cur.fetchall()
        if not data:
        	print("There are no data in this range")
        else:
        	if data!= None:
        		print("Downloading data ...")
        	else:
        		print("Couldn't download data")
        for i in data:
            objectKey = i[0]
            startTime = i[1]
            stopTime = i[2]
            print("Downloading: ", objectKey, startTime, stopTime)
            downloadFile(objectKey)
            queryDynamo.timeRange(str(startTime), str(stopTime))

# download using participant name
def patientID(participantId):
    rds_handler()
    conn = rds_handler()

    with conn.cursor() as cur:
        cur = conn.cursor()
        query = ("SELECT ObjectKey, StartTime, StopTime FROM edfPatientInfo WHERE PatientID=%s")
        cur.execute(query, (participantId))
        data = cur.fetchall()
        if not data:
            print("There are no data in this range")
        else:
            if data!= None:
                print("Downloading data ...")
            else:
                print("Couldn't download data")
        for i in data:
            objectKey = i[0]
            startTime = i[1]
            stopTime = i[2]
            print("Downloading: ", objectKey, startTime, stopTime)
            downloadFile(objectKey)
            queryDynamo.timeRange(str(startTime), str(stopTime))

def downloadFile(fileObject):
    s3 = boto3.resource('s3')
    cwd = os.getcwd()
    folder = localFolder
    filename = fileObject.split("/")[1]
    download_destination = os.path.join(cwd, folder, filename)
    if not os.path.exists(os.path.dirname(download_destination)):
        os.makedirs(os.path.dirname(download_destination))
        s3.Object(s3BucketEDF, fileObject).download_file(download_destination)
    else:
        s3.Object(s3BucketEDF, fileObject).download_file(download_destination)
        

def dateTimeConvertor(day, time):
    Hours = time
    Minutes = 60 * (Hours % 1)
    Seconds = 60 * (Minutes % 1)
    timeq =  ("%d:%02d:%02d" % (Hours, Minutes, Seconds))
    
    start_date = "2000-01-01"
    date_1 = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end_date = date_1 + datetime.timedelta(days = day, hours = Hours, minutes = Minutes, seconds = Seconds)
    return end_date

if __name__ == '__main__':
    rds_handler()
