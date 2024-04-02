from settings import settings
from aiohttp import request, BasicAuth
from typing import Optional
import logging

logger = logging.getLogger(__name__)

async def post_to_wordpress(post_data: dict) -> Optional[dict]:
    """Post a message to WordPress."""
    post_url =  get_wp_posts_url()

    async with request("POST", post_url, json=post_data, auth=BasicAuth(login=settings.WP_USERNAME, password=settings.WP_PASSWORD)) as response:
        res = await response.json()
        logger.info(f"post_to_wordpress Response: {res}")

        if response.status == 201:
            print('Message posted to WordPress successfully!')
        else:
            print('Error posting message to WordPress:', response.text)

    return res if response.status == 201 and res else False

from typing import Any
async def upload_media_to_wordpress(image) -> Optional[Any]:
    """Upload an image to WordPress media library."""
    auth = BasicAuth(login=settings.WP_USERNAME, password=settings.WP_PASSWORD)
    headers = {'Content-Type': 'image/jpeg'}

    #prepare image for uploading:
    #my code is = image.download_as_bytearray()

    # with open(image, 'rb') as file:
    #     # Prepare data payload with image file
    #     data = {
    #         'file': file
    #     }
    # async with request("POST", get_wp_media_url(), data=data , headers=headers, auth=auth) as response:
    async with request("POST", get_wp_media_url(), data=image, headers=headers, auth=auth) as response:

        print("we are here?!")

        res = await response.json()
        logger.info(f"upload_media_to_wordpress Response: {res}")

        if response.status == 201:
            # Image upload successful, extract the image URL from the response
            image_url = res['source_url']
            return image_url
        else:
            # Image upload failed
            print('Error uploading image to WordPress:', response.text)
            return None


def get_wp_base_url(domain_url:str):
    return f"{domain_url}/wp-json/wp/v2"


def get_wp_posts_url():
    return get_wp_base_url(settings.DOMAIN_BASE) + '/posts'

def get_wp_media_url():
    return get_wp_base_url(settings.DOMAIN_BASE) + '/media'