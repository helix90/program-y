import unittest

import metoffer
from programytest.services.library.metoffice.payloads.forecast_daily import (
    forecast_daily_payload,
)

from programy.services.library.metoffice.metoffice import MetOfficeForecast


class MetOfficeForecastTests(unittest.TestCase):

    def test_parse_json(self):
        forecast = MetOfficeForecast(metoffer.DAILY)
        self.assertIsNotNone(forecast)

        forecast.parse_json(forecast_daily_payload)

        self.assertEquals(0, len(forecast.get_forecasts()))
