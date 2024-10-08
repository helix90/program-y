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

from programy.clients.ping.config import PingResponderConfig
from programy.config.bot.bot import BotConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.config.container import BaseContainerConfigurationData
from programy.scheduling.config import SchedulerConfiguration
from programy.storage.config import StorageConfiguration
from programy.triggers.config import TriggerConfiguration
from programy.utils.email.config import EmailConfiguration
from programy.utils.logging.ylogger import YLogger
from programy.utils.substitutions.substitues import Substitutions


class ClientConfigurationData(BaseContainerConfigurationData):

    def __init__(self, name):
        BaseContainerConfigurationData.__init__(self, name)
        self._description = "ProgramY AIML2.0 Client"
        self._renderer = self._get_renderer_class()
        self._scheduler = SchedulerConfiguration()
        self._storage = StorageConfiguration()
        self._email = EmailConfiguration()
        self._triggers = TriggerConfiguration()
        self._responder = PingResponderConfig()

        self._bot_selector = self._get_bot_selector_class()
        bot_config = BotConfiguration("bot")
        self._bot_configs = [bot_config]

    def _get_renderer_class(self):
        return "programy.clients.render.text.TextRenderer"

    def _get_bot_selector_class(self):
        return "programy.clients.botfactory.DefaultBotSelector"

    @property
    def description(self):
        return self._description

    @property
    def configurations(self):
        return self._bot_configs

    @property
    def bot_selector(self):
        return self._bot_selector

    @property
    def scheduler(self):
        return self._scheduler

    @property
    def storage(self):
        return self._storage

    @property
    def renderer(self):
        return self._renderer

    @property
    def email(self):
        return self._email

    @property
    def triggers(self):
        return self._triggers

    @property
    def responder(self):
        return self._responder

    def load_configuration(
        self, configuration_file, bot_root, subs: Substitutions = None
    ):
        client = configuration_file.get_section(self.section_name)
        if client is None:
            YLogger.error(
                None,
                'Client section named [%s] not found, trying "client"',
                self.section_name,
            )
            client = configuration_file.get_section("client")

        if client is not None:
            self.load_configuration_section(configuration_file, client, bot_root, subs)

        else:
            YLogger.error(None, "No client section not found!")

    def load_configuration_section(
        self, configuration_file, section, bot_root, subs: Substitutions = None
    ):

        assert configuration_file is not None
        assert section is not None

        self._description = configuration_file.get_option(
            section, "description", missing_value="ProgramY AIML2.0 Client", subs=subs
        )

        self._scheduler.load_config_section(
            configuration_file, section, bot_root, subs=subs
        )

        self._storage.load_config_section(
            configuration_file, section, bot_root, subs=subs
        )

        self._renderer = configuration_file.get_option(section, "renderer", subs=subs)

        self._email.load_config_section(
            configuration_file, section, bot_root, subs=subs
        )

        self._triggers.load_config_section(
            configuration_file, section, bot_root, subs=subs
        )

        self._responder.load_config_section(
            configuration_file, section, bot_root, subs=subs
        )

        self._load_bot_configurations(configuration_file, section, bot_root, subs)

    def _load_bot_configurations(self, configuration_file, section, bot_root, subs):
        bots = configuration_file.get_section("bots", section)
        if bots is not None:
            bot_keys = configuration_file.get_keys(bots)
            first = True
            for name in bot_keys:
                if first is True:
                    self._bot_configs.clear()
                    first = False
                bot_config = configuration_file.get_section(name, bots)
                config = BotConfiguration(name)
                config.load_configuration_section(
                    configuration_file, bot_config, bot_root, subs=subs
                )
                self._bot_configs.append(config)

        if len(self._bot_configs) == 0:
            YLogger.warning(
                self,
                "No bot name defined for client [%s], defaulting to 'bot'.",
                self.section_name,
            )
            self._bot_configs.append(BotConfiguration("bot"))
            self._bot_configs[0].configurations.append(BrainConfiguration("brain"))

        self._bot_selector = configuration_file.get_option(
            section,
            "bot_selector",
            missing_value="programy.clients.botfactory.DefaultBotSelector",
            subs=subs,
        )

    def to_yaml(self, data, defaults=True):

        assert data is not None

        if defaults is True:
            data["description"] = "ProgramY AIML2.0 Client"
            data["bot_selector"] = "programy.clients.botfactory.DefaultBotSelector"

            data["scheduler"] = {}
            self._scheduler.to_yaml(data["scheduler"], defaults)

            data["email"] = {}
            self._email.to_yaml(data["email"], defaults)

            data["triggers"] = {}
            self._triggers.to_yaml(data["triggers"], defaults)

            data["responder"] = {}
            self._responder.to_yaml(data["responder"], defaults)

            data["renderer"] = "programy.clients.render.text.TextRenderer"

            data["storage"] = {}
            self._storage.to_yaml(data["storage"], defaults)

            data["bots"] = {}
            data["bots"]["bot"] = {}
            bot_config = BotConfiguration("bot")
            bot_config.to_yaml(data["bots"]["bot"], defaults)

        else:
            data["description"] = self._description
            data["bot_selector"] = self.bot_selector

            data[self._scheduler.id] = {}
            self._scheduler.to_yaml(data[self._scheduler.id], defaults)

            data["email"] = {}
            self._email.to_yaml(data["email"], defaults)

            data["triggers"] = {}
            self._triggers.to_yaml(data["triggers"], defaults)

            data["responder"] = {}
            self._responder.to_yaml(data["responder"], defaults)

            data["renderer"] = self.renderer

            data["storage"] = {}
            self._storage.to_yaml(data["storage"], defaults)

            data["bots"] = {}
            for botconfig in self._bot_configs:
                data["bots"][botconfig.id] = {}
                botconfig.to_yaml(data["bots"][botconfig.id], defaults)
