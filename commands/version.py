import discord
import discord.ext.commands as commands
import subprocess
import os
import time
import sys
sys.path.insert(0, "../")
import util

class Version(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def version(self, ctx):
        embed = discord.Embed(title="Version info", color=discord.Color(0xffff00))

        git_status = subprocess.run(["git", "status"], capture_output=True)
        git_status = b"\n".join(git_status.stdout.split(b"\n")[0:2])
        git_status = git_status.decode("utf8")
        embed.add_field(name="Branch info", value=git_status)

        head_mtime = int(os.stat(".git/FETCH_HEAD").st_mtime)
        embed.add_field(name="Last git pull", value=util.time_calc.time_period_human_readable(time.time() - head_mtime) + " ago")

        git_show = subprocess.run(["git", "show"], capture_output=True)
        git_show = git_show.stdout.split(b"\n")[0]
        git_show = git_show.decode("utf8")
        embed.add_field(name="Current commit", value=git_show)

        await ctx.send(content="", embed=embed)
