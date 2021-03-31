import traceback
import lorem
import re
from random import randint

from telegram import Message, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, MessageFilter, Filters

from botele import Botele
from botele.filter import UnknownCommand
from botele.botlib import file_name
from cstream import stderr, stdout

class MoonEmoji(MessageFilter):

    MOONS = [
        "🌝",
        "🌕",
        "🌗",
        "🌘",
        "🌖",
        "🌙",
        "🌜",
        "🌛",
        "🌚",
        "🌑",
        "🌓",
        "🌒",
        "🌔",
        "☪",
        "☾",
        "☽",
    ]

    def __init__(self):
        self.regex = re.compile("|".join(self.MOONS), re.MULTILINE | re.UNICODE)

    def filter(self, message: Message):
        return self.regex.search(message.text) is not None


class OVilaBot(Botele):
    def get_answer(self, text: str, **kwargs):
        return text

    @Botele.command("start", "Inicializa um chat com o bot")
    def _start(self, info):
        stdout[2] << f"> /start from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": self.uivo(),
        }
        return info["bot"].send_message(**kwargs)

    @Botele.command("lorem", "Gera um parágrafo Lorem Ipsum")
    def lorem(self, info):
        stdout[2] << f"> /lorem from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": lorem.paragraph(),
        }
        return info["bot"].send_message(**kwargs)

    @Botele.command("comandos", "Lista os comandos disponíveis")
    def comandos(self, info):
        stdout[2] << f"> /comandos from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": "\n".join([f"/{cmd}" for cmd, des in self.command_list]),
        }
        return info["bot"].send_message(**kwargs)

    @Botele.command("durma", "Bota o VilaBot para dormir")
    def durma(self, info):
        stdout[2] << f"> /durma from @{info['username']}"
        kwargs = {"chat_id": info["chat_id"], "text": f"🌙 {self.sono()} 🌙"}
        return info["bot"].send_message(**kwargs)

    @Botele.command("acorde", "Manda o VilaBot acordar")
    def acorde(self, info):
        stdout[2] << f"> /acorde from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": f"☀️ {self.uivo()} ☀️",
        }
        return info["bot"].send_message(**kwargs)

    @Botele.command("uive", "Uiva o lobo")
    def uive(self, info):
        stdout[2] << f"> /uive from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": self.uivo(),
        }
        return info["bot"].send_message(**kwargs)

    @Botele.command("lista")
    def _lista(self, info):
        stdout[2] << f"> /lista from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": self.command_list,
        }
        return info["bot"].send_message(**kwargs)

    @Botele.message(Filters.text & MoonEmoji())
    def moon_emoji(self, info):
        stdout[
            2
        ] << f"> Text Message with Moon Emoji from @{info['username']}:\n{info['text']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": self.uivo(),
            "reply_to_message_id": info["message_id"],
        }
        return info["bot"].send_message(**kwargs)

    @Botele.message(~Filters.command, Filters.text, ~Filters.group)
    def echo(self, info):
        stdout[2] << f"> Text Message from @{info['username']}:\n{info['text']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": self.get_answer(info["text"]),
        }
        return info["bot"].send_message(**kwargs)

    @Botele.message(UnknownCommand)
    def unknown(self, info):
        stdout[2] << f"> Unknown command '{info['text']}' from @{info['username']}"
        kwargs = {
            "chat_id": info["chat_id"],
            "text": f"Comando desconhecido: `{info['text']}`",
            "parse_mode": self.MARKDOWN,
        }
        return info["bot"].send_message(**kwargs)

    @Botele.error
    def error(self, info):
        for line in traceback.format_tb(info["error"].__traceback__):
            stderr << line
        stderr << info["error"]

    def sono(self):
        return f"{randint(2,4)*'Z'}{randint(3,6)*'z'}"

    def uivo(self):
        return f"{randint(1,3)*'A'}{randint(4,6)*'a'}{randint(5,8)*'u'}!"
