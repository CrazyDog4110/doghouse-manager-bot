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
        


async def setup(bot):
    await bot.add_cog(Memes(bot))