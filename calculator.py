import requests
from telegram import Update
from telegram.ext import ContextTypes

NEWTON_API_URL = "https://newton.now.sh/api/v2"

async def calculate(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Perform a mathematical operation using the Newton API."""
    user_input = update.message.text

    operation = context.user_data.get("state")

    try:
        response = requests.get(f"{NEWTON_API_URL}/{operation}/{user_input}")
        response.raise_for_status()  
        result = response.json().get("result", "No result returned.")

        await update.message.reply_text(f"Result: {result}")

    except requests.exceptions.RequestException as e:
        print(f"Error during API request: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")

    except Exception as e:
        print(f"Unexpected error: {e}")
        await update.message.reply_text("An unexpected error occurred. Please try again.")
