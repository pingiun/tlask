import sys
sys.path.append('..')
from tlask import Tlask
app = Tlask(__name__)

@app.route("/start")
def welcome(res, update):
    print(update['message']['text'])
    # Doesn't work yet:
    # res.send("Welcome!", [['Say Hi']])

if __name__ == "__main__":
    app.run("255364908:AAE9g6lPIT_Ti_xoU04JaBcXi1qR6ZB3AdU")