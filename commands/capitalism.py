import discord
import discord.ext.commands as commands
import pickle
import asyncio
import time
import random
import sys
sys.path.insert(0, "../")
import util

class StocksData():
    def __init__(self):
        self.money = {} # {author_id: money}
        self.stocks = [] # [{"name": name, "value": value in jrery dollars, "creator_id": id of creator, "creator_name": name#discriminator, "investments": {"investor1_id": amount in stocks}}]
        self.daily_cooldown = {} # {author_id: timestamp when cooldown expires}


class Capitalism(commands.Cog):
    def __init__(self, bot, timeouts, generic_responses):
        self.bot = bot
        self.timeouts = timeouts
        self.generic_responses = generic_responses
        self.stocks_explain = open("stocks.md", "r").read()
        self.stocks_changed = False

        try:
            self.data = pickle.load(open("user_data/stocks.pickle", "rb"))
        except:
            self.data = StocksData()
            self.stocks_changed = True

        bot.loop.create_task(self.stocks_autoflush())
        bot.loop.create_task(self.update_stocks())

    async def stocks_autoflush(self):
        while True:
            await asyncio.sleep(20)

            if self.stocks_changed:
                pickle.dump(self.data, open("user_data/stocks.pickle", "wb"))
                self.stocks_changed = False

    async def update_stocks(self):
        while True:
            await asyncio.sleep(120)
            for stock in self.data.stocks:
                stock["value"] += stock["value"] * (random.randint(-100, 100) / 100 / 100)
                if stock["value"] < 0.05:
                    stock["value"] = 0.05
            self.stocks_changed = True

    @commands.command()
    async def money(self, ctx, *user: discord.User):
        if len(user) == 0:
            user = ctx.message.author

        if user.id in self.data.money:
            await ctx.send(user.name + " currently has **" + str(round(self.data.money[user.id], 2)) + "** jrery dollars")
        else:
            await ctx.send(user.name + " currently has **0** jrery dollars")

    @commands.group()
    async def stocks(self, ctx):
        """Call this command without any arguments for a full explanation of the stocks system"""
        if ctx.message.content.endswith("stocks"):
            await ctx.message.author.send(self.stocks_explain.replace("\n\n", "\n"))
            await ctx.send("Sent you a DM")

    @stocks.command()
    async def create(self, ctx, name):
        for stock in self.data.stocks:
            if stock["creator_id"] == ctx.message.author.id:
                await ctx.send("You have already created a stock! Please delete it if you want to create another one")
                return

            if stock["name"] == name:
                await ctx.send("A stock with this name already exists!")
                return

        self.data.stocks.append({"name": name, "value": 1,"creator_id": ctx.message.author.id, "creator_name": ctx.message.author.name + "#" + ctx.message.author.discriminator, "investments": {}})
        await ctx.send("Stock **" + name + "** has been created!")
        self.stocks_changed = True

    @stocks.command()
    async def delete(self, ctx, name):
        stocks = self.data.stocks.copy()
        for stock in stocks:
            if stock["name"] == name:
                if stock["creator_id"] == ctx.message.author.id:
                    self.data.stocks.remove(stock)
                    await ctx.send("**" + name + "** has been deleted")
                else:
                    await ctx.send("You can only delete stocks owned by yoursel!")
                return
        await ctx.send("No stocks named **" + name + "** could be found!")
        self.stocks_changed = True

    @stocks.command()
    async def cashout(self, ctx, name, amount):
        stock_index = None
        for stock in self.data.stocks:
            if stock["name"] == name:
                stock_index = self.data.stocks.index(stock)

        if stock_index == None:
            await ctx.send("No stock with name **" + name + "** found")
            return

        if ctx.message.author.id not in self.data.stocks[stock_index]["investments"]:
            await ctx.send("You don't have any stocks in **" + name + "**")
            return

        if amount == "all":
            amount = self.data.stocks[stock_index]["investments"][ctx.message.author.id]
        else:
            try:
                amount = float(amount)
                if amount < 0:
                    raise Exception("fick dich alex")
            except:
                await ctx.send("Amount is not a valid number! (Try using . instead of , as a decimal point)")

        if self.data.stocks[stock_index]["investments"][ctx.message.author.id] < amount:
            await ctx.send("You don't have that many stocks in **" + name + "**!")
            return

        jrery_dollars = amount * self.data.stocks[stock_index]["value"]
        self.data.money[ctx.message.author.id] += jrery_dollars
        self.data.stocks[stock_index]["investments"][ctx.message.author.id] -= amount

        await ctx.send("You sold **" + str(amount) + " " + name + "** for **" + str(round(jrery_dollars, 5)) + " jrery dollars**")

        if self.data.stocks[stock_index]["investments"][ctx.message.author.id] == 0:
            del self.data.stocks[stock_index]["investments"][ctx.message.author.id]

        self.stocks_changed = True

    @stocks.command()
    async def invest(self, ctx, name, amount):
        stock_index = None
        for stock in self.data.stocks:
            if stock["name"] == name:
                stock_index = self.data.stocks.index(stock)

        if stock_index == None:
            await ctx.send("No stock with name **" + name + "** found")
            return

        if amount == "all":
            amount = self.data.money[ctx.message.author.id]
        else:
            try:
                amount = float(amount)
                if amount < 0:
                    raise Exception("fick dich alex")
            except:
                await ctx.send("Amount is not a valid number! (Try using . instead of , as a decimal point)")

        jrery_dollars = amount / self.data.stocks[stock_index]["value"]

        if self.data.money[ctx.message.author.id] < amount:
            await ctx.send("You don't have that many jrery dollars!")
            return

        self.data.money[ctx.message.author.id] -= jrery_dollars
        if ctx.message.author.id in self.data.stocks[stock_index]["investments"]:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] += amount
        else:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] = amount

        await ctx.send("You bought **" + str(amount) + " " + name + "** for **" + str(round(jrery_dollars, 5)) + " jrery dollars**")
        self.stocks_changed = True

    @stocks.command()
    async def daily(self, ctx):
        tm = time.time()
        if ctx.message.author.id in self.data.daily_cooldown:
            if self.data.daily_cooldown[ctx.message.author.id] > tm:
                await ctx.send("Please wait another " + util.time_calc.time_period_human_readable(self.data.daily_cooldown[ctx.message.author.id] - tm) + " before getting your free jrery dollars")
                return

        if ctx.message.author.id in self.data.money:
            self.data.money[ctx.message.author.id] += 100
        else:
            self.data.money[ctx.message.author.id] = 100

        self.data.daily_cooldown[ctx.message.author.id] = int(tm) + 24*60*60

        await ctx.send("**100** jrery dollars have been added to your account!")
        self.stocks_changed = True

    @stocks.command()
    async def list(self, ctx):
        message = "**All stocks registered on this bot:**\n"
        for stock in self.data.stocks:
            message += "**" + stock["name"] + "**" + " - current value: 1 " + stock["name"] + " = **" + str(round(stock["value"], 5)) + "** jrery dollar - created by " + stock["creator_name"] + "\n"

        if len(self.data.stocks) == 0:
            message += "(None)"

        await ctx.send(message)

    @stocks.command()
    async def mylist(self, ctx):
        message = "**Your stocks:**\n"
        for stock in self.data.stocks:
            if ctx.message.author.id in stock["investments"]:
                message += "**" + stock["name"] + "**" + " - current value: 1 " +\
                        stock["name"] + " = **" + str(round(stock["value"], 5)) +\
                        "** jrery dollars - You have **" +\
                        str(round(stock["investments"][ctx.message.author.id], 5)) +\
                        "**, currently worth **" +\
                        str(round(stock["investments"][ctx.message.author.id] * stock["value"], 5)) + "** jrery dollars - created by " + stock["creator_name"] + "\n"

        if message == "**Your stocks:**\n":
            message += "(None)"

        await ctx.send(message)
