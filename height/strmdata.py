#!/usr/bin/python2
import pygrib
import matplotlib.pyplot as plt
import os
from numpy import *
from urllib import *
import zipfile

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

	latIndex = round((1 - latDecimal) * 3600)
	lonIndex = round((1 - lonDecimal) * 3600)
	
	return [latIndex, lonIndex]

lat = 44.9026
lon = -68.6699

fileName = getFileNameFromDegrees(lat, lon)

[latIndex, lonIndex] = getArrayLocation(lat, lon)

zipName = fileName + '.zip'
webURL = 'http://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_06/'
fullURL = webURL + zipName 

if (os.path.exists(fileName) == False):
	print 'File ' + fileName + ' does not exist.'
	print 'Downloading file from ' + fullURL + '.' 
	print 'This may take some time.'
	urlretrieve(fullURL, zipName)
	with zipfile.ZipFile(zipName) as myzip:
		myzip.extractall()
	
t=fromfile(fileName, dtype=dtype('>H'))

t=reshape(t, (3601,3601))

elevation = t[latIndex, lonIndex]

print elevation

#data from here: http://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_06/


