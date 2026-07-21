"""
config.py
Налаштування Telegram Assistant
"""
import os
TOKEN = os.getenv("TOKEN")
DATABASE_FILE = "database.json"
PHOTO_FOLDER = "photos"
MAX_NOTE_LENGTH = 1000
MAX_NOTES = 100
BOT_NAME = "Bot for Divas 💜 💛"
WELCOME_TEXT = (
    "🤖 hi! im ur telegram assistant \n\n"
    "hi my Diva!\n"
    "i'll help u w:\n\n"
    "📝 add ur notes\n"
    "📷 add ur photos\n"
    "📊 look for statistic \n\n"
    "lets get meet each other!\n"
    "whats ur name???????;3"
)