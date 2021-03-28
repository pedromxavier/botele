## Standard Library
import re
import json
from pathlib import Path
from functools import wraps, reduce

## Third-Party
from telegram import Update
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters, CallbackContext
from telegram.ext import (
    MessageHandler,
    CommandHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
)

from pyckage.pyckagelib import PackageData
from cstream import stderr, stdlog

class BotCallback(object):
    def __init__(self, bot, callback):
        self.bot = bot
        self.callback = callback

    def __call__(self, *args, **kwargs):
        return self.callback(self.bot, self.bot.get_info(*args), **kwargs)


class MessageCallback(BotCallback):
    def __init__(self, bot, callback, filters: list, *, kwargs: dict = None):
        BotCallback.__init__(self, bot, callback)
        self.filters = reduce(lambda x, y: x & y, filters)
        self.kwargs = kwargs


class CommandCallback(BotCallback):
    def __init__(
        self,
        bot,
        callback,
        command_name: str,
        description: str = None,
        *,
        kwargs: dict = None,
    ):
        BotCallback.__init__(self, bot, callback)
        self.command_name = command_name
        self.description = description
        self.kwargs = kwargs


class QueryCallback(BotCallback):
    def __init__(self, bot, callback, pattern: str = None):
        BotCallback.__init__(self, bot, callback)
        self.pattern = pattern


class ErrorCallback(BotCallback):
    def __init__(self, bot, callback):
        BotCallback.__init__(self, bot, callback)


class MetaBotele(type):
    """"""

    def __new__(cls, name: str, bases: tuple, attrs: dict):
        cls.get_handlers(attrs)
        return super().__new__(cls, name, bases, attrs)

    @classmethod
    def get_handlers(cls, attrs: dict):
        command_list = []
        command_handlers = []
        message_handlers = []
        query_handlers = []
        error_handler = None

        for name, item in attrs.items():
            if isinstance(item, CommandCallback):
                command_handlers.append(item)
                # Commands handled by functions which name is started with '_' are ignored.
                if not name.startswith("_"):
                    command_list.append((item.name, item.description))
            if isinstance(item, MessageCallback):
                message_handlers.append(item)
            if isinstance(item, MessageCallback):
                query_handlers.append(item)
            if isinstance(item, ErrorCallback):
                # Adds the latest defined error handler
                error_handler = item

        attrs.update(
            {
                "command_list": command_list,
                "command_handlers": command_handlers,
                "message_handlers": message_handlers,
                "query_handlers": query_handlers,
                "error_handler": error_handler,
            }
        )


