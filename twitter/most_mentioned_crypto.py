import tweepy
from textblob import TextBlob


def get_most_talked_about_coins():
    # Replace these with your own Twitter API keys and tokens
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    # Use tweepy to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Download the latest tweets that mention crypto coins
    query = '#Bitcoin OR #Ethereum OR #XRP OR #Litecoin OR #BitcoinCash'
    tweets = api.search_tweets(q=query, lang='en', count=100)

    # Perform sentiment analysis on the downloaded tweets
    coin_sentiments = {}
    for tweet in tweets:
        text = tweet.full_text
        sentiment = TextBlob(text).sentiment.polarity
        for coin in ['#Bitcoin', '#Ethereum', '#XRP', '#Litecoin', '#BitcoinCash']:
            if coin in text:
                if coin not in coin_sentiments:
                    coin_sentiments[coin] = 0
                coin_sentiments[coin] += sentiment

    # Return the most talked about crypto coins
    return sorted(coin_sentiments, key=coin_sentiments.get, reverse=True)


# Download and analyze the tweets
most_talked_about_coins = get_most_talked_about_coins()

# Print out the most talked about stock tickers
print('Most talked about stocks:')
for coin in most_talked_about_coins:
    print(coin)
