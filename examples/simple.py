import sys
sys.path.append('..')

import logging
logging.basicConfig(
    format='%(asctime)s (%(levelname)s)%(name)s: %(message)s',
    level=logging.DEBUG)

from tlask import Tlask
app = Tlask(__name__)


@app.route('/')  # '/' is a special name for /start, like on websites
async def start(res, update):
    print(update['message']['text'])
    await res.send("Welcome!")


"""
@app.route('/language') # Change the language of the app
def languages(res, update):
    res.send("Select a language from the list:", ['English', 'Deutsch'])

@app.route('/language/<language>')
def set_language(res, update, language):
    update.session.set('language', language)
    res.redirect('/', "Language set to ")
"""
if __name__ == "__main__":
    app.loglevel = logging.DEBUG
    app.run("255364908:AAE9g6lPIT_Ti_xoU04JaBcXi1qR6ZB3AdU")
