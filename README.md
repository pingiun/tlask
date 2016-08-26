# Tlask
![Travis Status](https://travis-ci.org/pingiun/tlask.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/pingiun/tlask/badge.svg?branch=master)](https://coveralls.io/github/pingiun/tlask?branch=master)

This will be a Telegram bot API for Python. Right now it doesn't do all the
things you'd expect from a Telegram bot api. I'll  focus on supporting Python
3.5 first, and if that works the way it should,  maybe I will make the library
compatible with other Python versions.

## Features:
- Async
- Nice routing (not yet)
- Behaves somewhat like Flask
- Enables easy middelware making

## Installation

I do not recommend using this api for your bots right now, it isn't nearly
finished and I can't guarantee that it will ever work 100%, because this is my
first serious library. If you really do want to install this though, you can
follow these instructions (make sure you have Python 3.5.x or higher):
1. Clone this repostory (`git clone https://github.com/pingiun/tlask.git`)
2. Get the

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

Tlask code: MIT licence 

See [LICENCE](https://github.com/pingiun/tlask/blob/master/LICENSE.md) for more
information.

## TODO
- Implement routing
- Make nice middelwares
  - User context  