import discord
import discord.ext.commands as commands

import random

class Decide(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def decide(self, ctx, *choices):
        choices = " ".join(choices)
        choices = choices.split("|")

        if len(choices) == 1:
            await ctx.send("brudi du musst die optionen mit | trennen\nalso so jer!decide flexis|janos")

        choice = random.choice(choices)
        await ctx.send("jrery bot sagt **" + choice.replace("**", "\\*\\*") + "**")

