import logging
import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict
import time

# Replace with your bot's token
TOKEN = '7359450442:AAENFfHP_ZkysXmLRR3lCIOo7ihixZeUC-w'

# List of unique_ids for GIFs and stickers to be deleted
GIFS_TO_DELETE = ['file_id_of_gif1']  # Replace with actual file_id of GIFs
STICKERS_TO_DELETE = [
    'AgADQAgAApt6iFU',  # Replace with actual unique_id of stickers
    'AgADnwgAAivsiVU',
    'AgADgQYAAmosiFU',
    'AgADMAgAAlbXgFU',
    'AgAD-gcAAhPniFU',
    'AgADzAcAAsFYiVU',
    'AgADpQYAAnHUiVU',
    'AgADhQgAAuKeiVU',
    'AgADOAgAAiDtgFU',
    'AgADIQkAAqgvgFU',
    'AgADjwcAAtf-iFU',
    'AgAD5wYAAv0oiFU',
    'AgAD8gcAAohmiVU',
    'AgAD0QgAAnKqiV',
    'AgAD6wUAAiVWiFU',
    'AgADAwcAApwGgVU',
    'AgADJQoAAhlmiVU',
    'AgADxwYAAkeqiFU',
    'AgADpQYAAqKRiFU',
    'AgADYwkAAgRdiFU',
    'AgADOAgAAksTgVU',
    'AgADJggAAr45iFU',
    'AgADiwcAArYwiFU',
    'AgADJgUAApmSiVU',
    'AgADYgcAAtu_gVU',
    'AgADaAkAAqeygFU',
    'AgADgAUAArsSgFU',
    'AgAD0wcAAlTfgFU',
    'AgADPQkAApRjgVU',
    'AgAD5wUAAh_3iFU',
    'AgADyw8AAtNvYVU',
    'AgAD6Q0AApTcOFU',
    'AgAD8wsAAhXIQVU',
    'AgADDA8AAnMNQFU',
    'AgADCgwAApXjQF',
    'AgADVREAAo-Z4Uo',
    'AgAD5g0AAgpxmUo',
    'AgADywEAAsoDBgs',
    'AgAD4AEAAsoDBgs',
    'AgAD0gEAAsoDBgs',
    'AgAD0AEAAsoDBgs',
    'AgAD-CEAAuW2IUg',
    'AgADDB4AAlB-cEg',
    'AgADTwIAAsoDBgs',
    'AgADWwIAAsoDBgs',
    'AgADdAMAAm2wQgM',
    'AgADawMAAm2wQgM',
    'AgADfwMAAm2wQgM',
    'AgADpxMAAjJyiEo',
    'AgADBDIAAt3EMUk',
    'AgADSDsAAhNy-Ug',
    'AgADmzcAApeDEEg',
    'AgADNwcAAm4y2AAB',
    'AgADMQMAAm4y2AAB',
    'AgADFwMAAm4y2AAB',
    'AgADMQcAAm4y2AAB',
    'AgAD9wIAAm4y2AAB',
    'AgADHwMAAm4y2AAB',
    'AgADDwMAAm4y2AAB',
    'AgADJQMAAm4y2AAB',
    'AgADCwEAAooSqg4',
    'AgADEgEAAooSqg4',
    'AgADJwEAAlKJkSM',
    'AgADMgEAAlKJkSM',
    'AgADMAEAAlKJkSM',
    'AgADRzkAAl5WcUo',
    'AgADJS0AAgNPSEs',
    'AgADlioAAjnKsUo',
    'AgADNC8AAnWvsUo',
    'AgADdDAAAjB6sEo',
    'AgADfzcAApQCsUo',
    'AgAD0QEAAjgOghE',
    'AgAD3QEAAjgOghE',
    'AgAD4A8AAh0FOFU',
    'AgADUg8AAhX8OFU',
    'AgADJQ8AAu6COVU',
    'AgADUhIAAsAXQVU',
    'AgADsRAAAuyBOFU',
    'AgADCxIAAirNOVU',
    'AgADOhIAApJFOVU',
    'AgADgA8AAk7xQVU',
    'AgADrA8AAvzNQFU',
    'AgAD2hEAAoP8QFU',
    'AgADkBAAAu7-OFU',
    'AgADUBEAAuRUQVU',
    'AgAD8hAAArAhQFU',
    'AgADMhEAAv8vQFU',
    'AgAD2gEAAq4xRgU',
    'AgAD3QEAAq4xRgU',
    'AgAD4gEAAq4xRgU',
    'AgAD5QEAAq4xRgU',
    'AgAD6AEAAq4xRgU',
    'AgAD7AEAAq4xRgU',
    'AgAD8wEAAq4xRgU',
    'AgAD-gEAAq4xRgU',
    'AgAD_gEAAq4xRgU',
    'AgADAQIAAq4xRgU',
    'AgADBQIAAq4xRgU',
    'AgADBAIAAq4xRgU',
    'AgADOwIAAq4xRgU',
    'AgADPAIAAq4xRgU',
    'AgADPgIAAq4xRgU',
    'AgADPwIAAq4xRgU',
    'AgADQwIAAq4xRgU',
    'AgADRQIAAq4xRgU',
    'AgADSAIAAq4xRgU',
    'AgADSQIAAq4xRgU',
    'AgADSgIAAq4xRgU',
    'AgADSwIAAq4xRgU',
    'AgADTAIAAq4xRgU',
    'AgADTQIAAq4xRgU',
    'AgADVQIAAq4xRgU',
    'AgADWQIAAq4xRgU',
    'AgADWgIAAq4xRgU',
    'AgADWwIAAq4xRgU',
    'AgADBAIAAjT0KVY',
    'AgADaAIAAtLZMFY',
    'AgADPQIAAiD5KVY',
    'AgADhAQAAvhgKFY',
    'AgADbgIAAjuWKVY',
    'AgADSQMAAlxxKFY',
    'AgAD0QEAAi6tMVY',
    'AgADuQEAAjCwKFY',
    'AgADfAIAAqeUKFY',
    'AgAD3gEAAsreMVY',
    'AgAD8AEAAkgVKFY',
    'AgADCwIAAg5RKVY',
    'AgAD6gEAAkG3-VY',
    'AgADEAIAArTw-FY',
    'AgADVAIAAgsV-VY',
    'AgAD0gEAAhYl-FY',
    'AgAD5gEAAq4xRgU',
    'AgAD7QEAAq4xRgU',
    'AgAD6QEAAq4xRgU',
    'AgAD8QEAAq4xRgU',
    'AgADQBIAAqRUOVU',
    'AgAD5wEAAq4xRgU',
    'AgADKRYAAmnE0Uo',
    'AgAD2wEAAq4xRgU',
    'AgAD_AEAAq4xRgU',
    'AgADMwUAAm3oiVU',
    'AgAD0QgAAnKqiVU',
    'AgAD3wEAAq4xRgU',
    'AgAD5AEAAq4xRgU',
    'AgADmBEAAkkJ0VU',
    'AgADpgADO2AkFA',
    'AgAD6BEAAkkJ0VU',
    'AgADRA8AAp3zQFU'
]

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dictionary to track user spam activity
user_spam_data = defaultdict(lambda: {'count': 0, 'last_message_time': 0})

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Received /start command.")
    await update.message.reply_text('Hello! I will delete specific GIFs and stickers.')

