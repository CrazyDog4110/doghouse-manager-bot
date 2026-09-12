import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

NO_TRAIN_ROLE = os.getenv("NO_TRAIN_ROLE")
NO_SPEEDRUN_ROLE = os.getenv("NO_SPEEDRUN_ROLE")
NO_VC_ROLE = os.getenv("NO_VC_ROLE")
ERROR_LOGGING_CHANNEL = os.getenv("ERROR_LOGGING_CHANNEL")
MOD_LOGGING_CHANNEL = os.getenv("MOD_LOGGING_CHANNEL")

async def blacklist(ctx, role, user, reason):
    role = discord.utils.get(ctx.guild.roles, id=int(role))
    user = await ctx.guild.fetch_member(user)

    try:
        await user.add_roles(role)
    except:
        await ctx.send("Failed to give role to user, prehaps my role isn't high enough in the hierachy.")
        return
    
    # Add user's ID to a file to prevent them from rejoining to remove the role
    with open(str(role.id)+".txt", "a") as f:
        f.write(str(user.id)+"\n")
    
    await ctx.message.delete()

async def unblacklist(ctx, role, user, reason):
    role = discord.utils.get(ctx.guild.roles, id=int(role))
    user = await ctx.guild.fetch_member(user)

    try:
        await user.remove_roles(role)
    except:
        await ctx.send("Failed to remove role to user, prehaps my role isn't high enough in the hierachy.")
        return
    
    # Add user's ID to a file to prevent them from rejoining to remove the role
    with open(str(role.id)+".txt", "r") as f:
                data = f.read()
                data = data.replace(str(user.id), "")
    with open(str(role.id)+".txt", "w") as f:
        f.write(data)
    
    await ctx.message.delete()

