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

import datetime
import re
import xml.etree.ElementTree as ET  # pylint: disable=wrong-import-order

from programy.dialog.sentence import Sentence
from programy.parser.exceptions import DuplicateGrammarException, ParserException
from programy.parser.pattern.graph import PatternGraph
from programy.parser.pattern.matchcontext import MatchContext
from programy.parser.template.graph import TemplateGraph
from programy.storage.factory import StorageFactory
from programy.utils.console.console import outputLog
from programy.utils.files.filefinder import FileFinder
from programy.utils.logging.ylogger import YLogger
from programy.utils.parsing.linenumxml import LineNumberingParser
from programy.utils.text.text import TextUtils


class AIMLLoader(FileFinder):

    def __init__(self, aiml_parser):
        FileFinder.__init__(self)
        self._aiml_parser = aiml_parser

    @property
    def parser(self):
        return self._aiml_parser

    def load_file_contents(self, fileid, filename, userid="*"):
        del fileid
        return self._aiml_parser.parse_from_file(filename, userid=userid)


class AIMLParser:
    RE_PATTERN_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile(r"^\{.*\}.*$")
    RE_MATCH_OF_TAG_AND_NAMESPACE_FROM_TEXT = re.compile(r"^(\{.*\})(.*)$")

    def __init__(self, brain):
        self._brain = brain
        self._pattern_parser = self.create_pattern_graph()
        self._template_parser = self.create_template_graph()
        self._aiml_loader = self.create_aiml_loader()
        self._num_categories = 0
        self._duplicates = None
        self._errors = None

    def create_pattern_graph(self):
        return PatternGraph(aiml_parser=self)

    def create_template_graph(self):
        return TemplateGraph(aiml_parser=self)

    def create_aiml_loader(self):
        return AIMLLoader(self)

    def __getstate__(self):
        # We don't need to pickle the File Writes for duplicates and errors,
        # __getstate__ is called during the pickling process to determin whih
        # attributes to load, so we remove the ones we don't want pickling
        d = dict(self.__dict__)
        del d["_brain"]
        if "_errors" in d:
            del d["_errors"]
        if "_duplicates" in d:
            del d["_duplicates"]
        return d

    @property
    def brain(self):
        return self._brain

    @property
    def num_categories(self):
        return self._num_categories

    @property
    def pattern_parser(self):
        return self._pattern_parser

    @property
    def template_parser(self):
        return self._template_parser

    def empty(self):
        self._pattern_parser.empty()

    def load_aiml(self):

        self.create_debug_storage()

        if (
            self.brain.bot.client.storage_factory.entity_storage_engine_available(
                StorageFactory.CATEGORIES
            )
            is True
        ):
            storage_engine = (
                self.brain.bot.client.storage_factory.entity_storage_engine(
                    StorageFactory.CATEGORIES
                )
            )
            category_store = storage_engine.category_store()
            category_store.load_all(self)
        else:
            YLogger.error(None, "No category storage defined, no aiml loaded!")

        self.save_debug_files()
        self.display_debug_info()

    @staticmethod
    def check_aiml_tag(aiml, filename=None):
        # Null check just to be sure
        if aiml is None:
            raise ParserException("Null root tag", filename=filename)

        tag_name, namespace = TextUtils.tag_and_namespace_from_text(aiml.tag)

        # Then if check is just <aiml>, thats OK
        if tag_name != "aiml":
            raise ParserException("Root tag is not <aiml>", filename=filename)

        return tag_name, namespace

    def parse_from_file(self, filename, userid="*"):
        YLogger.info(self, "Loading aiml file: " + filename)

        try:
            tree = ET.parse(filename, parser=LineNumberingParser())
            aiml = tree.getroot()

            _, namespace = AIMLParser.check_aiml_tag(aiml, filename=filename)

            start = datetime.datetime.now()
            num_categories = self.parse_aiml(aiml, namespace, filename, userid=userid)
            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.info(
                self,
                "Processed %s with %d categories in %f.2 secs",
                filename,
                num_categories,
                diff.total_seconds(),
            )

            return True

        except Exception as excep:
            YLogger.exception(
                self, "Failed to load contents of AIML file from [%s]", excep, filename
            )

        return False

    def parse_from_text(self, text):
        """
        Parse an AIML text version of an aiml file and return all the cateogeries found in the file
        :param text: Fully validated AIML snippet
        :return list of categories parsed from file:
        """

        start = datetime.datetime.now()
        aiml = ET.fromstring(text)

        _, namespace = AIMLParser.check_aiml_tag(aiml)

        num_categories = self.parse_aiml(aiml, namespace)

        stop = datetime.datetime.now()
        diff = stop - start
        YLogger.info(
            self,
            "Processed text with %d categories in %f.2 secs",
            num_categories,
            diff.total_seconds(),
        )

        return bool(num_categories > 0)

    def create_debug_storage(self):
        if self.brain.configuration.debugfiles.save_errors is True:
            self._errors = []
        if self.brain.configuration.debugfiles.save_duplicates is True:
            self._duplicates = []

    def save_debug_files(self):
        if self.brain.configuration.debugfiles.save_errors is True:
            if (
                self.brain.bot.client.storage_factory.entity_storage_engine_available(
                    StorageFactory.ERRORS
                )
                is True
            ):
                storage_engine = (
                    self.brain.bot.client.storage_factory.entity_storage_engine(
                        StorageFactory.ERRORS
                    )
                )
                errors_store = storage_engine.errors_store()
                errors_store.save_errors(self._errors)

        if self.brain.configuration.debugfiles.save_duplicates is True:
            if (
                self.brain.bot.client.storage_factory.entity_storage_engine_available(
                    StorageFactory.DUPLICATES
                )
                is True
            ):
                storage_engine = (
                    self.brain.bot.client.storage_factory.entity_storage_engine(
                        StorageFactory.DUPLICATES
                    )
                )
                duplicates_store = storage_engine.duplicates_store()
                duplicates_store.save_duplicates(self._duplicates)

    def display_debug_info(self):
        if self._errors is not None:
            outputLog(
                self,
                "Found a total of %d errors in your grammars, check your errors store"
                % len(self._errors),
            )
        if self._duplicates is not None:
            outputLog(
                self,
                "Found a total of %d duplicates in your grammars, check your duplicates store"
                % len(self._duplicates),
            )

    def handle_aiml_duplicate(self, dupe_excep, filename, expression):
        if self._duplicates is not None:
            dupe_excep.filename = filename
            msg = dupe_excep.format_message()
            YLogger.error(self, msg)

            startline = None
            endline = None
            if expression is not None:
                if hasattr(expression, "_start_line_number"):
                    startline = str(
                        expression._start_line_number
                    )  # pylint: disable=protected-access

                if hasattr(expression, "_end_line_number"):
                    endline = str(
                        expression._end_line_number
                    )  # pylint: disable=protected-access

            self._duplicates.append([dupe_excep.message, filename, startline, endline])

    def handle_aiml_error(self, parser_excep, filename, expression):
        if self._errors is not None:
            parser_excep.filename = filename
            msg = parser_excep.format_message()
            YLogger.error(self, msg)

            startline = None
            endline = None
            if expression is not None:
                if hasattr(expression, "_start_line_number"):
                    startline = str(
                        expression._start_line_number
                    )  # pylint: disable=protected-access

                if hasattr(expression, "_end_line_number"):
                    endline = str(
                        expression._end_line_number
                    )  # pylint: disable=protected-access

            self._errors.append([parser_excep.message, filename, startline, endline])

    def parse_aiml(self, aiml_xml, namespace, filename=None, userid="*"):
        del namespace

        self.parse_version(aiml_xml)

        categories_found = False
        num_category = 0
        for expression in aiml_xml:
            tag_name, namespace = TextUtils.tag_and_namespace_from_text(expression.tag)
            if tag_name == "topic":
                try:
                    num_topic_categories = self.parse_topic(expression, namespace)
                    num_category += num_topic_categories
                    categories_found = True

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename, expression)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename, expression)

            elif tag_name == "category":
                try:
                    self.parse_category(expression, namespace, userid=userid)
                    categories_found = True
                    num_category += 1

                except DuplicateGrammarException as dupe_excep:
                    self.handle_aiml_duplicate(dupe_excep, filename, expression)

                except ParserException as parser_excep:
                    self.handle_aiml_error(parser_excep, filename, expression)

            else:
                raise ParserException(
                    "Unknown top level tag, %s" % expression.tag, xml_element=expression
                )

        if categories_found is False:
            if filename is not None:
                YLogger.warning(self, "no categories in aiml file")
            else:
                YLogger.warning(self, "no categories in aiml file [%s]" % filename)

        return num_category

    def parse_version(self, aiml):
        if "version" in aiml.attrib:
            version = aiml.attrib["version"]
            if version not in ["0.9", "1.0", "1.1", "2.0"]:
                YLogger.warning(
                    self, "Version number not a supported version: %s", version
                )
        else:
            YLogger.warning(self, "No version info, defaulting to 2.0")
            version = "2.0"
        return version

    def parse_topic(self, topic_element, namespace):

        if "name" in topic_element.attrib:
            name = topic_element.attrib["name"]
            if name is None or not name:
                raise ParserException(
                    "Topic name empty or null", xml_element=topic_element
                )
            xml = "<topic>%s</topic>" % name
            YLogger.info(self, "Topic attrib converted to %s", xml)
            topic_pattern = ET.fromstring(xml)
        else:
            raise ParserException(
                "Missing name attribute for topic", xml_element=topic_element
            )

        category_found = False
        num_category = 0
        for child in topic_element:
            tag_name, _ = TextUtils.tag_and_namespace_from_text(child.tag)
            if tag_name == "category":
                self.parse_category(child, namespace, topic_pattern)
                category_found = True
                num_category += 1
            else:
                raise ParserException(
                    "Unknown child node of topic, %s" % child.tag,
                    xml_element=topic_element,
                )

        if category_found is False:
            raise ParserException("No categories in topic", xml_element=topic_element)

        return num_category

    def find_all(self, element, name, namespace):
        if namespace is not None:
            search = "%s%s" % (namespace, name)
            return element.findall(search)
        return element.findall(name)

    def find_topic(self, category_xml, namespace, topic_element=None):
        topics = self.find_all(category_xml, "topic", namespace)

        if topic_element is not None:
            if topics:
                raise ParserException(
                    "Topic exists in category AND as parent node",
                    xml_element=category_xml,
                )

        else:
            if len(topics) > 1:
                raise ParserException(
                    "Multiple <topic> nodes found in category", xml_element=category_xml
                )
            elif len(topics) == 1:
                topic_element = topics[0]
            else:
                topic_element = ET.fromstring("<topic>*</topic>")

        return topic_element

    def find_that(self, category_xml, namespace):
        thats = self.find_all(category_xml, "that", namespace)
        if len(thats) > 1:
            raise ParserException(
                "Multiple <that> nodes found in category", xml_element=category_xml
            )
        elif len(thats) == 1:
            that_element = thats[0]
        else:
            that_element = ET.fromstring("<that>*</that>")
        return that_element

    def get_template(self, category_xml, namespace):
        templates = self.find_all(category_xml, "template", namespace)
        if not templates:
            raise ParserException(
                "No template node found in category", xml_element=category_xml
            )
        elif len(templates) > 1:
            raise ParserException(
                "Multiple <template> nodes found in category", xml_element=category_xml
            )
        else:
            return self._template_parser.parse_template_expression(templates[0])

    def get_pattern(self, category_xml, namespace):
        patterns = self.find_all(category_xml, "pattern", namespace)
        if not patterns:
            raise ParserException(
                "No pattern node found in category", xml_element=category_xml
            )
        elif len(patterns) > 1:
            raise ParserException(
                "Multiple <pattern> nodes found in category", xml_element=category_xml
            )
        else:
            return patterns[0]

    def parse_category(
        self, category_xml, namespace, topic_element=None, add_to_graph=True, userid="*"
    ):

        topic_element = self.find_topic(category_xml, namespace, topic_element)

        that_element = self.find_that(category_xml, namespace)

        template_graph_root = self.get_template(category_xml, namespace)

        pattern = self.get_pattern(category_xml, namespace)

        if add_to_graph is True:
            self._pattern_parser.add_pattern_to_graph(
                pattern, topic_element, that_element, template_graph_root, userid=userid
            )
            self._num_categories += 1

        return (pattern, topic_element, that_element, template_graph_root)

    def match_sentence(
        self, client_context, pattern_sentence, topic_pattern, that_pattern
    ):

        topic_sentence = Sentence(client_context, topic_pattern)
        that_sentence = Sentence(client_context, that_pattern)

        YLogger.debug(
            client_context,
            "AIML Parser matching sentence [%s], topic=[%s], that=[%s] ",
            pattern_sentence.text(client_context),
            topic_pattern,
            that_pattern,
        )

        sentence = Sentence(client_context)
        sentence.append_sentence(pattern_sentence)
        sentence.append_word("__TOPIC__")
        sentence.append_sentence(topic_sentence)
        sentence.append_word("__THAT__")
        sentence.append_sentence(that_sentence)
        YLogger.debug(
            client_context,
            "Matching [%s]",
            sentence.words_from_current_pos(client_context, 0),
        )

        context = MatchContext(
            max_search_depth=client_context.bot.configuration.max_search_depth,
            max_search_timeout=client_context.bot.configuration.max_search_timeout,
        )

        template = self._pattern_parser.root.match(client_context, context, sentence)

        if template is not None:
            context.template_node = template

            context.list_matches(client_context)

            # Save the matched context for the associated sentence
            pattern_sentence.matched_context = context

            return context

        return None
