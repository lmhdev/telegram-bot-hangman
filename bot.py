import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import os

from hangman import start_new_game, active_games

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


# Your bot token
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text("Hi! I am your bot. How can I help you?")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "Commands:\n/start - Start the bot\n/help - Show help\n/newgame - Start a new Cracking game\n/g <letter> - Guess a letter in password"
        )


async def new_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game = start_new_game(chat_id)
    await update.message.reply_text(
        "New Cracking game started! " + game.get_display_word()
    )


async def guess(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id not in active_games:
        await update.message.reply_text(
            "No active game. Start a new game with /newgame"
        )
        return

    game = active_games[chat_id]
    if context.args:
        letter = context.args[0].lower()
        if len(letter) == 1 and letter.isalnum():
            response = game.guess(letter)
            await update.message.reply_text(response)
        else:
            await update.message.reply_text("Please guess a single character.")
    else:
        await update.message.reply_text(
            "Please provide a letter to guess using command /g <letter>."
        )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message:
        await update.message.reply_text(
            "I did not understand that command. Use /help to see available commands."
        )


def main() -> None:
    # Create the Updater and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("newgame", new_game))
    application.add_handler(CommandHandler("g", guess))

    # on non-command messages - echo the message on Telegram
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()


if __name__ == "__main__":
    main()
