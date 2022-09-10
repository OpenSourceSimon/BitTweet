import datetime
from time import sleep
import requests
import tweepy
import schedule

# Sleep time in seconds
sleep_time: int = 60

# Tweet by price change value
tweet_by_price_change: int = 100

# Set time for good morning tweet in 24-hour format
time = "09:00"

# The bitcoin API URL to get the current price in USD
bitcoin_api_url: str = "https://api.coindesk.com/v1/bpi/currentprice.json"

# Consumer keys and access tokens, used for OAuth
CONSUMER_KEY = 'XXXXXXXXXXXXXXXXXXXXXX'
CONSUMER_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_KEY = 'XXXXXXXXXXXXXXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXX'
ACCESS_SECRET = 'XXXXXXXXXXXXXXXXXXXXXX'

response = requests.get(bitcoin_api_url)
data = response.json()
start_price = data["bpi"]["USD"]["rate"]
start_price = int(float(start_price.replace(',', '')))
print("\033[95m" + "Started the bot! Starting price is: $" + str(start_price) + " Press CTRL+C to exit \033[0m")
print("\033[95m" + "The bot will check the bitcoin price every " + str(sleep_time) + " seconds \033[0m")
print("\033[95m" + f"The bot will tweet if the price changes by ${tweet_by_price_change} or more \033[0m")
print("\033[95m" + "The bot will tweet a good morning tweet at " + time + " \033[0m")


# Send a good morning tweet at 9:00
def job():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
    api = tweepy.API(auth)
    api.update_status("Good morning! The current Bitcoin price is: $" + str(price) + ".")
    print("\033[94m" + "Tweeted: Good morning! The current Bitcoin price is: $" + str(price) + ". \033[0m")


while True:
    response = requests.get(bitcoin_api_url)
    data = response.json()
    price = data["bpi"]["USD"]["rate"]
    # Format price to int and remove comma and decimal
    price = int(float(price.replace(',', '')))
    # Get current time and format it
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d %H:%M:%S")
    print(
        "Bitcoin price is: $" + str(price) + ". Current time is: " + str(now) + ". Difference is: $" + str(
            price - start_price) + ". "
                                   "Percentage change is: " + str(
            round(((price - start_price) / start_price) * 100, 2)) + "%")

    schedule.every().day.at(time).do(job)

    if price > (start_price + tweet_by_price_change):
        # Print the price and time to the console in blue
        print("\033[94m" + "Bitcoin price changed! Bitcoin price is: $" + str(price) + "\033[0m")
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(
            f"Bitcoin price just went up by ${price - start_price}!" + " Current price is: $" + str(
                price) + " #bitcoin #btc")
        print("\033[94m" + "Tweeted: Bitcoin price just went up by $" + str(
            price - start_price) + "!" + " Current price is: $" + str(
            price) + " #bitcoin #btc \033[0m")
    elif price < (start_price - tweet_by_price_change):
        # Print the price and time to the console in red
        print("\033[91m" + "Bitcoin price changed! Bitcoin price is: $" + str(price) + "\033[0m")
        auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
        auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
        api = tweepy.API(auth)
        api.update_status(
            f"Bitcoin price just went down by ${start_price - price}!" + " Current price is: $" + str(
                price) + " #bitcoin #btc")
        print("\033[94m" + "Tweeted: Bitcoin price just went down by $" + str(
            start_price - price) + "!" + " Current price is: $" + str(
            price) + " #bitcoin #btc \033[0m")

    sleep(sleep_time)
