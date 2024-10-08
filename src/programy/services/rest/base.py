"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import threading
from abc import ABC
from datetime import datetime

import requests
from requests.exceptions import HTTPError

from programy.services.base import Service, ServiceException
from programy.utils.logging.ylogger import YLogger


class RESTServiceException(ServiceException):

    def __init__(self, msg):
        ServiceException.__init__(self, msg)


class RESTService(Service, ABC):

    DEFAULT_RETRIES = [100, 500, 1000, 2000, 5000, 10000]

    def __init__(self, configuration):
        Service.__init__(self, configuration)

    def _response_to_json(self, api, response):
        raise NotImplementedError()  # pragma: no cover

    def _add_base_payload(self, data, status, api, url, call, retries, started, speed):
        data["response"]["status"] = status
        data["response"]["url"] = url
        data["response"]["api"] = api
        data["response"]["call"] = call
        data["response"]["retries"] = retries
        if started is not None:
            data["response"]["started"] = started.strftime("%d/%m/%Y, %H:%M:%S")
        if speed is not None:
            data["response"]["speed"] = str(speed.microseconds / 1000) + "ms"
        data["response"]["service"] = self.name
        data["response"]["category"] = self.category

    def _create_success_payload(
        self, api, url, call, retries, started, speed, response
    ):
        data = {}
        data["response"] = {}
        self._add_base_payload(data, "success", api, url, call, retries, started, speed)
        data["response"]["payload"] = self._response_to_json(api, response)
        return data

    def _create_statuscode_failure_payload(
        self, api, url, call, retries, started, speed, response
    ):
        data = {}
        data["response"] = {}
        self._add_base_payload(data, "failure", api, url, call, retries, started, speed)
        data["response"]["payload"] = {}
        data["response"]["payload"]["type"] = "statusCode"
        data["response"]["payload"]["statusCode"] = response.status_code
        return data

    def _create_http_failure_payload(
        self, api, url, call, retries, started, speed, http_err
    ):
        data = {}
        data["response"] = {}
        self._add_base_payload(data, "failure", api, url, call, retries, started, speed)
        data["response"]["payload"] = {}
        data["response"]["payload"]["type"] = "http"
        data["response"]["payload"]["httpError"] = str(http_err)
        return data

    def _create_general_failure_payload(
        self, api, url, call, retries, started, speed, err
    ):
        data = {}
        data["response"] = {}
        self._add_base_payload(data, "failure", api, url, call, retries, started, speed)
        data["response"]["payload"] = {}
        data["response"]["payload"]["type"] = "general"
        data["response"]["payload"]["error"] = str(err)
        return data

    def _requests_get(self, url, headers, timeout):
        response = requests.get(url, headers=headers, timeout=timeout)
        return response

    def _do_get(self, url, headers=None):

        response = self._requests_get(
            url, headers=headers, timeout=self.configuration.timeout
        )
        if response.status_code != 408:
            return response, 0

        count = 1
        while count < len(self.configuration.retries):
            YLogger.warning(
                self,
                "Timeout, sleeping for {0}ms".format(
                    (self.configuration.retries[count])
                ),
            )
            threading.sleep(self.configuration.retries[count])

            response = self._requests_get(
                url, headers=headers, timeout=self.configuration.timeout
            )
            YLogger.debug(self, response)
            if response.status_code != 408:
                break

            count += 1

        return response, count

    def _get(self, api, url, headers=None):
        started = None
        speed = None
        retries = 0
        try:
            started = datetime.now()
            if self.configuration.timeout:
                response, retries = self._do_get(url, headers)
            else:
                response = requests.get(url, headers)
            speed = started - datetime.now()

            # If the response was successful, no Exception will be raised
            response.raise_for_status()

            if response.status_code == 200:
                return self._create_success_payload(
                    api, url, "GET", retries, started, speed, response
                )

            else:
                return self._create_statuscode_failure_payload(
                    api, url, "GET", retries, started, speed, response
                )

        except HTTPError as http_err:
            return self._create_http_failure_payload(
                api, url, "GET", retries, started, speed, http_err
            )

        except Exception as err:
            return self._create_general_failure_payload(
                api, url, "GET", retries, started, speed, err
            )

    def _requests_post(self, url, headers, params, timeout):
        return requests.post(url, headers=headers, data=params, timeout=timeout)

    def _do_post(self, url, params, headers=None):

        response = self._requests_post(
            url, headers=headers, params=params, timeout=self.configuration.timeout
        )
        if response.status_code != 408:
            return response, 0

        count = 1
        while count < len(self.configuration.retries):
            YLogger.warning(
                self,
                "Timeout, sleeping for {0}ms".format(
                    (self.configuration.retries[count])
                ),
            )
            threading.sleep(self.configuration.retries[count])

            response = self._requests_post(
                url, headers=headers, data=params, timeout=self.configuration.timeout
            )
            if response.status_code != 408:
                break

            count += 1

        return response.count

    def _post(self, api, url, params, headers=None):
        started = None
        speed = None
        retries = 0
        try:
            started = datetime.now()
            if self.configuration.timeout:
                response, retries = self._do_post(url, params, headers)
            else:
                response = requests.post(url, headers=headers, data=params)
            speed = started - datetime.now()

            # If the response was successful, no Exception will be raised
            response.raise_for_status()

            if response.status_code == 200:
                return self._create_success_payload(
                    api, url, "post", retries, started, speed, response
                )

            else:
                return self._create_statuscode_failure_payload(
                    api, url, "post", retries, started, speed, response
                )

        except HTTPError as http_err:
            return self._create_http_failure_payload(
                api, url, "post", retries, started, speed, http_err
            )

        except Exception as err:
            return self._create_general_failure_payload(
                api, url, "post", retries, started, speed, err
            )

    def query(self, api, url, type="GET", params=None, headers=None):

        if type == "GET":
            return self._get(api, url, headers=headers)

        elif type == "POST":
            return self._post(api, url, params, headers=headers)

        else:
            raise RESTServiceException("Invalid REST call type [%s]" % (type))
