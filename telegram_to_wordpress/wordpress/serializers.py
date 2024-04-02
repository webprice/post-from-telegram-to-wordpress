from typing import Optional
from pydantic import BaseModel
from settings import settings
class ParsedMessage(BaseModel):
    title: Optional[str]
    content: Optional[str]

    @staticmethod
    def parse_message(message:str):
        title = message.split("\n")[0]
        content = "\n".join(message.split("\n")[1:])
        return ParsedMessage(title=title, content=content)
from enum   import Enum
class PostStatus(str, Enum):
    publish = 'publish'

class  PostData(BaseModel):
    title: Optional[str]
    content: Optional[str]
    status: Optional[str] = PostStatus.publish.value
    categories: Optional[list] = [settings.WP_CATEGORY_ID]
    featured_media: Optional[str]

    @staticmethod
    def to_dict(parsed_msg,categories: Optional[list] = None, status: Optional[str] = PostStatus.publish.value):

        return {
            'title': parsed_msg.title,
            'content': parsed_msg.content,
            'status': status,
            'categories': categories if categories else [settings.WP_CATEGORY_ID]
        }