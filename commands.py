from myUtils import clearChatWindow
from myUtils import UserToMember
from myUtils import clearMemberRoles
from role_dialogue import sendRoleMsgs
import private
from datetime import datetime

# Global Command Vars
RESTART = "$restart"
CLEAR = "$clear"
FORCE_DIALOGUE = "$forcedialogue "
FORCE_DIALOGUE_ALL = "$forcedialogue -a"
POST = "$post "

global rolesList
rolesList = {}

# COMMAND HANDLER: CLEAR
# Clears bot messages from issuers chat window
async def clear(client, msg) :
    await clearChatWindow(client, msg)

# COMMAND HANDLER: RESTART
# Precondition: requires a member object - NOT USER
async def restart(client, member, reason = "This user issued the reset command to reselect their roles.") :
    for m in client.get_all_members():
        if (str(m) == str(member)):
            #print("[DEBUG] Found User " + m.name)
            await clearMemberRoles(client, m, reason)
            await sendRoleMsgs(m, client)
            return

# COMMAND HANDLER: FORCE DIALOGUE ALL
# Admin command to restart dialogue on ALL users on the server
async def forceDialogueAll(client, msg) :
    reason = "The forcedialogueall command was issued by " + str(msg.author.name)
    mlist = list(dict.fromkeys(client.get_all_members()))       # create list of members and remove duplicates
    for m in mlist:
        print("[DEBUG] Running $reset command on user " + m.name + " ~command issued by " + msg.author.name + "~")
##        await restart(client, m, reason)

# COMMAND HANDLER: FORCE DIALOGUE
# Pre-Condition: Admin sends $forcedialogue command with a username including discord id
# Post-Condition: Restarts the role dialogue with specified user
async def forceDialogue(client, msg) :
    reason = str(msg.author.name) + " issued forcedialogue command on this user."
    try:
        username = msg.content.replace(FORCE_DIALOGUE, '')
        #print("[DEBUG] Got Username from message: " + username)
        member_list = client.get_all_members()
        #print("[DEBUG] Looking for username in list...")
        for m in member_list:
            #print(m)
            if (str(m) == username) :
                #print("[DEBUG] Found Username in member_list!")
                await clearMemberRoles(client, m, reason)
                await restart(client, m, reason)
                break
    except:
        await msg.author.send("[ERROR] Command was invalid. Please enter with correct syntax!\n`$forcedialogue UserName#0000`")

# COMMAND HANDLER: POST
# Admin command to post update on role channel
async def post(msg) :
    # Remove command prefix and send message on public bot channel
    await private.BOT_CHANNEL.send(msg.content.replace(POST, ''))
    await msg.author.send("Update has been posted to " + private.BOT_CHANNEL.name + " 😁")

# Pre-Condition: Command was verified to be incorrect or cast by non-admin user
# Post-Condition: Sends a silent warning to the bot admin containing the command that was issued illegally by non-admin user
async def illegalCommandUsage(msg) :
    print("[WARNING] Admin command issued by non-admin user " + str(msg.author.name) + " silent warning sent to BOT ADMIN")
    await private.BOTADMIN.send("[WARNING] " + str(datetime.now()) + " " + str(msg.author.name) + " attempted to issue command \n#####\n" + str(msg.content) + "\n#####")

# Pre-Condition: Takes a membertype to verify if they have admin priviledges on the server
# Post-Condition: Returns true if user is admin or false if user is not admin
async def isAdmin(member):
    for r in member.roles:
        if (r.name == "admin"): return True
    return False


#############################
#
#       Check If Command Valid
#
# Pre-condition: Reaction is made by non-bot user on a private dm with Charlie
# Post-condition: If reaction is part of role dialogue then appropriate role will be assigned
#
#############################
async def decipherCommand(client, guild, msg, roles) :

    global rolesList
    rolesList = roles
    issuer = await UserToMember(guild, msg.author.id)
    command_string = str(msg.content)

    # Figure out which command was issued
    if (RESTART in command_string) :
        await restart(client, issuer)   # untested

    elif (CLEAR in command_string) :
        await clear(client, msg)

    elif (FORCE_DIALOGUE_ALL in command_string):
        if (await isAdmin(issuer) or issuer == private.GUILD.owner) :    # Is user admin role
            await forceDialogueAll(client, msg)
        else:
            illegalCommandUsage(msg)

    elif (FORCE_DIALOGUE in command_string) :
        if (await isAdmin(issuer) or issuer == private.GUILD.owner) :    # Is user admin role
            await forceDialogue(client, msg)
        else:
            illegalCommandUsage(msg)

    elif (POST in command_string) :
        if (await isAdmin(issuer) or issuer == private.GUILD.owner) :    # Is user admin role
            await post(msg)
        else:
            illegalCommandUsage(msg)

    else:
        await issuer.send("Command Invalid. Please try again.")
        print("[WARNING] " + str(datetime.now()) + issuer + " attempted to issue invalid command\n#####\n" + str(msg.content) + "\n#####")














