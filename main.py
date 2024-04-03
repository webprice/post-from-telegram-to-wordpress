from telegram_to_wordpress.telegram_bot.core import run_bot
import uvicorn


def app():
    print('Starting bot...')
    run_bot()

if __name__ == '__main__':

    uvicorn.run("main:app", host="0.0.0.0",port=8000, reload=True)


