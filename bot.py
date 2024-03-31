
from wp import post_to_wordpress
import telegram
from telegram.ext import Updater,CommandHandler
from settings import settings


bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)


def handle_message(update, context):
    message = ' '.join(context.args)
    x = post_to_wordpress(message)
    if x:
        update.message.reply_text('Message posted to WordPress successfully!')
    else:
        update.message.reply_text('Failed to post message to WordPress.')

def run_bot():
    updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handler for /post
    dispatcher.add_handler(CommandHandler("post", handle_message))

    # Start polling for updates
    updater.start_polling()
    updater.idle()