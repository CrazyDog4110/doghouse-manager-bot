import discord
from discord.ext import commands
import dotenv
import os
from ollama import chat
from ollama import ChatResponse
from ollama import Client
from ollama import generate

dotenv.load_dotenv()

OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")

ollamaclient = Client(
    host='https://ollama.com',
    headers={'Authorization': 'Bearer ' + OLLAMA_API_KEY}
)

conversations = {}
dumbconversations = {}

class Memes(commands.Cog):
    @commands.command(aliases=["AI", "ask", "askgpt"])
    @commands.has_permissions(moderate_members=True)
    async def ai(self, ctx, *, userrequest):
        userrequest = str(userrequest)

        if ctx.author.id not in conversations:
            conversations[ctx.author.id] = [
        {
            "role": "system",
            "content": """
            You are a casual, friendly human-like Discord user.
            Talk naturally and conversationally.
            Keep responses short and to the point.
            Maximum 2 sentences.
            """
        }
        ]

        conversation = conversations[ctx.author.id]

        conversation.append({
            "role": "user",
            "content": userrequest
        })
        APIresponse = ollamaclient.chat(model='gpt-oss:120b', messages=conversation)
        conversation.append({
                    "role": "assistant",
                    "content": APIresponse.message.content
                })
        await ctx.send(APIresponse.message.content)


    @commands.command(aliases=["fillet", "minyan", "chud", "fillet-minyan"])
    async def chudminyan(self, ctx):
        await ctx.send("https://files.catbox.moe/brhxnj.png")
    
    @commands.command()
    async def warm(self, ctx, user: discord.User):
        await ctx.send(user.display_name+" has been warmed. User in now a toasty 75 degrees celcius.")

    @commands.command()
    async def burn(self, ctx, user: discord.User):
        await ctx.send(user.display_name+" has been burned. User in now a crispy 389 degrees celcius.")

    @commands.command()
    async def checkpoint(self, ctx):
        await ctx.send("https://www.twitch.tv/bfrawg6/clip/PuzzledCuriousNarwhalBrainSlug-6ViPGeFh9XNu-OTE <@1228864356305866792> EXPLAIN", allowed_mentions=discord.AllowedMentions.none()) 

    @commands.command(aliases=["67"])
    async def sixseven(self, ctx):
        await ctx.send("Yo mods can we ban this hooligan please?")

    @commands.command()
    async def gillette(self, ctx, money: float):
        amount = money/3.25
        if amount < 1:
            await ctx.send("Wow u so broke can't even afford an 8 pack of Gillette Super Thin Long Handle Disposable Razors")
        else:
            await ctx.send("You can afford "+str(amount)+" 8 pack('s) of Gillette Super Thin Long Handle Disposable Razors")
    
    @commands.command()
    async def stroke(self, ctx):
        await ctx.send("fiowfhfueuf8sduv8uv8auv89ug89waur89uv8uzhvughfoiwanguangiojbioxj b8dhbuxfhbufbhudgjhrjighdfjhvjxdhbhfkjeh iuhfiughaweiughuwagyhudfhabuishughfudhguieht")

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def aibutrude(self, ctx, *, userrequest):
        userrequest = str(userrequest)

        if ctx.author.id not in dumbconversations:
            dumbconversations[ctx.author.id] = [
        {
            "role": "system",
            "content": """
            You are a casual, unfriendly human-like Discord user.
            Talk naturally and conversationally.
            Keep responses short and to the point.
            Maximum 2 sentences.
            You are also really rude, dismissive and just generally a dickhead but don't worry the user knows that this is a joke.
            """
        }
        ]

        conversation = dumbconversations[ctx.author.id]

        conversation.append({
            "role": "user",
            "content": userrequest
        })
        APIresponse = ollamaclient.chat(model='gpt-oss:120b', messages=conversation)
        conversation.append({
                    "role": "assistant",
                    "content": APIresponse.message.content
                })
        await ctx.send(APIresponse.message.content)

    @commands.command()
    @commands.has_permissions(moderate_members=True)
    async def send(self, ctx, *, content):
        await ctx.message.delete()
        await ctx.send(content)

async def setup(bot):
    await bot.add_cog(Memes(bot))