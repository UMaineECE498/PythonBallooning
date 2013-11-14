#!/usr/bin/python
import pygrib
import matplotlib.pyplot as plt
from numpy import *

t=fromfile('N45W070.hgt', dtype=dtype('>H'))
t=reshape(t, (3601,3601))
lat=linspace(45, 44, 3601)
lon=linspace(69, 70, 3601)
p=plt.contour(lon, lat, t, 128)
plt.show()

#data from here: http://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_06/