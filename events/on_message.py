import discord
import discord.ext.commands as commands
import random

class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.randint(1, 300) == 150:
            await message.channel.send("<:trogi:615175220256309261>")
            return
