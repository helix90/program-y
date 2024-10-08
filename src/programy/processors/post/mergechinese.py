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

import re

from programy.processors.processing import PostProcessor
from programy.utils.language.chinese import ChineseLanguage
from programy.utils.logging.ylogger import YLogger


class MergeChinesePostProcessor(PostProcessor):

    def __init__(self):
        PostProcessor.__init__(self)

    def process(self, context, word_string):
        YLogger.debug(context, "Merging Chinese into understandable words...")

        words = word_string.split(" ")
        processed = ""
        for word in words:
            if ChineseLanguage.is_language(word):
                processed += word
            else:
                processed += " " + word + " "
        processed = re.sub(r"\s+", " ", processed)
        return processed.strip()
