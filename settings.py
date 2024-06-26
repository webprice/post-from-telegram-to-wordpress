from dotenv import load_dotenv
import os

load_dotenv()


class Settings():
    TELEGRAM_BOT_TOKEN: str =  os.environ.get("TELEGRAM_BOT_TOKEN")
    WP_USERNAME: str =  os.environ.get("WP_USERNAME")
    WP_PASSWORD: str =  os.environ.get("WP_PASSWORD")
    WP_CATEGORY_ID: int = os.environ.get("WP_CATEGORY_ID")
    DOMAIN_BASE: str = os.environ.get("DOMAIN_BASE")
    GITHUB_REPO_URL: str = "https://github.com/webprice/post-from-telegram-to-wordpress/"
    OWNER_TELEGRAM_ID: str = os.environ.get("OWNER_TELEGRAM_ID")

settings = Settings()


