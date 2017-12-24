
import unittest
import datetime
from api_server.api import format_duration, pods

class TestFormatHelpers(unittest.TestCase):

    def test_format_duration(self):

        start_time = datetime.datetime(2017, 12, 24, 14, 49, 38)

        now = datetime.datetime(2017, 12, 25, 16, 49, 38)
        self.assertEqual(format_duration(start_time, now=now), "1 day")

        now = datetime.datetime(2017, 12, 27, 16, 49, 38)
        self.assertEqual(format_duration(start_time, now=now), "3 days")

        now = datetime.datetime(2017, 12, 24, 15, 49, 38)
        self.assertEqual(format_duration(start_time, now=now), "1 hour")

        now = datetime.datetime(2017, 12, 24, 16, 49, 38)
        self.assertEqual(format_duration(start_time, now=now), "2 hours")

        now = datetime.datetime(2017, 12, 24, 14, 54, 38)
        self.assertEqual(format_duration(start_time, now=now), "5 minutes")

        now = datetime.datetime(2017, 12, 24, 14, 50, 44)
        self.assertEqual(format_duration(start_time, now=now), "1 minute")

class TestApi(unittest.TestCase):

    def test_pods(self):
        json = pods()



if __name__ == '__main__':
    unittest.main()



