import discord
import discord.ext.commands as commands
import random

class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if "<@" + str(self.bot.user.id) + ">" in message.content or "<@!" + str(self.bot.user.id) + ">" in message.content:
                await message.channel.send("was los")

        return
