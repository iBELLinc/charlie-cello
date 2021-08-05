import discord

# Information that should not be publicly acessible


TOKEN = "ODA3NTI3MDIxMjk4NzEyNTc3.YB5SJQ.EbfWCzciQCI1ziBceyU1g_OEru8"
bot_admin = 389911131944124418      # UID
guild_id = 801165638219464704       # The guild ID that the bot is active on
bot_channel = 802663681291976704    # ID of the channel that bot posts updates to

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