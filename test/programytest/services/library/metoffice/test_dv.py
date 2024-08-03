import unittest

import metoffer

from programy.services.library.metoffice.metoffice import DV, MetOfficeWeatherReport


class DVTests(unittest.TestCase):

    def test_init(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        self.assertEqual(MetOfficeWeatherReport.FORECAST, dv._data_type)
        self.assertEqual(metoffer.DAILY, dv._time_period)

        self.assertIsNone(dv._date)
        self.assertIsNone(dv._type)
        self.assertIsNone(dv._location)

    def test_parse_json(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {
            "Location": {
                "Period": [
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "S",
                                "Dm": "15",
                                "FDm": "13",
                                "Gn": "16",
                                "Hn": "54",
                                "PPd": "0",
                                "S": "9",
                                "U": "4",
                                "V": "VG",
                                "W": "1",
                            },
                            {
                                "$": "Night",
                                "D": "SSW",
                                "FNm": "7",
                                "Gm": "16",
                                "Hm": "86",
                                "Nm": "9",
                                "PPn": "57",
                                "S": "7",
                                "V": "GO",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-03Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "N",
                                "Dm": "13",
                                "FDm": "11",
                                "Gn": "11",
                                "Hn": "82",
                                "PPd": "49",
                                "S": "7",
                                "U": "2",
                                "V": "GO",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "4",
                                "Gm": "11",
                                "Hm": "81",
                                "Nm": "5",
                                "PPn": "9",
                                "S": "4",
                                "V": "VG",
                                "W": "2",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-04Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "NW",
                                "Dm": "12",
                                "FDm": "10",
                                "Gn": "20",
                                "Hn": "59",
                                "PPd": "9",
                                "S": "11",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "6",
                                "Gm": "11",
                                "Hm": "79",
                                "Nm": "6",
                                "PPn": "8",
                                "S": "7",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-05Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "14",
                                "FDm": "13",
                                "Gn": "11",
                                "Hn": "61",
                                "PPd": "8",
                                "S": "4",
                                "U": "4",
                                "V": "VG",
                                "W": "7",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "7",
                                "Gm": "9",
                                "Hm": "81",
                                "Nm": "7",
                                "PPn": "10",
                                "S": "4",
                                "V": "VG",
                                "W": "8",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-06Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "13",
                                "FDm": "12",
                                "Gn": "11",
                                "Hn": "66",
                                "PPd": "11",
                                "S": "4",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "8",
                                "Gm": "7",
                                "Hm": "76",
                                "Nm": "8",
                                "PPn": "8",
                                "S": "4",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-07Z",
                    },
                ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE",
            },
            "dataDate": "2017-04-03T09:00:00Z",
            "type": "Forecast",
        }

        dv.parse_json(json)

        self.assertIsNotNone(dv.location)
        self.assertEquals(MetOfficeWeatherReport.FORECAST, dv._data_type)
        self.assertEquals("Forecast", dv._type)

    def test_parse_json_location_missing(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {"dataDate": "2017-04-03T09:00:00Z", "type": "Forecast"}

        with self.assertRaises(ValueError):
            dv.parse_json(json)

    def test_parse_json_dataDate_missing(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {
            "Location": {
                "Period": [
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "S",
                                "Dm": "15",
                                "FDm": "13",
                                "Gn": "16",
                                "Hn": "54",
                                "PPd": "0",
                                "S": "9",
                                "U": "4",
                                "V": "VG",
                                "W": "1",
                            },
                            {
                                "$": "Night",
                                "D": "SSW",
                                "FNm": "7",
                                "Gm": "16",
                                "Hm": "86",
                                "Nm": "9",
                                "PPn": "57",
                                "S": "7",
                                "V": "GO",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-03Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "N",
                                "Dm": "13",
                                "FDm": "11",
                                "Gn": "11",
                                "Hn": "82",
                                "PPd": "49",
                                "S": "7",
                                "U": "2",
                                "V": "GO",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "4",
                                "Gm": "11",
                                "Hm": "81",
                                "Nm": "5",
                                "PPn": "9",
                                "S": "4",
                                "V": "VG",
                                "W": "2",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-04Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "NW",
                                "Dm": "12",
                                "FDm": "10",
                                "Gn": "20",
                                "Hn": "59",
                                "PPd": "9",
                                "S": "11",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "6",
                                "Gm": "11",
                                "Hm": "79",
                                "Nm": "6",
                                "PPn": "8",
                                "S": "7",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-05Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "14",
                                "FDm": "13",
                                "Gn": "11",
                                "Hn": "61",
                                "PPd": "8",
                                "S": "4",
                                "U": "4",
                                "V": "VG",
                                "W": "7",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "7",
                                "Gm": "9",
                                "Hm": "81",
                                "Nm": "7",
                                "PPn": "10",
                                "S": "4",
                                "V": "VG",
                                "W": "8",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-06Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "13",
                                "FDm": "12",
                                "Gn": "11",
                                "Hn": "66",
                                "PPd": "11",
                                "S": "4",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "8",
                                "Gm": "7",
                                "Hm": "76",
                                "Nm": "8",
                                "PPn": "8",
                                "S": "4",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-07Z",
                    },
                ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE",
            },
            "type": "Forecast",
        }
        with self.assertRaises(ValueError):
            dv.parse_json(json)

    def test_parse_json_dataDate_wrong_format(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {
            "Location": {
                "Period": [
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "S",
                                "Dm": "15",
                                "FDm": "13",
                                "Gn": "16",
                                "Hn": "54",
                                "PPd": "0",
                                "S": "9",
                                "U": "4",
                                "V": "VG",
                                "W": "1",
                            },
                            {
                                "$": "Night",
                                "D": "SSW",
                                "FNm": "7",
                                "Gm": "16",
                                "Hm": "86",
                                "Nm": "9",
                                "PPn": "57",
                                "S": "7",
                                "V": "GO",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-03Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "N",
                                "Dm": "13",
                                "FDm": "11",
                                "Gn": "11",
                                "Hn": "82",
                                "PPd": "49",
                                "S": "7",
                                "U": "2",
                                "V": "GO",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "4",
                                "Gm": "11",
                                "Hm": "81",
                                "Nm": "5",
                                "PPn": "9",
                                "S": "4",
                                "V": "VG",
                                "W": "2",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-04Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "NW",
                                "Dm": "12",
                                "FDm": "10",
                                "Gn": "20",
                                "Hn": "59",
                                "PPd": "9",
                                "S": "11",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "6",
                                "Gm": "11",
                                "Hm": "79",
                                "Nm": "6",
                                "PPn": "8",
                                "S": "7",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-05Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "14",
                                "FDm": "13",
                                "Gn": "11",
                                "Hn": "61",
                                "PPd": "8",
                                "S": "4",
                                "U": "4",
                                "V": "VG",
                                "W": "7",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "7",
                                "Gm": "9",
                                "Hm": "81",
                                "Nm": "7",
                                "PPn": "10",
                                "S": "4",
                                "V": "VG",
                                "W": "8",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-06Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "13",
                                "FDm": "12",
                                "Gn": "11",
                                "Hn": "66",
                                "PPd": "11",
                                "S": "4",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "8",
                                "Gm": "7",
                                "Hm": "76",
                                "Nm": "8",
                                "PPn": "8",
                                "S": "4",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-07Z",
                    },
                ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE",
            },
            "dataDate": "xxxxxxx",
            "type": "Forecast",
        }
        with self.assertRaises(ValueError):
            dv.parse_json(json)

    def test_parse_json_type_missing(self):
        dv = DV(MetOfficeWeatherReport.FORECAST, metoffer.DAILY)
        self.assertIsNotNone(dv)

        json = {
            "Location": {
                "Period": [
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "S",
                                "Dm": "15",
                                "FDm": "13",
                                "Gn": "16",
                                "Hn": "54",
                                "PPd": "0",
                                "S": "9",
                                "U": "4",
                                "V": "VG",
                                "W": "1",
                            },
                            {
                                "$": "Night",
                                "D": "SSW",
                                "FNm": "7",
                                "Gm": "16",
                                "Hm": "86",
                                "Nm": "9",
                                "PPn": "57",
                                "S": "7",
                                "V": "GO",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-03Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "N",
                                "Dm": "13",
                                "FDm": "11",
                                "Gn": "11",
                                "Hn": "82",
                                "PPd": "49",
                                "S": "7",
                                "U": "2",
                                "V": "GO",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "4",
                                "Gm": "11",
                                "Hm": "81",
                                "Nm": "5",
                                "PPn": "9",
                                "S": "4",
                                "V": "VG",
                                "W": "2",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-04Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "NW",
                                "Dm": "12",
                                "FDm": "10",
                                "Gn": "20",
                                "Hn": "59",
                                "PPd": "9",
                                "S": "11",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NNW",
                                "FNm": "6",
                                "Gm": "11",
                                "Hm": "79",
                                "Nm": "6",
                                "PPn": "8",
                                "S": "7",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-05Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "14",
                                "FDm": "13",
                                "Gn": "11",
                                "Hn": "61",
                                "PPd": "8",
                                "S": "4",
                                "U": "4",
                                "V": "VG",
                                "W": "7",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "7",
                                "Gm": "9",
                                "Hm": "81",
                                "Nm": "7",
                                "PPn": "10",
                                "S": "4",
                                "V": "VG",
                                "W": "8",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-06Z",
                    },
                    {
                        "Rep": [
                            {
                                "$": "Day",
                                "D": "WNW",
                                "Dm": "13",
                                "FDm": "12",
                                "Gn": "11",
                                "Hn": "66",
                                "PPd": "11",
                                "S": "4",
                                "U": "3",
                                "V": "VG",
                                "W": "8",
                            },
                            {
                                "$": "Night",
                                "D": "NW",
                                "FNm": "8",
                                "Gm": "7",
                                "Hm": "76",
                                "Nm": "8",
                                "PPn": "8",
                                "S": "4",
                                "V": "VG",
                                "W": "7",
                            },
                        ],
                        "type": "Day",
                        "value": "2017-04-07Z",
                    },
                ],
                "continent": "EUROPE",
                "country": "ENGLAND",
                "elevation": "4.0",
                "i": "351747",
                "lat": "51.4007",
                "lon": "-0.3337",
                "name": "HAMPTON COURT PALACE",
            },
            "dataDate": "2017-04-03T09:00:00Z",
        }

        with self.assertRaises(ValueError):
            dv.parse_json(json)
