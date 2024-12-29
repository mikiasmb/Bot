import requests
from telegram import Update

async def summarize(update: Update) -> None:
    if update:
        term = update.message.text
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{term}"
        try:
            response = requests.get(url).json()
            summary = response["extract"]
            await update.message.reply_text(summary)
        except Exception as e:
            await update.message.reply_text(f"An error occurred: {e}")
    else:
        await update.message.reply_text("Please provide a term to define. Usage: /summarize <term> (Example: /define DNA)")
