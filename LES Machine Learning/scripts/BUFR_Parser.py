"""

BUFR File Parser

Carter J. Humphreys
Email: chumphre@oswego.edu | GitHub:@HumphreysCarter | Website: http://carterhumphreys.com

For updates see: https://github.com/HumphreysCarter/BUFR-Data-Parser

"""


from metpy.units import units
from urllib.request import urlopen
from datetime import datetime

class bufkitProfile:
    def __init__(self, stnData, model, run, profileParams, profileDerived, sfcParam):
        self.stationData = stnData
        self.model = model
        self.run = run
        self.SoundingParameters = profileParams
        self.SoundingDerivedData = profileDerived
        self.SurfaceParameters = sfcParam

class SoundingParameters:
    # PRES - Pressure (hPa)
    # TMPC - Temperature (C)
    # TMWC - Wet bulb temperature (C)
    # DWPC - Dewpoint (C)
    # THTE - Equivalent potential temperature (K)
    # DRCT - Wind direction (degrees)
    # SKNT - Wind speed (knots)
    # OMEG - Vertical velocity (Pa/s)
    # CFRL - Fractional cloud coverage (percent)
    # HGHT - Height of pressure level (m)
    def __init__(self, pres, tmpc, tmwc, dwpc, thte, drct, sknt, omeg, cfrl, hght):
        self.pres = float(pres) * units.hPa
        self.tmpc = float(tmpc) * units.degC
        self.tmwc = float(tmwc) * units.degC
        self.dwpc = float(dwpc) * units.degC
        self.thte = float(thte) * units.kelvin
        self.drct = float(drct) * units.degrees
        self.sknt = float(sknt) * units.knots
        self.omeg = float(omeg) * units.Pa / units.seconds
        self.cfrl = float(cfrl) * units.percent
        self.hght = float(hght) * units.meters

class SoundingDerivedData:
    # SHOW - Showalter Index
    # LIFT - Lifted Index
    # SWET - SWET Index
    # KINX - K Index
    # LCLP - Pressure at the LCL (hPa)
    # PWAT - Precipitable water (mm)
    # TOTL - Total Totals Index
    # CAPE - CAPE (Convective Available Potential Energy)
    # LCLT - Temperature at the LCL (K)
    # CINS - CINS (Convective Inhibition)
    # EQLV - Equilibrium level (hPa)
    # LFCT - Level of free convection (hPa)
    # BRCH - Bulk Richardson number
    def __init__(self, show, lift, swet, kinx, lclp, pwat, totl, cape, lclt, cins, eqlv, lfct, brch):
        self.show = float(show) * units.dimensionless
        self.lift = float(lift) * units.dimensionless
        self.swet = float(swet) * units.dimensionless
        self.kinx = float(kinx) * units.dimensionless
        self.lclp = float(lclp) * units.hPa
        self.pwat = float(pwat) * units.mm
        self.totl = float(totl) * units.dimensionless
        self.cape = float(cape) * (units.joules / units.kg)
        self.lclt = float(lclt) * units.kelvin
        self.cins = float(cins) * (units.joules / units.kg)
        self.eqlv = float(eqlv) * units.hPa
        self.lfct = float(lfct) * units.hPa
        self.brch = float(brch) * units.dimensionless

