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

This is an example extension that allow you to call an external service to save the results of a survey
Currently contains no authentication
"""

from programy.extensions.base import Extension
from programy.utils.logging.ylogger import YLogger


class SurveyExtension(Extension):

    # execute() is the interface that is called from the <extension> tag in the AIML
    def execute(self, client_context, data):
        YLogger.debug(client_context, "Survey Storage - Storing data [%s]", data)

        # Data is bar delimited, so you could write to a file, add to a database, or send to another REST service
        for answer in data.split("|"):
            YLogger.debug(client_context, "Answer = %s", answer.strip())

        return "OK"
