__author__ = 'bcarlson'
from altitude import Altitude
from wind import *


class DataManager:
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

class PredictorInput:
    def __init__(self, ascent, descent, burst, launch_time):

        self.params = DataManager()
        # Load all the passed data into a common data structure
        self.params.ascent = ascent
        self.params.descent = descent
        self.params.burst = burst
        self.params.launch_time = launch_time

        self.Altitude = Altitude(self)
        self.WindServer = WindServer(self)