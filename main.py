from telegram_to_wordpress.telegram_bot.core import run_bot

def app():
    print('Starting bot...')
    run_bot()

if __name__ == '__main__':
    #run with uvicorn main:app --reload
    import uvicorn

    uvicorn.run("main:app", host="8000", reload=True)

