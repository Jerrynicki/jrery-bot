import discord
import discord.ext.commands
import logging
import json
import asyncio
import os

import commands
import events
import timeouts as touts

logging.basicConfig(level=logging.INFO)

config = json.load(open("config.json"))
generic_responses = json.load(open("commands/generic_reponses.json"))

if os.path.isdir("cache"):
    for file in os.listdir("cache"):
        os.unlink("cache/" + file)
else:
    os.mkdir("cache")

if not os.path.isdir("user_data"):
    os.mkdir("user_data")

timeouts = touts.Timeouts()

bot = discord.ext.commands.Bot(
    command_prefix=config["prefix"], description="hello ladies")
bot.owner_id = config["owner_id"]
bot.is_debug = False

bot.add_cog(events.update_uptime.UpdateUptime(bot))
bot.add_cog(events.on_message.OnMessageEvent(bot))
bot.add_cog(events.on_message.OnMessageDeleteEvent(bot))

bot.add_cog(commands.generic.Generic(bot, timeouts, generic_responses))
bot.add_cog(commands.inspirobot.Inspirobot(bot, timeouts, generic_responses))
bot.add_cog(commands.neofetch.Neofetch(bot, timeouts, generic_responses))
bot.add_cog(commands.music.Music(bot, timeouts, generic_responses))
bot.add_cog(commands.reminders.Reminders(bot, timeouts, generic_responses))
bot.add_cog(commands.streets.Streets(bot, timeouts, generic_responses))
bot.add_cog(commands.update.Update(bot, timeouts, generic_responses))
bot.add_cog(commands.ffmpeg.FFmpeg(bot, timeouts, generic_responses))
bot.add_cog(commands.execute.Exec(bot, timeouts, generic_responses))
bot.add_cog(commands.webcam.Webcam(bot, timeouts, generic_responses))
bot.add_cog(commands.screenshot.Screenshot(bot, timeouts, generic_responses))
bot.add_cog(commands.minecraft.Minecraft(bot, timeouts, generic_responses))
bot.add_cog(commands.decide.Decide(bot, timeouts, generic_responses))
bot.add_cog(commands.version.Version(bot, timeouts, generic_responses))
bot.add_cog(commands.capitalism.Capitalism(bot, timeouts, generic_responses))
bot.add_cog(commands.quotes.Quotes(bot, timeouts, generic_responses))

try:
    bot.last_up = int(open("uptime", "r").read())
    bot.loop.create_task(events.update_uptime.SaveUptime(bot).announce_last_uptime(bot.last_up))
except:
    bot.last_up = 0

bot.loop.create_task(events.update_uptime.SaveUptime(bot).save_uptime())

while True:
    print("Starting event loop...")
    asyncio.get_event_loop().run_until_complete(bot.start(config["token"]))
