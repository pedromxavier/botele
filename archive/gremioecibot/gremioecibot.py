import traceback
import lorem
import re
from random import randint

from telegram import Message, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, Filters
from cstream import stdwar, stderr, stdout

from botele import Botele


class GremioEciBot(Botele):
    """"""

    @Botele.command("start", "Inicializa um chat com o bot")
    def _start(self, info: dict):
        stdout[2] << f"> /start from @{info['username']}"
        params = {
            "chat_id": info["chat_id"],
            "text": "Olá, eu sou o bot do Grêmio ECI/UFRJ.",
        }
        return info["bot"].send_message(**params)

    @Botele.command("lorem", "Gera um parágrafo Lorem Ipsum")
    def lorem(self, info: dict):
        stdout[2] << f"> /lorem from @{info['username']}"
        params = {
            "chat_id": info["chat_id"],
            "text": lorem.paragraph(),
        }
        return info["bot"].send_message(**params)

    @Botele.command("comandos", "Lista os comandos disponíveis")
    def comandos(self, info: dict):
        stdout[2] << f"> /comandos from @{info['username']}"
        params = {
            "chat_id": info["chat_id"],
            "text": "\n".join([f"/{cmd}" for cmd, des in self.command_list]),
        }
        return info["bot"].send_message(**params)

    @Botele.command("lista")
    def _lista(self, info):
        stdout[2] << f"> /lista from @{info['username']}"
        params = {
            "chat_id": info["chat_id"],
            "text": self.list_commands(),
        }
        return info["bot"].send_message(**params)

    @Botele.message(Filters.command)
    def unknown(self, info: dict):
        stdout[2] << f"> Unknown command '{info['text']}' from @{info['username']}"
        params = {
            "chat_id": info["chat_id"],
            "text": f"Comando inválido: `{info['text']}`",
            "parse_mode": self.MARKDOWN,
        }
        return info["bot"].send_message(**params)

    @Botele.error
    def error(self, info: dict):
        for line in traceback.format_tb(info["error"].__traceback__):
            stderr[0] << line
        stderr[0] << info["error"]