class Botele(metaclass=MetaBotele):

    package_data = PackageData("botele")

    ## Constants
    MARKDOWN = ParseMode.MARKDOWN_V2

    command_list = []
    command_handlers = []
    message_handlers = []
    query_handlers = []
    error_handler = None

    __data__ = {}

    def __init__(self, token: str, name: str, path: str, *, source: str = None):
        self.__name = name
        self.__path = Path(path)
        self.__token = token
        self.__source = source

    @property
    def source(self) -> Path:
        return None if self.__source is None else Path(self.__source)

    @property
    def name(self) -> str:
        return self.__name

    @property
    def path(self) -> Path:
        return self.__path

    @property
    def token(self) -> str:
        return self.__token

    def setup(self):
        ## Setup Updater
        self.updater = Updater(token=self.token, use_context=True)
        stdlog[1] << "> Updater setup"

        ## Retrieve Dispatcher
        self.dispatcher = self.updater.dispatcher

        ## Add Handlers
        self.add_handlers()
        stdlog[1] << "> Handlers added"

    def run(self, idle: bool = True):
        """"""
        try:
            self.updater.start_polling()
            if idle:
                stdlog[0] << "> Started Polling, going idle."
                self.updater.idle()
            else:
                stdlog[0] << "> Started Polling."
        except KeyboardInterrupt:
            stderr[1] << "Keyboard Interrupt"
            return
        finally:
            if idle:
                if self.updater.running:
                    self.updater.stop()
                stdlog[0] << "> Stopped"
            else:
                stdlog[0] << "> remember calling 'bot.stop()' afterwards."

    def stop(self):
        try:
            stdlog[1] << "> Stopping bot."
            return self.updater.stop()
        except:
            stderr[1] << "> Failed to stop bot."

    @classmethod
    def load(cls, data: dict):
        """"""
        return cls(**data)

    def save(self) -> dict:
        return {
            "name": self.name,
            "path": self.path,
            "token": self.token,
            "source": self.source,
        }

    def get_data_path(self) -> str:
        """"""
        data_path = self.path.joinpath(".bot-data")

        if not data_path.exists():
            raise FileNotFoundError("Bot data not found.")
        else:
            return data_path

    def load_data(self):
        """"""
        with open(self.get_data_path(), mode="r") as file:
            self.__data__.update(json.load(file))

    def save_data(self):
        """"""
        with open(self.get_data_path(), mode="w") as file:
            json.dump(self.__data__, file)

    ## Context Management
    def __enter__(self, *args, **kwargs):
        self.load_data()
        return self

    def __exit__(self, *args, **kwargs):
        self.save_data()

    ## Event Handlers
    def add_handlers(self):
        self.add_command_handlers()
        self.add_message_handlers()
        self.add_query_handlers()
        self.add_error_handler()

    def add_command_handlers(self):
        for cmd in self.command_handlers:
            ## Create Handler Object
            handler = CommandHandler(cmd.name, cmd, **cmd.kwargs)

            ## Add Handler to Dispatcher
            self.dispatcher.add_handler(handler)

            stdlog[3] << f"> Add Command Handler: /{cmd.name} @{cmd}"

    def add_message_handlers(self):
        for msg in self.message_handlers:
            ## Create Handler Object
            handler = MessageHandler(msg.filters, msg, **msg.kwargs)

            ## Add Handler to Dispatcher
            self.dispatcher.add_handler(handler)

            stdlog[3] << f"> Add Message Handler: [{msg.filters}] @{msg}"

    def add_query_handlers(self):
        for query in self.query_handlers:
            if query.pattern is None:
                handler = CallbackQueryHandler(query)
            else:
                handler = CallbackQueryHandler(query, pattern=query.pattern)

            ## Add Handler to Dispatcher
            self.dispatcher.add_handler(handler)

            stdlog[3] << f"> Add Query Handler: [{query.pattern}] @{query}"

    def add_error_handler(self):
        if self.error_handler is not None:
            self.dispatcher.add_error_handler(self.error_handler)
            stdlog[3] << f"> Add Error Handler: @{self.error_handler}"

    @classmethod
    def get_info(cls, *args):
        return args[0] if (len(args) == 1) else cls._get_info(args[0], args[1])

    @classmethod
    def _get_info(cls, update: Update, context) -> dict:
        """get_info(update, context) -> dict
        This function is intended to gather the most relevant information
        from these two objects into a single dictionary.
        """
        return {
            "error": context.error,
            "chat": update.effective_chat,
            "chat_id": update.effective_chat.id,
            "type": update.effective_chat.type,
            "title": update.effective_chat.title,
            "message": update.message,
            "message_id": update.message.message_id,
            "text": update.message.text,
            "args": context.args,
            "username": update.effective_user.username,
            "name": update.effective_user.name,
            "full_name": update.effective_user.full_name,
            "query": update.callback_query,
            "user": update.effective_user,
            "user_id": update.effective_user.id,
            "bot": context.bot,
        }

    @classmethod
    def keyboard_markup(cls, key: str, *rows) -> InlineKeyboardMarkup:
        """
        Examples
        --------
        >>> keyboard_markup("data-01",
            ["Option1", "Option2"],
            [("Pay!", {'pay': True})],
            [("some fancy url", {'url': 'http://fancy.url'})]
        )

        """
        if re.match("[a-zA-Z][a-zA-Z0-9_-]+", key) is None:
            raise ValueError(
                f"Key `{key}` doesn't match regex `[a-zA-Z][a-zA-Z0-9_-]+`."
            )

        keyboard = []
        for row in rows:
            keyboard_row = []
            for value in row:
                if type(value) is str:
                    callback_data = f"{key}:{value}"
                    kwargs = {}
                elif type(value) is tuple and len(value) == 2:
                    text, kwargs = value
                    if "data" in kwargs:
                        data = kwargs["data"]
                        del kwargs["data"]
                    else:
                        data = text
                    callback_data = f"{key}:{data}"
                else:
                    raise ValueError("DOCUMENT ME PLEASE :'(")
                button = InlineKeyboardButton(
                    text, callback_data=callback_data, **kwargs
                )
                stdlog[3] << f">>> Add key `{callback_data}`"
                keyboard_row.append(button)
            keyboard.append(keyboard_row)
        return InlineKeyboardMarkup(keyboard)

    @classmethod
    def command(cls, command_name: str, description: str = "?", **kwargs: dict):
        """"""

        def decor(callback):
            return CommandCallback(
                cls, callback, command_name, description, kwargs=kwargs
            )

        return decor

    @classmethod
    def message(cls, *filters: Filters, **kwargs: dict):
        """"""

        def decor(callback):
            return MessageCallback(cls, callback, filters, kwargs=kwargs)

        return decor

    @classmethod
    def query(cls, key: str = None):
        # if key is not None:
        #     pattern = r'^{}\:(.+)$'.format(key)
        #     regex = re.compile(pattern)
        #     if re.match('[a-zA-Z]+', key) is None:
        #             raise ValueError(f"Key `{key}` doesn't match regex `[a-zA-Z]+`.")
        # else:
        #     pattern = None
        #     regex = re.compile('.*')
        def decor(callback: callable) -> callable:
            return QueryCallback(cls, callback, None)

        return decor

    @classmethod
    def error(cls, callback):
        return ErrorCallback(cls, callback)

    @property
    def username(self):
        return self.updater.bot.name

    def list_commands(self) -> str:
        """"""
        return "\n".join("{0} - {1}".format(*cmd) for cmd in self.command_list)
