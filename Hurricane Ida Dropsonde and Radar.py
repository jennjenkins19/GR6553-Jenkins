#%%Importing the Library

import numpy as np
import netCDF4
import matplotlib.pyplot as plt

import cartopy  #imports all of cartopy
import cartopy.feature as cf #imports the feature class
import pygrib

import cartopy.crs as ccrs
import matplotlib.gridspec as gridspec

from metpy.calc import azimuth_range_to_lat_lon
from metpy.cbook import get_test_data
from metpy.io import Level2File
from metpy.plots import add_metpy_logo, add_timestamp, USCOUNTIES
from metpy.units import units

#%% Defining Functions to help improve the speed of getting the data

#Function for the wind
def wind_function(grb,position):  #(name of the grb file,level wanted for the data)
    u_data = grb.select(name='U component of wind',level=position)[0]
    u = (u_data.values)*1.9438 #Converting from m/s to knots
    v_data = grb.select(name='V component of wind',level=position)[0]
    v = (v_data.values)*1.9438 #Converting from m/s to knots
    wind = np.hypot(u,v)
    return(u,v,wind)

#Function for determining latitude and Longitude for each flight (want the drop down location instead of top)
def lon_lat_function(dropsonde):
    latitude = dropsonde.variables['lat'][:]
    longitude = dropsonde.variables['lon'][:]
    location_miss = dropsonde.variables['lat'].missing_value
    lat = []
    long = []

    for i in range(0,len(latitude)):
        if (latitude[i] != location_miss):
            lat.append(latitude[i])

    for i in range(0,len(longitude)):
        if (longitude[i] != location_miss):
            long.append(longitude[i])
        
    final_lat = lat[-1]
    final_long = long[-1]
    
    return(final_lat,final_long)

#Function for creating a table of the dropsondes and numbers to correspond with the radar maps
def table_function(name,Flight_Points): 
    dropsonde_number = [row[0] for row in Flight_Points]
    dropsonde_ID = [row[1] for row in Flight_Points]
    cell_text = [[val_x, val_y] for val_x, val_y in zip(dropsonde_number, dropsonde_ID)]

    fig, ax = plt.subplots(figsize=(5.5,7))
    ax.axis('off')
    ax.axis('tight')

    ax.table(cellText=cell_text, colLabels=["Drop Number", "Dropsonde ID"], loc='center', cellLoc = 'center')

    plt.savefig('%s Dropsonde List.png' %(name))
    plt.show()

#%% Flight 1: 0520Z-1230Z Saturday August 28th, 20210828N1
"""Not used due to the latitude and longitude missing in the data"""

#%% Flight 2: 1955Z-0413Z Saturday August 28th-29th, 20210828I1

times = ['091908','093202','094016','094454','095057','100108','101114','104206','105043','105831','110159','111333','112119','112720','114408','115408','120338','120554','121057','122216','122821','124608','130116','133458','134738','135850','140232','140534','141540','142931']

#Looping through all of the time values to get longitude and latitude
Flight_2_Points = []
j = 1

for i in times:
    hours = str(i).zfill(6)
    filename=f'D20210828_{hours}QC.nc'
    
    #Reading in Dropsonde Data
    dropsonde = netCDF4.Dataset(filename)
    dropsonde.set_auto_mask(False)
    
    #Collecting the Locations
    lon,lat = lon_lat_function(dropsonde)
    
    data_array=[j,filename,lon,lat]
    Flight_2_Points.append(data_array)
    j = j + 1

Flight_2_Average_Time = ((2400-1955)+(413))/2  #for picking a time in the middle for the radar
Flight_2_Radar_Time = Flight_2_Average_Time + 1955

#%% Flight 3: 1955Z-0156Z Saturday August 28th, 20210828H1

"""Not used due to being in the middle of the intensification process"""      

#%% Flight 4: 0738Z-1604Z Sunday August 29th, 20210829I1

times = ['085222','090304','091416','091425','091439','091707','092626','092638','092650','093550','094605','101448','101816','102240','102300','102919','103310','104809','105849','110714','111604','111624','111821','114116','123339','123415','123607','131651','134457','135826','135934']

