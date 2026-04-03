#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 06:57:37 2024

@author: sarahrysanek
"""

import pandas as pd
import numpy as np

#%%

#read in the sed thickness txt file and fill nans with 0s

df = pd.read_csv('/path/to/your/gridfile.txt', sep='\t')

twt = df.iloc[:,2]
lat = df.iloc[:,1]
long = df.iloc[:,0]

#from QGIS, km, vel km/sec Walton et al. 2014
area = 225945103590.512/1000/1000
perim = 1990383/1000
spacing = 30/1000
vel = 2

#from Gulick et al. 2015, uncert calc
u1 = spacing*(perim/2)
frac_uncert= u1/area
area_uncert = frac_uncert*area
vel_uncert = vel *0.07
wave_res = 40/1000

twtt = pd.DataFrame(twt)

twtt = twtt.fillna(0)

#dividing twtt by 2 to get one way travel time
owtt = twtt/2

#multiplying by seismic velocity for sediment (2000m/sec)=(2km/sec)
sed_h = owtt*vel

#new grd cell size is (500mx500m)=(0.5kmx0.5km)
cell_size = 0.5
cell_area = cell_size*cell_size
box_vol = sed_h*cell_area

#sum the volumnes for total volumne:
sed_vol = box_vol.sum()

print(sed_vol)

max_thick = sed_h.max()

print(max_thick)
#%%
sed_h_np = sed_h.to_numpy()

def mean_without_zeros(data):
    """Calculates the mean of a list, excluding zeros."""
    non_zeros = [x for x in data if x != 0]
    if not non_zeros:  # Handle the case where all elements are zero
        return 0
    return sum(non_zeros) / len(non_zeros)

# Example usage:
sed_h_avg = mean_without_zeros(sed_h_np)
print(sed_h_avg)  
#%%
#uncertainty calculation
uncert_sed_h = sed_h_avg*(((vel_uncert/vel)**2)+((wave_res/sed_h_avg)**2))**(0.5)
vol_uncert = sed_vol*(((area_uncert/area)**2)+((uncert_sed_h/sed_h_avg)**2))**(0.5)

print(vol_uncert)

#%%
#sequence I

df = pd.read_csv('/path/to/plate/age/grd.txt', sep='\t')

mya_o = df.iloc[:,2]
#%%
#sequence I
#mya = mya_o - 2.8

#sequence II
mya = 2.8-1.2

#sequence III
#mya = 1.2

sed_h_cm = sed_h * 100000
sed_h_depo = sed_h[sed_h>0.5]
sed_h_depo_cm = sed_h_depo*1000*100

kya = mya*1000
yr = mya*1e6


#%%
sed_rate_cm_kyr = sed_h_cm/kya
sed_rate_cm_yr = sed_h_cm/yr

sed_rate_cm_kyr_depo = sed_h_depo_cm/kya


#%%
max_rate = sed_rate_cm_kyr.max()
max_rate_yr = sed_rate_cm_yr.max()
min_rate =  sed_rate_cm_kyr[sed_rate_cm_kyr > 0.1].min()

sed_rate_cm_kyr[sed_rate_cm_kyr == 0] = np.nan
avg_rate = np.mean(sed_rate_cm_kyr)

sed_rate_cm_kyr_depo[sed_rate_cm_kyr_depo == 0] = np.nan
min_rate_depo =  sed_rate_cm_kyr_depo.min()
avg_rate_depo = np.mean(sed_rate_cm_kyr_depo)

print(max_rate)
print(avg_rate)

#%%
#save as xyz to take back to gmt
sed_rate_cm_kyr = pd.Series(sed_rate_cm_kyr)
sed_rate_cm_kyr.replace(0, np.nan, inplace=True)
lat = pd.Series(lat)
long = pd.Series(long)

#sed_rate_cm_kyr = sed_rate_cm_kyr.fillna(0)
grd_dict = pd.concat([long, lat, sed_rate_cm_kyr], axis=1)

print(grd_dict)

#%%

grd_dict.to_csv('/path/to/where/your/output/files/go.csv', na_rep='NaN', index=False, header=False)

#%%
