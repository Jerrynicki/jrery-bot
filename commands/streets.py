import discord
import discord.ext.commands as commands

import random
import sys
import os
import requests
import asyncio
import logging
import threading

sys.path.insert(0, "../")
import util

class Streets(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.logger = logging.getLogger(__name__)

        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses
        self.strassen_osm_txt = open("strassen_osm.txt", "r").readlines()
        self.staedte_osm_txt = open("staedte_osm.txt", "r").readlines()

        self.image_search_cache = list()

        bot.loop.create_task(self.refresh_search_cache_loop())

    def refresh_search_cache(self):
        self.logger.info("Refreshing image cache...")
        
        if self.bot.is_debug:
            self.logger.info("Debugging is on, not downloading image cache.")
            return

        self.image_search_cache = list()
        
        search_terms = ("house", "building", "apartment house", "small house")

        for term in search_terms:
            self.image_search_cache += next(util.duckduckgo_api.search(term, max_results=200))
            self.logger.info(str(search_terms.index(term) + 1) + "/" + str(len(search_terms)))

        self.logger.info("Done. Got " + str(len(self.image_search_cache)) + " results.")

    async def refresh_search_cache_loop(self):
        await asyncio.sleep(5)

        while True:
            try:
                thread = threading.Thread(target=self.refresh_search_cache)
                thread.start()
                thread.join(timeout=5)
            except Exception as exc:
                self.logger.error("Couldn't refresh search cache: " + str(exc))

            if len(self.image_search_cache) == 0:
                await asyncio.sleep(30)
            else:
                await asyncio.sleep(30 * 60 + random.randint(-100, 100)) # adding a bit of randomness so it doesn't seem like a bot ;))))))
            

    @commands.command()
    async def address(self, ctx):
        if self.timeouts.is_timeout(ctx.message.channel.id, "address"):
            await ctx.send(content=self.generic_responses["timeout"])
            return

        if len(self.image_search_cache) == 0:
            await ctx.send("The image search cache is not ready yet! Try again in a few seconds.")
            return

        self.timeouts.add_timeout(ctx.message.channel.id, "address", 7)

        city = random.choice(self.staedte_osm_txt)[1:-2]
        street = random.choice(self.strassen_osm_txt)[1:-2]
        number = random.randint(1, 24)

        chosen_image = random.choice(self.image_search_cache)

        filename = "cache/" + str(ctx.message.channel.id) + "_address.png"

        response = requests.get(chosen_image["thumbnail"], stream=True)

        with open(filename , "wb") as file:
            for buffer in response.iter_content(chunk_size=2048):
                file.write(buffer)

        await ctx.send(content=street + " " + str(number) + ", " + city, file=discord.File(filename))

        os.unlink(filename)