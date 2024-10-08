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

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programy.utils.text.text import TextUtils


class TemplateLinkNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._text = None
        self._url = None

    def resolve_to_string(self, client_context):
        resolved = "<link>"
        resolved += "<text>%s</text>" % self._text.resolve(client_context)
        if self._url is not None:
            resolved += "<url>%s</url>" % self._url.resolve(client_context)
        resolved += "</link>"
        return resolved

    def to_string(self):
        return "[LINK %d]" % (len(self._children))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        if "text" in expression.attrib:
            self._text = graph.get_word_node(expression.attrib["text"])

        if "url" in expression.attrib:
            self._url = graph.get_word_node(expression.attrib["url"])

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == "text":
                self._text = self.parse_children_as_word_node(graph, child)
            elif tag_name == "url":
                self._url = self.parse_children_as_word_node(graph, child)
            else:
                raise ParserException("Invalid child nodes in link")

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self._text is None:
            raise ParserException("Missing text from link")
