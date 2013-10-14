#

from datetime import datetime
from dateutil import tz

class timeConvert:


    def utc2est(self, utc, format='%Y-%m-%d %H:%M:%S'):
        # @todo should we not hard code zones?
        from_zone = tz.gettz('UTC')
        to_zone = tz.gettz('America/New_York')

        # provide the format of the input
        utc = datetime.strptime(utc, format)

        # Tell the datetime object that it's in UTC time zone since
        # datetime objects are 'naive' by default
        utc = utc.replace(tzinfo=from_zone)

        # Convert time zone
        est = utc.astimezone(to_zone)
        return est
