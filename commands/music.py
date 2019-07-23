import discord
import discord.ext.commands as commands
import discord.opus

import sys
import os
import threading
import asyncio

sys.path.insert(0, "../")
import util

class Music(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses
        self.connections = list()

    def find_connection(self, channel):
        for voice_client in self.connections:
            if voice_client.channel == channel:
                return voice_client
        
        return None

    @commands.command()
    async def connect(self, ctx):
        """Connect the bot to your current voice channel"""
        channel = ctx.message.author.voice.channel

        async with ctx.message.channel.typing():
            voice_client = await channel.connect()
            self.connections.append(voice_client)

            await ctx.send("привет сука блять")

    @commands.command()
    async def disconnect(self, ctx):
        """Disconnect the bot from your current voice channel"""
        voice_client = self.find_connection(ctx.message.author.voice.channel)

        if voice_client is None:
            await ctx.send(self.generic_responses["not_in_same_vc"])
            return

        await voice_client.disconnect()

        self.connections.remove(voice_client)

        await ctx.send("до свидания")

    @commands.command()
    async def play(self, ctx, link):
        """Play any link supported by youtube-dl"""

        await ctx.send("WARUM FUNKTIONIERT ES DENN NICHT AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
        return

        await ctx.send("поиск торрента...")

        async with ctx.message.channel.typing():
            voice_client = self.find_connection(ctx.message.author.voice.channel)

            if voice_client is None:
                await ctx.send(self.generic_responses["not_in_same_vc"])
                return

            if voice_client.is_playing():
                await ctx.send("already playing something брат")
                return

            target_file = "cache/" + str(voice_client.channel.id) + "_voice"

            if os.path.isfile(target_file):
                os.unlink(target_file)
            if os.path.isfile(target_file + ".wav"):
                os.unlink(target_file + ".wav")

            # store the return value in a list, since it will be the same across threads
            return_value = list()

            dl_conv_thread = threading.Thread(target=util.ytdl_download.download_and_convert_audio, args=(link, target_file, return_value))
            dl_conv_thread.start()

            while True:
                # yield to other threads so the connection won't be lost
                await asyncio.sleep(1.5)
                if dl_conv_thread.is_alive():
                    pass
                else:
                    break

            await asyncio.sleep(0.5)

            if return_value[0] != True:
                await ctx.send("сука блять " + return_value[0])
                return

            audio_source = discord.FFmpegPCMAudio(target_file, options="-vn", executable="/usr/bin/ffmpeg")
            voice_client.play(audio_source)

            await ctx.send("играть русский хардбас сейчас")

    @commands.command()
    async def stop(self, ctx):
        """Stop whatever is currently playing in your voice channel"""
        voice_client = self.find_connection(ctx.message.author.voice.channel)

        if voice_client is None:
            await ctx.send(self.generic_responses["not_in_same_vc"])
            return

        if not voice_client.is_playing():
            await ctx.send("nothing's playing товарищ")
            return

        voice_client.stop()

        await ctx.send("остановить капитализм...")