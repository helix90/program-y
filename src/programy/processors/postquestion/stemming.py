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
from programy.nlp.stemming import Stemmer
from programy.processors.processing import PostQuestionProcessor
from programy.utils.logging.ylogger import YLogger


class StemmingPostQuestionProcessor(PostQuestionProcessor):

    def __init__(self):
        PostQuestionProcessor.__init__(self)

    def process(self, context, word_string):
        YLogger.debug(context, "Stemming sentence...")
        stemmer = Stemmer()
        unstemmed_words = context.brain.tokenizer.texts_to_words(word_string)
        stemmed_words = [stemmer.stem(x) for x in unstemmed_words]
        text = context.brain.tokenizer.words_to_texts(stemmed_words)
        sentence = Sentence(context, text)
        response = context.brain.ask_question(context, sentence)
        return response
