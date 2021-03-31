from botele import Botele

from cstream import stderr

class TestBot(Botele):

    @Botele.error
    def error(self, info: dict):
        stderr[0] << info['error']