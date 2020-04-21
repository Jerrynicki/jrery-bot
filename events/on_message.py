import discord
import discord.ext.commands as commands

class OnMessageEvent(commands.Cog):
    def __init__(self, bot, kommusnism):
        self.bot = bot
        self.kommusnism = kommusnism

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if "<@" + str(self.bot.user.id) + ">" in message.content or "<@!" + str(self.bot.user.id) + ">" in message.content:
                await message.channel.send("was los")

            if len(message.attachments) >= 1 and message.attachments[0].filename == "kommusnism.gif":
                self.kommusnism.time_start(message.channel.id)
                await message.channel.send("kommusnism.gif speedrun timer started!")

        return

class OnMessageDeleteEvent(commands.Cog):
    def __init__(self, bot, kommusnism):
        self.bot = bot
        self.kommusnism = kommusnism

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if len(message.attachments) >= 1 and message.attachments[0].filename == "kommusnism.gif" and message.channel.id in self.kommusnism.kommusnism_times:
            time = self.kommusnism.time_stop(message.channel.id)
            await message.channel.send("kommusnism.gif speedrun time (message received->message deleted): **" + str(time) + "** seconds\n(keep in mind that the run still needs to be recorded and that this time is not exactly the same as the actual time)")
