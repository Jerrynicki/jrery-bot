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
        self.reminders = {} # {id: [(stock, event, threshold)]} # event can be: "below" if stock goes below threshold or "above" if stock goes above threshold


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

        self.events = {} # for storing information about stock events, e.g. one stock only rising over multiple iterations

        bot.loop.create_task(self.stocks_autoflush())
        bot.loop.create_task(self.update_stocks())

    async def stocks_autoflush(self):
        while True:
            await asyncio.sleep(20)

            #if self.stocks_changed:
            #    pickle.dump(self.data, open("user_data/stocks.pickle", "wb"))
            #    self.stocks_changed = False
            # TODO: Make this work with the stocks_changed variable
            pickle.dump(self.data, open("user_data/stocks.pickle", "wb"))

    async def update_stocks(self):
        while True:
            await asyncio.sleep(120)
            for stock in self.data.stocks:
                
                if stock["name"] not in self.events:
                    val_change = random.randint(-100, 100) / 100 / 100 * 5
                    stock["value"] += val_change

                    if random.randint(1, 50) == 25:
                        self.events[stock["name"]] = [random.randint(1, 20), random.randint(-100, 100) / 100 / 100 * 10]
                                                     # duration of event     # how much the value changes

                else:
                    self.events[stock["name"]][0] -= 1
                    stock["value"] += self.events[stock["name"]][1]
                    if self.events[stock["name"]][0] == 0:
                        del self.events[stock["name"]]

                if stock["value"] < 0.05:
                    stock["value"] = 0.05

                for user in self.data.reminders:
                    delete = []
                    for reminder in self.data.reminders[user]:
                        if reminder[0] == stock["name"]:
                            try:
                                if reminder[1] == "above":
                                    if stock["value"] >= reminder[2]:
                                        user_ = self.bot.get_user(user)
                                        await user_.send("Hello " + user_.name + "!\n**" + stock["name"] + "** has just reached a value of **" + str(round(stock["value"], 5)) + "**! Come check it out!")
                                        delete.append(reminder)
                                elif reminder[1] == "below":
                                    if stock["value"] <= reminder[2]:
                                        user_ = self.bot.get_user(user)
                                        await user_.send("Hello " + user_.name + "!\n**" + stock["name"] + "** has just reached a value of **" + str(round(stock["value"], 5)) + "**! Come check it out!")
                                        delete.append(reminder)
                                elif reminder[1] == "event":
                                    if stock["name"] in self.events:
                                        user_ = self.bot.get_user(user)
                                        await user_.send("Hello " + user_.name + "!\n**" + stock["name"] + "** is currently undergoing an event! (**" + str(round(self.events[stock["name"]][1], 5)) + "** per round for **" + str(self.events[stock["name"]][0]) + "** rounds)\nCome check it out!")
                                        delete.append(reminder)
                            except Exception as exc:
                                print(exc)
                                delete.append(reminder)
                    for x in delete:
                        self.data.reminders[user].remove(x)
                                        

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
            message = self.stocks_explain.replace("\n\n", "\n").split("\n")
            for i in range(0, len(message), 10):
                try:
                    await ctx.message.author.send("\n".join(message[i:i+10]))
                except IndexError:
                    await ctx.message.author.send("\n".join(message[i:]))
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
                    investment_amount = 0
                    value = stock["value"]
                    for id in stock["investments"]:
                        jrery_dollars = stock["investments"][id] * value
                        self.data.money[id] += jrery_dollars
                        investment_amount += jrery_dollars

                    self.data.stocks.remove(stock)
                    await ctx.send("**" + name + "** has been deleted and a total of **" + str(round(investment_amount, 3)) + "** jrery dollars have been payed back to investors.")

                    self.stocks_changed = True
                else:
                    await ctx.send("You can only delete stocks owned by yoursel!")
                return
        await ctx.send("No stocks named **" + name + "** could be found!")

    @stocks.command()
    async def sell(self, ctx, name, amount):
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

        await ctx.send("You sold **" + str(round(amount, 3)) + " " + name + "** for **" + str(round(jrery_dollars, 3)) + " jrery dollars**")

        if self.data.stocks[stock_index]["investments"][ctx.message.author.id] == 0:
            del self.data.stocks[stock_index]["investments"][ctx.message.author.id]

        self.stocks_changed = True

    @stocks.command()
    async def cashout(self, ctx, name, jrery_dollars):
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

        if jrery_dollars == "all":
            jrery_dollars = self.data.stocks[stock_index]["value"] * self.data.stocks[stock_index]["investments"][ctx.message.author.id]
        else:
            try:
                jrery_dollars = float(jrery_dollars)
                if jrery_dollars < 0:
                    raise Exception("fick dich alex")
            except:
                await ctx.send("Amount is not a valid number! (Try using . instead of , as a decimal point)")

        if self.data.stocks[stock_index]["investments"][ctx.message.author.id] * self.data.stocks[stock_index]["value"] < jrery_dollars:
            await ctx.send("You don't have that many stocks in **" + name + "**!")
            return

        amount = jrery_dollars / self.data.stocks[stock_index]["value"]
        self.data.money[ctx.message.author.id] += jrery_dollars
        self.data.stocks[stock_index]["investments"][ctx.message.author.id] -= amount

        await ctx.send("You sold **" + str(round(amount, 3)) + " " + name + "** for **" + str(round(jrery_dollars, 3)) + " jrery dollars**")

        if self.data.stocks[stock_index]["investments"][ctx.message.author.id] == 0:
            del self.data.stocks[stock_index]["investments"][ctx.message.author.id]

        self.stocks_changed = True

    @stocks.command()
    async def buy(self, ctx, name, amount):
        stock_index = None
        for stock in self.data.stocks:
            if stock["name"] == name:
                stock_index = self.data.stocks.index(stock)

        if stock_index == None:
            await ctx.send("No stock with name **" + name + "** found")
            return

        if amount == "all":
            amount = self.data.money[ctx.message.author.id] / self.data.stocks[stock_index]["value"] 
        else:
            try:
                amount = float(amount)
                if amount < 0:
                    raise Exception("fick dich alex")
            except:
                await ctx.send("Amount is not a valid number! (Try using . instead of , as a decimal point)")

        jrery_dollars = amount * self.data.stocks[stock_index]["value"]

        if self.data.money[ctx.message.author.id] < jrery_dollars:
            await ctx.send("You don't have that many jrery dollars!")
            return

        self.data.money[ctx.message.author.id] -= jrery_dollars
        if ctx.message.author.id in self.data.stocks[stock_index]["investments"]:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] += amount
        else:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] = amount

        await ctx.send("You bought **" + str(round(amount, 3)) + " " + name + "** for **" + str(round(jrery_dollars, 3)) + " jrery dollars**")
        self.stocks_changed = True

    @stocks.command()
    async def invest(self, ctx, name, jrery_dollars):
        stock_index = None
        for stock in self.data.stocks:
            if stock["name"] == name:
                stock_index = self.data.stocks.index(stock)

        if stock_index == None:
            await ctx.send("No stock with name **" + name + "** found")
            return

        if jrery_dollars == "all":
            jrery_dollars = self.data.money[ctx.message.author.id]
        else:
            try:
                jrery_dollars = float(jrery_dollars)
                if jrery_dollars < 0:
                    raise Exception("fick dich alex")
            except:
                await ctx.send("Amount is not a valid number! (Try using . instead of , as a decimal point)")

        amount = jrery_dollars / self.data.stocks[stock_index]["value"]

        if self.data.money[ctx.message.author.id] < jrery_dollars:
            await ctx.send("You don't have that many jrery dollars!")
            return

        self.data.money[ctx.message.author.id] -= jrery_dollars
        if ctx.message.author.id in self.data.stocks[stock_index]["investments"]:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] += amount
        else:
            self.data.stocks[stock_index]["investments"][ctx.message.author.id] = amount

        await ctx.send("You bought **" + str(round(amount, 3)) + " " + name + "** for **" + str(round(jrery_dollars, 3)) + " jrery dollars**")
        self.stocks_changed = True

    @commands.command()
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
            in_circulation = 0
            for investments in stock["investments"]:
                in_circulation += stock["investments"][investments]
            in_circulation_value = stock["value"] * in_circulation

            message += "**" + stock["name"] + "**" + " - current value: 1 " + stock["name"] + " = **" + str(round(stock["value"], 3)) + "** jrery dollars - **" +\
                    str(round(in_circulation, 3)) + "** in circulation (=" + str(round(in_circulation_value, 3)) + " jrery dollars) - created by " + stock["creator_name"] + "\n"

        if len(self.data.stocks) == 0:
            message += "(None)"

        await ctx.send(message)

    @stocks.command()
    async def mylist(self, ctx):
        message = "**Your stocks:**\n"
        for stock in self.data.stocks:
            if ctx.message.author.id in stock["investments"]:
                message += "**" + stock["name"] + "**" + " - current value: 1 " +\
                        stock["name"] + " = **" + str(round(stock["value"], 3)) +\
                        "** jrery dollars - You have **" +\
                        str(round(stock["investments"][ctx.message.author.id], 3)) +\
                        "**, currently worth **" +\
                        str(round(stock["investments"][ctx.message.author.id] * stock["value"], 3)) + "** jrery dollars - created by " + stock["creator_name"] + "\n"

        if message == "**Your stocks:**\n":
            message += "(None)"

        await ctx.send(message)

    @stocks.command()
    async def notification(self, ctx, stock, event, threshold=0):
        if event not in ("above", "below", "event"):
            await ctx.send("Event type not recognized. Try jer!stocks to get an explanation of the stocks system.")
            return
        try:
            threshold = float(threshold)
        except Exception:
            await ctx.send("Threshold is not a valid number. (Try using . for the decimal point instead of ,)")
            return

        stock_exists = False
        for stock_ in self.data.stocks:
            if stock_["name"] == stock:
                stock_exists = True
                break

        if not stock_exists:
            await ctx.send("This stock doesn't exist!")
            return

        if ctx.message.author.id not in self.data.reminders:
            self.data.reminders[ctx.message.author.id] = []
        self.data.reminders[ctx.message.author.id].append((stock, event, threshold))

        if event != "event":
            await ctx.send("I will notify you when the value of **" + stock_["name"] + "** goes " + event + " **" + str(round(threshold, 5)) + "**")
        else:
            await ctx.send("I will notify you when an event with **" + stock_["name"] + "** happens")

    @stocks.command()
    async def events(self, ctx):
        message = "**Current ongoing events:**\n"

        for event in self.events:
            message += "**" + event + "** | **" + str(round(self.events[event][1], 5)) + "** per round | **" + str(self.events[event][0]) + "** rounds left\n"

        if len(self.events) == 0:
            message += "(None)"

        await ctx.send(message)

