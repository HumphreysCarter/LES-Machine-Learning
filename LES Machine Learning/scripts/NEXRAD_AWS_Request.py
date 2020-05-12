"""

AWS NEXRAD Request

Carter J. Humphreys
Email: chumphre@oswego.edu | GitHub:@HumphreysCarter | Website: http://carterhumphreys.com

For updates see: https://github.com/HumphreysCarter/AWS-NOAA-Data-Request

"""

from datetime import datetime, timedelta
import s3fs
import numpy as np
import os

# Use the anonymous credentials to access public data
fs = s3fs.S3FileSystem(anon=True)

def getLatestScan(radarSite, download=False, path='', name=''):
    # List contents of NOAA NEXRAD L2 bucket
    radarBin = np.array(fs.ls('s3://noaa-nexrad-level2/'))

    # Get latest year (Subtract 2 to remove index.html)
    radarBin = np.array(fs.ls(radarBin[len(radarBin)-2]))

    # Get latest month
    radarBin = np.array(fs.ls(radarBin[len(radarBin)-1]))

    # Get latest day
    radarBin = np.array(fs.ls(radarBin[len(radarBin)-1] + '/' + radarSite))

    # Get latest file
    radarBin = np.array(fs.ls(radarBin[len(radarBin)-1]))
    latestScan = radarBin[0].replace('_MDM', '')

    # Download scan
    fileName=latestScan[latestScan.rindex('/'):]
    if download and os.path.exists(path):
        if name == '':
            if os.path.exists(f'{path}/{fileName}') == False:
                fs.get(latestScan, f'{path}/{fileName}')
        else:
            fileName=name
            fs.get(latestScan, f'{path}/{name}')

    return fileName


def getArchivedScan(radarSite, time):
    # List contents of NOAA NEXRAD L2 bucket for given date/time and radar
    radarBin = np.array(fs.ls('s3://noaa-nexrad-level2/' + time.strftime('%Y/%m/%d') + '/' + radarSite + '/'))

    closestScan=radarBin[0]
    closestScanTime=99999
    for scan in radarBin:

        if '.ta' not in scan and '_MDM' not in scan:
            # Capture time from scan
            s = scan.rfind('/') + 1
            e = scan.rfind('_V06')

            scanTime = datetime.strptime(scan[s:e], radarSite+'%Y%m%d_%H%M%S')

            # Find closest scan
            timeDif = scanTime-time
            if (abs(timeDif.total_seconds())<=closestScanTime):
                closestScanTime = abs(timeDif.total_seconds())
                closestScan = scan

    return closestScan








