import discord
import discord.ext.commands as commands
from mcstatus import MinecraftServer

class Minecraft(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

    @commands.command(aliases=["mc"])
    async def minecraft(self, ctx, address="mc.leo.immobilien", port=25565):
        try:
            server = MinecraftServer.lookup(address + ":" + str(port))
            status = server.status()
        except Exception as exc:
            await ctx.send("Error! `" + str(exc) + "`")
            return

        embed = discord.Embed(title="Stats for " + address, color=discord.Color.red())
        # embed.set_thumbnail(status.favicon)

        player_count = str(status.players.online) + "/" + str(status.players.max)

        print(status.version.name)
        # Some servers reply with nothing
        if status.version.name is None or status.version.name == "":
            status.version.name = "Unknown"
        if status.description["text"] is None or status.description["text"] == "":
            status.description["text"] = "Unknown"

        if status.players.sample is None: 
            players = "No player list"
        else:
            i = 0
            players = ""
            for player in zip(status.players.sample, range(5)):
                players += player[0].name + "\n"

            if len(status.players.sample) == 5:
                players += status.players.sample[-1].name
            elif len(status.players.sample) > 5:
                players += "+ " + str(status.players.online - 5) + " more players"

        embed.add_field(name="Server version", value=status.version.name, inline=False)
        embed.add_field(name="MOTD", value=status.description["text"], inline=False)
        embed.add_field(name="Online Players: " + player_count, value=players, inline=False)
        embed.add_field(name="Ping", value=str(int(status.latency)) + " ms", inline=False)

        await ctx.send(content="", embed=embed)
