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

    # Download the expert investment suggestions using yfinance
    ticker = yfinance.Ticker(ticker)
    recommendations = ticker.recommendations

    # Format the recommendations into a string
    message = 'Expert investment suggestions for {}:\n\n'.format(ticker.info['shortName'])
    for recommendation in recommendations:
        message += '- {}: {}\n'.format(recommendation['toGrade'], recommendation['firm'])

    # Send the expert investment suggestions back to the user
    bot.sendMessage(chat_id, message)


# Start listening for messages
bot.message_loop(handle_message)
