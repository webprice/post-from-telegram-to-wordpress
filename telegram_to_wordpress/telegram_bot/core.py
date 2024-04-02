
from telegram_to_wordpress.wordpress.core import post_to_wordpress
import telegram
from telegram.ext import Updater,CommandHandler
from settings import settings
import asyncio

bot = telegram.Bot(token=settings.TELEGRAM_BOT_TOKEN)


def handle_message(update, context):
    if context.args:
        message = ' '.join(context.args)
    else:
        message = ''

    if update.message.photo:
        print("update.message.photo:", update.message.photo)
        #get the last image sent and save in memory as bytes:
        image = update.message.photo[-1].download_as_bytearray()
        image = bot.get_file(update.message.photo[-1].file_id).file_path
        #upload to wordpress:



        # image = update.message.photo[-1].get_file()
        print("image, bool(image):", image, bool(image))
        # bot.get_file(update.message.photo[-1].file_id).file_path

        #upload image to wordpress media library and set as featured image:
        request = asyncio.run(post_to_wordpress(message, image=image))
    else:
        request  = asyncio.run(post_to_wordpress(message))

    if request:
        article_url = request.get('link')
        update.message.reply_text(f'Message posted to WordPress successfully!, Article url: {article_url}')

    else:
        update.message.reply_text('Failed to post message to WordPress.'
                                  ' Visit official repo: https://github.com/webprice/post-from-telegram-to-wordpress')

def run_bot():
    updater = Updater(token=settings.TELEGRAM_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Register command handler for /post
    # make sure it works if the command sent with image??!
    # dispatcher.add_handler(CommandHandler("post", handle_message))
    from telegram.ext import MessageHandler, Filters
    # dispatcher.add_handler(MessageHandler(Filters.photo & Filters.command, handle_message))
    dispatcher.add_handler(CommandHandler("post", handle_message))
    # Add handler for image messages
    dispatcher.add_handler(MessageHandler(Filters.photo, handle_message))


    # Start polling for updates
    updater.start_polling()
    updater.idle()


def handle_post_command(update, context):
    update.message.reply_text("Please send an image along with the command.")

# Function to handle image messages
def handle_image(update, context):
    # Get the file ID of the largest photo sent
    file_id = update.message.photo[-1].file_id
    # Get the file object
    file = context.bot.get_file(file_id)
    # Download the file
    # file.download('image.jpg')
    update.message.reply_text("Image received and saved.")