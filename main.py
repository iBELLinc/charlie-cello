from asyncio.tasks import shield
from commands import decipherCommand
from typing import get_type_hints
from aiohttp.helpers import HeadersMixin
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.core import check
from role_dialogue import sendRoleMsgs
from myUtils import UserToMember, roleFormat
#from private import TOKEN, bot_admin, guild_id, bot_channel
import private

############################################################
#              BOT PERMISSIONS
# View Audit Log    -   To write events to server audit log
# Manage Roles      -   To add and remove server members from various roles
# View Channels     -   To identify if a recieved message is from a server channel or dm
# Send Messages     -   So that the bot can send messages to server members
# Manage Messages   -   So bot can modify existing messages (ONLY it's own for now)
# Read Msg Hist     -   So bot can review old messages if needed
# Add reactions     -   So bot can add emoji reactions to messages
#
############################################################

intents = intents = discord.Intents.default()
intents.members = True
intents.reactions = True
private.CLIENT = client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='$')

# ### GLOBAL VARS ###
# global CLIENT           # The Bot
# global GUILD            # The Server
# global BOTADMIN         # The Bot Admin
# global SERVEROWNER      # The Owner of the Server
# global BOT_CHANNEL      # The channel that the bot speaks in
# global ROLES            # All server roles

# CLIENT = client
# GUILD = None
# BOTADMIN = None
# SERVEROWNER = None
# BOT_CHANNEL = None
# ROLES = {}
# ###################

#############################
#
#       BOT RESTART
#
# Pre-condition: Bot crashed, lost internet connectivity, or was closed by admin
# Post-condition: Server roles and owner are refreshed
#
#############################
@client.event
async def on_ready():
    print(str(datetime.now()) + ': Bot restarted.')

    private.GUILD = private.CLIENT.get_guild(private.guild_id)                      # Retrieve Server pointer
    private.BOTADMIN = private.GUILD.get_member(private.bot_admin)          # Retrieve bot admins member data
    private.SERVEROWNER = private.GUILD.owner                               # Retrieve current guild owner pointer
    private.BOT_CHANNEL = private.GUILD.get_channel(private.bot_channel)    # Retrieve Bot Channel pointer

    print("[DEBUG] SERVER INFORMATION\nServer Name: " + private.GUILD.name + "\nServer Owner: " + private.SERVEROWNER.name + "\nBot Admin: " + private.BOTADMIN.name)

    #print("[DEBUG] Loading roles...")
    # Creates dictionary of all server roles
    for role in private.GUILD.roles:
        private.ROLES[roleFormat(str(role.name))] = role

    ### Testing for ROLES dictionary
    #print(ROLES)
    #KNIGHT = ROLES.get("KNIGHT")
    #print(str(KNIGHT.name))
    #print(str(KNIGHT.permissions))

    #print("[DEBUG] Roles Loaded")

#############################
#
#       NEW SERVER MEMBER
#
# Pre-condition: Non-bot member joins the server
# Post-condition: Member is assigned applicable roles if they opt-in
#
#############################
@client.event
async def on_member_join(member):
    if (member.bot == False) :
        await sendRoleMsgs(member, client)

#############################
#
#       NEW REACTION
#
# Pre-condition: Reaction is made by non-bot user on a private dm with Charlie
# Post-condition: If reaction is part of role dialogue then appropriate role will be assigned
#
#############################
@client.event
async def on_raw_reaction_add(payload):
    if (not private.GUILD.get_member(payload.user_id).bot and payload.guild_id == None) :       #str(client.get_channel(payload.channel_id).type) == "private"
        msg_id = payload.message_id
        channel_id = payload.channel_id
        channel = await client.fetch_channel(channel_id)
        msg = await channel.fetch_message(msg_id)               # retrieve msg object
        content = msg.content                                   # save msg content
        #print ("[DEBUG] " + str(content))
        await msg.delete()                                      # delete msg in Discord (so user cannot interact further)
        await sendRoleMsgs(private.GUILD.get_member(payload.user_id), client, str(content), str(payload.emoji))

#############################
#
#       COMMAND INPUT
#
# Pre-condition: Command is entered in in private dm with bot by non-bot member
# Post-condition: Command is executed if member has appropriate permissions
#
#############################
@client.event
async def on_message(msg):
    if (not msg.author.bot and msg.content.startswith('$') and msg.guild == None) :
        await decipherCommand(client, private.GUILD, msg, private.ROLES)

client.run(private.TOKEN)