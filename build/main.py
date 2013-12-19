__author__ = 'bcarlson'

from datetime import datetime
from data import PredictorInput
import time
from altitude import Altitude
from wind import Wind

pred = PredictorInput(4.2, 3.2, 30000, 44, -68, datetime(2013, 12, 15, 06, 00, 00))
# pred.params.files = ['./wind/49-43-290-294-2013112800-gfs.t12z.mastergrb2f00', './wind/49-43-290-294-2013112803-gfs.t12z.mastergrb2f03']
start_time = time.time()
pred.Wind.runPrediction()
print "Run Time", time.time() - start_time