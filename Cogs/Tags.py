import discord
from discord.ext import commands
import json

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("tags.txt", "r") as f:
            self.tags = json.load(f)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def addtag(self, ctx, tagname: str, *, tagcontent: str):
        self.tags[tagname.lower()] = tagcontent
        with open("tags.txt", "w") as f:
            f.write(json.dumps(self.tags))
        await ctx.send("Tag "+tagname+" has been added successfully")

    @commands.command()
    async def tag (self, ctx, tagname: str):
        if self.tags.get(tagname.lower()) == None:
            await ctx.send("The tag "+tagname+" does not exist.")
            return
        await ctx.send(self.tags.get(tagname.lower()))

    @commands.command(aliases=["deletetag", "deltag"])
    @commands.has_permissions(manage_messages=True)
    async def removetag(self, ctx, tagname: str):
        self.tags.pop(tagname.lower())
        with open("tags.txt", "w") as f:
            f.write(json.dumps(self.tags))
        await ctx.send("Tag "+tagname+" has been removed successfully")
        
async def setup(bot):
    await bot.add_cog(Tags(bot))