import discord
import discord.ext.commands as commands
import sys
sys.path.insert(0, "../")
import util
import random

class Quotes(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

        with open("data/quotes.txt", "r") as f:
            self.quotes = f.read().split("\n")

    @commands.command()
    async def jreryai(self, ctx):
        """A random quote from an AI fed with my messages
        from the supermarkt server"""

        quote = random.choice(self.quotes)

        await ctx.send(content="jrery: " + quote)
