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

This is an example extension that allow syou to call an external service to retreive the bank balance
of the customer. Currently contains no authentication
"""

from programy.extensions.base import Extension
from programy.utils.logging.ylogger import YLogger


class BankingBalanceExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(
            client_context,
            "Bank Balance - Calling external service for with extra data [%s]",
            data,
        )

        #
        # Add the logic to receive the balance and format it into pounds and pence and either CREDIT|DEBIT
        #
        #

        return "0 00 CREDIT"