class Moderation(commands.Cog):
    # No train command, removes user from the train channel
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def notrains(self, ctx, user: discord.User, *, reason: str=None):
        if reason == None:
            reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # Blacklist user via function
        await blacklist(ctx, int(NO_TRAIN_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " removed " + user.name + "'s access to the train channel. Reason: " + reason)
        # Attempt to DM user
        try:
            await user.send("Your access to the train channel was revoked. Given reason: "+reason)
            await ctx.send(user.name+" was found travelling without a valid ticket and was forced to exit the train at the next station.")
        except:
            await ctx.send(user.name+" was found travelling without a valid ticket and was forced to exit the train at the next station.\n-# User disabled direct messages so I wasn't able to notify them.")

    # Yes train command, does the opposite of above
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def yestrains(self, ctx, user: discord.User, *, reason: str=None):
        if reason == None:
                reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        await unblacklist(ctx, int(NO_TRAIN_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " reinstated " + user.name + "'s access to the train channel. Reason: " + reason)
        try:
            await user.send("Your access to the train channel was reinstated. Given reason: "+reason)
            await ctx.send(user.name+" has paid their fine and is allowed to re-board the train.")
        except:
            await ctx.send(user.name+" has paid their fine and is allowed to re-board the train.\n-# User disabled direct messages so I wasn't able to notify them.")    

    # No speedrun command, removes user from the speedrunning channels
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def nospeedrun(self, ctx, user: discord.User, *, reason: str=None):
        if reason == None:
            reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # Blacklist user via function
        await blacklist(ctx, int(NO_SPEEDRUN_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " removed " + user.name + "'s access to the speedrunning channels. Reason: " + reason)
        # Attempt to DM user
        try:
            await user.send("Your access to the speedrunning channels was revoked. Given reason: "+reason)
            await ctx.send(user.name+" is now stuck in cap.")
        except:
            await ctx.send(user.name+" is now stuck in cap.\n-# User disabled direct messages so I wasn't able to notify them.")

    # Yes train command, does the opposite of above
    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def yesspeedrun(self, ctx, user: discord.User, *, reason: str=None):
        if reason == None:
            reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # Blacklist user via function
        await unblacklist(ctx, int(NO_SPEEDRUN_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " reinstated " + user.name + "'s access to the speedrunning channels. Reason: " + reason)
        # Attempt to DM user
        try:
            await user.send("Your access to the speedrunning channels was reinstated. Given reason: "+reason)
            await ctx.send(user.name+" is now speedy.")
        except:
            await ctx.send(user.name+" is now speedy.\n-# User disabled direct messages so I wasn't able to notify them.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def novc(self, ctx, user: discord.User, *, reason:str=None):
        if reason == None:
            reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # Blacklist user via function
        await blacklist(ctx, int(NO_VC_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " removed " + user.name + "'s access to the voice channels. Reason: " + reason)
        # Attempt to DM user
        try:
            await user.send("Your access to the voice channels was revoked. Given reason: "+reason)
            await ctx.send(user.name+" is now mute.")
        except:
            await ctx.send(user.name+" is now mute.\n-# User disabled direct messages so I wasn't able to notify them.")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def yesvc(self, ctx, user: discord.User, *, reason:str=None):
        if reason == None:
            reason = "No reason provided."
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # Blacklist user via function
        await unblacklist(ctx, int(NO_VC_ROLE), user.id, reason)
        await modlogs.send(ctx.author.name + " reinstated " + user.name + "'s access to the voice channels. Reason: " + reason)
        # Attempt to DM user
        try:
            await user.send("Your access to the voice channels was reinstated. Given reason: "+reason)
            await ctx.send(user.name+" is now audible again.")
        except:
            await ctx.send(user.name+" is now audible again.\n-# User disabled direct messages so I wasn't able to notify them.")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def scamkick(self, ctx, user: discord.User):
        # Get the user to softban's object
        user = await ctx.guild.fetch_member(user.id)
        modlogs = discord.utils.get(ctx.guild.channels, id=int(MOD_LOGGING_CHANNEL))
        # notify the user
        try:
            await user.send("Your account was hacked and sent scams in our server, to prevent this, your account was kicked. Rejoin by using this link: https://discord.gg/MYWbvN2yvc")
        except:
            pass
        # ban and unban the user to remove their previous messages
        try:
            await user.ban(delete_message_seconds=86400, reason="Hacked Account")
            await user.unban(reason="Softban removal")
        except:
            await ctx.send("I don't have permissions to softban this user.")
            return
        # Send success message and log the action
        await ctx.message.delete()
        await ctx.send(user.name+" fell for a free robux scam and got hacked.")
        await modlogs.send(ctx.author.name+" scam kicked "+user.name)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # Obtain user id's in blacklist file
        with open(str(NO_TRAIN_ROLE)+".txt", "r") as f:
            data = f.read().splitlines()
            # If the user who just joined has their ID in the blacklist file, add the role back.
            if str(member.id) in data:
                notrainrole = discord.utils.get(member.guild.roles, id=int(NO_TRAIN_ROLE))
                await member.add_roles(notrainrole)
        # do the same for speedrunning role
        with open(str(NO_SPEEDRUN_ROLE)+".txt", "r") as f:
                data = f.read().splitlines()
                # If the user who just joined has their ID in the blacklist file, add the role back.
                if str(member.id) in data:
                    nospeedrunrole = discord.utils.get(member.guild.roles, id=int(NO_SPEEDRUN_ROLE))
                    await member.add_roles(nospeedrunrole)
        with open(str(NO_VC_ROLE)+".txt", "r") as f:
                    data = f.read().splitlines()
                    # If the user who just joined has their ID in the blacklist file, add the role back.
                    if str(member.id) in data:
                        novcrole = discord.utils.get(member.guild.roles, id=int(NO_VC_ROLE))
                        await member.add_roles(novcrole)
        if member.id == 1228864356305866792:
            bfrawgrole = discord.utils.get(member.guild.roles, id=int(1546083621868150834))
            await member.add_roles(bfrawgrole)

async def setup(bot):
    await bot.add_cog(Moderation(bot))