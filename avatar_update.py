# Selects which avatar to use for Charlie based on selected holidays and events

import main
from aiohttp.helpers import parse_mimetype
from discord.ext.commands.converter import PartialEmojiConverter

DEFAULT = 'avatar/default.png'
EASTER = 'avatar/easter.png'
PARTY = 'avatar/party.png'
PIRATE = 'avatar/pirate.png'
THANKSGIVING = 'avatar/thanksgiving.png'

async def checkHoliday(date) :
    if (date.month == 4):
        await main.client.user.edit(avatar = EASTER)

    elif (date.month == 2):
        await main.client.user.edit(avatar = PARTY)

    elif (date.month == 9 and date.day == 19):
        await main.client.user.edit(avatar = PIRATE)

    elif (date.month == 11):
        await main.client.user.edit(avatar = THANKSGIVING)

    else:
        await main.client.user.edit(avatar = DEFAULT)