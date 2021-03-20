"""
Simple Bot to shorten url.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send a valid URL, and it will response the shortened link.
Press Ctrl-C on the command line or send a signal to the process to stop the bot.
"""

import logging
import pyshorteners
import re

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    update.message.reply_text(f'Hi, {update.message.from_user.first_name}! I\'m a bot created by @jmbenck.')
    update.message.reply_text('My goal is to make your life easier. Give me an URL and I\'ll short it for you')


def help_command(update: Update, _: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Give an URL and I will make it shorter for you!')


def url_shortener(update: Update, _: CallbackContext) -> None:
    """Validate text input data as URL and shorten it."""
    s = pyshorteners.Shortener()
    link = re.findall(r'(\w*\.\w+\.*\w+.*)', update.message.text)
    if link:
        url = s.tinyurl.short(f'https://{link[0]}')
        update.message.reply_text(url)
        print(update.message.from_user.first_name, 'shorted this link:', f'https://{link[0]}')
    else:
        update.message.reply_text('Please, send me a valid URL')


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("Token")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - Shorten the URL
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, url_shortener))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
