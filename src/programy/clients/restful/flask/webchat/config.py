"""
Copyright (c) 2016-2020 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without webchatriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.clients.restful.config import RestConfiguration
from programy.utils.substitutions.substitues import Substitutions


class WebChatConfiguration(RestConfiguration):

    def __init__(self):
        RestConfiguration.__init__(self, "webchat")
        self._cookie_id = "ProgramYSession"
        self._cookie_expires = 90

    def _get_renderer_class(self):
        return "programy.clients.render.html.HtmlRenderer"

    @property
    def cookie_id(self):
        return self._cookie_id

    @property
    def cookie_expires(self):
        return self._cookie_expires

    def load_configuration_section(
        self, configuration_file, section, bot_root, subs: Substitutions = None
    ):

        assert section is not None

        self._cookie_id = configuration_file.get_option(
            section, "cookie_id", missing_value="ProgramYSession", subs=subs
        )
        self._cookie_expires = configuration_file.get_int_option(
            section, "cookie_expires", missing_value=90, subs=subs
        )
        super(WebChatConfiguration, self).load_configuration_section(
            configuration_file, section, bot_root, subs=subs
        )

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data["cookie_id"] = "ProgramYSession"
            data["cookie_expires"] = 90
        else:
            data["cookie_id"] = self._cookie_id
            data["cookie_expires"] = self._cookie_expires

        super(WebChatConfiguration, self).to_yaml(data, defaults)
