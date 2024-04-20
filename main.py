
import uvicorn
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
def app():
    from telegram_to_wordpress.telegram_bot.core import run_bot
    print("Starting Telegram bot")
    run_bot()
    print("Telegram bot started")


if __name__ == '__main__':
    from telegram_to_wordpress.telegram_bot.core import run_bot
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info",reload=True)
