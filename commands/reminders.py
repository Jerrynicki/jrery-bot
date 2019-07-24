import discord
import discord.ext.commands as commands

import time as time_module
import sys
import pickle
import asyncio

sys.path.insert(0, "../")
import util

class Reminders(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses

        try:
            self.reminders = pickle.load(open("user_data/reminders.pickle", "rb"))
        except FileNotFoundError:
            self.reminders = list()
        self.reminders_changed = False

        try:
            self.reminders_blocklist = pickle.load(open("user_data/reminders_blocklist.pickle", "rb"))
        except FileNotFoundError:
            self.reminders_blocklist = dict()
        self.reminders_blocklist_changed = False

        bot.loop.create_task(self.reminders_autoflush())
        bot.loop.create_task(self.reminders_remind())

    async def reminders_autoflush(self):
        while True:
            await asyncio.sleep(20)

            if self.reminders_changed:
                pickle.dump(self.reminders, open("user_data/reminders.pickle", "wb"))
                self.reminders_changed = False

            if self.reminders_blocklist_changed:
                pickle.dump(self.reminders_blocklist, open("user_data/reminders_blocklist.pickle", "wb"))
                self.reminders_blocklist_changed = False

    async def reminders_remind(self):
        while True:
            await asyncio.sleep(10)

            current_time = time_module.time()

            reminders = self.reminders.copy()

            for reminder in reminders:
                try:
                    if reminder[1] < current_time:
                        user = self.bot.get_user(reminder[0])
                        user_dm = await user.create_dm()

                        await user_dm.send("привет. you wanted me to remind you of:\n```" + reminder[2] + "```")

                        self.reminders.remove(reminder)
                        self.reminders_changed = True
                except:
                    pass

    def add_reminder(self, user, timestamp, text):
        self.reminders.append([user, timestamp, text])
        self.reminders_changed = True

    def get_reminders(self, user):
        reminders_list = list()

        for reminder in self.reminders:
            if reminder[0] == user:
                buffer = reminder.copy()
                buffer = buffer[1:]
                reminders_list.append(buffer)

        reminders_list.sort()

        return reminders_list

    @commands.command()
    async def remind(self, ctx, time, *message): # TODO: Rewrite this command as a command group, so it's less cluttered
        """The remind command can remind you or another user of something. Usage:

        remind [time] [message] will set a reminder for yourself
        remind [@user] [time] [message] will set a reminder for another user
        remind list will send a message with a list of set reminders
        remind list [@user] will send a message with a list of set reminders for the mentioned user
        remind blocklist will send a message with a list of blocked users (who can't set reminders for you)
        remind blocklist add [@user] will add a user to your blocklist
        remind blocklist remove [@user] will remove a user from your blocklist"""
        message = " ".join(message)

        if time == "list":
            if len(ctx.message.mentions) > 0:
                user = ctx.message.mentions[0]
            else:
                user = ctx.message.author
               
            reminders_list = self.get_reminders(user.id)

            if len(reminders_list) == 0:
                await ctx.send("No reminders are set!")
                return

            current_time = int(time_module.time())
            i = 0
            message = "**Reminders for " + user.name + "**\n"
            for reminder in reminders_list:
                message += "**[" + str(i) + "]**" + " in " + util.time_calc.time_period_human_readable(reminder[0] - current_time) + " `" + reminder[1] + "`\n"
                i += 1

            await ctx.send(message[:-1])

        elif time == "blocklist":
            if len(ctx.message.mentions) > 0:
                message = message.split(" ")

                user = ctx.message.mentions[0]

                if ctx.message.author.id not in self.reminders_blocklist:
                    self.reminders_blocklist[ctx.message.author.id] = list()
                
                if message[0] == "add":
                    self.reminders_blocklist[ctx.message.author.id].append(user.id)
                    self.reminders_blocklist_changed = True
                    await ctx.send("Added **" + user.name + "** to your blocklist!")

                elif message[0] == "remove":
                    try:
                        self.reminders_blocklist[ctx.message.author.id].remove(user.id)
                        self.reminders_blocklist_changed = True
                        await ctx.send("Removed **" + user.name + "** from your blocklist!")
                    except ValueError:
                        await ctx.send("**" + user.name + "** was not found in your blocklist!")

            else:
                if ctx.message.author.id not in self.reminders_blocklist or len(self.reminders_blocklist[ctx.message.author.id]) == 0:
                    await ctx.send("**You haven't blocked anyone!**")
                    return

                message = "**Reminders blocklist:**\n"
                for blocked in self.reminders_blocklist[ctx.message.author.id]:
                    user = self.bot.get_user(blocked)
                    if user == None:
                        username = "[Username not available]"
                    else:
                        username = user.name
                    message += "**" + username + "** (" + str(blocked) + ")\n"

                await ctx.send(message)

        else:
            if len(ctx.message.mentions) > 0 and time.startswith("<@"):
                user = ctx.message.mentions[0]
                offset_args = True
            else:
                user = ctx.message.author
                offset_args = False

            if offset_args:
                time = message.split(" ")[0]
                message = " ".join(message.split(" ")[1:])

            if user.id == self.bot.user.id:
                await ctx.send("and i say no")
                return

            timestamp = int(util.time_calc.timestamp_in(time))

            if user.id in self.reminders_blocklist and ctx.message.author.id in self.reminders_blocklist[user.id]:
                await ctx.send("This user has blocked you from creating reminders for them!")
                return

            self.add_reminder(user.id, timestamp, message)

            if offset_args:
                await ctx.send("я буду remind " + user.name)
            else:
                await ctx.send("я буду remind you")


