import discord
import discord.ext.commands as commands
import util

import time
import asyncio

class UpdateUptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.uptime = 0

    @commands.Cog.listener()
    async def on_ready(self, *args):
        self.bot.uptime = time.time()

class SaveUptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def announce_last_uptime(self, tm):
        await self.bot.wait_until_ready()
        await self.bot.get_channel(652606510257537035).send("hello ladies i am back\nwas down for: " + util.time_calc.time_period_human_readable(time.time() - tm))

    async def save_uptime(self):
        await self.bot.wait_until_ready()
        await asyncio.sleep(15)
        while True:
            await asyncio.sleep(1.5)
            file = open("uptime", "w")
            file.write(str(int(time.time())))
            file.close()
