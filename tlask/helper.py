from .utils import get_flavor

class Sender(object):

    def __init__(self, app, update):
        self.app = app
        self.update = update
        flavor = get_flavor(update)
        if flavor == 'message' or flavor == 'edited_message':
            self.chat = update['message']['chat']['id']
            self.user = update['message']['from']['id'] 
        elif flavor == 'callback_query':
            self.chat = update['callback_query']['message']['chat']['id']
            self.user = update['callback_query']['message']['from']['id']

    async def send(self, text, **options):
        await self.app.sendMessage(self.chat, text, **options)

    async def senduser(self, text, **options):
        await self.app.sendMessage(self.user, text, **options)