"""

Batch AWS NEXRAD Request

Carter J. Humphreys
Email: chumphre@oswego.edu | GitHub:@HumphreysCarter | Website: http://carterhumphreys.com

For updates see: https://github.com/HumphreysCarter/AWS-NOAA-Data-Request

"""

import NEXRAD_AWS_Request as NEXRAD
import s3fs as AWSbucket
import pandas as pd
from datetime import datetime, timedelta

fs = AWSbucket.S3FileSystem(anon=True)

def getNEXRAD(outputDir, filePrefix, radarSite, startDate, endDate, interval):
    fileList = []

    # Get files from start to end date at specified interval
    while startDate <= endDate:
        dataFile = NEXRAD.getArchivedScan(radarSite, startDate)
        fileList.append(dataFile)
        startDate += interval

    for file in fileList:
        print('Downloading ', file, '...')
        fs.get(file, outputDir + filePrefix + file.split('/')[-1])

timeInt = 1


df=pd.read_csv('../events/Ontario_LES_Events_FY2015-FY2020.csv')

dataDIR='../data/NEXRAD'

for index, row in df.iterrows():
    eventID=row['Event ID']
    sdate=row['Event Begin']
    edate=row['Event End']
    sdate=datetime.strptime(sdate,'%Y-%m-%d %H:%M')
    edate=datetime.strptime(edate,'%Y-%m-%d %H:%M')

    try:
        if eventID==24:
            getNEXRAD(f'{dataDIR}/Ontario_LES_Event{str(eventID).zfill(2)}/', f'Ontario_LES_Event{str(eventID).zfill(2)}-', 'KBGM', sdate, edate, timedelta(hours=timeInt))
        else:
            getNEXRAD(f'{dataDIR}/Ontario_LES_Event{str(eventID).zfill(2)}/', f'Ontario_LES_Event{str(eventID).zfill(2)}-', 'KTYX', sdate, edate, timedelta(hours=timeInt))
    except:
        print(f'No data found: Ontario_LES_Event{str(eventID).zfill(2)}')