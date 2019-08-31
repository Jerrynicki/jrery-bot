import discord
import discord.ext.commands as commands

class Webcam(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command(aliases=["wc"])
    async def webcam(self, ctx):
        await ctx.message.channel.send("", file=discord.File("data/selfie.jpg"))