# global GENERAL
# member = CELLO.get_member(msg.author.id)
# #print("[TEST] msg recieved")
# _roledialogue = "$force roledialogue"
# _restart = "$restart"
# _clear = "$clear"
# if (msg.author.bot):
#     print("[TEST] Bot user sent a message")
#     return          # Ignore message from bot.
# elif msg.author.id != client.user.id and msg.channel == GENERAL and msg.author == SERVEROWNER:        # if !bot user and msg is from guild channel
#     if msg.content.startswith(_roledialogue):
#         await msg.delete()                # delete the command
#         await BOTADMIN.send("ATTENTION! The " + _roledialogue + " command was issued by: " + msg.author.name)
#         await SERVEROWNER.send("ATTENTION! The " + _roledialogue + " command was issued by: " + msg.author.name)

#         for m in CELLO.members:         # get every user
#             if m.bot == False:
#                 print("[DEBUG] Deleting roles for " + str(m.name))
#                 for r in m.roles:
#                     if r != None and r.name != "@everyone":
#                         await m.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = "[ALL] Role reset command has been issued on " + str(m.name) + " by " + str(msg.author))    # delete specific user's roles
#                 print("[TEST: force command] Sending role dialogue to " + str(m.name))
#                 await sendRoleMsgs(m)       # send role dialogue
#     elif msg.content.startswith(_restart) and msg.channel == GENERAL and msg.author == SERVEROWNER:
#         await msg.delete()                # delete the command
#         if msg.mentions != None:
#             for m in msg.mentions:
#                 if m.bot == False:          # if reset called on non-bot user
#                     for r in m.roles:
#                         if r.name != "@everyone":           # if role is not @everyone (which cannot be removed)
#                             await m.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = "[INDIVIDUAL] Role reset command has been issued on " + str(m.name) + " by " + str(msg.author))
#                     print("[TEST: restart command] Sending role dialogue to " + str(m.name))
#                     await sendRoleMsgs(m)
#                 else:
#                     await msg.author.send("Your request could not be completed on bot user. Bot users must have their roles manually adjusted by an admin. All other mentions will still be processed.")
#         else:       # If an error occurs then let the ServerAdmin and BotAdmin know
#             await member.send("Your request was unable to be processed because of a command input error. Please contact the bot admin for assistance.")
#             await BOTADMIN.send("ATTENTION! The " + _roledialogue + " command was attempted but failed. Issuer: " + msg.author.name)
#             await SERVEROWNER.send("ATTENTION! The " + _roledialogue + " command was attempted but failed. Issuer: " + msg.author.name)
#     else:
#         return          # ignore general chatter
# elif msg.author.bot == False and msg.guild == None:             # Command issued by user through DM
#     print("[TEST] Command recieved")
#     if msg.content.startswith(_restart) and member.roles != None:
#         for r in member.roles:
#             print(r.name)
#             if r.name != "@everyone":
#                 await member.remove_roles(ROLES.get(roleFormat(str(r.name))), reason = msg.author.name + " requested to reset their roles.")
#             await clearChatWindow(msg)
#         await sendRoleMsgs(member)
#     elif msg.content.startswith(_clear):                # Command to clear user's bot chat window
#         await clearChatWindow(msg)
#     else:
#         await member.send("I apologize but I can only understand specific commands and emoji reactions. If you need assistance please reach out on the server.")
# elif msg.content.startswith('$') and msg.channel == GENERAL:           # supress command attempt and alert admins
#     await msg.delete()
#     print("[DEBUG] " + str(member.name) + " attempted to issue the following command in the general channel: " + str(msg.content))
#     await BOTADMIN.send("ATTENTION! **" + str(member.name) + "** may have attempted to issue a command but failed. Please check the logs. Message content: " + str(msg.content))
#     await SERVEROWNER.send("ATTENTION! **" + str(member.name) + "** may have attempted to issue a command but failed. Please check the logs. Message content: " + str(msg.content))
# else:
#     return      # ignore general messages from users via dm or server channels
