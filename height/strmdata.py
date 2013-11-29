#!/usr/bin/python2
import pygrib
import matplotlib.pyplot as plt
import os
from numpy import *
from urllib import *
import zipfile
import re

def trunc(val):
	sp = str(val).split('.')
	return sp[0]

def getFileNameFromDegrees(lat, lon):
	"""Takes a latitude and longitude in dotted decimal format and returns the corresponding STRM file name containing that coordinate.

	The return value is a string containing the file name.
	"""
	# cast to floats
	lat = float(lat)
	lon = float(lon)

	# default to North and East
	ns = 'N'
	ew = 'E'

	# check if it's South instead of North
	if (lat < 0):
		ns = 'S'

	# check if it's West instead of East
	if (lon < 0):
		ew = 'W'

	# add the 0 if needed
	if (-100 < lon < 100):
		ew += '0'

	# find the lowest closest integer absolute value
	latFloat = abs(floor(lat))
	latF = trunc(latFloat)

	# find the lowest closest integer absolute value
	lonFloat = abs(floor(lon))
	lonF = trunc(lonFloat)

	# create the filename string
	fileName = ns+latF+ew+lonF+'.hgt'

	return fileName

def getArrayLocation(lat, lon):
	"""Takes a latitude and longitude in dotted decimal format and returns the corresponding indices for a STRM file assuming 3601x3601 grid.

	The return values are integer indicies for latitude and longitude respectively.
	"""

	# cast to floats
	lat = float(lat)
	lon = float(lon)

	# get the decimal portion (different for positive and negative)
	if (lat > 0):
		# uses 1-decimal value because file names specify that the coordinate pair starts
		# at the bottom left but we read in from the top left
		latDecimal = 1 - abs(lat - floor(lat))
	else:
		latDecimal = abs(lat - ceil(lat))

	# get the decimal portion (different for positive and negative)
	if (lon > 0):
		lonDecimal = abs(lon - floor(lon))
	else:
		# uses 1-decimal value because file names specify that the coordinate pair starts
		# at the bottom left but we read in from the top left
		lonDecimal = 1 - abs(lon - ceil(lon))

	# round to the nearest index
	latIndex = round(latDecimal * 3600)
	lonIndex = round(lonDecimal * 3600)
	
	return [latIndex, lonIndex]

def getElevation(lat, lon):
	"""Takes a latitude and longitude and returns the corresponding elevation.

	The return value is the elevation at the specified latitude and longitude or None if inputs are invalid.
	"""

	# make sure lat is valid and convert to dotted decimal form
	lat = getDottedDecimal(str(lat))
	if (lat == None):
		return None

	# make sure lon is valid and convert to dotted decimal form
	lon = getDottedDecimal(str(lon))
	if (lon == None):
		return None

	# get the file name
	fileName = getFileNameFromDegrees(lat, lon)
	
	if (os.path.exists(fileName) == False):
		# information about the zip file to download if needed	
		zipName = fileName + '.zip'
		webURL = 'http://dds.cr.usgs.gov/srtm/version2_1/SRTM1/Region_06/'
		fullURL = webURL + zipName 
		
		print('File ' + fileName + ' does not exist.')
		print('Downloading file from ' + fullURL + '.') 
		print('This may take some time.')
	
		# download the zip file		
		urlretrieve(fullURL, zipName)

		# extract the zip file
		with zipfile.ZipFile(zipName) as myzip:
			myzip.extractall()

	# read in the STRM file		
	t=fromfile(fileName, dtype=dtype('>H'))

	# reshape the file to fit the known size of the data of 3601x3601	
	t=reshape(t, (3601,3601))

	# get the indices for the data file
	[latIndex, lonIndex] = getArrayLocation(lat, lon)

	# get the elevation at the index	
	elevation = t[latIndex, lonIndex]
	
	return elevation

def getDottedDecimal(string):
	"""Takes a string latitude or longitude and returns the corresponding float value.

	The following input forms are recognized
	DDD.dddddddd
	DDD MM SS
	DDD MM'SS"
	DDD MM.mmmmm
	DDD MM.mmmmm'
	The return value is in the form DDD.dddddddddddd or None if the string is invalid.
	S and W either appended or prepended, but not both, negate the value, even if there is already a '-' in front.  Therefore, either use just a '-' or use S or W but not both.
	"""

	# matching regular expressions to try
	res = ['^(?P<dir1>[NSEW])?\s*(?P<sign>[-+])?(?P<degrees>\d+\.\d+)\s*(?P<dir2>[NSEW])?$','^(?P<dir1>[NSEW])?\s*(?P<sign>[-+])?(?P<degrees>\d+)\s+(?P<minutes>\d+)\'?\s+(?P<seconds>\d+)\"?\s*(?P<dir2>[NSEW])?$',"^(?P<dir1>[NSEW])?\s*(?P<sign>[-+])?(?P<degrees>\d+)\s+(?P<minutes>\d+\.\d+)\'?\s*(?P<dir2>[NSEW])?$"]
	
	val = 0
	m = None

	# check each regex pattern for a match
	for regex in res:
		# compile each regex pattern
		pattern = re.compile(regex)
		# check for a match
		m = pattern.match(string)
		if (m != None):
			break;

	if (m != None):
		# initialize the return value
		val = 0;
		# with 2 groups only degrees are present
		if (pattern.groups < 5):
			val += float(m.group('degrees'))
		# with 3 groups degrees and minutes are present 
		elif (pattern.groups < 6):
			val += float(m.group('degrees'))
			val += float(m.group('minutes')) / 60
		# with 4 groups degrees, minutes, and seconds are present
		elif (pattern.groups < 7):
			val += float(m.group('degrees'))
			val += float(m.group('minutes')) / 60
			val += float(m.group('seconds')) / 3600
		# check if a sign was found and negate the value if it was a '-'
		if (m.group('sign') != None):
			if (m.group('sign') == '-'):
				val *= -1;
		# check if N, S, E, or W are appended or prepended
		if (m.group('dir1') != None or m.group('dir2') != None):
			# if a value is both appended and prepended, the string is invalid
			if (m.group('dir1') != None and m.group('dir2') != None):
				val = None
			# if it's an S or a W, negate the value
			elif (m.group('dir1') == 'S' or m.group('dir1') == 'W' or m.group('dir2') == 'S' or m.group('dir2') == 'W'):
				val *= -1
	else:
		val = None

	return val
