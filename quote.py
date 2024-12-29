import requests
from telegram import Update

async def get_quote(update: Update) -> None:
    url = "https://zenquotes.io/api/random"
    try:
        respond = requests.get(url).json()
        quote = respond[0]["q"]
        author = respond[0]["a"]
        await update.message.reply_text(f"{quote}\n-{author}")
    except Exception as e:
        print(e)
