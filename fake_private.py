import discord

# Information that should not be publicly acessible

TOKEN = "<placeholder>"             # You will need to add your own token for testing
bot_admin = #<int placeholder>      # UID of bot admin
guild_id = #<int placeholder>       # The guild ID that the bot is active on
bot_channel = #<int placeholder>    # ID of the channel that bot posts updates to

global CLIENT           # The Bot
global GUILD            # The Server
global BOTADMIN         # The Bot Admin
global SERVEROWNER      # The Owner of the Server
global BOT_CHANNEL      # The channel that the bot speaks in
global ROLES            # All server roles

CLIENT = None
GUILD = None
BOTADMIN = None
SEVREROWNER = None
BOT_CHANNEL = None
ROLES = {}