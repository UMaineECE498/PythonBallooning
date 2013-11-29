__author__ = 'bcarlson'
import math
from datetime import timedelta
import calendar

class Altitude:
    def __init__(self, input):
        self.input = input
        self.input.params.profile = {}

        self.updateAltitudeProfile()


    def updateAltitudeProfile(self):
        """Generates an altitude profile from a launch's input parameters
        """

        # If the ascent or descent rate have changed, the burst time must be recalculated
        self.input.params.burst_time = timedelta(seconds=self.input.params.burst / self.input.params.ascent) + self.input.params.launch_time

        # Convert to unix timestamps to ease iteration
        launch_time = calendar.timegm(self.input.params.launch_time.timetuple())
        burst_time = calendar.timegm(self.input.params.burst_time.timetuple())

        # Generate ascent phase of altitude profile
        for time in range(launch_time, int(burst_time)):          # Should go from launch to a second before burst
            self.input.params.profile[launch_time + time] = self.input.params.ascent * (time - launch_time)

        # From burst to ground, generate descent phase
        time = int(burst_time)
        altitude = self.input.params.burst
        while altitude > 0:
            altitude -= (self.input.params.descent * 1.1045) / math.sqrt(self.getDensity(altitude))
            self.input.params.profile[launch_time + time] = altitude
            time += 2

    # Would like to use the grib files to do this, if possible...
    def getDensity(self, altitude):

        if altitude > 25000:
            temp = -131.21 + 0.00299 * altitude
            pressure = 2.488*(((temp+273.1)/216.6)**-11.388)
        elif altitude <= 25000 and altitude > 11000:
            temp = -56.46
            pressure = 22.65 * math.exp(1.73-0.000157*altitude)
        elif altitude <= 11000:
            temp = 15.04 - 0.00649 * altitude;
            pressure = 101.29 * (((temp + 273.1)/288.08)**5.256)

        return pressure / (0.2869*(temp+273.1))