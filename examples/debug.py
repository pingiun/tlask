# This program will continuously get updates and print the json to the console

import asyncio

import sys
sys.path.append('..')

from tlask.api import Api

TOKEN = '260374523:AAG4GhPUVaz6GqJ3j0nMRFEoFP1myB-oGVo'

async def getupdates():
    api = Api(TOKEN)
    me = await api.getMe()
    print(me)
    while True:
        updates = await api.getUpdates()
        print(updates)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(getupdates())
    loop.run_forever()