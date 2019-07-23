import discord
import discord.ext.commands as commands
import subprocess

class Neofetch(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command()
    async def neofetch(self, ctx):
        """Post output of neofetch to the channel"""
        if self.timeouts.is_timeout(ctx.message.channel.id, "neofetch"):
            await ctx.send(content=self.generic_responses["timeout"])
        else:
            self.timeouts.add_timeout(ctx.message.channel.id, "neofetch", 5)

            full_output = ""
            # sed removes all ANSI codes from output
            with subprocess.Popen("neofetch | sed -r \"s/\\x1b\\[[0-9;]*[a-zA-Z]//g\"", stdout=subprocess.PIPE, shell=True) as neofetch_proc:
                full_output += neofetch_proc.stdout.read().decode("ascii")

            # get rid of wHaCkY characters
            full_output = full_output.replace("\x1b[?25l\x1b[?7l", "")
            full_output = full_output.replace("\x1b[?25h\x1b[?7h", "")

            await ctx.send("```\n" + full_output + "```")

