# jrery bot stocks

The stocks system in jrery bot works kind of similar to stocks in the real world. But not really.

All of the commands are subcommands of jer!stocks, so you can use them by sending `jer!stocks subcommand arg1 arg2 ...`

You can see your jrery dollars by using jer!money and get 100 free jrery dollars every 24h with jer!daily

Subcommands and explanations:

**create** name

* Creates a new stock with name `name`

* Each user can only have 1 stock

**delete** name

* Deletes the stock `name`

* You can only delete stocks that were created by you

* **WARNING**: When you delete a stock, everyone's investments will get converted back to jrery dollars at the current value

**buy** name amount

* Buys `amount` of the stock `name`

* Use `all` for `amount` to invest all of your jrery dollars

**invest** name jrery\_dollars

* Invest `jrery_dollars` into the stock `name`

* Use `all` for `jrery_dollars` to invest all of your jrery dollars

**sell** name amount

* Sells `amount` of stock `name` at the current value

* Use `all` for amount to cash out all of your investments on the stock

* Example: `jer!stocks sell jrery 50` will give you 100 jrery dollars if the value of `jrery` is 2.00 at the time of selling

**cashout** name jrery\_dollars

* Sell the amount of `name` required to give back `jrery_dollars` jrery dollars

* Use all for amount to cash out all of your investments on the stock

* Example: `jer!stocks cashout jrery 50` will give you 50 jrery dollars and will sell 25 stock if the value of `jrery` is 2.0 at the time of cashing out

**list**

* Lists all current stocks and their values

**mylist**

* Gives you a personalized list, showing all the stocks you have invested in, their current value, how many you have and how much they are worth currently

**notification** stock event threshold

* Notifies you when a stock goes above or below a specific value

* The name of the stock is specified in `stock`

* The type of event is specified in `event` - either "above", "below" or "event"

* The value the stock should be above or below of is specified in `threshold`

* When the event is "event", you will be notified when an event with the stock happens. No value for `threshold` is necessary

**events**

* Lists current ongoing events

The value of each currency is increased or decreased between -0.05 to 0.05 (changes can be as low as 0.0001) randomly every 2 minutes

"Events" have a 1:50 chance of occuring and will cause a constant value change over 1-20 rounds between -0.1 to 0.1
