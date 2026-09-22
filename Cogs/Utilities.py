import discord
from discord.ext import commands
import subprocess

class Utilities(commands.Cog):

    @commands.command()
    @commands.is_owner()
    async def pull(self, ctx):
        await ctx.send("Attempting to pull from origin:main")

        try:
            subprocess.run(["git", "pull", "origin", "main", "--squash"])
            await ctx.send("Success! Please restart bot to apply changes.")
        except:
            await ctx.send("Failed :(")

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx):
        await ctx.send("Shutting Down...")
        await ctx.bot.close()
        quit()

    @commands.command(aliases=["sm"])
    @commands.has_permissions(manage_messages=True)
    async def slowmode(self, ctx, duration, *, channel: discord.TextChannel = None):
        if channel == None:
            channel = ctx.channel

        try:
            duration = int(duration)
        except:
            await ctx.send("The slowmade duration has to be a number...")

        await channel.edit(slowmode_delay=duration)
        await ctx.send("Set slowmode in <#"+str(channel.id)+"> to "+str(duration)+" seconds")

async def setup(bot):
    await bot.add_cog(Utilities(bot))