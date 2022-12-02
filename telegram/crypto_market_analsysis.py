import os

import ccxt
import telepot

# Replace TOKEN with your bot's token
bot = telepot.Bot(os.getenv("TELEGRAM_MOMENTUM_BOT_TOKEN"))


def get_market_analysis():
    # Use ccxt to access the Binance API
    exchange = ccxt.binance()

    # Download the latest prices and volumes for all the coins traded on Binance
    tickers = exchange.fetch_tickers()

    # Calculate the total market capitalization
    market_cap = 0
    for ticker in tickers:
        price = ticker['last']
        volume = ticker['baseVolume']
        market_cap += price * volume

    # Calculate the top performers and losers
    top_performers = sorted(tickers, key=lambda x: x['percentage'], reverse=True)[:5]
    top_losers = sorted(tickers, key=lambda x: x['percentage'])[:5]

    # Calculate the 24-hour volume
    volume_24h = 0
    for ticker in tickers:
        volume_24h += ticker['baseVolume']

    # Return the calculated market analysis
    return {
        'market_cap': market_cap,
        'top_performers': top_performers,
        'top_losers': top_losers,
        'volume_24h': volume_24h,
    }


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Only handle text messages
    if content_type != 'text':
        return

    # Download and analyze the data from Binance
    most_momentum_coins = get_market_analysis()

    # Create the message
    message = f"Current market state: {most_momentum_coins}"
    # Send the expert investment suggestions back to the user
    bot.sendMessage(chat_id, message)


# Start listening for messages
bot.message_loop(handle_message)
