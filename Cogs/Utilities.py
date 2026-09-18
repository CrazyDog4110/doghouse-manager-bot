import discord
from discord.ext import commands
import subprocess

class Utilities(commands.Cog):

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        ctx.send("Attempting to pull from origin:main")

        try:
            subprocess.run(["git", "pull", "origin", "main"])
            ctx.send("Success! Please restart bot to apply changes.")
        except:
            ctx.send("Failed :(")

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send("Shutting Down...")
        await ctx.bot.close()
        quit()

async def setup(bot):
    await bot.add_cog(Utilities(bot))