#Looping through all of the time values to get longitude and latitude
Flight_4_Points = []
j = 1

for i in times:
    hours = str(i).zfill(6)
    filename=f'D20210829_{hours}QC.nc'
    
    #Reading in Dropsonde Data
    dropsonde = netCDF4.Dataset(filename)
    dropsonde.set_auto_mask(False)
    
    #Collecting the Locations
    lon,lat = lon_lat_function(dropsonde)
        
    data_array=[j,filename,lon,lat]
    Flight_4_Points.append(data_array)
    j = j + 1

Flight_4_Radar_Time = (738+1604)/2  #for picking a time in the middle for the radar


#%% Flight 5: 1703Z-2320Z Saturday August 29th, 20210898H1

times = ['183656','184446','184537','184720','190732','191150','191504','192834','193750','194930','195713','200406','202610','202958','203457','204523','211838','212104']

#Looping through all of the time values to get longitude and latitude
Flight_5_Points = []
j = 1

for i in times:
    hours = str(i).zfill(6)
    filename=f'D20210829_{hours}_PQC.nc'
    
    #Reading in Dropsonde Data
    dropsonde = netCDF4.Dataset(filename)
    dropsonde.set_auto_mask(False)
    
    #Collecting the Locations
    lon,lat = lon_lat_function(dropsonde)
        
    data_array=[j,filename,lon,lat]
    Flight_5_Points.append(data_array)
    j = j + 1

Flight_5_Radar_Time = (1703+2320)/2  #for picking a time in the middle for the radar

#%% Importing the Data for Wind Field for the First Map since Radar is too far away
position = 800
grb28_12 = pygrib.open('gfs.0p25.2021082812.f000.grib2')
[grb28_12_u,grb28_12_v,grb28_12_wind] = wind_function(grb28_12,position)  #Getting the wind data

#%% General Parameters for the Wind Map
data = grb28_12.select(name='Geopotential height',level=position)[0]
grb_data = data.values
[lats,lons] = data.latlons()
extent = [-90.0,-80.0,21.0,28.0]  #long min, long max, lat min, lat max
#extent = [-88.0,-83.0,22.5,27.0]  #For zoomed version
center = [-95.0,24.5] #long, lat
#center = [-85.5,25.0]  #For zoomed version
bar_values_wind = (30,40,50,60,80,100,125,150,200)

#%% Function for plotting the data on the map

def wind_map(name,wind,U,V,Flight_Points):
    plt.figure(figsize = (6.5,7.5))
    plt.figure
    
    proj = ccrs.LambertConformal(central_longitude=center[0], central_latitude=center[1], standard_parallels=(30.0,30.0))

    ax = plt.axes(projection = proj)
    ax.set_extent([extent[0],extent[1],extent[2],extent[3]],crs=ccrs.PlateCarree())
    
    #Adding the dropsonde data locations overlay
    x = [row[3] for row in Flight_Points]  #Longitude
    y = [row[2] for row in Flight_Points]  #Latitude
    ax.scatter(x, y, color='red', marker='x', transform=ccrs.PlateCarree(), zorder=10)
    for i in range(len(x)):
        ax.text(x[i], y[i], i+1, transform=ccrs.PlateCarree(), fontsize=12, ha='right', va='bottom')
    
    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=False, linewidth=1, color='white', alpha=0.5, linestyle='--')
    gl.left_labels = True
    gl.bottom_labels = True

    #Make the Map Pretty
    ax.add_feature(cf.BORDERS,color='grey')
    ax.add_feature(cf.STATES,edgecolor ='grey')
    ax.add_feature(cf.LAND,color='wheat')
    ax.add_feature(cf.OCEAN,color='lightskyblue')
    ax.add_feature(cf.LAKES,color='lightskyblue')

    #Putting the Data on the Map
    plt.title('%s mb Isotachs (knots)\n%s'%(position,name), fontsize=12)

    plot = plt.contourf(lons,lats,wind, levels=bar_values_wind, cmap='hot_r', transform=ccrs.PlateCarree())
    mush = plt.colorbar(plot, ax=ax, orientation = 'horizontal', pad=0.05, aspect=30)  #AKA my brain is mush right now lol
    mush.set_label('Knots')
    
    plt.savefig('%s Flight 2 - Zoomed.png' %(name))
    
    plt.show()

