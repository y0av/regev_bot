from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
import logging

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


BOT_TOKEN = '6459804125:AAHRR3GNqWMe0qVhP1WUCoCqOasAogth4ok'

# Initialize an empty array to store user IDs
user_answered_ids = []
group_users = []

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! Press the button below to answer a question.")
    """Sends a message with three inline buttons attached."""
    keyboard = [
        [
            InlineKeyboardButton("Option 1", callback_data="1"),
            InlineKeyboardButton("Option 2", callback_data="2"),
        ],
        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text=f"Selected option: {query.data}")
    user_id = query.from_user.id
    user_answered_ids.append(user_id)
    logging.info("users who answered the poll list: %s", user_answered_ids)

async def sign_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.message.chat_id
    group_users.append(chat_id)
    logging.info("users signed in: %s", group_users)

def main():
    """Start the bot."""

    # Create the Application and pass it your bot's token.

    application = Application.builder().token(BOT_TOKEN).build()


    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(CommandHandler("add_me", sign_user))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
    application.idle()

if __name__ == '__main__':
    main()
