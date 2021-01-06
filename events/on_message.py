import discord
import discord.ext.commands as commands
import datetime

class OnMessageEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id != self.bot.user.id:
            if "<@" + str(self.bot.user.id) + ">" in message.content or "<@!" + str(self.bot.user.id) + ">" in message.content:
                await message.channel.send("was los")

        return

class OnMessageDeleteEvent(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if len(message.attachments) >= 1 and message.attachments[0].filename == "kommusnism.gif":
            delta = datetime.datetime.now().timestamp() - message.created_at.timestamp()
            await message.channel.send("kommusnism.gif speedrun time (message creation timestamp->message deleted): **" + str(round(delta, 3)) + "** seconds\n(keep in mind that the run still needs to be recorded and that this time is not exactly the same as the actual time)")
