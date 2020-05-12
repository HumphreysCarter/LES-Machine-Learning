"""

BUFR File Request

Carter J. Humphreys
Email: chumphre@oswego.edu | GitHub:@HumphreysCarter | Website: http://carterhumphreys.com

For updates see: https://github.com/HumphreysCarter/BUFR-Data-Parser

"""

import BUFR_Request as BUFKIT
import pandas as pd
import metpy.calc as mpcalc
import SkewT

from datetime import datetime, timedelta
from metpy.units import units

def LinearInterpolation(x, x1, x2, y1, y2):
    return y1+(x-x1)*((y2-y1)/(x2-x1))

def getDataFrame_UpperAir(model, station, init, hour):
    bufrData = BUFKIT.getBufkitData(model, station, init)

    if bufrData != False: # Verify data found
        modelSoundings = bufrData.SoundingParameters
        surfaceData = bufrData.SurfaceParameters[hour]
        soundingData = modelSoundings[hour+1]

        z = [0* units.meters]
        p = [surfaceData.pres]
        T = [surfaceData.t2ms]
        Td = [surfaceData.td2m]
        #Tw = [mpcalc.wet_bulb_temperature(surfaceData.pres, surfaceData.t2ms, surfaceData.td2m)]
        theta = [mpcalc.potential_temperature(surfaceData.pres, surfaceData.t2ms)]
        theta_e = [mpcalc.equivalent_potential_temperature(surfaceData.pres, surfaceData.t2ms, surfaceData.td2m)]
        u = [surfaceData.uwnd]
        v = [surfaceData.vwnd]

        for level in soundingData:
            z.append(level.hght)
            p.append(level.pres)
            T.append(level.tmpc)
            Td.append(level.dwpc)
            #Tw.append(mpcalc.wet_bulb_temperature(level.pres, level.tmpc, level.dwpc))
            theta.append(mpcalc.potential_temperature(level.pres, level.tmpc))
            theta_e.append(mpcalc.equivalent_potential_temperature(level.pres, level.tmpc, level.dwpc))
            uv = mpcalc.wind_components(level.sknt, level.drct)
            u.append(uv[0])
            v.append(uv[1])

        return pd.DataFrame(list(zip(z, p, T, Td, theta, theta_e, u, v)), columns =['height', 'pressure', 'temperature', 'dewpoint', 'theta', 'theta_e', 'u_wind', 'v_wind'])
    else:
        return False

def getData(model, station, time, fileExport=False, exportPath=''):

    df = getDataFrame_UpperAir(model, station, time, 0)

    try: # Verify data found
        df.head
        print(f'Reading {model} profile for {station} valid {time}')
    except:
        print(f'ERROR reading {model} profile for {station} valid {time}. No data found')
        return None

    if station == 'LO1':
        plot = SkewT.drawSkewT([model, time, 0, station, df], 10, 10, 100, True, 250, True, False, False, True, True)
        plotPath=exportPath.replace('data/BUFKIT', 'plots/SkewT')
        plotPath=plotPath.replace('.csv', time.strftime("_SkewT_%Y%m%d_%H%M")+'.png')
        plot.savefig(plotPath, bbox_inches='tight')

    pblHeight=0
    dgzLayer=[-999,-999]
    desiredLevels=[[925.00*units.hPa, False], [850.00*units.hPa, False], [700.00*units.hPa, False], [500.00*units.hPa, False]]

    dataString=f'{model},{station},{time}'

    z = df['height'].values
    p = df['pressure'].values
    T = df['temperature'].values
    Td = df['dewpoint'].values
    theta = df['theta'].values
    theta_e = df['theta_e'].values
    u = df['u_wind'].values
    v = df['v_wind'].values

    for i in range(len(z)):

        if i > 0:

            # Calculate temperature lapse-rate
            dT = T[i] - T[i-1]
            dz = (z[i] - z[i-1]).to('km')
            dT_dz = dT/dz

            # Calculate dewpoint lapse-rate
            dTd = Td[i] - Td[i-1]
            dTd_dz = dTd/dz

            # Calculate potential temperature lapse-rate
            thetaLwr=mpcalc.potential_temperature(p[i-1], T[i-1])
            thetaUpr=mpcalc.potential_temperature(p[i], T[i])
            dTheta_dz = (thetaUpr - thetaLwr) / dz

            # Calculate equivalent potential temperature lapse-rate
            theta_eLwr=mpcalc.equivalent_potential_temperature(p[i-1], T[i-1], Td[i-1])
            theta_eUpr=mpcalc.equivalent_potential_temperature(p[i], T[i], Td[i])
            dThetaE_dz = (theta_eUpr - theta_eLwr) / dz

            #print(p[i], z[i], dT_dz, dTd_dz, dTheta_dz, dThetaE_dz)

            # Find PBL height
            # Look for where (dT/dz >= -9.8 and dθ/dz >= 0) or (dθ/dz >= 0.0 and dθ-e/dz >= 2)
            if (((dT_dz.magnitude >= -5.7) and (dTheta_dz.magnitude >= 0.0)) or ((dTheta_dz.magnitude >= 0.0) and (dThetaE_dz.magnitude >= 2.0))) and pblHeight==0:
                pblHeight=z[i]
                #print('*****', p[i], z[i], dT_dz, dTheta_dz, dThetaE_dz)

            # Find DGZ layer
            if (-18.0 <= T[i].magnitude <= -12.0):
                # Update lower bound if not set
                if dgzLayer[0] == -999:
                    dgzLayer[0] = p[i]
                # Update upper bound
                dgzLayer[1] = p[i]

            # Extract values at desired levels
            for dataLevel in desiredLevels:
                if (p[i-1] >= dataLevel[0]) and (p[i] <= dataLevel[0]) and dataLevel[1]==False:

                    # Interpolate values to data level
                    tmpc=LinearInterpolation(dataLevel[0], p[i-1], p[i], T[i-1], T[i])
                    dwpc=LinearInterpolation(dataLevel[0], p[i-1], p[i], Td[i-1], Td[i])
                    hght=LinearInterpolation(dataLevel[0], p[i-1], p[i], z[i-1], z[i])

                    # RH from dewpoint
                    relh=mpcalc.relative_humidity_from_dewpoint(tmpc, dwpc).to('percent')

                    # Calculate wind vector and interpolate values to data level
                    uwnd=LinearInterpolation(dataLevel[0], p[i-1], p[i], u[i-1], u[i])
                    vwnd=LinearInterpolation(dataLevel[0], p[i-1], p[i], v[i-1], v[i])

                    # Wind speed/direction from u,v
                    drct=mpcalc.wind_direction(uwnd, vwnd)
                    sknt=mpcalc.wind_speed(uwnd, vwnd)

                    # Output values
                    dataString+=f',{round(hght.magnitude, 2)},{round(tmpc.magnitude, 2)},{round(relh.magnitude, 2)},{round(uwnd.magnitude, 2)},{round(vwnd.magnitude, 2)}'
                    dataLevel[1]=True

            # Derived quantities
            #dataString+=f',{round(pblHeight.magnitude, 2)}'


        # Go to next level
        i+=1

    # Export to file
    if fileExport and exportPath != '':
        file=open(exportPath,'a+')
        file.write(dataString+'\n')
        file.close()

    dataString=''