class SurfaceParameters:
    # STN  - Station ID
    # DATE - YYMMDD/HHMM
    # PMSL - Mean sea level pressure (hPa)
    # PRES - Station pressure (hPa)
    # SKTC - Skin temperature (C)
    # STC1 - Layer 1 soil temperature (K)
    # SNFL - 1-hour accumulated snowfall (Kg/m**2)
    # WTNS - Soil moisture availability (percent)
    # P01M - 1-hour total precipitation (mm)
    # C01M - 1-hour convective precipitation (mm)
    # STC2 - Layer 2 soil temperature (K)
    # LCLD - Low cloud coverage (percent)
    # MCLD - Middle cloud coverage (percent)
    # HCLD - High cloud coverage (percent)
    # SNRA - Snow ratio from explicit cloud scheme (percent)
    # UWND - 10-meter U wind component (m/s)
    # VWND - 10-meter V wind component (m/s)
    # R01M - 1-hour accumulated surface runoff (mm)
    # BFGR - 1-hour accumulated baseflow-groundwater runoff (mm)
    # T2MS - 2-meter temperature (C)
    # Q2MS - 2-meter specific humidity
    # WXTS - Snow precipitation type (1=Snow)
    # WXTP - Ice pellets precipitation type (1=Ice pellets)
    # WXTZ - Freezing rain precipitation type (1=Freezing rain)
    # WXTR - Rain precipitation type (1=Rain)
    # USTM - U-component of storm motion (m/s)
    # VSTM - V-component of storm motion (m/s)
    # HLCY - Storm relative helicity (m**2/s**2)
    # SLLH - 1-hour surface evaporation (mm)
    # WSYM - Weather type symbol number
    # CDBP - Pressure at the base of cloud (hPa)
    # VSBK - Visibility (km)
    # TD2M - 2-meter dewpoint (C)
    def __init__(self, dataArray):
        self.stn = int(dataArray[0])
        self.date = datetime.strptime(dataArray[1], "%y%m%d/%H%M")
        self.pmsl = float(dataArray[2]) * units.hPa
        self.pres = float(dataArray[3]) * units.hPa
        self.sktc = float(dataArray[4]) * units.degC
        self.stc1 = float(dataArray[5]) * units.kelvin
        self.snfl = float(dataArray[6]) * (units.kg / (units.meter * units.meter))
        self.wtns = float(dataArray[7]) * units.percent
        self.p01m = float(dataArray[8]) * units.mm
        self.c01m = float(dataArray[9]) * units.mm
        self.stc2 = float(dataArray[10]) * units.kelvin
        self.lcld = float(dataArray[11]) * units.percent
        self.mcld = float(dataArray[12]) * units.percent
        self.hcld = float(dataArray[13]) * units.percent
        self.snra = float(dataArray[14]) * units.percent
        self.uwnd = float(dataArray[15]) * (units.meter / units.seconds)
        self.vwnd = float(dataArray[16]) * (units.meter / units.seconds)
        self.r01m = float(dataArray[17]) * units.mm
        self.bfgr = float(dataArray[18]) * units.mm
        self.t2ms = float(dataArray[19]) * units.degC
        self.q2ms = float(dataArray[20]) * units.dimensionless
        self.wxts = float(dataArray[21]) * units.dimensionless
        self.wxtp = float(dataArray[22]) * units.dimensionless
        self.wxtz = float(dataArray[23]) * units.dimensionless
        self.wxtr = float(dataArray[24]) * units.dimensionless
        self.ustm = float(dataArray[25]) * (units.meter / units.seconds)
        self.vstm = float(dataArray[26]) * (units.meter / units.seconds)
        self.hlcy = float(dataArray[27]) * ((units.meter * units.meter ) / (units.seconds * units.seconds))
        self.sllh = float(dataArray[28]) * units.mm
        self.wsym = float(dataArray[29]) * units.dimensionless
        self.cdbp = float(dataArray[30]) * units.hPa
        self.vsbk = float(dataArray[31]) * units.km
        self.td2m = float(dataArray[32]) * units.degC


def getBufkitData(model, station, run):

    # Create data URL from station and model
    if run == 'latest':
        if model == "GFS":
             dataURL = "http://www.meteo.psu.edu/bufkit/data/" + model + "/" + str(run) + "/" + model.lower() + "3_" + station.lower() + ".buf"
        else:
            dataURL = "http://www.meteo.psu.edu/bufkit/data/" + model + "/" + str(run) + "/" + model.lower() + "_" + station.lower() + ".buf"
    else:
        dataURL = "https://mtarchive.geol.iastate.edu/" + run.strftime('%Y/%m/%d/bufkit/%H') + "/" + model.lower() + "/" + model.lower() + '_' + station.lower() + ".buf"

    try:
        fileData = urlopen(dataURL)

        # BUFKIT profile object data arrays
        profileParams  = []
        profileDerived = []
        sfcParams      = []

        dataString = ""
        captureData_sdg = False
        captureData_sfc = False
        firstRun_sfc = True
        timeCaptured = False
        runTime  = -9999
        tempData = []
        sdgProfile = []

        # Parse each line in data file
        for line in fileData:
            # Remove HTML data
            line = str(line).replace("b'", "").replace("\\r\\n'", "")

            # Capture Run Time
            if timeCaptured == False and ("TIME = " in line):
                runTime = datetime.strptime(line[line.index("TIME = ")+7:].strip(), "%y%m%d/%H%M")
                timeCaptured = True

            #
            # Find Sounding Data Section
            if "TMPC" in line:
                captureData_sdg = True

            # Capture sounding data and create data string
            if captureData_sdg and ("TMPC" in line) == False and line.strip():

                if '' == line or 'STN' in line:
                    captureData_sdg = False
                    profileParams.append(sdgProfile)
                    sdgProfile = []

                elif 'CFRL' not in line:
                    dataArray = line.split(' ')

                    if len(dataArray) == 2:
                        soundingProfile = SoundingParameters(tempData[0], tempData[1], tempData[2], tempData[3], tempData[4], tempData[5], tempData[6], tempData[7], dataArray[0], dataArray[1])
                        sdgProfile.append(soundingProfile)
                        tempData = []
                    else:
                        tempData = dataArray


            #
            # Find Sfc Data Section
            if "TD2M" in line:
                captureData_sfc = True

            # Capture surface data and create data string
            if captureData_sfc and ("TD2M" in line) == False and line.strip():

                # Search for start character and parse data
                if "/" in line or "" == line:
                    if not firstRun_sfc:
                        sfcParam = SurfaceParameters(dataString.split(";"))
                        sfcParams.append(sfcParam)

                    firstRun_sfc = False
                    dataString = line.replace("  ", " ").replace(" ", ";") + ";"
                else:
                    dataString += line.replace("  ", " ").replace(" ", ";") + ";"

        # Create BUFKIT profile object from data
        BUFKITprofile = bufkitProfile(station, model, runTime, profileParams, profileDerived, sfcParams)
        return BUFKITprofile

    except:
        print ('ERROR: No BUFKIT profiles found for ' + dataURL)
        return False


