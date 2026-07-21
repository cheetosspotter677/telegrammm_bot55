import os
import uuid
from datetime import datetime
from config import PHOTO_FOLDER, MAX_NOTE_LENGTH
def create_photo_folder():
    if not os.path.exists(PHOTO_FOLDER):
        os.makedirs(PHOTO_FOLDER)

def current_date():
    return datetime.now().strftime("%d.%m.%Y")

def current_time():
    return datetime.now().strftime("%H:%M")

def current_datetime():
    return datetime.now().strftime("%d.%m.%Y %H:%M")

def generate_photo_name(user_id):
    unique = uuid.uuid4().hex
    filename = f"{user_id}_{unique}.jpg"
    return os.path.join(PHOTO_FOLDER, filename)

def note_is_valid(note):
    return len(note) <= MAX_NOTE_LENGTH

def short_text(text, length=35):
    if len(text) <= length:
        return text
    return text[:length] + '...'

def format_notes(notes):
    if len(notes) == 0:
        return "u dont have any notes rn"
    result = "ur notes\n\n"
    for number, note in enumerate(notes, start=1):
        result += f"{number}. {note}\n"
    return result

def format_search(notes):
    if len(notes) == 0:
        return "theres nothing rn"
    result = "heres the result!\n\n"
    for number, note in enumerate(notes, start=1):
        result += f"{number}. {note}\n"
        return result

def format_statistics(stat):
    return (
        " statistics\n\n"
        f" name: {stat['name']}\n"
        f" notes: {stat['notes']}\n"
        f" photos: {stat['photos']}\n"
    )
def greeting(name):
    hour = datetime.now().hour
    if hour < 12:
        hello  = " mornin'"
    elif hour < 18:
        hello = " afternoon"
    else:
        hello = " evening"
    return f"{hello}, {name}!"

def about_bot():
    return (
        "🤖 telegram assistant\n\n"
        "version: 1.0\n"
        "programming language: Python\n"
        "library: python-telegram-bot\n"
        "data base: JSON\n\n"
        "educational project.\n"
    )

def setup_project():
    create_photo_folder()