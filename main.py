import telegram
from telegram.ext import Updater,MessageHandler,MessageFilter, Filters,CommandHandler
from settings import settings
from bot import run_bot

def main():
    # Start Telegram bot
    run_bot()

if __name__ == '__main__':
    main()