#    for level in bufrData.rows:
#
#        # Setup Layers for calculations
#        dataLayers=[[0*units.meter, pblHeight], dgzLayer]
#
#        # Do layer calculations
#        for layer in dataLayers:
#            qtySum=0 * units.dimensionless
#            delta=0 * units.dimensionless
#
#            upperLimit=layer[1]
#            lowerLimit=layer[0]
#            delta=upperLimit-lowerLimit
#
#            for level in initSounding:
#                pres = level.pres
#                hght = level.hght
#                theta=mpcalc.potential_temperature(pres, tmpc)
#
#                if (lowerLimit.units == units.meters) and (lowerLimit <= hght <= upperLimit):
#                    qtySum+=level.tmpc.magnitude
#
#                if (lowerLimit.units == units.hPa) and (lowerLimit <= pres <= upperLimit):
#                    qtySum+=level.tmpc.magnitude
#
#            if qtySum!=0.0 and delta.magnitude!=0.0:
#                layerMean = qtySum / delta.magnitude


def batchRequest(model, station, startDate, endDate, interval, fileExport=False, exportPath=''):
    if fileExport and exportPath != '':
        file=open(exportPath,'w+')
        file.write('model,station,time [UTC],z_925mb [m],T_925mb [degC],RH_925mb [%],u_925mb [kt],v_925mb [kt],z_850mb [m],T_850mb [degC],RH_850mb [%],u_850mb [kt],v_850mb [kt],z_700mb [m],T_700mb [degC],RH_700mb [%],u_700mb [kt],v_700mb [kt],z_500mb [m],T_500mb [degC],RH_500mb [%],u_500mb [kt],v_500mb [kt]\n')
        file.close()

    while startDate <= endDate:
        getData(model, station, startDate, fileExport, exportPath)
        startDate += interval

model = 'RAP'
stationList = ['LO1', 'LO2', 'KSYR', 'KART', 'KUCA', 'KROC', 'KIAG', 'CYYZ', 'CYPQ', 'CYHM', 'CYQA', 'GNB', 'LE3', 'OGS', 'RME', 'GTB']
df=pd.read_csv('../events/Ontario_LES_case_list_FY2015-19.csv')

for station in stationList:
    dataDIR='../data/BUFKIT'

    for index, row in df.iterrows():
        eventID=row['Event ID']
        sdate=row['Event Begin']
        edate=row['Event End']
        sdate=datetime.strptime(sdate,'%Y-%m-%d %H:%M')
        edate=datetime.strptime(edate,'%Y-%m-%d %H:%M')

        batchRequest(model, station, sdate, edate, timedelta(hours=1), True, f'{dataDIR}/Ontario_LES_Event{str(eventID).zfill(2)}/Ontario_LES_Event{str(eventID).zfill(2)}_{model}_{station}.csv')




