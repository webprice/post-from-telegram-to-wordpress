import logging
import random
from typing import Any, Optional

import aiohttp

from settings import settings

logger = logging.getLogger(__name__)

async def post_to_wordpress(post_data: dict) -> Optional[dict]:
    """Post a message to WordPress."""
    post_url =  get_wp_posts_url()
    auth = aiohttp.BasicAuth(login=settings.WP_USERNAME, password=settings.WP_PASSWORD)
    async with aiohttp.ClientSession() as session:
        async with session.post(post_url, json=post_data, auth=auth) as response:
            res = await response.json()
            logger.info(f"post_to_wordpress Response: {res}")

            if response.status == 201:
                print('Message posted to WordPress successfully!')
            else:
                print('Error posting message to WordPress:', response.text)

    return res if response.status == 201 and res else False

async def upload_media_to_wordpress(image: bytes, content_type: str) -> Optional[Any]:
    """Upload an image to WordPress media library."""
    auth = aiohttp.BasicAuth(login=settings.WP_USERNAME, password=settings.WP_PASSWORD)

    filename = f"image_{random.randint(1,1000)}"
    url = get_wp_media_url()

    headers = {'Content-Type': f'image/{content_type}', 'Content-Disposition': f'attachment; filename={filename}.{content_type}'}

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=image, headers=headers, auth=auth) as response:
            if response.status == 201:
                return await response.json()
            else:
                print('Error uploading image to WordPress:', response.text)
                return None


def get_wp_base_url(domain_url:str):
    return f"{domain_url}/wp-json/wp/v2"


def get_wp_posts_url():
    return get_wp_base_url(settings.DOMAIN_BASE) + '/posts'

def get_wp_media_url():
    return get_wp_base_url(settings.DOMAIN_BASE) + '/media'