import discord
import discord.ext.commands as commands

import time

class UpdateUptime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.uptime = 0

    @commands.Cog.listener()
    async def on_ready(self, *args):
        self.bot.uptime = time.time()