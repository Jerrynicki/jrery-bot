import discord
import discord.ext.commands as commands
import random

class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if random.randint(1, 300) == 150:
            trogi_emote = None
            for emote in message.guild.emojis:
                print(emote.name)
                if emote.name == "trogi":
                    trogi_emote = emote

            if trogi_emote == None:
                return

            await message.channel.send("<:" + trogi_emote.name + ":" + str(trogi_emote.id) + ">")
            return
