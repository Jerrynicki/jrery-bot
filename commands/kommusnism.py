import discord
import discord.ext.commands as commands
import time

class Kommusnism():
    def __init__(self):
        self.kommusnism_times = dict()

    def time_start(self, channel):
        self.kommusnism_times[channel] = time.time()

    def time_stop(self, channel):
        delta = round(time.time() - self.kommusnism_times[channel], 2)
        del self.kommusnism_times[channel]

        return delta
