# Tlask
This will be a Telegram bot API for Python. Right now it doesn't work yet. I'll 
focus on supporting Python 3.5 first, and if that works the way it should, 
maybe I will make the library compatible with other Python versions.

## Features:
- Async
- Nice routing
- Behaves somewhat like Flask
- Enables easy middelware making

## Thanks 

I took some code from [werkzeug](https://github.com/pallets/werkzeug)
and  [flask](https://github.com/pallets/flask/). The code is clearly marked, and
the licence text is left in place. Please check these projects out if you
haven't heard about them, together they make the best Python web  framework:
http://flask.pocoo.org/.

The middelware design is taken from express.js, before I worked with Python,
I used node.js + express.js and I really liked their middelware so I made
Tlask middelware look like theirs.

## Licence

Flask and Werkzeug code: BSD licence 

Tlask code: MIT licence, see
[LICENCE](https://github.com/pingiun/tlask/blob/master/LICENSE.md)

## TODO
- Implement routing
- Make nice middelwares
  - User context  