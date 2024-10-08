"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import time

from programy.clients.client import BotClient
from programy.utils.logging.ylogger import YLogger


class PollingBotClient(BotClient):

    def __init__(self, botid, argument_parser=None):
        BotClient.__init__(self, botid, argument_parser=argument_parser)
        self._running = False

    def connect(self):
        return True

    def disconnect(self):
        return True

    def pre_poll(self):
        pass

    def poll_and_answer(self):
        raise NotImplementedError(
            "You must override this and implement the logic poll for messages and "
            "send answers back"
        )  # pragma: no cover

    def sleep(self, period):
        time.sleep(period)

    def display_connected_message(self):
        raise NotImplementedError()  # pragma: no cover

    def run(self, app=None):
        del app
        try:
            self.startup()

            if self.connect():
                self.display_connected_message()

                self.pre_poll()

                self._running = True
                while self._running:
                    self._running = self.poll_and_answer()

                YLogger.debug(self, "Exiting gracefully...")

            else:
                raise Exception("Connection failed....")

        except Exception as e:
            YLogger.exception(self, "Polling run error", e)

        finally:
            self.disconnect()

        self.shutdown()
