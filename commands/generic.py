import discord
import discord.ext.commands as commands
import time

import sys

sys.path.insert(0, "../")
import util

class Generic(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(str(int(self.bot.latency * 1000)) + " ms")

    @commands.command()
    async def uptime(self, ctx):
        tm = time.time() - self.bot.uptime
        tm_human_readable = util.time_calc.time_period_human_readable(tm)

        await ctx.send("Uptime: " + tm_human_readable)