#%% Generating the Map for Aug 28th at 1200 UTC and Table Data for all three flights
wind_map('Aug 28th, 1200UTC', grb28_12_wind, grb28_12_u, grb28_12_v, Flight_2_Points)
table_function('Flight 2',Flight_2_Points)
table_function('Flight 4',Flight_4_Points)
table_function('Flight 5',Flight_5_Points)

#%%  Radar Flight 4 KLIZ Aug 29th at 092744UTC (New Orleans, LA)

# Open the file
f = Level2File('KLIX20210829_092744_V06')  #Beginning of Flight
#f = Level2File('KLIX20210829_115456_V06') #Middle of flight
#f = Level2File('KLIX20210829_135407_V06') #End of flight

print(f.sweeps[0][0])

# Pull data out of the file
sweep = 0

# First item in ray is header, which has azimuth angle
az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])

###########################################
# We need to take the single azimuth (nominally a mid-point) we get in the data and
# convert it to be the azimuth of the boundary between rays of data, taking care to handle
# where the azimuth crosses from 0 to 360.
diff = np.diff(az)
crossed = diff < -180
diff[crossed] += 360.
avg_spacing = diff.mean()

# Convert mid-point to edge
az = (az[:-1] + az[1:]) / 2
az[crossed] += 180.

# Concatenate with overall start and end of data we calculate using the average spacing
az = np.concatenate(([az[0] - avg_spacing], az, [az[-1] + avg_spacing]))
az = units.Quantity(az, 'degrees')

###########################################
# Calculate ranges for the gates from the metadata

# 5th item is a dict mapping a var name (byte string) to a tuple of (header, data array)
ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
ref_range = (np.arange(ref_hdr.num_gates + 1) - 0.5) * ref_hdr.gate_width + ref_hdr.first_gate
ref_range = units.Quantity(ref_range, 'kilometers')
ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])

rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
rho_range = units.Quantity(rho_range, 'kilometers')
rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])

# Extract central longitude and latitude from file
cent_lon = f.sweeps[0][0][1].lon
cent_lat = f.sweeps[0][0][1].lat

###########################################
spec = gridspec.GridSpec(1, 1)
fig = plt.figure(figsize=(8,8))

for var_data, var_range, ax_rect in zip((ref, rho), (ref_range, rho_range), spec):
    # Turn into an array, then mask
    data = np.ma.array(var_data)
    data[np.isnan(data)] = np.ma.masked

    # Convert az,range to x,y
    xlocs, ylocs = azimuth_range_to_lat_lon(az, var_range, cent_lon, cent_lat)

    # Plot the data
    crs = ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=cent_lat)
    ax = fig.add_subplot(ax_rect, projection=crs)
    ax.add_feature(USCOUNTIES, linewidth=0.5)
    ax.pcolormesh(xlocs, ylocs, data, cmap='viridis', transform=ccrs.PlateCarree())
    #ax.set_extent([cent_lon - 2, cent_lon + 2, cent_lat - 3, cent_lat])   #For the Zoomed Version for degrees
    ax.set_extent([cent_lon - 3, cent_lon + 4, cent_lat - 3, cent_lat + 1])   #For the Normal Version for degrees
    ax.set_aspect('equal', 'datalim')
    
    #Scatter Plot Data for the Dropsonde Locations
    x = [row[3] for row in Flight_4_Points]
    y = [row[2] for row in Flight_4_Points]
    ax.scatter(x, y, color='red', marker='x', transform=ccrs.PlateCarree(), zorder=10)

    for i in range(len(x)):
        ax.text(x[i], y[i], i, transform=ccrs.PlateCarree(), fontsize=12, ha='right', va='bottom')

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='grey', alpha=0.5, linestyle='--')

