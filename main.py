import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

import config
import database
import keyboards
import states
import utils


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starting to use the bot or showing the main menu."""
    user_id = update.effective_user.id


    if database.user_exists(user_id):
        name = database.get_name(user_id)
        await update.message.reply_text(
            utils.greeting(name),
            reply_markup=keyboards.main_keyboard()
        )
        return ConversationHandler.END
    else:
        await update.message.reply_text(config.WELCOME_TEXT)
        return states.ASK_NAME


async def ask_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Obtaining a username and registration."""
    name = update.message.text.strip()
    user_id = update.effective_user.id

    database.create_user(user_id, name)

    await update.message.reply_text(
        f"nice to meet u, {name}! registration is closed.",
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancel the current action and return to the main menu."""
    await update.message.reply_text(
        "the action has been cancelled.",
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END


async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Return to the main menu upon pressing the corresponding button."""
    await update.message.reply_text(
        "u've returned to the main menu",
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END



async def handle_new_note_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request to enter a new note."""
    user_id = update.effective_user.id
    notes = database.get_notes(user_id)

    if len(notes) >= config.MAX_NOTES:
        await update.message.reply_text(
            f"❌ note limit reached ({config.MAX_NOTES}).",
            reply_markup=keyboards.main_keyboard()
        )
        return ConversationHandler.END

    await update.message.reply_text(
        "enter the text of ur note (max 1,000 characters):",
        reply_markup=keyboards.back_keyboard()
    )
    return states.ADD_NOTE


async def add_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saving the new note."""
    text = update.message.text
    user_id = update.effective_user.id

    if not utils.note_is_valid(text):
        await update.message.reply_text(
            f"❌ the note is too long. max length: {config.MAX_NOTE_LENGTH} characters. try again:",
            reply_markup=keyboards.back_keyboard()
        )
        return states.ADD_NOTE
    full_note = f"[{utils.current_datetime()}] {text}"
    database.add_note(user_id, full_note)

    await update.message.reply_text(
        "✅ note successfully added!",
        reply_markup=keyboards.note_keyboard()
    )
    return ConversationHandler.END


async def show_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show list of notes."""
    user_id = update.effective_user.id
    notes = database.get_notes(user_id)
    await update.message.reply_text(
        utils.format_notes(notes),
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END


async def clear_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Clear all notes."""
    user_id = update.effective_user.id
    database.clear_notes(user_id)
    await update.message.reply_text(
        "🗑 all ur notes have been deleted.",
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END



async def handle_search_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Search keyword query."""
    await update.message.reply_text(
        "enter text to search through the notes:",
        reply_markup=keyboards.back_keyboard()
    )
    return states.SEARCH_NOTE


async def search_notes(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Search for notes by keyword."""
    text = update.message.text
    user_id = update.effective_user.id
    results = database.search_notes(user_id, text)

    await update.message.reply_text(
        utils.format_search(results),
        reply_markup=keyboards.search_keyboard()
    )
    return ConversationHandler.END



async def handle_add_photo_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request to send a photo."""
    await update.message.reply_text(
        "send me the photo as a photo (and not as a file):",
        reply_markup=keyboards.back_keyboard()
    )
    return states.ADD_PHOTO


async def add_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Saving the photo."""
    user_id = update.effective_user.id
    photo_file = await update.message.photo[-1].get_file()

    photo_path = utils.generate_photo_name(user_id)
    await photo_file.download_to_drive(photo_path)

    database.add_photo(user_id, photo_path)

    await update.message.reply_text(
        "✅ photo successfully added!",
        reply_markup=keyboards.photo_keyboard()
    )
    return ConversationHandler.END


async def show_gallery(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Viewing saved photos."""
    user_id = update.effective_user.id
    photos = database.get_photos(user_id)

    if not photos:
        await update.message.reply_text(
            "📭 u dont have any photos in ur gallery.",
            reply_markup=keyboards.main_keyboard()
        )
        return ConversationHandler.END

    await update.message.reply_text("🖼 ur gallery:")
    for path in photos:
        try:
            with open(path, 'rb') as photo:
                await update.message.reply_photo(photo)
        except Exception as e:
            logger.error(f"error sending photo{path}: {e}")

    return ConversationHandler.END



async def show_statistics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Displaying user statistics."""
    user_id = update.effective_user.id
    stat = database.get_statistics(user_id)
    await update.message.reply_text(
        utils.format_statistics(stat),
        reply_markup=keyboards.statistics_keyboard()
    )
    return ConversationHandler.END


async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Display bot information."""
    await update.message.reply_text(
        utils.about_bot(),
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END


async def handle_change_name_request(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Request a new name."""
    await update.message.reply_text(
        "enter ur new name:",
        reply_markup=keyboards.back_keyboard()
    )
    return states.CHANGE_NAME


async def change_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Change username."""
    new_name = update.message.text.strip()
    user_id = update.effective_user.id

    database.set_name(user_id, new_name)

    await update.message.reply_text(
        f"👤 ur name has been successfully changed to: {new_name}",
        reply_markup=keyboards.main_keyboard()
    )
    return ConversationHandler.END


def main() -> None:
    """Launching the bot."""
    utils.setup_project()

    if config.TOKEN == "8994077418:AAFuxU-prb5M-PVEJngoBrE8D-Rdverbf5c":
        print("Error: please specify your unique Bot Token in the config.py file.")
        return

    application = Application.builder().token(config.TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", start),
            MessageHandler(filters.Regex("^📝 new note$"), handle_new_note_request),
            MessageHandler(filters.Regex("^📷 add a photo$"), handle_add_photo_request),
            MessageHandler(filters.Regex("^🔍 search$"), handle_search_request),
            MessageHandler(filters.Regex("^👤 change a name$"), handle_change_name_request),
        ],
        states={
            states.ASK_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, ask_name)
            ],
            states.ADD_NOTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^🏠 main menu$"), add_note)
            ],
            states.SEARCH_NOTE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^🏠 main menu$"), search_notes)
            ],
            states.ADD_PHOTO: [
                MessageHandler(filters.PHOTO, add_photo)
            ],
            states.CHANGE_NAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & ~filters.Regex("^🏠 main menu$"), change_name)
            ]
        },
        fallbacks=[
            MessageHandler(filters.Regex("^🏠 main menu$"), show_main_menu),
            CommandHandler("cancel", cancel)
        ],
        allow_reentry=True
    )

    application.add_handler(MessageHandler(filters.Regex("^📚 my notes$"), show_notes))
    application.add_handler(MessageHandler(filters.Regex("^🗑 clear all notes$"), clear_notes))
    application.add_handler(MessageHandler(filters.Regex("^🖼 gallery$"), show_gallery))
    application.add_handler(MessageHandler(filters.Regex("^📊 statistics$"), show_statistics))
    application.add_handler(MessageHandler(filters.Regex("^ℹ️ abt bot$"), show_about))
    application.add_handler(MessageHandler(filters.Regex("^🏠 main menu$"), show_main_menu))

    application.add_handler(conv_handler)

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()