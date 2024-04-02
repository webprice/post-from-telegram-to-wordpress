from telegram_to_wordpress.wordpress.serializers import ParsedMessage, PostData
from telegram_to_wordpress.rest import wordpress as wp_rest
from typing import Optional, Any

async def post_to_wordpress(message, image:Optional[Any] = None) -> Optional[dict]:
    """Post a message to WordPress."""
    #from tg:
    serialised_message = ParsedMessage.parse_message(message)
    #to wordpress:
    serialised_post_data = PostData.to_dict(serialised_message)
    if image:
        #upload image to wordpress media library and set as featured image:
        #bot.get_file(update.message.photo[-1].file_id).file_path
        img = image.download_as_bytearray()

        image_url = await wp_rest.upload_media_to_wordpress(img)
        serialised_post_data['featured_media'] = image_url


    return await wp_rest.post_to_wordpress(serialised_post_data)

