"""
keyboards.py

Усі клавіатури Telegram Assistant
"""

from telegram import ReplyKeyboardMarkup


def main_keyboard():

    keyboard = [

        ["📝 new note", "📚 my notes"],

        ["📷 add photo", "🖼 gallery"],

        ["🔍 search", "📊 statistics"],

        ["👤 change name", "🗑 clear all notes"],

        ["ℹ️ abt bot"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )



def note_keyboard():

    keyboard = [

        ["📝 new note"],

        ["📚 my notes"],

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )



def photo_keyboard():

    keyboard = [

        ["📷 add photo"],

        ["🖼 gallery"],

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )



def statistics_keyboard():

    keyboard = [

        ["📊 statistics"],

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )




def search_keyboard():

    keyboard = [

        ["🔍 search"],

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )




def settings_keyboard():

    keyboard = [

        ["👤 change name"],

        ["🗑 clear all notes"],

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )




def back_keyboard():

    keyboard = [

        ["🏠 main menu"]

    ]

    return ReplyKeyboardMarkup(

        keyboard,

        resize_keyboard=True

    )