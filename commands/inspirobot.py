import discord
import discord.ext.commands as commands
import requests
import os

class Inspirobot(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def inspirobot(self, ctx):
        """Generate a random quote using the Inspirobot API"""
        if self.timeouts.is_timeout(ctx.message.channel.id, "inspirobot"):
            await ctx.send(content=self.generic_responses["timeout"])
        else:
            self.timeouts.add_timeout(ctx.message.channel.id, "inspirobot", 15)

            response = requests.get("https://inspirobot.me/api", params={"generate": "true"})
            image_stream = requests.get(response.text, stream=True)

            filename = "cache/" + str(ctx.message.channel.id) + "_inspirobot.png"

            with open(filename , "wb") as file:
                for buffer in image_stream.iter_content(chunk_size=2048):
                    file.write(buffer)

            await ctx.send(content="", file=discord.File(filename))

            os.unlink(filename)