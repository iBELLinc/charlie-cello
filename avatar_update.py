# Selects which avatar to use for Charlie based on selected holidays and events

import main
from aiohttp.helpers import parse_mimetype
from discord.ext.commands.converter import PartialEmojiConverter

DEFAULT = 'assets/avatar/default.png'
EASTER = 'assets/avatar/easter.png'
PARTY = 'assets/avatar/party.png'
PIRATE = 'assets/avatar/pirate.png'
THANKSGIVING = 'assets/avatar/thanksgiving.png'

async def checkHoliday(date) :
    if (date.month == 4):
        with open(DEFAULT, 'rb') as image:
            await main.client.user.edit(avatar = image.read())

    elif (date.month == 2):
        with open(PARTY, 'rb') as image:
            await main.client.user.edit(avatar = image.read())

    elif (date.month == 9 and date.day == 19):
        with open(PIRATE, 'rb') as image:
            await main.client.user.edit(avatar = image.read())

    elif (date.month == 11):
        with open(THANKSGIVING, 'rb') as image:
            await main.client.user.edit(avatar = image.read())

    else:
        with open(DEFAULT, 'rb') as image:
            await main.client.user.edit(avatar = image.read())