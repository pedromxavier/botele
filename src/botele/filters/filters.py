from telegram import Message
from telegram.ext import MessageFilter

class Mention(MessageFilter):

    def __init__(self, username):
        self.username = username

    def filter(self, message: Message):
        for entity in message.entities:
            if entity['type'] == 'mention':
                i = entity['offset']
                j = entity['length']
                if message.text[i:i+j] == f'@{self.username}':
                    return True
        else:
            return False