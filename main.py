from asyncio.tasks import shield
from aiohttp.helpers import HeadersMixin
import discord
from datetime import datetime
from discord.ext import commands
from discord.ext.commands.core import check

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

TOKEN = 'ODA3NTI3MDIxMjk4NzEyNTc3.YB5SJQ.PeZM1VOl36gMJT3z_Lzv4fafkfI'
intents = intents = discord.Intents.default()
intents.members = True
intents.reactions = True
client = discord.Client(intents = intents)
bot = commands.Bot(command_prefix='$')

# GLOBAL VARS #
CELLO = None            # The server
ROLES = {}              # Dictionary of server roles
BOTADMIN = None         # Bot Admin pointer
SERVEROWNER = None      # Server Owner pointer
GENERAL = None          # General Chat Channel

# Converts given string by removing unicode and leading/trailing whitespace and making all letters UPPERCASE
# REQUIRES A STRING INPUT
def roleFormat(s):
    s = s.encode("ascii", "ignore").decode()        # Remove unicode from KEY string
    s = s.strip()                                   # Remove leading/trailing whitespace
    return s.upper()                                # Convert KEY to all upper case and return

@client.event
async def on_ready():
    print(str(datetime.now()) + ': Bot restarted.')
    print("[DEBUG] Loading roles...")

    global ROLES
    global CELLO
    global BOTADMIN
    global SERVEROWNER
    global GENERAL

    CELLO = client.get_guild(806658570103816202)
    BOTADMIN = CELLO.get_member(389911131944124418)     # Retrieve Ian's member data for global var
    SERVEROWNER = CELLO.get_member(389911131944124418)  # Retrieve Amelia's member data for global var
    GENERAL = CELLO.get_channel(806658570103816205)     # Retrieve General Chat Channel pointer for global var)



    # Creates dictionary of all server roles
    for role in CELLO.roles:
        ROLES[roleFormat(str(role.name))] = role

    ### Testing for ROLES dictionary
    #print(ROLES)
    #KNIGHT = ROLES.get("KNIGHT")
    #print(str(KNIGHT.name))
    #print(str(KNIGHT.permissions))

    print("[DEBUG] Roles Loaded")




