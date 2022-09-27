import datetime
from time import sleep

import requests
import schedule
import tweepy

# Sleep time in seconds
sleep_time: int = 10

# Tweet by price change value
tweet_by_price_change: int = 100

# Set time for good morning tweet in 24-hour format
good_morning_tweet = "09:00"

# Which coin to track. For example: BTCUSDT or ETHUSDT. !!Don't change the 0 in the end!! It's the starting price.
dictcoins = {'BTCUSDT': 0, 'ETHUSDT': 0, 'BNBUSDT': 0, 'NEOUSDT': 0, 'BCCUSDT': 0, 'LTCUSDT': 0, 'ADAUSDT': 0,
             'EOSUSDT': 0, 'HOTUSDT': 0, 'OMGUSDT': 0, 'BNTUSDT': 0, 'GMTUSDT': 0, 'DASHUSDT': 0, 'ZECUSDT': 0,
             'ONGUSDT': 0, 'NULSUSDT': 0, 'BTTCUSDT': 0, 'LOKAUSDT': 0, 'XNOUSDT': 0, 'TUSDT': 0, 'NBTUSDT': 0,
             'KDAUSDT': 0, 'STEEMUSDT': 0, 'NEXOUSDT': 0, 'BIFIUSDT': 0, 'ALPINEUSDT': 0,
             'ASTRUSDT': 0, 'WOOUSDT': 0, 'STGUSDT': 0, 'EPXUSDT': 0, 'ENJUSDT': 0, 'CELRUSDT': 0, 'FETUSDT': 0,
             'BATUSDT': 0, 'XMRUSDT': 0, 'LINKUSDT': 0}

# Consumer keys and access tokens, used for OAuth
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'

# For in coin in dictcoins do:
for coin in dictcoins:
    # Get current price
    try:
        price = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + coin).json()['price']
        # Set current price as old price
        dict = {coin: price}
        dictcoins.update(dict)
    except KeyError:
        print("\033[91m" + "Error: Coin not found! \033[0m")
        continue

    # Print starting the bot with the current price
    print("\033[95m" + "Started the bot for " + coin + " with price: $" + str(
        dictcoins[coin]) + " Press CTRL+C to exit" + "\033[0m")

print("\033[95m" + "The bot will check the prices every " + str(sleep_time) + " seconds \033[0m")
print("\033[95m" + f"The bot will tweet if the price changes by ${tweet_by_price_change} or more \033[0m")
print("\033[95m" + "The bot will tweet a good morning tweet at " + good_morning_tweet + " \033[0m")
# Print a line in the console
print("\033[95m" + "-------------------------------------------------------------------------------- \033[0m")

sleep(sleep_time)


# Send a good morning tweet at 9:00
def job():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    # Get a random quote from api.quotable.io
    data = requests.get('https://api.quotable.io/random?maxLength=200')
    json = data.json()
    quote = json['content']
    author = json['author']
    try:
        api.update_status('Good morning! The quote of the day is "' + quote + '" by ' + author)
    except tweepy.TweepError as e:
        if e.api_code == 187:
            print("\033[91m" + "Error: Duplicate tweet! \033[0m")
        elif e.api_code == 186:
            print("\033[91m" + "Error: Tweet is too long! \033[0m")
        else:
            print("\033[91m" + "Error: Something went wrong! \033[0m")
            print(e)
    print("\033[92m" + "Good morning tweet sent! \033[0m")


schedule.every().day.at(good_morning_tweet).do(job)
while True:
    schedule.run_pending()
    print("\033[94m" + "Checking prices... \033[0m")
    for coin in dictcoins:
        try:
            price = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=' + coin).json()['price']
        except KeyError:
            print("\033[91m" + "Error: Coin not found! \033[0m")
            continue
        now = datetime.datetime.now()
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        difference = float(int(float(price)) - int(float(dictcoins[coin])))
        print(
            "\033[92m" + f"{now} - {coin.replace('USDT', '')} - Current price: ${price} - Old price: ${dictcoins[coin]} - Difference: ${difference} \033[0m")
        if difference >= tweet_by_price_change:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)
            # Tweet the price change and round it to 2 decimals
            try:
                api.update_status(
                    f"{coin.replace('USDT', '')} price has increased by ${round(difference, 2)}! Current price: ${round(float(price), 2)}")
                print(
                    "\033[94m" + f"{coin.replace('USDT', '')} price has increased by ${difference}! Current price: ${price} \033[0m")
                dict = {coin: price}
                dictcoins.update(dict)
            except tweepy.TweepError as e:
                if e.api_code == 187:
                    print("\033[91m" + "Error: Duplicate tweet! \033[0m")
                    continue
                elif e.api_code == 186:
                    print("\033[91m" + "Error: Tweet is too long! \033[0m")
                    continue
                else:
                    print("\033[91m" + "Error: Something went wrong! \033[0m")
                    print(e)
                    continue
        elif difference <= -tweet_by_price_change:
            auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
            auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
            api = tweepy.API(auth)
            # Remove - from difference
            difference = float(difference * -1)
            try:
                api.update_status(
                    f"{coin.replace('USDT', '')} price has decreased by ${round(difference, 2)}! Current price: ${round(float(price), 2)}")
                print(
                    "\033[94m" + f"{coin.replace('USDT', '')} price has decreased by ${difference}! Current price: ${price}  \033[0m")
                dict = {coin: price}
                dictcoins.update(dict)
            except tweepy.TweepError as e:
                if e.api_code == 187:
                    print("\033[91m" + "Error: Duplicate tweet! \033[0m")
                    continue
                elif e.api_code == 186:
                    print("\033[91m" + "Error: Tweet is too long! \033[0m")
                    continue
                else:
                    print("\033[91m" + "Error: Something went wrong! \033[0m")
                    print(e)
                    continue

    sleep(sleep_time)
