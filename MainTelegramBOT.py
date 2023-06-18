#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /search to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the bot.

Url:
https://t.me/noncapiscocosastasuccedendobot
"""

# from telegram import __version__ as TG_VER
# try:
#     from telegram import __version_info__
# except ImportError:
#     __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]
# if __version_info__ < (20, 0, 0, "alpha", 1):
#     raise RuntimeError(
#         f"This example is not compatible with your current PTB version {TG_VER}. To view the "
#         f"{TG_VER} version of this example, "
#         f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
#     )

import json
import logging
from Classes.TorrentHandlers import *
from Classes.TorrentSelection import *
from Classes.TelegramDownload import *
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler,
    CallbackContext
)


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
settings = json.load(open("settings.json"))


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Hi! I'm Major Tom.")
    await update.message.reply_text(f"""For torrent search type /search\nFor download by Telegram type /dwtelegram""")


async def error(update: Update, context: CallbackContext):
    """Log Errors caused by Updates."""
    try:
        logger.warning('Update "%s" caused error "%s"', update, context.error)
        message = f'Error:\n{context.error}'
        if (update.message):
            await update.message.reply_text(message)
        if (update.callback_query):
            await update.callback_query.message.reply_text(message)
    except Exception as e:
        logger.error(e)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(
        settings['botToken']).base_url(
            settings['baseUrl']
    ).base_file_url(
        settings['base_file_url']
    ).read_timeout(
        settings['read_timeout']
    ).build()
    # Add conversation handler with the states CATEGORIES, PHOTO, LOCATION, KEYWORD
    conv_handler1 = ConversationHandler(
        entry_points=[CommandHandler("search", start_torrent)],
        states={
            CATEGORIES: [
                CallbackQueryHandler(categories),
                CommandHandler("skip", skip_categories),
            ],
            SUBCATEGORIES: [
                CallbackQueryHandler(subcategories),
                CommandHandler("skip", skip_subcategories),
            ],
            KEYWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, keyword),
                CallbackQueryHandler(keyword)
            ],
            CHOOSE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, choose),
                CallbackQueryHandler(choose)
            ],
            CONFIRM: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, confirm),
                CallbackQueryHandler(confirm)
            ]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    conv_handler2 = ConversationHandler(
        entry_points=[CommandHandler('dwtelegram', dw_telegram)],
        states={
            SPECIFY: [
                CommandHandler('ls', ls_dir_command),
                CommandHandler('space', space_on_specify),
                CommandHandler('next', next_command),
                CallbackQueryHandler(dir_specify),
                MessageHandler(filters.TEXT, dir_specify),
            ],
            DOC: [
                CommandHandler('end', end_telegram_download),
                CommandHandler('prev', dw_telegram),
                CommandHandler('space', space_on_doc),
                CommandHandler('dwList', dw_list),
                CommandHandler('setsNew', set_to_new),
                MessageHandler(filters.ALL, append_download),
            ],
        },
        fallbacks=[CommandHandler('end', end_telegram_download)],
    )

    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    application.add_handler(CommandHandler("space", space))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("pauseall", pauseall))
    application.add_handler(CommandHandler("resumeall", resumeall))
    application.add_handler(CommandHandler("forceall", forceall))

    # log all errors
    application.add_error_handler(error)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

# start - Start the conversation
# search - New torrent search
# cancel - Stop the conversation
# status - Check local torrents
# pauseall - Pause all torrents
# resumeall - Resume all torrents
# forceall - Force start all torrents
# dwtelegram - For download file with TG
# space - For check disks space
# next - For send file
# prev - For select directory
# dwList - For show list of files and download status
# end - For exit from download TG