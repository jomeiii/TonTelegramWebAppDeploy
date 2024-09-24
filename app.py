from config import SHORT_NAMEGAME, TOKEN

from flask import Flask
from telegram import Update, Bot
from telegram.ext import CommandHandler, CallbackQueryHandler, InlineQueryHandler, Application
import os
import asyncio

queries = {}

app = Flask(__name__, static_folder='TonTelegramWebAppDeploy')

bot = Bot(token=TOKEN)

async def start_game(update: Update, context):
    await update.message.reply_game(SHORT_NAMEGAME)


async def callback_query_handler(update: Update, context):
    query = update.callback_query
    if query.game_short_name != SHORT_NAMEGAME:
        await bot.answer_callback_query(query.id, text=f"Sorry, '{query.game_short_name}' is not available.")
    else:
        queries[query.id] = query
        game_url = f"https://jomeiii.github.io/TonTelegramWebAppDeploy/?user_id={update.effective_user.id}"
        await bot.answer_callback_query(
            callback_query_id=query.id,
            url=game_url
        )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    updater = Application.builder().token(token=TOKEN).build()
    updater.add_handler(CommandHandler("start", start_game))
    updater.add_handler(CommandHandler("game", start_game))
    updater.add_handler(CallbackQueryHandler(callback_query_handler))
    asyncio.run(updater.run_polling())
    
    app.run(port=port)
