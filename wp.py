import requests
from settings import settings
from pydantic import BaseModel
from typing import Optional

wordpress_base_url = f"{settings.WP_URL}/wp-json/wp/v2/"
class ParsedMessage(BaseModel):
    title: Optional[str]
    content: Optional[str]
def parse_message(message) -> ParsedMessage:
    title = message.split("\n")[0]
    content = "\n".join(message.split("\n")[1:])
    return ParsedMessage(title=title, content=content)
def post_to_wordpress(message) -> bool:
    serialised_message = parse_message(message)
    post_data = {
        'title': serialised_message.title,
        'content': serialised_message.content,
        'status': 'publish',
        'categories': [settings.WP_CATEGORY_ID]  # ID of the category where you want to post
    }

    # Authenticate with WordPress
    auth = (settings.WP_USERNAME, settings.WP_PASSWORD)

    # Make POST request to WordPress REST API
    response = requests.post(settings.WP_URL + '/posts', json=post_data, auth=auth)

    if response.status_code == 201:
        print('Message posted to WordPress successfully!')
    else:
        print('Error posting message to WordPress:', response.text)

    return True if response.status_code == 201 else False

