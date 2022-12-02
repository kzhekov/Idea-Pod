import os

import telepot
import yfinance


# Replace TOKEN with your bot's token
bot = telepot.Bot(os.getenv("TELEGRAM_MOMENTUM_BOT_TOKEN"))


def handle_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)

    # Only handle text messages
    if content_type != 'text':
        return

    # Get the stock ticker from the message
    ticker = msg['text']

    # Download the stock data using yfinance
    data = yfinance.Ticker(ticker).history(start='1/1/2000', end='1/1/2022')

    # Calculate the momentum of the stock
    momentum = (data['Close'][-1] - data['Close'][-21]) / data['Close'][-21]

    # Send the calculated momentum back to the user
    bot.sendMessage(chat_id, 'The momentum of {} is {}'.format(ticker, momentum))


# Start listening for messages
bot.message_loop(handle_message)
