from __future__ import print_function
import boto3
import json
import datetime
import database
import sys
import os.path
import os
import dynamo_config

client = boto3.client('dynamodb')

tableName = dynamo_config.table_name
s3Bucket = dynamo_config.s3_bucket

# getting the json file based on the experiment name
# passing date-time range for corresponding experiment's name
def experimentName(exptName):
    response = client.query(
        TableName=tableName,
        Select='ALL_ATTRIBUTES',
        ConsistentRead=True,
        KeyConditions={
            'experiment': {
                'AttributeValueList': [
                    {
                        'S': exptName,
                    },
                ],
                'ComparisonOperator': 'EQ'
            }
        },
    )
    output = response["Items"]
    dictionary = output[0]
    startValue = str(dictionary["start time"]["S"])
    stopValue = str(dictionary["stop time"]["S"])
    fileName = str(dictionary["file name"]["S"])
    # day = int(dictionary["stop time"]["N"])

    startDate = datetime.datetime.strptime(startValue, "%Y-%m-%d %H:%M:%S")
    stopDate = datetime.datetime.strptime(stopValue, "%Y-%m-%d %H:%M:%S")
    database.timeRange(startDate, stopDate)
    downloadFile(fileName)

# passing date-time range to download the json file along with .chn file
def timeRange(start, stop):
    response = client.scan(
        TableName=tableName,
        Select='ALL_ATTRIBUTES',
        ScanFilter={
            'start time': {
                'AttributeValueList': [
                    {
                        'S': start,
                    },
                ],
                'ComparisonOperator': 'GE'
            },
            'stop time': {
                'AttributeValueList': [
                    {
                        'S': stop,
                    },
                ],
                'ComparisonOperator': 'LE'
            }
        }
    )
    output = response["Items"]
    for i in range(len(output)):
        dictionary = output[i]
        fileName = str(dictionary["file name"]["S"])
        print("Downloading: ", fileName)
        downloadFile(fileName)

def downloadFile(fileObject):
    s3 = boto3.resource('s3')
    cwd = os.getcwd()
    folder = "s3_download/behavioral_data"
    download_destination = os.path.join(cwd, folder, fileObject)
    if not os.path.exists(os.path.dirname(download_destination)):
        os.makedirs(os.path.dirname(download_destination))
        s3.Object(s3Bucket, fileObject).download_file(download_destination)
    else:
        s3.Object(s3Bucket, fileObject).download_file(download_destination)
