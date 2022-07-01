import datetime

import pytz
from freezegun import freeze_time


def mock_time(time):
    time = time.strftime('%Y-%m-%dT%H:%M:%S')
    mocked = datetime.datetime.strptime(str(time), '%Y-%m-%dT%H:%M:%S')
    mocked = pytz.utc.localize(mocked)
    return freeze_time(mocked)