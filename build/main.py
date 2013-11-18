__author__ = 'bcarlson'

from datetime import datetime
from data import PredictorInput
from altitude import Altitude
from wind import Wind

pred = PredictorInput(4.2, 3.2, 30000, datetime.now())
pred.WindServer.updateFiles()
print pred.params.profile