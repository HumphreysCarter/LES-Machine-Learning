# Make plot of RAP profile sites

# Carter J. Humphreys
# Email: chumphre@oswego.edu | GitHub:@HumphreysCarter | Website: http://carterhumphreys.com

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from metpy.plots import USCOUNTIES

# Plot extent
plotExtent = [-81, -74.5, 42.3, 45.3]

# Create the figure and an axes set to the projection
proj = ccrs.Stereographic(central_longitude=((plotExtent[1]-plotExtent[0])/2+plotExtent[0]), central_latitude=((plotExtent[3]-plotExtent[2])/2+plotExtent[2]))
fig = plt.figure(figsize=(15, 15))
ax = fig.add_subplot(1, 1, 1, projection=proj)
ax.set_extent(plotExtent)

# Add geographic features
ax.add_feature(USCOUNTIES.with_scale('500k'), edgecolor='gray', linewidth=0.25)
state_borders = cfeature.NaturalEarthFeature(category='cultural', name='admin_1_states_provinces_lakes', scale='50m', facecolor='none')
ax.add_feature(state_borders, edgecolor='black', linewidth=0.5)
country_borders = cfeature.NaturalEarthFeature(category='cultural', name='admin_0_countries', scale='50m', facecolor='none')
ax.add_feature(country_borders, edgecolor='black', linewidth=1.0)

# Plot Points
markerSymbol='o'
markerSize=100
# Lake Enviroment
ax.scatter(-77.41, 43.62, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='b') # LO1
ax.scatter(-79.45, 43.40, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='b') # LO2

# Near-Lake Enviroment
#ax.scatter(-76.51, 43.45, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # OSW
ax.scatter(-76.01, 44.00, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # KART
ax.scatter(-77.67, 43.12, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # KROC
ax.scatter(-78.94, 43.10, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # KIAG
ax.scatter(-79.63, 43.67, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # CYYZ
ax.scatter(-78.37, 44.23, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='g') # CYPQ

# Downstream Enviroment
#ax.scatter(-77.05, 42.64, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # KPEO
ax.scatter(-75.46, 43.47, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # RME
ax.scatter(-75.73, 44.05, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # GTB
ax.scatter(-76.12, 43.12, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # KSYR
ax.scatter(-75.37, 43.15, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # KUCA
#ax.scatter(-75.68, 43.76, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # MTG
ax.scatter(-75.47, 44.68, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='y') # OGS

# Upstream Enviroment
ax.scatter(-79.93, 43.17, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='r') # CYHM
ax.scatter(-79.30, 44.97, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='r') # CYQA
ax.scatter(-80.42, 44.92, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='r') # GNB
ax.scatter(-79.35, 42.74, transform=ccrs.PlateCarree(), marker=markerSymbol, s=markerSize, c='r') # LE3


# Set a title and show the plot
ax.set_title('RAP BUFKIT Profile Sites', loc='Left')

# Export fig
fig.savefig('/home/CarterHumphreys/research/les_neural_network/plots/RAP_Profile_Sites.png', bbox_inches='tight', dpi=100)
