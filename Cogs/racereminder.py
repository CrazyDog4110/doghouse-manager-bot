import discord
from discord.ext import commands, tasks
import dotenv
import os
import datetime

dotenv.load_dotenv()

RACE_CHANNEL = os.getenv("RACE_CHANNEL")

class racereminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_sent = None
        self.reminder.start()

    @tasks.loop(seconds=15)
    async def reminder(self):
        timezone = datetime.timezone(datetime.timedelta(hours=11))
        now = datetime.datetime.now(tz=timezone)
        if now.weekday() == 0 and now.hour == 9 and now.minute == 20:
            if self.last_sent == now.date():
                return
            channel = self.bot.get_channel(int(RACE_CHANNEL))
            await channel.send("Hiya @everyone\nI have a race against 4lettaz in about 10 minutes over at https://twitch.tv/smo_community\nIf you're interested please go take a look to support me :)\n-# Future pings will have a ping role instead of an everyone ping I just haven't set it up yet.")
            self.last_sent = now.date()

    @reminder.before_loop
    async def before_reminder(self):
        await self.bot.wait_until_ready()



async def setup(bot):
    await bot.add_cog(racereminder(bot))
