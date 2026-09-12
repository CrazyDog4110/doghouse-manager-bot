import discord
from discord.ext import commands
import dotenv
import os

dotenv.load_dotenv()

TOKEN = os.getenv("TOKEN")
PREFIX = os.getenv("PREFIX")
NO_TRAIN_ROLE = os.getenv("NO_TRAIN_ROLE")
NO_SPEEDRUN_ROLE = os.getenv("NO_SPEEDRUN_ROLE")
NO_VC_ROLE = os.getenv("NO_VC_ROLE")
ERROR_LOGGING_CHANNEL = os.getenv("ERROR_LOGGING_CHANNEL")
MOD_LOGGING_CHANNEL = os.getenv("MOD_LOGGING_CHANNEL")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_ready():
    await bot.load_extension('Cogs.Moderation')
    print(f'We have logged in as {bot.user}')

@bot.command()
@commands.is_owner()
async def stop(ctx):
    if ctx.author.id == bot.owner_id:
        await ctx.send("Shutting Down...")
        await ctx.bot.close()
        quit()
    else:
         ctx.send("No lol")
         return

@bot.command()
async def comeng(ctx):
     await ctx.send("Comeng is a bot for Crazy_Dog's discord server.\nThe source code is available at: https://github.com/CrazyDog4110/doghouse-manager-bot")

@bot.event       
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(f"You do not have the required permissions to run this command!", ephemeral= True)
    elif isinstance(error, commands.MissingRequiredArgument):
         await ctx.send(f"You are missing a required argument. Did you specify the user you wanted to run the action on?", ephemeral= True)
    elif isinstance(error, commands.CommandNotFound):
             pass
    else:
         logchannel = discord.utils.get(ctx.guild.channels, id=int(ERROR_LOGGING_CHANNEL))
         await ctx.send(str(error))
         await logchannel.send("An exception occoured: "+ str(error))
         print(str(error))

bot.run(TOKEN)