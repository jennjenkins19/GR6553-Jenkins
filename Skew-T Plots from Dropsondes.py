#%% Importing the Library

import numpy as np
import netCDF4
import os
import pygrib

import cartopy.crs as ccrs
import cartopy 
import cartopy.feature as cf

import matplotlib as mpl
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt

from metpy.calc import azimuth_range_to_lat_lon
from metpy.io import Level2File
from metpy.plots import USCOUNTIES
from metpy.units import units
from metpy.plots import SkewT
from metpy.plots.ctables import registry

from scipy.ndimage import minimum_filter

#%%
"""
Skew T Data for Rapid Intensification
Flight 2 Aug 28th 1200 UTC: Dropsonde Number 10
     D20210828_105831QC.nc
     
Flight 4 Aug 29th 092626 UTC: Dropsonde Number 7
     D20210829_092626QC.nc

"""
#%% Dropsonde Skew_T plots 

# Create list of all the time values
time=['20210828_105831','20210829_092626']

# Loop to run through all the time values
# Creates individual timestep plots of the dropsonde data
for i in time: 
    full_name=str(i).zfill(15)
    name = full_name[-6:]
    filename=f'D{full_name}QC.nc'
    
    try: 
        # Read in dropsonde data
        dropsonde = netCDF4.Dataset(filename)
        # Save dropsonde data
        z = dropsonde.variables['gpsalt']
        z_profile_mask = z[0:]
        z_profile = []
        for i in range(len(z_profile_mask)):
           if z_profile_mask.mask[i] == False:
                z_profile = np.append(z_profile, z_profile_mask[i])
        
        launch_time = dropsonde.variables['time']
        launch_time_mask = launch_time[0:]
        
        i=0
        launch_time_list = []
        for i in range(len(launch_time_mask)):
            if z_profile_mask.mask.data[i] == False:
                launch_time_list = np.append(launch_time_list, launch_time_mask.data[i])
        
        # Create time variable
        flight_start_time = launch_time.units
        
        YYYY = flight_start_time[14:18]
        DD = flight_start_time[22:24]
        MM = flight_start_time[19:21]
        HH = flight_start_time[25:27]
        MIN = flight_start_time[28:30]
        SS = flight_start_time[31:33]
        
        flight_start_trakfile = MM + '/' + DD + '/' +YYYY
        flight_start_trakfile_time = HH + ':' + MIN + ':' + SS
        
        #Pressure Data
        pressure = dropsonde.variables['pres']
        pressure_profile_mask = pressure[0:]
        pressure_profile = []
        for i in range(len(pressure_profile_mask)):
           if pressure_profile_mask.mask[i] == False:
                pressure_profile = np.append(pressure_profile, pressure_profile_mask[i])
        
        #Dew Point Data        
        dp = dropsonde.variables['dp']
        dp_profile_mask = dp[0:]
        dp_profile = []
        for i in range(len(dp_profile_mask)):
           if dp_profile_mask.mask[i] == False:
                dp_profile = np.append(dp_profile, dp_profile_mask[i])
        
        #Temperature Data
        t = dropsonde.variables['tdry']
        t_profile_mask = t[0:]
        t_profile = []
        for i in range(len(t_profile_mask)):
           if t_profile_mask.mask[i] == False:
                t_profile = np.append(t_profile, t_profile_mask[i])
        
        #u-Wind        
        u_raw_data = dropsonde.variables['u_wind'][:]
        u_profile_mask = u_raw_data[0:]
        u_profile = []
        for i in range(len(u_profile_mask)):
            if u_profile_mask.mask[i] == False:
                u_profile = np.append(u_profile, u_profile_mask[i])
        
        #v-Wind        
        v_raw_data = dropsonde.variables['v_wind'][:]
        v_profile_mask = v_raw_data[0:]
        v_profile = []
        for i in range(len(v_profile_mask)):
            if v_profile_mask.mask[i] == False:
                v_profile = np.append(v_profile, v_profile_mask[i])
                
        # Ensure data are the same same size and assigning proper units
        p = pressure_profile[0:len(dp_profile)] * units.hPa
        T = t_profile[0:len(dp_profile)] * units.degC
        Td = dp_profile[0:len(dp_profile)] * units.degC
        u = u_profile[0:len(dp_profile)] * units.knots
        v = v_profile[0:len(dp_profile)] * units.knots
        
        # Plot figure
        fig = plt.figure(figsize=(6.5,7.5))

        skew = SkewT(fig, rotation=45)
        skew.plot(p, T, 'r')
        skew.plot(p, Td, 'g')
        
        # Set Limits for x and y with labeling
        skew.ax.set_xlim(15, 40)
        skew.ax.set_xlabel('Temperature (\N{DEGREE SIGN}C)')
        skew.ax.set_ylim(1020, 650)
        skew.ax.set_ylabel('Pressure (hPa)')
        
        # Add the relevant special lines to plot throughout the figure
        skew.plot_dry_adiabats(t0=np.arange(233, 533, 10) * units.K, alpha=0.25, color='orangered')
        skew.plot_moist_adiabats(t0=np.arange(233, 400, 5) * units.K, alpha=0.25, color='tab:green')
        
        #Add the wind barbs
        skew.plot_barbs(p[::40], u[::40], v[::40])
        
        plt.title(f"Flight: {flight_start_trakfile} - {name}")
        plt.savefig(f'Sounding_{full_name}.png')
        
        plt.show()
        plt.close()
        
    except Exception as e:
        print(f'failed: {e}')  #will print the error for the failure
        