plt.savefig('Flight 4 Radar.png')
plt.show()

#%%  Radar Flight 5 KLIZ Aug 29th at 2010244UTC (New Orleans, LA)

# Open the file
f = Level2File('KLIX20210829_201024_V06')
print(f.sweeps[0][0])

# Pull data out of the file
sweep = 0

# First item in ray is header, which has azimuth angle
az = np.array([ray[0].az_angle for ray in f.sweeps[sweep]])

###########################################
# We need to take the single azimuth (nominally a mid-point) we get in the data and
# convert it to be the azimuth of the boundary between rays of data, taking care to handle
# where the azimuth crosses from 0 to 360.
diff = np.diff(az)
crossed = diff < -180
diff[crossed] += 360.
avg_spacing = diff.mean()

# Convert mid-point to edge
az = (az[:-1] + az[1:]) / 2
az[crossed] += 180.

# Concatenate with overall start and end of data we calculate using the average spacing
az = np.concatenate(([az[0] - avg_spacing], az, [az[-1] + avg_spacing]))
az = units.Quantity(az, 'degrees')

###########################################
# Calculate ranges for the gates from the metadata

# 5th item is a dict mapping a var name (byte string) to a tuple of (header, data array)
ref_hdr = f.sweeps[sweep][0][4][b'REF'][0]
ref_range = (np.arange(ref_hdr.num_gates + 1) - 0.5) * ref_hdr.gate_width + ref_hdr.first_gate
ref_range = units.Quantity(ref_range, 'kilometers')
ref = np.array([ray[4][b'REF'][1] for ray in f.sweeps[sweep]])

rho_hdr = f.sweeps[sweep][0][4][b'RHO'][0]
rho_range = (np.arange(rho_hdr.num_gates + 1) - 0.5) * rho_hdr.gate_width + rho_hdr.first_gate
rho_range = units.Quantity(rho_range, 'kilometers')
rho = np.array([ray[4][b'RHO'][1] for ray in f.sweeps[sweep]])

# Extract central longitude and latitude from file
cent_lon = f.sweeps[0][0][1].lon
cent_lat = f.sweeps[0][0][1].lat

###########################################
spec = gridspec.GridSpec(1, 1)
fig = plt.figure(figsize=(8,8))

for var_data, var_range, ax_rect in zip((ref, rho), (ref_range, rho_range), spec):
    # Turn into an array, then mask
    data = np.ma.array(var_data)
    data[np.isnan(data)] = np.ma.masked

    # Convert az,range to x,y
    xlocs, ylocs = azimuth_range_to_lat_lon(az, var_range, cent_lon, cent_lat)

    # Plot the data
    crs = ccrs.LambertConformal(central_longitude=cent_lon, central_latitude=cent_lat)
    ax = fig.add_subplot(ax_rect, projection=crs)
    ax.add_feature(USCOUNTIES, linewidth=0.5)
    ax.pcolormesh(xlocs, ylocs, data, cmap='viridis', transform=ccrs.PlateCarree())
    #ax.set_extent([cent_lon - 2, cent_lon + 2, cent_lat - 3, cent_lat])   #For the Zoomed Version for degrees
    ax.set_extent([cent_lon - 3, cent_lon + 4, cent_lat - 3, cent_lat + 1])   #For the Normal Version for degrees
    ax.set_aspect('equal', 'datalim')
    
    #Scatter Plot Data for the Dropsonde Locations
    x = [row[3] for row in Flight_5_Points]
    y = [row[2] for row in Flight_5_Points]
    ax.scatter(x, y, color='red', marker='x', transform=ccrs.PlateCarree(), zorder=10)

    for i in range(len(x)):
        ax.text(x[i], y[i], i+1, transform=ccrs.PlateCarree(), fontsize=12, ha='right', va='bottom')

    gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='grey', alpha=0.5, linestyle='--')

plt.savefig('Flight 5 Radar.png')
plt.show()


