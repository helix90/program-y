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

from telegram.ext import CommandHandler, filters, MessageHandler, Updater

from programy.clients.polling.client import PollingBotClient
from programy.clients.polling.telegram.config import TelegramConfiguration
from programy.utils.console.console import outputLog
from programy.utils.logging.ylogger import YLogger


def start(telegram_bot, update):
    if TelegramBotClient.TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TelegramBotClient.TELEGRAM_CLIENT.start(telegram_bot, update)


def message(telegram_bot, update):
    if TelegramBotClient.TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TelegramBotClient.TELEGRAM_CLIENT.message(telegram_bot, update)


def unknown(telegram_bot, update):
    if TelegramBotClient.TELEGRAM_CLIENT is None:
        raise Exception("Please initialise Telegram Client first")
    TelegramBotClient.TELEGRAM_CLIENT.unknown(telegram_bot, update)


class TelegramBotClient(PollingBotClient):

    TELEGRAM_CLIENT = None

    def __init__(self, argument_parser=None):
        self._updater = None
        self._telegram_token = None
        PollingBotClient.__init__(self, "telegram", argument_parser)

    def get_client_configuration(self):
        return TelegramConfiguration()

    def get_license_keys(self):
        self._telegram_token = self.license_keys.get_key("TELEGRAM_TOKEN")

    def create_updater(self, telegram_token):
        self._updater = Updater(token=telegram_token)

    def register_handlers(self):
        start_handler = CommandHandler("start", start)
        message_handler = MessageHandler(filters.text, message)
        unknown_handler = MessageHandler(filters.command, unknown)

        self._updater.dispatcher.add_handler(start_handler)
        self._updater.dispatcher.add_handler(message_handler)
        # Add unknown last
        self._updater.dispatcher.add_handler(unknown_handler)

    def get_initial_question(self, update):
        client_context = self.create_client_context(update.message.chat_id)
        initial_question = client_context.bot.get_initial_question(client_context)
        processed_question = client_context.bot.post_process_response(
            client_context, initial_question, srai=False
        )
        return processed_question

    def ask_question(self, userid, question):
        self._questions += 1
        client_context = self.create_client_context(userid)
        response = client_context.bot.ask_question(
            client_context, question, responselogger=self
        )
        return self.renderer.render(client_context, response)

    def start(self, telegram_bot, update):
        try:
            initial_question = self.get_initial_question(update)
            if initial_question:
                telegram_bot.send_message(
                    chat_id=update.message.chat_id, text=initial_question
                )
            else:
                YLogger.error(self, "Not initial question to return in start()")

        except Exception as e:
            YLogger.exception(self, "Failed to start", e)

    def message(self, telegram_bot, update):
        try:
            response = self.ask_question(update.message.chat_id, update.message.text)
            if response:
                telegram_bot.send_message(chat_id=update.message.chat_id, text=response)
            else:
                YLogger.error(self, "Not response to return in message()")

        except Exception as e:
            YLogger.exception(self, "Failed to handle message", e)

    def get_unknown_response(self, userid):
        return self.ask_question(
            userid, self.configuration.client_configuration.unknown_command_srai
        )

    def get_unknown_command(self, userid):
        if self.configuration.client_configuration.unknown_command_srai is None:
            unknown_response = self.configuration.client_configuration.unknown_command
        else:
            unknown_response = self.get_unknown_response(userid)
            if unknown_response is None or unknown_response == "":
                unknown_response = (
                    self.configuration.client_configuration.unknown_command
                )
        return unknown_response

    def unknown(self, telegram_bot, update):
        try:
            unknown_response = self.get_unknown_command(update.message.chat_id)
            if unknown_response:
                telegram_bot.send_message(
                    chat_id=update.message.chat_id, text=unknown_response
                )
                YLogger.error(self, "No response to return in unknown()")

        except Exception as e:
            YLogger.exception(self, "Failed to handle unknown", e)

    def display_connected_message(self):
        outputLog(self, "Telegram Bot connected and running...")

    def connect(self):
        if self._telegram_token is not None:
            self.create_updater(self._telegram_token)
            self.register_handlers()
            return True

        outputLog(self, "No telegram token defined, unable to connect")
        return False

    def poll_and_answer(self):

        running = True
        try:
            self._updater.start_polling()
            # Without this the system goes into 100% CPU utilisation
            self._updater.idle()

        except KeyboardInterrupt:
            outputLog(self, "Telegram client stopping....")
            running = False
            self._updater.stop()

        except Exception as excep:
            YLogger.exception(self, "Failed to poll and answer", excep)

        return running


if __name__ == "__main__":

    outputLog(None, "Initiating Telegram Client...")

    TelegramBotClient.TELEGRAM_CLIENT = TelegramBotClient()
    TelegramBotClient.TELEGRAM_CLIENT.run()
