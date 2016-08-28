import functools


class Sender(object):

    def __init__(self, app, update):
        self.app = app
        self.update = update

    async def send(self, text, **options):
        await self.app.sendMessage(self.update['message']['chat']['id'], text, **options)

    async def senduser(self, text, **options):
        await self.app.sendMessage(self.update['from']['chat']['id'], text, **options)