import discord
import discord.ext.commands as commands
import sys
sys.path.insert(0, "../")
import util
import random
import datetime

class Quotes(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

        with open("data/quotes.txt", "r") as f:
            self.quotes = f.read().split("\n")

    @commands.command(aliases=["ai"])
    async def jreryai(self, ctx, *lines: int):
        """A random quote from an AI fed with my messages
        from the supermarkt server"""

        if len(lines) == 0 or len(lines) > 7:
            lines = [1]

        lines = lines[0]

        if lines > 0:
            quote = ""
            starting_point = random.randint(0, len(self.quotes))
            for x in range(lines):
                quote += self.quotes[starting_point + x] + "\n"

            await ctx.send(content=quote)
        else:
            await ctx.send(content="???")
