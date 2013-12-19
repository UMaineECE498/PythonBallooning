__author__ = 'bcarlson'
import pygrib
from datetime import datetime, timedelta
from pytz import timezone
import wget
import shutil
import os
from math import *
import data as DataManager
import time
import calendar

class Wind:
    def __init__(self, data):
        self.data = data        # Initialize with all data
        # When doing wind predictions, ensure we're up to date with files
        self.data.WindServer.updateFiles()

        self.coordinates = []
        self.position = []


    def runPrediction(self):

        lat_meter = 200.0/22226349.0
        lon_meter = 1.0/78846.80572069259

        try:
            start_time = time.time()
            grb_p = pygrib.open(self.data.params.files[0])

            grb_p_test = pygrib.index(self.data.params.files[0], 'name', 'level')
            grb_s = pygrib.open(self.data.params.files[1])
            print "Open Files - ", time.time() - start_time, "seconds"
        except:
            print "Could not open valid wind files"

        grb_p.seek(0)


        print self.pressureAltitude(100)

        start_time = time.time()
        d_now = DataManager.DataManager()
        d_now.u = grb_p.select(name='U component of wind')
        d_now.v = grb_p.select(name='V component of wind')
        print "Grib Selection - ", time.time() - start_time, "seconds"

        # Assuming all data has the same shape and lat/lon axis
        start_time = time.time()
        shape = {}
        shape['latitude'] = {}
        shape['latitude']['min'] = d_now.u[0].latlons()[0].min()
        shape['latitude']['max'] = d_now.u[0].latlons()[0].max()
        shape['longitude'] = {}
        shape['longitude']['min'] = d_now.u[0].latlons()[1].min()
        shape['longitude']['max'] = d_now.u[0].latlons()[1].max()
        print "Min/Max Calculation - ", time.time() - start_time, "seconds"

        self.coordinates.append((self.data.params.launch_time, self.grbLat(shape, self.data.params.launch_lat), self.grbLon(shape, self.data.params.launch_lon)))
        self.position.append((self.data.params.launch_time, self.data.params.launch_lat, self.data.params.launch_lon))



        cur_u = grb_p.select(name='U component of wind', level=1000)
        cur_v = grb_p.select(name='V component of wind', level=1000)

        print cur_u

        print self.coordinates
        print self.position
        # S0, we've got a now dict holding heights, u, and v components
        # 1) Iterate through heights, given our altitude, find correct index
        # 2) Use the same index for u and v wind components
        # 3) ....
        # 4) Predictions?

        print self.data.params.profile
        print len(self.data.params.profile)

        cur_u = grb_p_test(name='U component of wind', level=200/100)
        cur_v = grb_p_test(name='V component of wind', level=200/100)
        current_values = {}
        current_values['pressure'] = 200


        descent = 0
        # Could remove altitude/Pressure steps in the future to speed this stage up...
        for balloon_time in sorted(self.data.params.profile.iterkeys()):
            if balloon_time > calendar.timegm(self.data.params.burst_time.timetuple()):
                descent = 1

            pressure = self.pressureAltitude(self.data.params.profile[balloon_time])
            if pressure != current_values['pressure']:

                print "New Level: ", pressure
                start_time = time.time()

                cur_u = grb_p_test(name='U component of wind', level=pressure/100)
                cur_v = grb_p_test(name='V component of wind', level=pressure/100)

                print "Select Pressure - ", time.time() - start_time, "seconds"

                current_values['pressure'] = pressure

                # If we change pressure level, throw away all previous data
                current_values['grbLat'] = -1
                current_values['grbLon'] = -1

            # If we're looking at a new .5 degree index into the file, get new values, otherwise continue
            if self.grbLat(shape, self.position[-1][1]) != current_values['grbLat'] or self.grbLon(shape, self.position[-1][2]) != current_values['grbLon']:
                start_time = time.time()

                # Update Current Latitude and Longitude index in grb file
                current_values['grbLat'] = self.grbLat(shape, self.position[-1][1])
                current_values['grbLon'] = self.grbLon(shape, self.position[-1][2])


                current_values['u'] = cur_u[0].values[self.grbLat(shape, self.position[-1][1])-2:self.grbLat(shape, self.position[-1][1]),
                                                        self.grbLon(shape, self.position[-1][2])-2:self.grbLon(shape, self.position[-1][2])]
                current_values['v'] = cur_v[0].values[self.grbLat(shape, self.position[-1][1])-2:self.grbLat(shape, self.position[-1][1]),
                                      self.grbLon(shape, self.position[-1][2])-2:self.grbLon(shape, self.position[-1][2])]

                # Update Current U and V components of wind
                current_values['u_hh'] = current_values['u'][1,1]
                current_values['v_hh'] = current_values['v'][1,1]

                current_values['u_ll'] = current_values['u'][0,0]
                current_values['v_ll'] = current_values['v'][0,0]

                current_values['u_lh'] = current_values['u'][0,1]
                current_values['v_lh'] = current_values['v'][0,1]

                current_values['u_hl'] = current_values['u'][1,0]
                current_values['v_hl'] = current_values['v'][1,0]

                print "Select Wind Speed - ", time.time() - start_time, "seconds"

            u_move = self.squareInterpolate(self.grbLat(shape, self.position[-1][1])-1 * .5,
                                            self.grbLon(shape, self.position[-1][2])-1 * .5,
                                            self.grbLat(shape, self.position[-1][1]) * .5,
                                            self.grbLon(shape, self.position[-1][2]) * .5,
                                            self.position[-1][1],
                                            self.position[-1][2],
                                            current_values['u_ll'],
                                            current_values['u_lh'],
                                            current_values['u_hl'],
                                            current_values['u_hh'])

            v_move = self.squareInterpolate(self.grbLat(shape, self.position[-1][1])-1 * .5,
                                            self.grbLon(shape, self.position[-1][2])-1 * .5,
                                            self.grbLat(shape, self.position[-1][1]) * .5,
                                            self.grbLon(shape, self.position[-1][2]) * .5,
                                            self.position[-1][1],
                                            self.position[-1][2],
                                            current_values['v_ll'],
                                            current_values['v_lh'],
                                            current_values['v_hl'],
                                            current_values['v_hh'])

            u_degrees = u_move * self.data.params.ascent_step * lat_meter
            v_degrees = v_move * self.data.params.ascent_step * lon_meter

            self.position.append((0, self.position[-1][1] + u_degrees, self.position[-1][2] + v_degrees))

        for point in self.position:
            print point[1], ',', point[2]


    def pressureAltitude(self, altitude):
        pressure = 101325 * (1 - 0.0000225577 * altitude)**5.25588

        pressures = [100, 200, 300, 500, 700, 1000, 2000, 3000, 5000, 7000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 92500, 95000, 97500, 100000]

        return min(pressures, key=lambda x:abs(x-pressure))


    def grbLat(self, shape, latitude):
        # Latitude is traditionally -90 to 90 degrees...
        # Need to do some parsing here to get our latitude into a 0-180 format
        # We're also assuming .5 degree scaling, so... we really want 0-360

        minimum = shape['latitude']['min']
        maximum = shape['latitude']['max']

        if latitude < minimum or latitude > maximum:
            print "Latitude outside bounds"
            return 0
        else:
            index = 0.5 * ceil( 4.0 * (latitude - minimum))  # Effectively round to the nearest half and generate an index
            return index

    def grbLon(self, shape, longitude):
        # Longitude is traditionally -180 to 180 degrees
        # Need to do some conversion to get that to 0 - 360
        # We're also assuming .5 degree scaling, so 0 - 720
        longitude = longitude + 180
        # Sadly, our default min and max comes in as 0 - 360 :(

        minimum = shape['longitude']['min']
        maximum = shape['longitude']['max']


        if longitude < minimum or longitude > maximum:
            print longitude, minimum, maximum
            print "Longitude outside bounds"
            return 0
        else:
            index = 0.5 * ceil( 4.0 * (longitude - minimum)) # Same as above, round to the nearest half degree and generate index
            return index

    def interpolate(self, al, ah, a, vl ,vh):
        a_d = float(a - al)/float(ah - al)
        return ((1 - a_d)*vl + a_d*vh)

    def squareInterpolate(self, xl, yl, xh, yh, x, y, vll, vlh, vhl, vhh):
        v0 = self.interpolate(xl, xh, x, vll, vhl)
        v1 = self.interpolate(xl, xh, x, vlh, vhh)
        return self.interpolate(yl, yh, y, v0, v1)

