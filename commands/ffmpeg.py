import discord
import discord.ext.commands as commands
import subprocess
import os
import requests


class FFmpeg(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def ffmpeg(self, ctx, *command):
        """Execute an FFmpeg command and send the resulting file
        Special syntax: instead of giving the filename as the last argument, you should give just the file extension; instead of giving a -i argument, you should give a link to a file as the first argument"""

        if self.timeouts.is_timeout(ctx.message.channel.id, "ffmpeg"):
            await ctx.send(self.generic_responses["timeout"])
            return

        self.timeouts.add_timeout(ctx.message.channel.id, "ffmpeg", 15)

        if "-i" in command:
            await ctx.send("Sorry, but the -i option is disabled for security reasons.")
            return

        response = requests.get(command[0], stream=True)

        filename1 = "cache/" + str(ctx.message.channel.id) + "_ffmpeg_raw"
        filename2 = "cache/" + \
            str(ctx.message.channel.id) + "_ffmpeg." + command[-1]

        with open(filename1, "wb") as file:
            for buffer in response.iter_content(chunk_size=2048):
                file.write(buffer)

        proc_command = ["ffmpeg"]
        proc_command.extend(["-i", filename1])
        proc_command.extend(command[1:-1])
        proc_command.append(filename2)
        proc = subprocess.Popen(
            proc_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            proc.communicate(timeout=20)
        except:
            await ctx.send("FFmpeg command timed out")
            return

        await ctx.send(content="", file=discord.File(filename2))

        os.unlink(filename1)
