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

from programy.config.base import BaseConfigurationData
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions


class BotSentimentAnalyserConfiguration(BaseConfigurationData):

    def __init__(self):
        BaseConfigurationData.__init__(self, name="sentiment")
        self._classname = None
        self._scores = None

    @property
    def classname(self):
        return self._classname

    @property
    def scores(self):
        return self._scores

    def load_config_section(
        self, configuration_file, configuration, bot_root, subs: Substitutions = None
    ):
        del bot_root
        sentiment = configuration_file.get_section(self._section_name, configuration)
        if sentiment is not None:
            self._classname = configuration_file.get_option(
                sentiment, "classname", missing_value=None, subs=subs
            )
            self._scores = configuration_file.get_option(
                sentiment,
                "scores",
                missing_value="programy.nlp.sentiment.scores.SentimentScores",
                subs=subs,
            )
        else:
            YLogger.warning(
                self, "'sentiment' section missing from bot config, using defaults"
            )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["classname"] = (
                "programy.nlp.sentiment.textblob_sentiment.TextBlobSentimentAnalyser"
            )
            data["scores"] = "programy.nlp.sentiment.scores.SentimentScores"

        else:
            data["classname"] = self._classname
            data["scores"] = self._scores
