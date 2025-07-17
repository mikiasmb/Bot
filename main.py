from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
from Features import calculator, quote, summarize, text_generation_command

TOKEN = "BOT TOKEN"
keyboard = {
    "main-menu": [
        [KeyboardButton("Calculate"), KeyboardButton("Generate AI-text")],
        [KeyboardButton("Summarize term"), KeyboardButton("Quote")]
    ],
    "calculate-menu": [
        [KeyboardButton("Factorize"), KeyboardButton("Simplify"), KeyboardButton("Derive"), KeyboardButton("Integrate")],
        [KeyboardButton("Find 0's"), KeyboardButton("Absolute value"), KeyboardButton("log"),
         KeyboardButton("Area under curve")],
        [KeyboardButton("Back")]
    ]
}

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    full_name = update.effective_user.full_name
    reply_markup = ReplyKeyboardMarkup(keyboard["main-menu"], resize_keyboard=True)
    context.user_data["state"] = "main-menu"

    await update.message.reply_text(f"Welcome {full_name}!", reply_markup=reply_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    hint = """
    Factorize -> x^2 + 2x -> x (x + 2)
    Simplify -> 2^2+2(2) -> 8
    Derive -> x^2+2x -> 2 x + 2
    Integrate -> x^2+2x -> 1/3 x^3 + x^2 + C
    Find 0's -> x^2+2x -> [-2,0]
    Absolute value -> -2 -> 2
    log -> 2|8 -> 3
    Area under curve -> 2:4lx^3 -> 60
    """

    reply_markup = ReplyKeyboardMarkup(keyboard["main-menu"], resize_keyboard=True)
    context.user_data["state"] = "main-menu"

    await update.message.reply_text(hint, reply_markup=reply_markup)


async def handle_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_input = update.message.text
    current_state = context.user_data.get("state")

    if current_state == "main-menu":
        if user_input == "Calculate":
            context.user_data["state"] = "calculate-menu"
            reply_markup = ReplyKeyboardMarkup(keyboard["calculate-menu"], resize_keyboard=True)
            await update.message.reply_text("choose", reply_markup=reply_markup)

    elif current_state == "calculate-menu":
        if user_input == "Factorize":
            context.user_data["state"] = "factor"
            await update.message.reply_text("Send an expression to factorize.")
        elif user_input == "Simplify":
            context.user_data["state"] = "simplify"
            await update.message.reply_text("Send an expression to simplify.")
        elif user_input == "Derive":
            context.user_data["state"] = "derive"
            await update.message.reply_text("Send an expression to derive.")
        elif user_input == "Integrate":
            context.user_data["state"] = "integrate"
            await update.message.reply_text("Send an expression to integrate.")
        elif user_input == "Find 0's":
            context.user_data["state"] = "zeroes"
            await update.message.reply_text("Send an expression to find the zeroes.")
        elif user_input == "Absolute value":
            context.user_data["state"] = "abs"
            await update.message.reply_text("Send an expression to find the absolute value.")
        elif user_input == "log":
            context.user_data["state"] = "log"
            await update.message.reply_text("Send an expression to find the logarithm.")
        elif user_input == "Back":
            context.user_data["state"] = "main-menu"
            reply_markup = ReplyKeyboardMarkup(keyboard["calculate-menu"], resize_keyboard=True)
            await update.message.reply_text("choose an option to continue.", reply_markup=reply_markup)

    elif current_state in ["factor", "simplify", "derive", "integrate", "zeroes", "abs", "log"]:
        await math_command.calculate(update, context)
        context.user_data["state"] = "calculate-menu"
        reply_markup = ReplyKeyboardMarkup(keyboard["calculate-menu"], resize_keyboard=True)
        await update.message.reply_text("choose an option to continue.", reply_markup=reply_markup)

    elif current_state == "Quote":
        await quote_command.get_quote(update)
        context.user_data["state"] = "main-menu"
        reply_markup = ReplyKeyboardMarkup(keyboard["main-menu"], resize_keyboard=True)
        await update.message.reply_text("choose an option to continue.", reply_markup=reply_markup)

    elif current_state == "Generate AI-text":
        await update.message.reply_text("Send a text")
        await text_generation_command.process_text_generation(update, context)
        context.user_data["state"] = "main-menu"
        reply_markup = ReplyKeyboardMarkup(keyboard["main-menu"], resize_keyboard=True)
        await update.message.reply_text("choose an option to continue.", reply_markup=reply_markup)

    elif current_state == "Summarize term":
        await update.message.reply_text("Send a term to summarize.")
        await summarize_command.summarize(update)
        context.user_data["state"] = "main-menu"
        reply_markup = ReplyKeyboardMarkup(keyboard["main-menu"], resize_keyboard=True)
        await update.message.reply_text("choose an option to continue.", reply_markup=reply_markup)


def main():
    app = Application.builder().token(TOKEN).build()
    print("Bot starting..")

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_main_menu))

    print("Polling..")
    app.run_polling()


if __name__ == '__main__':
    main()
