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

import os
import logging
from Models.EnvKeysConsts import EnvKeysConsts

log_level = os.getenv(EnvKeysConsts.LOG_LEVEL, EnvKeysConsts.LOG_LEVEL_DEFALUT_VALUE)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=log_level
)
logger = logging.getLogger(__name__)

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

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text(f"""For torrent send /search\nfor magnet link download send /magnet\nfor telegram download send /dwtelegram""")


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
    # Verify enviroment variable
    bot_token = os.getenv(EnvKeysConsts.BOT_TOKEN)
    qbittorent_url = os.getenv(EnvKeysConsts.QBITTORENT_URL)
    if bot_token is None or qbittorent_url is None:
        raise Exception(f"Uno or more variable is null: {EnvKeysConsts.BOT_TOKEN}={bot_token} | {EnvKeysConsts.QBITTORENT_URL}={qbittorent_url}")

    base_file_url = os.getenv(EnvKeysConsts.BASE_FILE_URL, EnvKeysConsts.BASE_FILE_URL_DEFAULT_VALUE)
    base_url = os.getenv(EnvKeysConsts.API_BASE_URL, EnvKeysConsts.API_BASE_URL_DEFAULT_VALUE)
    read_timeout = os.getenv(EnvKeysConsts.READ_TIMEOUT, EnvKeysConsts.READ_TIMEOUT_DEFAULT_VALUE)
    # Create the Application and pass it your bot's token.
    application = Application.builder(
    ).token(
        bot_token
    ).base_url(
        base_url
    ).base_file_url(
        base_file_url
    ).read_timeout(
        read_timeout
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
                CommandHandler('setName', run_set_name),
                MessageHandler(filters.ALL, append_download),
            ],
            SETNAME: [
                CommandHandler('dwList', dw_list_set_name),
                CommandHandler('nameEnd', end_set_name),
                MessageHandler(filters.TEXT, set_name_to_file),
            ],
        },
        fallbacks=[CommandHandler('end', end_telegram_download)],
    )

    conv_handler3 = ConversationHandler(
        entry_points=[CommandHandler("magnet", download_magnet)],
        states={
            DOWNLOAD_MODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, download_by_link),
            ]
        },
        fallbacks=[CommandHandler("end", download_by_link_end)]
    )

    application.add_handler(conv_handler1)
    application.add_handler(conv_handler2)
    application.add_handler(conv_handler3)
    application.add_handler(CommandHandler("space", space))
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("qbittorrent", qbittorent_command))
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
