# jrery bot stocks

The stocks system in jrery bot works kind of similar to stocks in the real world. But not really.

All of the commands are subcommands of jer!stocks, so you can use them by sending `jer!stocks subcommand arg1 arg2 ...`

You can see your jrery dollars by using jer!money

Subcommands and explanations:

**create** name

* Creates a new stock with name `name`

* Each user can only have 1 stock

**delete** name

* Deletes the stock `name`

* You can only delete stocks that were created by you

* **WARNING**: When you delete a stock, everyone's investments will get converted back to jrery dollars at the current value

**invest** name amount

* Invests `amount` jrery dollars in the stock `name`

* Use `all` for `amount` to invest all of your jrery dollars

**cashout** name amount

* Cashes out `amount` of stock `name` with the current value

* Use `all` for amount to cash out all of your investments on the stock

* Example: `jer!stocks cash-out jrery 50` will give you 100 jrery dollars if the value of `jrery` is 2.00 at the time of cashing out

**daily**

* Will give you 100 free jrery dollars

* Can only be used once every 24 hours

**list**

* Lists all current stocks and their values

**mylist**

* Gives you a personalized list, showing all the stocks you have invested in, their current value, how many you have and how much they are worth currently

The value of each currency is increased or decreased between -1 to 1 percent (with 2 decimal points) randomly every 2 minutes