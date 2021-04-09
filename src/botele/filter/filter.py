# Standard Library
import datetime as dt

from telegram import Message, MessageEntity
from telegram.ext import MessageFilter, Filters


class Recent(MessageFilter):
    def __init__(self, delay: dt.timedelta = dt.timedelta(days=1)):
        self.delay = delay

    def filter(self, message: Message):
        return abs(dt.datetime.now() - message.date) <= self.delay


class Mention(MessageFilter):
    def __init__(self, username):
        self.username = username

    def filter(self, message: Message):
        for entity in message.entities:
            if entity.type == MessageEntity.MENTION:
                i = entity.offset
                j = entity.length
                if message.text[i : i + j] == f"@{self.username}":
                    return True
        else:
            return False


class UnknownCommand(MessageFilter):
    def __init__(self, bot_name: str):
        """"""
        self.bot_name = bot_name

    def filter(self, message: Message):
        """"""
        if message.entities:
            first_entity = message.entities[0]
            if first_entity.type == MessageEntity.BOT_COMMAND:
                i = first_entity.offset
                if i == 0:
                    if Filters.chat_type.private:
                        return True
                    elif Filters.chat_type.groups:
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False


__all__ = ["Mention", "UnknownCommand"]