"""
⚙️ TGBot-for-Orders - Created by Marc ⚙️

📄 License: Custom License Agreement
Copyright © 2025 Marc. All rights reserved.

🚫 Unauthorized use, copying, modification, or distribution of this software is strictly prohibited.
❗ Violators will be prosecuted under international copyright law.

⚠️ WARNING: Misuse of this code will lead to legal action. Unauthorized users may face endless debugging hell.

🔒 By using this software, you agree to these terms.
"""


import telebot
from handlers import register_handlers
from dotenv import load_dotenv
import os

load_dotenv()

# Load your Telegram bot token from an environment variable
TOKEN = os.getenv("TELEGRAM_API_TOKEN")

bot = telebot.TeleBot(TOKEN)

# Register handlers
register_handlers(bot)

# Run the bot
if __name__ == '__main__':
    bot.polling(none_stop=True)

