__author__ = 'bcarlson'
#from pygrib import *
from datetime import datetime, timedelta
from pytz import timezone
import wget
import shutil
import os

class Wind:
    def __init__(self, altitude):
        self.altitude = altitude

    def test(self):
        print self.altitude.ascent


class WindServer:
    def __init__(self, input):
        tz = timezone('America/New_York')       ## TODO: Make this not static?
        # Datetime objects representing the launch and current times, shifed for UTC
        self.launch_time = input.params.launch_time - tz.utcoffset(input.params.launch_time, is_dst=True)
        self.current_time = datetime.now() - tz.utcoffset(datetime.now(), is_dst=True)

        self.files = []
    def updateFiles(self):

        # Always assume that the most up to date runtime is not yet available
        runtime = ((self.current_time.hour-6) / 6) * 6	# Get the Model Runtime
        launch_time_offset = self.launch_time - self.current_time

        # For now, if the prediction take place in the past... don't
        if launch_time_offset < timedelta(0):
            launch_time_offset = timedelta(0)

        prediction_offset = (launch_time_offset.seconds / 3600 / 3) * 3

        ### NOTE THIS ISN'T DONE!
        if not os.path.isfile("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset, runtime, prediction_offset)):
            download_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t%02dz.mastergrb2f%02d&leftlon=290&rightlon=294&toplat=49&bottomlat=43&dir=%%2Fgfs.%04d%02d%02d%02d%%2Fmaster" % (runtime, prediction_offset, self.current_time.year, self.current_time.month, self.current_time.day, runtime)
            file = wget.download(download_url)
            shutil.move(file, './wind/49-43-290-294-%04d%02d%02d%02d-%s' % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset, file))
        if not os.path.isfile("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset+3, runtime, prediction_offset+3)):
            download_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t%02dz.mastergrb2f%02d&leftlon=290&rightlon=294&toplat=49&bottomlat=43&dir=%%2Fgfs.%04d%02d%02d%02d%%2Fmaster" % (runtime, prediction_offset+3, self.current_time.year, self.current_time.month, self.current_time.day, runtime)
            file = wget.download(download_url)
            shutil.move(file, './wind/49-43-290-294-%04d%02d%02d%02d-%s' % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset+3, file))

