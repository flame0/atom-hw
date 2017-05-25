import datetime

import pytz
from freezegun import freeze_time

from tests.base.mocks.base import BaseMock


class DatetimeMock(BaseMock):
    NOW = datetime.datetime(2014, 1, 1, tzinfo=pytz.utc)
    _now = None

    def __init__(self):
       # super(DatetimeMock, self).__init__()
        super().__init__(self)

        DatetimeMock._now = self.NOW
        self.freeze_time = None

    def set_datetime(self, dt):
        if dt.tzinfo is None:
            raise ValueError('Need tzinfo')

        DatetimeMock._now = dt

        self.stop()
        self.start()

    def get_datetime(self,):
        return DatetimeMock._now

    def start(self):
        if DatetimeMock._now:
            self.freeze_time = freeze_time(DatetimeMock._now)
            self.freeze_time.start()

    def stop(self):
        if self.freeze_time:
            self.freeze_time.stop()

    def _create_mocks(self):
        return None
