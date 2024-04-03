import asyncio

from telegram_to_wordpress.wordpress.core import post_to_wordpress


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

        # Get the file ID of the largest photo sent
        file_id = update.message.photo[-1].file_id
        # Get the file object
        file = context.bot.get_file(file_id)
        # Read the file content into memory
        bio = BytesIO()
        file.download(out=bio)
        # Get the bytes representation of the image
        image_bytes = bio.getvalue()
        # Now you have the image data stored in memory as bytes
        # You can further process the image or send it to WordPress
        # For example, you can call the upload_image_to_wordpress function
    print("image_bytes - ",bool(image_bytes))

    return image_bytes

def parse_wp_post_respose(response):
    if response:
        article_url = response.get('link')
        return f'Message posted to WordPress successfully!, Article url: {article_url}'
    else:
        from settings import settings
        return (f"Failed to post message to WordPress. Visit official repo: {settings.GITHUB_REPO_URL}")

def handle_message(update, context):

    message = parse_update_message(update)
    image_bytes = parse_update_photo(update,context)

    request = asyncio.run(post_to_wordpress(message, image=image_bytes))

    result =  parse_wp_post_respose(request)

    update.message.reply_text(result)

    return