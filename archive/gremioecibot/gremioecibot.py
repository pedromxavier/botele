import traceback
import lorem
import re
from random import randint

from telegram import Message, MessageEntity
from telegram.ext import Updater, CommandHandler, MessageHandler, BaseFilter, Filters

from telebot.bot import TeleBot
from telebot.proxy import Proxy, lock_start, lock_awake
from telebot.layer import Layer, with_info
from telebot.filters import Mention
from telebot.botlib import start_logging, load, stdwar, stderr, stdout

TOKEN = load('gremioecibot.token')

class GremioEciBot(TeleBot):

    __cast__ = [with_info, lock_start, lock_awake]

    def get_answer(self, text: str, **kwargs):
        return text
        
    @lock_start.invert
    @TeleBot.command('start', 'Inicializa um chat com o bot')
    def start(self, info):
        stdout[2] << f"> /start from @{info['username']}"
        ## Starts chat
        chat = self.get_chat(info['chat_id'])
        chat.start()
        kwargs = {
            'chat_id': info['chat_id'],
            'text': "Olá, eu sou o bot do Grêmio ECI/UFRJ.",
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.command('lorem', 'Gera um parágrafo Lorem Ipsum')
    def lorem(self, info):
        stdout[2] << f"> /lorem from @{info['username']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': lorem.paragraph(),
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.command('comandos', 'Lista os comandos disponíveis')
    def comandos(self, info):
        stdout[2] << f"> /comandos from @{info['username']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': "\n".join([f"/{cmd}" for cmd, des in self.commands]),
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.command('lista')
    def _lista(self, info):
        stdout[2] << f"> /lista from @{info['username']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': self.command_list,
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.message(Mention('ovilabot'))
    def mention(self, info):
        stdout[2] << f"> Text Message from @{info['username']}:\n{info['text']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': self.get_answer(info['text']),
            'reply_to_message_id': info['message_id'],
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.message(~Filters.command, Filters.text, ~Filters.group)
    def echo(self, info):
        stdout[2] << f"> Text Message from @{info['username']}:\n{info['text']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': self.get_answer(info['text']),
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.message(Filters.command)
    def unknown(self, info):
        stdout[2] << f"> Unknown command '{info['text']}' from @{info['username']}"
        kwargs = {
            'chat_id': info['chat_id'],
            'text': f"Comando desconhecido: `{info['text']}`",
            'parse_mode': self.MARKDOWN
        }
        return info['bot'].send_message(**kwargs)

    @TeleBot.catch_error
    def error(self, info):
        for line in traceback.format_tb(info['error'].__traceback__):
            stderr << line
        stderr << info['error']

if __name__ == '__main__':
    with GremioEciBot(TOKEN) as bot:
        bot.run()