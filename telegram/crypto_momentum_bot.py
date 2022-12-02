import os

import ccxt
import telepot

# Replace TOKEN with your bot's token
bot = telepot.Bot(os.getenv("TELEGRAM_MOMENTUM_BOT_TOKEN"))


def get_most_momentum_coins():
    # Use ccxt to access the Binance API
    exchange = ccxt.binance()

    # Download the latest prices and volumes for all the coins traded on Binance
    tickers = exchange.fetch_tickers()

    # Calculate the momentum for each coin
    coin_momentum = {}
    for ticker in tickers:
        symbol = ticker['symbol']
        price = ticker['last']
        volume = ticker['baseVolume']
        momentum = price / volume
        coin_momentum[symbol] = momentum

    # Return the coins with the highest momentum
    return sorted(coin_momentum, key=coin_momentum.get, reverse=True)


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Only handle text messages
    if content_type != 'text':
        return

    # Download and analyze the data from Binance
    most_momentum_coins = get_most_momentum_coins()

    # Create the message
    message = f"Coins with the most momentum currently: {most_momentum_coins}"
    # Send the expert investment suggestions back to the user
    bot.sendMessage(chat_id, message)


# Start listening for messages
bot.message_loop(handle_message)
