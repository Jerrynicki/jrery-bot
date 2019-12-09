import discord
import discord.ext.commands as commands
import os
import subprocess
import time

class Update(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def update(self, ctx):
        if ctx.message.author.id != self.bot.owner_id:
            await ctx.send("This command can only be executed by the bot owner!")
            return
        
        await ctx.send("Running `git pull --force`")
        git_proc = subprocess.Popen(["git", "pull", "--force"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            output = git_proc.communicate(timeout=30)
        except TimeoutError:
            await ctx.send("Timeout")
            return

        output = "stdout:\n" + output[0].decode("utf8") + "\nstderr:\n" + output[1].decode("utf8")

        await ctx.send("Finished. Output: ```" + output + "```")
        await ctx.send("Closing connection and restarting.")
        await self.bot.close()

        os._exit(0)