# content MUST be a string!
# response is the emoji reaction object
async def sendRoleMsgs(member, content = None, response = None):    # Take in member and original msg content
    welcome = "Welcome to the **Reddit Cello Meetup Discord Server**! I am going to ask you a few questions so that our other server members can get to know you a bit better. Please only use the emoji I add to each message. If you feel uncomfortable with any questions I ask, feel free to skip the question by selecting this reaction: ⏭️\n\nIf you ever want to reselect your roles at any time just type `$ restart` in this private chat."
    q_pronoun = "What is your prefered pronoun?\n💚 = *He*\n🧡 = *She*\n💙 = *They*"
    q_suzuki = "Are you currently a Suzuki student?"
    q_exp = "What is your experience level?\n🎻 = *Beginner*\n🎓 = *Student*\n💵 = *Professional*"
    q_rules = "Have you read the server rules?"
    q_teach = "Are you a cello teacher?"
    q_thx = "Thank you for taking the time to answer these quesitons and review the server rules. Feel free to reach out on the server if you need anything else. Happy cello-ing!"
    q_error = "I am terribly sorry. Something has gone wrong with my programming. I am letting the server admin know so that they can take care of this issue for you. You should receive a response from them within 48 hours. Otherwise please let someone know on the server."
    a_NOTIFY = "[ERROR] in `async def sendRoleMsgs(member, content)` \nrecieved response = " + str(response) + "\n" + member.name + " is awaiting a response."
    d_skip = "[DEBUG] " + member.name + " chose to skip pronoun question."
    d_noACT = "[DEBUG] ❌ was selected by " + member.name + ". No action taken."

    c = False

    # Thanks!
    # Prefered Pronoun?
    if content == None:
        loading = await member.send("Loading...")
        await loading.delete()
        await clearChatWindow(loading)
        #print("[TEST] content is None")
        await member.send(welcome)
        pronoun = await member.send(q_pronoun)
        await pronoun.add_reaction('💚')    # He
        await pronoun.add_reaction('🧡')    # She
        await pronoun.add_reaction('💙')    # They
        await pronoun.add_reaction('⏭️')    # Skip

    elif q_rules in content:
        #print("[TEST] q_rules in content")
        if response == '✔️':
            #print([TEST] d_noACT)
            await member.send(q_thx)            # send thank you message ONLY when user agrees they read the rules
        elif response == '❌':
            rules = await member.send(q_rules)
            await rules.add_reaction('❌')      # No
            await rules.add_reaction('✔️')      # Yes
        else:
            await member.send(q_error)
            await BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

    # Read the Rules?
    elif q_teach in content:
        #print("[TEST] q_teach in content")
        if response == '✔️':
            await member.add_roles(ROLES.get("TEACHER"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '❌':
            #print([TEST] d_noACT)
            c = True
        elif response == '⏭️':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            rules = await member.send(q_rules)
            await rules.add_reaction('❌')      # No
            await rules.add_reaction('✔️')      # Yes

    # Teacher?
    elif q_exp in content:
        #print("[TEST] q_exp in content")
        if response == '🎻':
            await member.add_roles(ROLES.get("HOBBYIST"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '🎓':
            await member.add_roles(ROLES.get("STUDENT"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '💵':
            await member.add_roles(ROLES.get("PROFESSIONAL"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '⏭️':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            teacher = await member.send(q_teach)
            await teacher.add_reaction('❌')    # No
            await teacher.add_reaction('✔️')    # Yes
            await teacher.add_reaction('⏭️')    # Skip

    # Exp Level?
    elif q_suzuki in content:
        #print("[TEST] q_suzuki in content")
        if response == '✔️':
            await member.add_roles(ROLES.get("SUZUKI"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '❌':
            #print([TEST] d_noACT)
            c = True
        elif response == '⏭️':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            exp = await member.send(q_exp)
            await exp.add_reaction('🎻')    # Hobby
            await exp.add_reaction('🎓')    # Student
            await exp.add_reaction('💵')    # Professional
            await exp.add_reaction('⏭️')    # Skip

    # Suzuki?
    elif q_pronoun in content:
        #print("[TEST] q_pronoun in content")
        if response == '💚':
            await member.add_roles(ROLES.get("HE/HIM"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '🧡':
            await member.add_roles(ROLES.get("SHE/HER"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '💙':
            await member.add_roles(ROLES.get("THEY/THEM"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '⏭️':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm
        
        if c == True:
            suzuki = await member.send(q_suzuki)
            await suzuki.add_reaction('❌')     # No
            await suzuki.add_reaction('✔️')     # Yes
            await suzuki.add_reaction('⏭️')    # Skip

    else:
        #print("[TEST] nothing contains content")
        await member.send(q_error)
        # send error report to Ian via dm
        await BOTADMIN.send(a_NOTIFY)

@client.event
async def on_member_join(member):
# Add condition: As long as joing member is not a bot account
    await sendRoleMsgs(member)

@client.event
async def on_raw_reaction_add(payload):
    if payload.user_id != client.user.id and payload.guild_id != CELLO.id:
        msg_id = payload.message_id
        channel_id = payload.channel_id
        channel = await client.fetch_channel(channel_id)
        msg = await channel.fetch_message(msg_id)               # retrieve msg object
        content = msg.content                                   # save msg content
        print (content)
        await msg.delete()                                      # delete msg in Discord (so user cannot interact further)
        await sendRoleMsgs(CELLO.get_member(payload.user_id), str(content), str(payload.emoji))

# Deletes every message in the bot chat window
async def clearChatWindow(msg):
    channel = client.get_channel(msg.channel.id)
    msg_list = await channel.history(limit = None).flatten()
    print("[DEBUG] Clearing chat window for " + str(msg.author))
    for m in msg_list:
        if m.author.bot == True:
            await m.delete()
    print("[DEBUG] Finished clearing chat window for " + str(msg.author))


@client.event
async def on_message(msg):
    global GENERAL
    member = CELLO.get_member(msg.author.id)
    #print("[TEST] msg recieved")
    _roledialogue = "$ force roledialogue"
    _restart = "$ restart"
    _clear = "$ clear"
    if (msg.author.bot):
        print("[TEST] Bot user sent a message")
        return          # Ignore message from bot.
    elif msg.author.id != client.user.id and msg.channel == GENERAL and msg.author == SERVEROWNER:        # if !bot user and msg is from guild channel
        if msg.content.startswith(_roledialogue):
            await msg.delete()                # delete the command
            await BOTADMIN.send("ATTENTION! The " + _roledialogue + " command was issued by: " + msg.author.name)
            await SERVEROWNER.send("ATTENTION! The " + _roledialogue + " command was issued by: " + msg.author.name)

            for m in CELLO.members:         # get every user
                if m.bot == False:
                    print("[DEBUG] Deleting roles for " + str(m.name))
                    for r in m.roles:
                        if r != None and r.name != "@everyone":
                            await m.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = "[ALL] Role reset command has been issued on " + str(m.name) + " by " + str(msg.author))    # delete specific user's roles
                    print("[TEST: force command] Sending role dialogue to " + str(m.name))
                    await sendRoleMsgs(m)       # send role dialogue
        elif msg.content.startswith(_restart) and msg.channel == GENERAL and msg.author == SERVEROWNER:
            await msg.delete()                # delete the command
            if msg.mentions != None:
                for m in msg.mentions:
                    if m.bot == False:          # if reset called on non-bot user
                        for r in m.roles:
                            if r.name != "@everyone":           # if role is not @everyone (which cannot be removed)
                                await m.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = "[INDIVIDUAL] Role reset command has been issued on " + str(m.name) + " by " + str(msg.author))
                        print("[TEST: restart command] Sending role dialogue to " + str(m.name))
                        await sendRoleMsgs(m)
                    else:
                        await msg.author.send("Your request could not be completed on bot user. Bot users must have their roles manually adjusted by an admin. All other mentions will still be processed.")
            else:       # If an error occurs then let the ServerAdmin and BotAdmin know
                await member.send("Your request was unable to be processed because of a command input error. Please contact the bot admin for assistance.")
                await BOTADMIN.send("ATTENTION! The " + _roledialogue + " command was attempted but failed. Issuer: " + msg.author.name)
                await SERVEROWNER.send("ATTENTION! The " + _roledialogue + " command was attempted but failed. Issuer: " + msg.author.name)
        else:
            return          # ignore general chatter
    elif msg.author.bot == False and msg.guild == None:             # Command issued by user through DM
        print("[TEST] Command recieved")
        if msg.content.startswith(_restart) and member.roles != None:
            for r in member.roles:
                print(r.name)
                if r.name != "@everyone":
                    await member.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = msg.author.name + " requested to reset their roles.")
                await clearChatWindow(msg)
            await sendRoleMsgs(member)
        elif msg.content.startswith(_clear):                # Command to clear user's bot chat window
            await clearChatWindow(msg)
        else:
            await member.send("I apologize but I can only understand specific commands and emoji reactions. If you need assistance please reach out on the server.")
    elif msg.content.startswith('$') and msg.channel == GENERAL:           # supress command attempt and alert admins
        await msg.delete()
        print("[DEBUG] " + str(member.name) + " attempted to issue the following command in the general channel: " + str(msg.content))
        await BOTADMIN.send("ATTENTION! **" + str(member.name) + "** may have attempted to issue a command but failed. Please check the logs. Message content: " + str(msg.content))
        await SERVEROWNER.send("ATTENTION! **" + str(member.name) + "** may have attempted to issue a command but failed. Please check the logs. Message content: " + str(msg.content))
    else:
        return      # ignore general messages from users via dm or server channels

client.run(TOKEN)


##### TODO

# retrieve server owner info automatically instead of via manual id input

# move highly confidential data to seperate secure file that nobody should ever touch to make bad edits very noticable.