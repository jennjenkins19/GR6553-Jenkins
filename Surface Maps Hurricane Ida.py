#%% Importing the Library

import matplotlib.pyplot as plt
import numpy as np
import pygrib
import cartopy  #imports all of cartopy
import cartopy.feature as cf #imports the feature class
import cartopy.crs as ccrs  #imports the coordinate reference system

#%% Importing the Data

grb28_00 = pygrib.open('gfs.0p25.2021082800.f000.grib2')
grb28_06 = pygrib.open('gfs.0p25.2021082806.f000.grib2')
grb28_12 = pygrib.open('gfs.0p25.2021082812.f000.grib2')
grb28_18 = pygrib.open('gfs.0p25.2021082818.f000.grib2')
grb29_00 = pygrib.open('gfs.0p25.2021082900.f000.grib2')
grb29_06 = pygrib.open('gfs.0p25.2021082906.f000.grib2')
grb29_12 = pygrib.open('gfs.0p25.2021082912.f000.grib2')
grb29_18 = pygrib.open('gfs.0p25.2021082918.f000.grib2')

#%% Defining Functions to help improve the speed of getting the data

#Function for the wind
def wind_function(grb,position):  #(name of the grb file,level wanted for the data)
    u_data = grb.select(name='U component of wind',level=position)[0]
    u = (u_data.values)*1.9438 #Converting from m/s to knots
    v_data = grb.select(name='V component of wind',level=position)[0]
    v = (v_data.values)*1.9438 #Converting from m/s to knots
    wind = np.hypot(u,v)
    return(u,v,wind)

#Function for the Geopotential Height
def geopotential_function(grb,position): #(name of the grb file,level wanted for the data)
    height_data = grb.select(name='Geopotential height',level=position)[0]
    height = (height_data.values) /10 #converting from m to dm
    return(height)

#%% Getting the wind data, using the function

position = 800
[grb28_00_u,grb28_00_v,grb28_00_wind] = wind_function(grb28_00,position)
[grb28_06_u,grb28_06_v,grb28_06_wind] = wind_function(grb28_06,position)
[grb28_12_u,grb28_12_v,grb28_12_wind] = wind_function(grb28_12,position)
[grb28_18_u,grb28_18_v,grb28_18_wind] = wind_function(grb28_18,position)
[grb29_00_u,grb29_00_v,grb29_00_wind] = wind_function(grb29_00,position)
[grb29_06_u,grb29_06_v,grb29_06_wind] = wind_function(grb29_06,position)
[grb29_12_u,grb29_12_v,grb29_12_wind] = wind_function(grb29_12,position)
[grb29_18_u,grb29_18_v,grb29_18_wind] = wind_function(grb29_18,position)

#%% Getting the Geopotential Height Data, using the function

position = 800
grb28_00_height = geopotential_function(grb28_00,position)
grb28_06_height = geopotential_function(grb28_06,position)
grb28_12_height = geopotential_function(grb28_12,position)
grb28_18_height = geopotential_function(grb28_18,position)
grb29_00_height = geopotential_function(grb29_00,position)
grb29_06_height = geopotential_function(grb29_06,position)
grb29_12_height = geopotential_function(grb29_12,position)
grb29_18_height = geopotential_function(grb29_18,position)

#%% General Parameters so I don't need to duplicate

data = grb28_00.select(name='Geopotential height',level=position)[0]
grb_data = data.values
[lats,lons] = data.latlons()
extent = [-100.0,-80.0,18.0,33.0]  #long min, long max, lat min, lat max
center = [-90.0,26.0] #long, lat
bar_values_wind = (30,40,50,60,80,100,125,150,200)
bar_values_GH = np.arange(grb_data.min()/10,grb_data.max()/10,5)


#%% Function for plotting the data on the map

def wind_map(name,GH,wind,U,V):
    plt.figure(figsize = (5.5,6.0))
    
    plt.figure
    
    proj = ccrs.LambertConformal(central_longitude=center[0], central_latitude=center[1], standard_parallels=(30.0,30.0))

    ax = plt.axes(projection = proj)
    ax.set_extent([extent[0],extent[1],extent[2],extent[3]],crs=ccrs.PlateCarree())
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
    plt.title('%s mb Heights (dm)/ Isotachs (knots)\n%s'%(position,name), fontsize=12)

    plot = plt.contour(lons,lats,GH, levels=bar_values_GH, linewidth = 0.005, colors='black', transform=ccrs.PlateCarree())
    plot = plt.contourf(lons,lats,wind, levels=bar_values_wind, cmap='hot_r', transform=ccrs.PlateCarree())
    mush = plt.colorbar(plot, ax=ax, orientation = 'horizontal', pad=0.05, aspect=30)  #AKA my brain is mush right now lol
    mush.set_label('Knots')

    ax.barbs(lons[::7,::7],lats[::7,::7],U[::7,::7],V[::7,::7], transform=ccrs.PlateCarree())
    
    plt.savefig('%s.png' %(name))
    
    plt.show()

#%%Generating the Maps

wind_map('Aug 28th, 0000UTC', grb28_00_height, grb28_00_wind, grb28_00_u, grb28_00_v)
wind_map('Aug 28th, 0600UTC', grb28_06_height, grb28_06_wind, grb28_06_u, grb28_06_v)
wind_map('Aug 28th, 1200UTC', grb28_12_height, grb28_12_wind, grb28_12_u, grb28_12_v)
wind_map('Aug 28th, 1800UTC', grb28_18_height, grb28_18_wind, grb28_18_u, grb28_18_v)
wind_map('Aug 29th, 0000UTC', grb29_00_height, grb29_00_wind, grb29_00_u, grb29_00_v)
wind_map('Aug 29th, 0600UTC', grb29_06_height, grb29_06_wind, grb29_06_u, grb29_06_v)
wind_map('Aug 29th, 1200UTC', grb29_12_height, grb29_12_wind, grb29_12_u, grb29_12_v)
wind_map('Aug 29th, 1800UTC', grb29_18_height, grb29_18_wind, grb29_18_u, grb29_18_v)

