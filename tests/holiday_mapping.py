import unittest
from workalendar.core import WesternCalendar
from workalendar.usa import UnitedStates

from amaasutils.holiday_mapping import get_calendar


class HolidayMappingTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_GetCalendar(self):
        country_code = 'USA'
        calendar = get_calendar(country_code)
        self.assertEqual(type(calendar), UnitedStates)

    def test_GetCalendarMissing(self):
        country_code = 'XXX'
        calendar = get_calendar(country_code)
        self.assertEqual(type(calendar), WesternCalendar)


if __name__ == '__main__':
    unittest.main()
