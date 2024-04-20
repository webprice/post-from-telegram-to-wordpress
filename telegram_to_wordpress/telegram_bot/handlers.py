import asyncio
from settings import settings

from telegram_to_wordpress.wordpress.core import post_to_wordpress
import logging

logger = logging.getLogger(__name__)

def parse_update_message(update):
    if update.message.text:
        message = update.message.text
    elif update.message.caption:
        message = update.message.caption
    else:
        message = ""
    return message

def parse_update_photo(update,context):
    image_bytes = None
    if update.message.photo:
        from io import BytesIO

        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        bio = BytesIO()
        file.download(out=bio)
        image_bytes = bio.getvalue()

    print("image_bytes - ",bool(image_bytes))

    return image_bytes

def parse_wp_post_respose(response):
    if response:
        article_url = response.get('link')
        return f'Message posted to WordPress successfully!, Article url: {article_url}'
    else:
        return (f"Failed to post message to WordPress. Visit official repo: {settings.GITHUB_REPO_URL}")

def handle_message(update, context):
    logger.info("update: %s", update)

    try:
        coverted = update.to_dict() #otherwise shadowing from builtins

    except Exception as e:
        logger.error("Error converting update to dict: %s", e)
        update.message.reply_text("Error processing your request")
        return

    if int(coverted["message"]["from"]["id"]) != int(settings.OWNER_TELEGRAM_ID):
        print(f'{coverted["message"]["from"]["id"]} - not authorized to use this bot')
        update.message.reply_text("You are not authorized to use this bot")
        return

    message = parse_update_message(update)
    image_bytes = parse_update_photo(update,context)

    request = asyncio.run(post_to_wordpress(message, image=image_bytes))

    result =  parse_wp_post_respose(request)

    update.message.reply_text(result)

    return