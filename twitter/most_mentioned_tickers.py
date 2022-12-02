import tweepy
from textblob import TextBlob


def get_most_talked_about_stocks():
    # Replace these with your own Twitter API keys and tokens
    consumer_key = 'YOUR_CONSUMER_KEY'
    consumer_secret = 'YOUR_CONSUMER_SECRET'
    access_token = 'YOUR_ACCESS_TOKEN'
    access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

    # Use tweepy to access the Twitter API
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    # Download the latest tweets that mention stock tickers
    query = '$AAPL OR $GOOGL OR $MSFT OR $AMZN OR $FB'
    tweets = api.search_tweets(q=query, lang='en', count=100)

    # Perform sentiment analysis on the downloaded tweets
    stock_sentiments = {}
    for tweet in tweets:
        text = tweet.full_text
        sentiment = TextBlob(text).sentiment.polarity
        for ticker in ['$AAPL', '$GOOGL', '$MSFT', '$AMZN', '$FB']:
            if ticker in text:
                if ticker not in stock_sentiments:
                    stock_sentiments[ticker] = 0
                stock_sentiments[ticker] += sentiment

    # Return the most talked about stock tickers
    return sorted(stock_sentiments, key=stock_sentiments.get, reverse=True)


# Download and analyze the tweets
most_talked_about_stocks = get_most_talked_about_stocks()

# Print out the most talked about stock tickers
print('Most talked about stocks:')
for stock in most_talked_about_stocks:
    print(stock)
