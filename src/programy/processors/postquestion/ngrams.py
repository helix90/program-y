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

from programy.dialog.sentence import Sentence
from programy.nlp.ngrams import NGramsCreator
from programy.processors.processing import PostQuestionProcessor
from programy.utils.logging.ylogger import YLogger


class NGramsPostQuestionProcessor(PostQuestionProcessor):

    def __init__(self):
        PostQuestionProcessor.__init__(self)

    def _ngrams(self, context, word_string):
        sentences = NGramsCreator.get_ngrams(word_string, 3)
        for ngram in sentences:
            text = context.brain.tokenizer.words_to_texts(ngram)
            sentence = Sentence(context, text)
            response = context.brain.ask_question(context, sentence)
            if response is not None:
                return response

        return None

    def process(self, context, word_string):
        YLogger.debug(context, "Creating ngrams from sentence...")
        try:
            return self._ngrams(context, word_string)

        except Exception as excep:
            YLogger.exception(self, "Failed to create NGrams", excep)

        return None
