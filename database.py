"""
database.py

Робота з JSON базою даних.
"""

import json
import os

from config import DATABASE_FILE


def create_database():

    if not os.path.exists(DATABASE_FILE):

        with open(DATABASE_FILE, "w", encoding="utf-8") as file:

            json.dump({}, file, indent=4, ensure_ascii=False)



def load_database():

    create_database()

    with open(DATABASE_FILE, "r", encoding="utf-8") as file:

        return json.load(file)



def save_database(database):

    with open(DATABASE_FILE, "w", encoding="utf-8") as file:

        json.dump(
            database,
            file,
            indent=4,
            ensure_ascii=False
        )



def create_user(user_id, name):

    database = load_database()

    user_id = str(user_id)

    if user_id not in database:

        database[user_id] = {

            "name": name,

            "notes": [],

            "photos": []

        }

        save_database(database)


def user_exists(user_id):

    database = load_database()

    return str(user_id) in database


def get_user(user_id):

    database = load_database()

    return database.get(str(user_id))



def get_name(user_id):

    user = get_user(user_id)

    if user:

        return user["name"]

    return None


def set_name(user_id, new_name):

    database = load_database()

    database[str(user_id)]["name"] = new_name

    save_database(database)



def add_note(user_id, note):

    database = load_database()

    database[str(user_id)]["notes"].append(note)

    save_database(database)


def get_notes(user_id):

    database = load_database()

    return database[str(user_id)]["notes"]


def update_note(user_id, index, new_note):

    database = load_database()

    notes = database[str(user_id)]["notes"]

    if 0 <= index < len(notes):

        notes[index] = new_note

        save_database(database)

        return True

    return False


def delete_note(user_id, index):

    database = load_database()

    notes = database[str(user_id)]["notes"]

    if 0 <= index < len(notes):

        notes.pop(index)

        save_database(database)

        return True

    return False


def clear_notes(user_id):

    database = load_database()

    database[str(user_id)]["notes"] = []

    save_database(database)


def search_notes(user_id, text):

    database = load_database()

    notes = database[str(user_id)]["notes"]

    result = []

    for note in notes:

        if text.lower() in note.lower():

            result.append(note)

    return result



def add_photo(user_id, path):

    database = load_database()

    database[str(user_id)]["photos"].append(path)

    save_database(database)


def get_photos(user_id):

    database = load_database()

    return database[str(user_id)]["photos"]


def delete_photo(user_id, index):

    database = load_database()

    photos = database[str(user_id)]["photos"]

    if 0 <= index < len(photos):

        photos.pop(index)

        save_database(database)

        return True

    return False


def clear_photos(user_id):

    database = load_database()

    database[str(user_id)]["photos"] = []

    save_database(database)



def get_statistics(user_id):

    database = load_database()

    user = database[str(user_id)]

    return {

        "name": user["name"],

        "notes": len(user["notes"]),

        "photos": len(user["photos"])

    }



def delete_user(user_id):

    database = load_database()

    user_id = str(user_id)

    if user_id in database:

        del database[user_id]

        save_database(database)



def get_all_users():

    return load_database()