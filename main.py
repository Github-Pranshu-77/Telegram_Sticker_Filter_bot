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
    'AgADCgwAApXjQFU',
    'AgAD6g0AAsbsQVU',
    'AgADHxMAAqZlOFU',
    'AgAD7RAAAqpWKFU',
    'AgADNxAAAlbOKFU',
    'AgAD5QwAAnJBKVU',
    'AgADuhEAAhbUSVU',
    'AgADwREAAngIgVU',
    'AgAD-REAAolesVU',
    'AgADZRAAAnWpKFU',
    'AgADRA8AAp3zQFU',
    'AgAD3QsAAmL0QFU',
    'AgADmwsAAljEQFU',
    'AgADDAwAArmHQVU',
    'AgADuhEAAhbUSVU',
    'AgADwREAAngIgVU',
    'AgAD-REAAolesVU',
    'AgADZBIAAvaSIVU',
    'AgADCREAAvK7IFU',
    'AgAD7g4AAtAXkVQ'
]

# List of banned words
BANNED_WORDS = ['chip', 'pizza']  # Replace with actual banned words

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Dictionary to track user spam activity
user_spam_data = defaultdict(lambda: {'count': 0, 'last_message_time': 0})

# List of admin user IDs (replace with actual admin IDs)
ADMINS = [6115961196]  # Replace with actual admin IDs

# Max concurrent delete operations to avoid hitting rate limits
MAX_CONCURRENT_DELETIONS = 10

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! I will delete specific GIFs, stickers, and banned words.')

async def delete_messages(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.message
    chat_id = message.chat_id
    user_id = message.from_user.id
    user_name = message.from_user.username
    current_time = time.time()  # Use time.time() to get the current timestamp

    # List of tasks to be processed
    tasks = []

    # Check if the message contains a GIF
    if message.animation and message.animation.file_id in GIFS_TO_DELETE:
        tasks.append(delete_message(context, chat_id, message.message_id, "GIF", user_id, user_name, current_time))

    # Check if the message contains a sticker
    if message.sticker and message.sticker.file_unique_id in STICKERS_TO_DELETE:
        tasks.append(delete_message(context, chat_id, message.message_id, "Sticker", user_id, user_name, current_time))

    # Check if the message contains banned words (only delete if sent by admins)
    if message.text:
        for banned_word in BANNED_WORDS:
            if banned_word in message.text.lower() and user_id in ADMINS:
                tasks.append(delete_message(context, chat_id, message.message_id, "Banned Word", user_id, user_name, current_time))

    # Run all tasks concurrently
    if tasks:
        await asyncio.gather(*tasks)

async def delete_message(context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int, content_type: str, user_id: int, user_name: str, last_message_time: float) -> None:
    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)

        # Update spam data
        user_spam_data[user_id]['count'] += 1
        user_spam_data[user_id]['last_message_time'] = last_message_time

        # Schedule warning message
        asyncio.create_task(schedule_warning(user_id, chat_id, user_name, context, last_message_time))
    except Exception as e:
        logging.error(f"Failed to delete {content_type} with message_id {message_id}: {e}")

async def schedule_warning(user_id: int, chat_id: int, user_name: str, context: ContextTypes.DEFAULT_TYPE, last_message_time: float) -> None:
    await asyncio.sleep(2)  # Wait for 2 seconds
    current_time = time.time()  # Get the current timestamp
    if user_spam_data[user_id]['last_message_time'] == last_message_time:
        try:
            warning_message = await context.bot.send_message(chat_id=chat_id, text=f'Warning: User @{user_name} (ID: {user_id}), please do not send restricted content.')

            # Wait for 10 seconds before deleting the warning message
            await asyncio.sleep(10)
            await context.bot.delete_message(chat_id=chat_id, message_id=warning_message.message_id)
        except Exception as e:
            logging.error(f"Failed to send or delete warning: {e}")

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

    # Separate message handlers for GIFs, Stickers, and Banned Words
    application.add_handler(MessageHandler(filters.ANIMATION, delete_messages))
    application.add_handler(MessageHandler(filters.Sticker.ALL, delete_messages))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, delete_messages))  # For banned words

    application.run_polling()

if __name__ == '__main__':
    main()