class WindServer:
    def __init__(self, data):
        return
        print "Initialize Wind File Server"

        tz = timezone('America/New_York')       ## TODO: Make this not static?
        # Datetime objects representing the launch and current times, shifed for UTC
        self.launch_time = data.params.launch_time - tz.utcoffset(data.params.launch_time, is_dst=True)
        self.current_time = datetime.now() - tz.utcoffset(datetime.now(), is_dst=True)

        self.data = data
        self.data.params.files = []     # Maintains record of downloaded files valid for this prediction sequence
    def updateFiles(self):
        return

        print "Update Files"
        # Clean out file array
        self.data.params.files = []

        # Always assume that the most up to date runtime is not yet available
        runtime = ((self.current_time.hour-6) / 6) * 6	# Get the Model Runtime
        if runtime < 0:
            runtime = 0

        launch_time_offset = self.launch_time - self.current_time

        # For now, if the prediction take place in the past... don't
        if launch_time_offset < timedelta(0):
            launch_time_offset = timedelta(0)

        prediction_offset = (launch_time_offset.seconds / 3600 / 3) * 3

        ### NOTE THIS ISN'T DONE!
        self.data.params.files.append("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset, runtime, prediction_offset))
        if not os.path.isfile("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset, runtime, prediction_offset)):
            download_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t%02dz.mastergrb2f%02d&leftlon=290&rightlon=294&toplat=49&bottomlat=43&dir=%%2Fgfs.%04d%02d%02d%02d%%2Fmaster" % (runtime, prediction_offset, self.launch_time.year, self.launch_time.month, self.launch_time.day, runtime)
            print download_url
            print (runtime, prediction_offset, self.current_time.year, self.current_time.month, self.current_time.day, runtime)
            file = wget.download(download_url)
            shutil.move(file, './wind/49-43-290-294-%04d%02d%02d%02d-%s' % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset, file))
        self.data.params.files.append("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset+3, runtime, prediction_offset+3))
        if not os.path.isfile("./wind/49-43-290-294-%04d%02d%02d%02d-gfs.t%02dz.mastergrb2f%02d" % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset+3, runtime, prediction_offset+3)):
            download_url = "http://nomads.ncep.noaa.gov/cgi-bin/filter_gfs_hd.pl?file=gfs.t%02dz.mastergrb2f%02d&leftlon=290&rightlon=294&toplat=49&bottomlat=43&dir=%%2Fgfs.%04d%02d%02d%02d%%2Fmaster" % (runtime, prediction_offset+3, self.current_time.year, self.current_time.month, self.current_time.day, runtime)
            file = wget.download(download_url)
            shutil.move(file, './wind/49-43-290-294-%04d%02d%02d%02d-%s' % (self.current_time.year, self.current_time.month, self.current_time.day, prediction_offset+3, file))

