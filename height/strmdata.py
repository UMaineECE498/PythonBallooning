#!/usr/bin/python2
import pygrib
import matplotlib.pyplot as plt
from numpy import *

def trunc(val):
	sp = str(val).split('.')
	return sp[0]

def getFileNameFromDegrees(lat, lon):
	ns = 'N'
	ew = 'E'
	if (lat < 0):
		ns = 'S'

	if (lon < 0):
		ew = 'W'

	if (-100 < lon < 100):
		ew += '0'

	latFloat = abs(floor(lat))
	latF = trunc(latFloat)

	lonFloat = abs(floor(lon))
	lonF = trunc(lonFloat)

	fileName = ns+latF+ew+lonF+'.hgt'
	return fileName

def getArrayLocation(lat, lon):
	if (lat > 0):
		latDecimal = abs(lat - floor(lat))
	else:
		latDecimal = abs(lat - ceil(lat))

	if (lon > 0):
		lonDecimal = abs(lon - floor(lon))
	else:
		lonDecimal = abs(lon - ceil(lon))

	latIndex = round(latDecimal * 3600)
	lonIndex = round(lonDecimal * 3600)
	
	print latDecimal, lonDecimal
	print latIndex, lonIndex
	return [latIndex, lonIndex]

lat = 44.9026
lon = -68.6699

fileName = getFileNameFromDegrees(lat, lon)

print fileName

[latIndex, lonIndex] = getArrayLocation(lat, lon)
print latIndex, lonIndex

t=fromfile(fileName, dtype=dtype('>H'))
t=reshape(t, (3601,3601))

print t[latIndex, lonIndex]
#print t[3250,2412]
#print t[0,0]

#lats=linspace(lat, lat-1, 3601)
#lons=linspace(lon, lon+1, 3601)
#p=plt.contour(lons, lats, t, 128)
#plt.show()

#data from here: http://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_06/


