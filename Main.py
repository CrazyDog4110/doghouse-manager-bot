import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
NO_TRAIN_ROLE = os.getenv("NO_TRAIN_ROLE")
MAIN_GUILD = os.getenv("MAIN_GUILD")
DIRECTORY_TO_TRAIN_BLACKLIST_FILE = os.getenv("DIRECTORY_TO_TRAIN_BLACKLIST_FILE")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

# No train command, removes user from the train channel
@bot.command()
@commands.has_permissions(moderate_members=True)
async def notrains(ctx, user: discord.User, reason: str=None):
    if reason == None:
        reason = "No reason provided."
    # Get No Train Role Object
    notrainrole = discord.utils.get(ctx.guild.roles, id=int(NO_TRAIN_ROLE))
    user = await ctx.guild.fetch_member(user.id)
    # Attempt to apply role to user
    try:
        await user.add_roles(notrainrole)
    except:
        await ctx.send("Failed to give role to user, prehaps my role isn't high enough in the hierachy.")

    # Add user's ID to a file to prevent them from rejoining to remove the role
    with open(DIRECTORY_TO_TRAIN_BLACKLIST_FILE, "a") as f:
                f.write(str(user.id)+"\n")

    # Attempt to DM user
    try:
        await user.send("Your access to the train channel was revoked. Given reason: "+reason)
        await ctx.send(user.name+" was found travelling without a valid ticket and was forced to exit the train at the next station.")
    except:
        await ctx.send(user.name+" was found travelling without a valid ticket and was forced to exit the train at the next station.\n-# User disabled direct messages so I wasn't able to notify them.")

# Yes train command, does the opposite of above
@bot.command()
@commands.has_permissions(moderate_members=True)
async def yestrains(ctx, user: discord.User, reason: str=None):
    if reason == None:
            reason = "No reason provided."
    notrainrole = discord.utils.get(ctx.guild.roles, id=int(NO_TRAIN_ROLE))
    user = await ctx.guild.fetch_member(user.id)
    try:
        await user.remove_roles(notrainrole)
    except:
        await ctx.send("Failed to remove role to user, prehaps my role isn't high enough in the hierachy.")

    try:
        await user.send("Your access to the train channel was reinstated. Given reason: "+reason)
        await ctx.send(user.name+" has paid their fine and is allowed to re-board the train.")
    except:
        await ctx.send(user.name+" has paid their fine and is allowed to re-board the train.\n-# User disabled direct messages so I wasn't able to notify them.")    

    with open(DIRECTORY_TO_TRAIN_BLACKLIST_FILE, "r") as f:
                data = f.read()
                data = data.replace(str(user.id), "")
    with open(DIRECTORY_TO_TRAIN_BLACKLIST_FILE, "w") as f:
         f.write(data)

@bot.event
async def on_member_join(member):
    # Obtain user id's in blacklist file
    with open(DIRECTORY_TO_TRAIN_BLACKLIST_FILE, "r") as f:
        data = f.read().splitlines()
        # If the user who just joined has their ID in the blacklist file, add the role back.
        if str(member.id) in data:
            notrainrole = discord.utils.get(member.guild.roles, id=int(NO_TRAIN_ROLE))
            await member.add_roles(notrainrole)
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the required permissions to run this command!", ephemeral= True)
    else:
         await ctx.send("<@902784993301004348> Something broke")

bot.run(TOKEN)