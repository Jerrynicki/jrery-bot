import discord
import discord.ext.commands as commands

class Exec(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def ihwell(self, ctx, *stuff):
        if ctx.message.author.id != self.bot.owner_id:
            await ctx.send("lol no")
            return

        stuff = " ".join(stuff)

        exec(stuff)
