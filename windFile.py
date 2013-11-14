from datetime import datetime, timedelta
from pytz import timezone
import pytz

def download(url):
	print url


def gen_url(current_time, launch_time):
	tz = timezone('America/New_York')

	# Convert Current Time and Launch Time to UTC
	current_time -= tz.utcoffset(current_time, is_dst=True)
	launch_time -= tz.utcoffset(launch_time, is_dst=True)

	runtime = (current_time.hour % 6) * 6	# Get the Model Runtime
	launch_time_offset = launch_time - current_time
	prediction_offset = (launch_time_offset.seconds / 3600 % 3) * 3

	# data_found = 0
	# while !data_found:
	download_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t%02dz.mastergrb2f%02d&leftlon=0&rightlon=360&toplat=90&bottomlat=-90&dir=%%2Fgfs.%04d%02d%02d%02d%%2Fmaster" % (runtime, prediction_offset, current_time.year, current_time.month, current_time.day, runtime)




launch_time = datetime(2013, 11, 15, 16, 24, 00)
now = datetime(2013, 11, 14, 16, 40, 00)


gen_url(now, launch_time)

