import discord
import discord.ext.commands
import logging
import json
import asyncio
import os

logging.basicConfig(level=logging.INFO)

config = json.load(open("config.json"))

bot = discord.ext.commands.Bot(command_prefix="jer!", description="hello ladies")
bot.owner_id = int(config["owner_id"])
bot.is_debug = False

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith("jer!"):
        await message.channel.send("jrery bot is currently down for maintenance!")

while True:
    print("Starting event loop...")
    asyncio.get_event_loop().run_until_complete(bot.start(config["token"]))
