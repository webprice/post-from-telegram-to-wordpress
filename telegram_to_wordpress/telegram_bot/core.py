
import asyncio

import telegram
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from settings import settings

from telegram_to_wordpress.telegram_bot.handlers import handle_message
from telegram_to_wordpress.wordpress.core import post_to_wordpress

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)


def run_bot():
    updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.text | Filters.photo, handle_message))

    updater.start_polling()
    updater.idle()

