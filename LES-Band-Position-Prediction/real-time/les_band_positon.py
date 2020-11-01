"""
Create plots of machine learning model LES band positions
11/01/2020
--------------------------------------------------------------------------------

Copyright (c) 2020, Carter J. Humphreys (chumphre@oswego.edu)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
   
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
   
3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.
   
THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import joblib
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
import metpy.calc as mpcalc
import BUFKIT_BUFR_Parser as BUFR
from shapely.geometry import Point, LineString
from datetime import datetime
from metpy.units import units
from metpy.plots import USCOUNTIES

# Water data
ice_cover_ontario = 0.0
ice_cover_huron = 0.0
ice_cover_erie = 0.0
water_temperature = 11.8 * units.degC

# Model parameters
station = 'LO1'
model   = 'RAP'

# Get BUFR data
BUFR_data=BUFR.getBUFR_data(station, model, sounding=True, surface=False)

# Get model profiles
dataset = pd.DataFrame()
profiles = model_data = BUFR_data['sounding']['PROFILE']
for (i, model_data) in zip(range(len(profiles)), profiles):

    # Added desired levels
    desired_levels = [925, 850, 700, 500]
    for level in desired_levels:
        row = [{'PRES':level, 'TMPC':np.nan, 'TMWC':np.nan, 'DWPC':np.nan, 'THTE':np.nan, 'DRCT':np.nan, 'SKNT':np.nan, 'OMEG':np.nan, 'CFRL':np.nan, 'HGHT':np.nan}]
        model_data=model_data.append(row, ignore_index=True)   

    # Sort and interpolate missing values
    model_data = model_data.sort_values(['PRES'], ascending=False)
    model_data = model_data.interpolate()

    # Select only desired levels
    model_data = model_data[model_data.PRES.isin(desired_levels)]

    # Pull model variables
    z_data = model_data.HGHT.to_list() * BUFR.getParameterUnit('HGHT')
    p_data = model_data.PRES.to_list() * BUFR.getParameterUnit('PRES')
    T_data = model_data.TMPC.to_list() * BUFR.getParameterUnit('TMPC')
    Td_data = model_data.DWPC.to_list() * BUFR.getParameterUnit('TMPC')
    WD_data = model_data.DRCT.to_list() * BUFR.getParameterUnit('DRCT')
    WS_data = model_data.SKNT.to_list() * BUFR.getParameterUnit('SKNT')
    u_data, v_data = mpcalc.wind_components(WS_data, WD_data)

    # Derive data and build dataset
    inital_data = {'DateTime':BUFR_data['sounding'].TIME[i], 'OntarioT':water_temperature.magnitude, 'OntarioIce':ice_cover_ontario, 'HuronIce':ice_cover_huron, 'ErieIce':ice_cover_erie}
    df = pd.DataFrame([inital_data])
    for i, z, p, T, Td, u, v in zip(range(len(z_data)), z_data, p_data, T_data, Td_data, u_data, v_data):

        # Add height
        df[f'{int(p.magnitude)}_hPa_z'] = [z.magnitude]

        # Add air temperature
        df[f'{int(p.magnitude)}_hPa_T'] = [T.magnitude]

        # Calculate lapse-rate from water if > 500 hPa
        if p > (500*units.hPa):
            gamma_water = -((T-water_temperature)/z).to('degC/km')
            df[f'{int(p.magnitude)}_hPa_Γwater'] = [gamma_water.magnitude]

        # Calculate RH
        rh = mpcalc.relative_humidity_from_dewpoint(T, Td)
        df[f'{int(p.magnitude)}_hPa_RH'] = [rh.magnitude*100]

        # Add u and v components
        df[f'{int(p.magnitude)}_hPa_u'] = [u.magnitude]
        df[f'{int(p.magnitude)}_hPa_v'] = [v.magnitude]

        # Derive bulk shear (except at first level)
        if p != p_data[0]:
            u_shear, v_shear = mpcalc.bulk_shear(p_data, u_data, v_data, bottom=p_data[0], depth=p_data[0]-p_data[i])
            bulk_shear = mpcalc.wind_speed(u_shear, v_shear)
            df[f'{int(p_data[0].magnitude)}-{int(p.magnitude)}_hPa_shear'] = [bulk_shear.magnitude]
            
    # Append to main dataset
    dataset = dataset.append(df)
    
# Load in model 
ai_model=joblib.load('../models/LES_Band_Position_Model_KNN(n=2)_LO1_LatLon')

# Get predictions from machine learning model
predictions = pd.DataFrame()
for (time, inputData) in zip(dataset.DateTime, dataset.values[:, 1:]):
    
    # Get model prediction
    prediction=ai_model.predict([inputData])[0]

    # Generate coordiante list from prediction
    data={'DateTime':time}
    for i in range(0, len(prediction), 2):
        
        lat, lon = prediction[i], prediction[i+1]       
        data[f'Point{int(i/2)}'] = Point(lon, lat)
                      
    predictions = predictions.append([data], ignore_index=True)
    
# Get maps for each frame
for (i, time, points) in zip(range(len(predictions.DateTime)), predictions.DateTime, predictions.values[:, 1:]):
    
    print(f'Plotting positions valid {time} ...')
    
    # Covenrt to LineString
    points = LineString(points)
    
    # Setup plot
    fig = plt.figure(figsize=(18, 10))

    # Generate Cartopy projections
    crs=ccrs.PlateCarree()
    domain=[-78.5, -73.5, 42.5, 45]
    proj = ccrs.Stereographic(central_longitude=(domain[1]-domain[0])/2+domain[0], central_latitude=(domain[3]-domain[2])/2+domain[2])
    ax = fig.add_subplot(1, 1, 1, projection=proj)
    ax.set_extent(domain, crs=crs)

    # Plot line
    plt.plot(*points.xy, 'k', *points.xy, 'bo', marker='o', linewidth=3, markersize=10, transform=crs)

    # Add geographic features
    country_borders=cfeature.NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='10m', facecolor='none')
    ax.add_feature(country_borders, edgecolor='black', linewidth=1.0)
    state_borders=cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lakes', scale='10m', facecolor='none')
    ax.add_feature(state_borders, edgecolor='black', linewidth=0.5)
    ax.add_feature(USCOUNTIES.with_scale('5m'), edgecolor='black', linewidth=0.1)

    # Add Headers
    rdate = predictions.DateTime[0]
    vdate = time
    plt.title(f'{model}-based LES Band Position from Machine Learning Algorithm\n{ai_model}', loc='left')
    plt.title(f'Run: {rdate.strftime("%a %Y-%m-%d %H:%M")} UTC\nValid: {vdate.strftime("%a %Y-%m-%d %H:%M")} UTC', loc='right')

    # Export
    plt.savefig(f'plots/LES_Band_Position_{str(i).zfill(2)}.jpg', bbox_inches='tight', dpi=100)
    plt.close()
    plt.clf