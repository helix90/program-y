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

from programy.utils.classes.loader import ClassLoader
from programy.utils.logging.ylogger import YLogger


class BaseTranslator:

    def initialise(self):
        pass  # pragma: no cover

    def languages(self):
        raise NotImplementedError()  # pragma: no cover

    def supports_language(self, language):
        raise NotImplementedError()  # pragma: no cover

    def language_code(self, code):
        raise NotImplementedError()  # pragma: no cover

    def detect(self, text, default="EN"):
        raise NotImplementedError()  # pragma: no cover

    def translate(self, text, from_lang, to_lang="EN"):
        raise NotImplementedError()  # pragma: no cover

    @staticmethod
    def initiate_translator(translator_config):
        if translator_config.classname is not None:
            try:
                YLogger.info(
                    None,
                    "Loading translator from class [%s]",
                    translator_config.classname,
                )
                translator_config = ClassLoader.instantiate_class(
                    translator_config.classname
                )
                translator = translator_config()
                translator.initialise()
                return translator
            except Exception as excep:
                YLogger.exception(None, "Failed to initiate translator", excep)
        else:
            YLogger.warning(None, "No configuration setting for translator!")

        return None