async def delete_gifs_and_stickers(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    user_name = message.from_user.username
    current_time = time.time()  # Use time.time() to get the current timestamp

    logging.info(f"Received message from user_id: {user_id} (username: {user_name}) in chat_id: {chat_id}")

    # Check if the message contains a GIF
    if message.animation and message.animation.file_id in GIFS_TO_DELETE:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            logging.info(f"Deleted GIF with file_id: {message.animation.file_id}")

            # Update spam data
            user_spam_data[user_id]['count'] += 1
            user_spam_data[user_id]['last_message_time'] = current_time

            # Schedule warning message
            asyncio.create_task(schedule_warning(user_id, chat_id, user_name, context, current_time))
        except Exception as e:
            logging.error(f"Failed to delete GIF: {e}")

    # Check if the message contains a sticker
    if message.sticker and message.sticker.file_unique_id in STICKERS_TO_DELETE:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            logging.info(f"Deleted sticker with file_id: {message.sticker.file_id}")

            # Update spam data
            user_spam_data[user_id]['count'] += 1
            user_spam_data[user_id]['last_message_time'] = current_time

            # Schedule warning message
            asyncio.create_task(schedule_warning(user_id, chat_id, user_name, context, current_time))
        except Exception as e:
            logging.error(f"Failed to delete sticker: {e}")

async def schedule_warning(user_id: int, chat_id: int, user_name: str, context: ContextTypes.DEFAULT_TYPE, last_message_time: float) -> None:
    await asyncio.sleep(2)  # Wait for 2 seconds
    current_time = time.time()  # Get the current timestamp
    # Check if the user is still spamming
    if user_spam_data[user_id]['last_message_time'] == last_message_time:
        try:
            await context.bot.send_message(chat_id=chat_id, text=f'Warning: User @{user_name} (ID: {user_id}), please do not send restricted content.')
            logging.info(f"Sent warning to user_id: {user_id} (username: {user_name})")
        except Exception as e:
            logging.error(f"Failed to send warning: {e}")

async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        if len(context.args) > 0:
            username_or_id = context.args[0]
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f'Warning issued to {username_or_id}. Please adhere to the group rules.')
        else:
            await update.message.reply_text('Please provide a username or user ID to warn.')
    except Exception as e:
        logging.error(f"Failed to execute /warn command: {e}")
        await update.message.reply_text('Failed to warn the user.')

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Command handler to start the bot
    application.add_handler(CommandHandler("start", start))
    
    # Command handler to warn a user
    application.add_handler(CommandHandler("warn", warn_user))

    # Separate message handlers for GIFs and Stickers
    application.add_handler(MessageHandler(filters.ANIMATION, delete_gifs_and_stickers))
    application.add_handler(MessageHandler(filters.Sticker.ALL, delete_gifs_and_stickers))

    logging.info("Bot started.")
    application.run_polling()

if __name__ == '__main__':
    main()