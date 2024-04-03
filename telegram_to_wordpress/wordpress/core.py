from typing import Any, Optional

from telegram_to_wordpress.rest import wordpress as wp_rest
from telegram_to_wordpress.wordpress.serializers import ParsedMessage, PostData


async def post_to_wordpress(message, image:Optional[bytes] = None) -> Optional[dict]:
    """Post a message to WordPress."""
    #from tg:
    serialised_message = ParsedMessage.parse_message(message)
    #to wordpress:
    serialised_post_data = PostData.to_dict(serialised_message)

    if image:
        media_response = await wp_rest.upload_media_to_wordpress(image=image, content_type='jpeg')
        # print("post_to_wordpress, media_response  - ",media_response)
        if media_response:
            media_url = media_response['guid']['rendered']
            print("media_url - ",media_url)
            media_id = media_response['id']
            serialised_post_data['featured_media'] = media_id


    return await wp_rest.post_to_wordpress(serialised_post_data)

