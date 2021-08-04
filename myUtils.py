import private
# Extra functions which are used in more than one section of Charlie Cello

# Converts given string by removing unicode and leading/trailing whitespace and making all letters UPPERCASE
# REQUIRES A STRING INPUT
def roleFormat(s):
    s = s.encode("ascii", "ignore").decode()        # Remove unicode from KEY string
    s = s.strip()                                   # Remove leading/trailing whitespace
    return s.upper()                                # Convert KEY to all upper case and return

# Deletes every bot message in specified chat window
async def clearChatWindow(client, msg):
    channel = client.get_channel(msg.channel.id)
    msg_list = await channel.history(limit = None).flatten()
    #print("[DEBUG] Clearing chat window for " + str(msg.author))
    for m in msg_list:
        if m.author.bot == True:
            await m.delete()
    #print("[DEBUG] Finished clearing chat window for " + str(msg.author))

# Precondition: requires a user object as input
# Postcondition: returns a member object from guild server
async def UserToMember(guild, id):
    return guild.get_member(id)

async def clearMemberRoles(client, member, reason) :
    # for r in member.roles:
    #     print("[DEBUG] Current role for " + member.name + " is: " + r.name)
    #     if (r.name != "admin" and r.name != "@everyone" and not member.bot):
    #         print("[DEBUG] Removing " + r.name)
    #         await member.remove_roles(r, reason)
    if (member.top_role.name == "admin" and member.bot == False):
        #print("[DEBUG] Resetting roles for a server admin")
        for r in member.roles:
            #print("[DEBUG] Current role for " + member.name + " is: " + r.name)
            if (r.name != "admin" and r.name != "@everyone"):
                #print("[DEBUG] Removing " + r.name)
                try:
                    await member.remove_roles(r, reason, atomic = True)
                except:
                    continue
    else:
        #print("[DEBUG] Resetting roles for a non-admin user")
        await member.edit(roles=[])
    