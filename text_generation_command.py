from transformers import pipeline
from telegram import Update

generator = pipeline(task="text-generation", model="distilgpt2")


async def text_generation(update: Update) -> None:
    user_text = update.message.text

    try:
        await update.message.reply_text("Generating text, please wait...")

        result = generator(
            user_text,
            pad_token_id=50256,  # required for GPT-2 models
            do_sample=True,      # sampling for creative text generation
            max_length=50        
        )

            
        generated_text = result[0]["generated_text"]
        await update.message.reply_text(generated_text)

    except Exception as e:
        print(f"Error during text generation: {e}")
        await update.message.reply_text("Sorry, something went wrong during text generation. Please try again!")

