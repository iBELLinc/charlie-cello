from myUtils import clearChatWindow
import private

# content MUST be a string!
# response is the emoji reaction object
async def sendRoleMsgs(member, client, content = None, response = None):    # Take in member and original msg content
    welcome = "Welcome to the **Reddit Cello Meetup Discord Server**! I am going to ask you a few questions so that our other server members can get to know you a bit better. Please only use the emoji I add to each message. If you feel uncomfortable with any questions I ask, feel free to skip the question by selecting this reaction: โญ๏ธ\n\nIf you ever want to reselect your roles at any time just type `$restart` in this private chat."
    q_pronoun = "What is your prefered pronoun?\n๐ = *He*\n๐งก = *She*\n๐ = *They*"
    q_suzuki = "Have you used/do you use the Suzuki method?"
    q_exp = "What is your experience level?\n๐ = *Student*\n๐ป = *Amateur*\n๐ต = *Professional*"
    q_skill = "What is your skill level?\n๐ฅ = *Beginner*\n๐ฅ = *Intermediate*\n๐ฅ = *Advanced*"
    q_rules = "Have you read the server rules?"
    q_teach = "Are you a cello teacher?"
    q_location = "What part of the world do you live in?\n๐ = *Europe/Africa*\n๐ = *Asia/Australia*\n๐ = *North/South America*"
    q_thx = "Thank you for taking the time to answer these quesitons and review the server rules. Feel free to reach out on the server if you need anything else. Happy cello-ing!"
    q_error = "I am terribly sorry. Something has gone wrong with my programming. I am letting the server admin know so that they can take care of this issue for you. You should receive a response from them within 48 hours. Otherwise please let someone know on the server."
    a_NOTIFY = "[ERROR] in `async def sendRoleMsgs(member, content)` \nrecieved response = " + str(response) + "\n" + member.name + " is awaiting a response."
    d_skip = "[DEBUG] " + member.name + " chose to skip pronoun question."
    d_noACT = "[DEBUG] โ was selected by " + member.name + ". No action taken."

    c = False

    # Thanks!
    # Prefered Pronoun?
    if content == None:
        loading = await member.send("Loading...")
        #await loading.delete()
        await clearChatWindow(client, loading)
        #print("[TEST] content is None")
        await member.send(welcome)
        pronoun = await member.send(q_pronoun)
        await pronoun.add_reaction('๐')    # He
        await pronoun.add_reaction('๐งก')    # She
        await pronoun.add_reaction('๐')    # They
        await pronoun.add_reaction('โญ๏ธ')    # Skip

    elif q_rules in content:
        #print("[TEST] q_rules in content")
        if response == 'โ๏ธ':
            #print([TEST] d_noACT)
            await member.send(q_thx)            # send thank you message ONLY when user agrees they read the rules
        elif response == 'โ':
            rules = await member.send(q_rules)
            await rules.add_reaction('โ')      # No
            await rules.add_reaction('โ๏ธ')      # Yes
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

    # Read the Rules?
    elif q_teach in content:
        #print("[TEST] q_teach in content")
        if response == 'โ๏ธ':
            await member.add_roles(private.ROLES.get("TEACHER"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โ':
            #print([TEST] d_noACT)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            rules = await member.send(q_rules)
            await rules.add_reaction('โ')      # No
            await rules.add_reaction('โ๏ธ')      # Yes

    # Teacher?
    elif q_skill in content:
        if response == '๐ฅ':
            await member.add_roles(private.ROLES.get("BEGINNER"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐ฅ':
            await member.add_roles(private.ROLES.get("INTERMEDIATE"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐ฅ':
            await member.add_roles(private.ROLES.get("ADVANCED"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True

        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            teacher = await member.send(q_teach)
            await teacher.add_reaction('โ')    # No
            await teacher.add_reaction('โ๏ธ')    # Yes
            await teacher.add_reaction('โญ๏ธ')    # Skip

    # Skill Level?
    elif q_exp in content:
        #print("[TEST] q_exp in content")
        if response == '๐':
            await member.add_roles(private.ROLES.get("STUDENT"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐ป':
            await member.add_roles(private.ROLES.get("AMATEUR MUSICIAN"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐ต':
            await member.add_roles(private.ROLES.get("PROFESSIONAL MUSICIAN"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            skill = await member.send(q_skill)
            await skill.add_reaction('๐ฅ')    # Beginner
            await skill.add_reaction('๐ฅ')    # Intermediate
            await skill.add_reaction('๐ฅ')    # Advanced
            await skill.add_reaction('โญ๏ธ')    # Skip

    # Experience Level?
    elif q_location in content:
        #print("[TEST] q_location in content")
        if response == '๐':
            await member.add_roles(private.ROLES.get("EUROPE-AFRICA"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐':
            await member.add_roles(private.ROLES.get("ASIA-AUSTRALIA"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐':
            await member.add_roles(private.ROLES.get("AMERICAS"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            exp = await member.send(q_exp)
            await exp.add_reaction('๐')    # Student
            await exp.add_reaction('๐ป')    # Amateur
            await exp.add_reaction('๐ต')    # Professional
            await exp.add_reaction('โญ๏ธ')    # Skip

        # Location?
    elif q_suzuki in content:
        #print("[TEST] q_suzuki in content")
        if response == 'โ๏ธ':
            await member.add_roles(private.ROLES.get("SUZUKI"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โ':
            #print([TEST] d_noACT)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm

        if c == True:
            exp = await member.send(q_location)
            await exp.add_reaction('๐')    # Europe/Africa
            await exp.add_reaction('๐')    # Asia/Australia
            await exp.add_reaction('๐')    # Americas
            await exp.add_reaction('โญ๏ธ')    # Skip

    # Suzuki?
    elif q_pronoun in content:
        #print("[TEST] q_pronoun in content")
        if response == '๐':
            await member.add_roles(private.ROLES.get("HE/HIM/HIS"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐งก':
            await member.add_roles(private.ROLES.get("SHE/HER/HERS"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == '๐':
            await member.add_roles(private.ROLES.get("THEY/THEM/THEIR"), reason = member.name + " opt in to role.", atomic = True)
            c = True
        elif response == 'โญ๏ธ':
            #print([TEST] d_skip)
            c = True
        else:
            await member.send(q_error)
            await private.BOTADMIN.send(a_NOTIFY)       # send error report to Ian via dm
        
        if c == True:
            suzuki = await member.send(q_suzuki)
            await suzuki.add_reaction('โ')     # No
            await suzuki.add_reaction('โ๏ธ')     # Yes
            await suzuki.add_reaction('โญ๏ธ')    # Skip

    else:
        print("[TEST] nothing contains content")
        await member.send(q_error)
        # send error report to bot admin via dm
        await private.BOTADMIN.send(a_NOTIFY)