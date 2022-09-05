#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Send /start to initiate the conversation.
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

import re
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from testThePirateBay import ThePirateBay

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CATEGORIES, KEYWORD, CHOOSE, CONFIRM = range(4)

foundtorrents = []
magnetlinks = []
urls = []
globalvar = ["", "", "", "", ""]

#input_field_placeholder="e.g: *artist* *album* *movie*" / e.g: 3 , 5, 12

async def start(update: Update, context: ContextTypes.context) -> int:
    """Starts the conversation and asks the user about categories."""
    delete_information()
    logger.info("START state")
    reply_keyboard = [["Music", "Movie", "Other"]]
    await update.message.reply_text("Hi! I'm Bot.\n")
    await update.message.reply_text(
        "Select a category or /skip.\n"
        "Send /cancel /start to restart conversation.\n\n",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Send /skip to go haead."
        ),
    )

    return CATEGORIES


async def categories(update: Update, context: ContextTypes.context) -> int:
    """Stores the selected categories and asks for keyword."""
    logger.info("CATEGORIES state")
    user = update.message.from_user
    logger.info("Category of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove()
    )

    return KEYWORD
# async def categories(update: Update, context: ContextTypes.context) -> int:
#     """Stores the selected categories and asks for keyword."""
#     logger.info("CATEGORIES state")
#     user = update.message.from_user
#     logger.info("Category of %s: %s", user.first_name, update.message.text)
#     await update.message.reply_text(
#         "I see! Now, input a keyword to search...",
#         reply_markup=ReplyKeyboardRemove(),
#     )

#     return KEYWORD

async def skip_categories(update: Update, context: ContextTypes.context) -> int:
    """Skips the categories and asks for keyword."""
    logger.info("SKIP state")
    user = update.message.from_user
    logger.info("User %s did not set a category.", user.first_name)
    await update.message.reply_text(
        "Ok! Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove()
    )

    return KEYWORD


async def keyword(update: Update, context: ContextTypes.context) -> int:
    """Stores the keyword to search and ends the conversation."""
    logger.info("KEYWORD state")
    user = update.message.from_user
    logger.info("User %s keyword is: %s", user.first_name, update.message.text)

    offset = 1
    search = update.message.text
    # If user press "Stop":
    if search == '@noncapiscocosastasuccedendobot Stop':
        await update.message.reply_text("OK! Write wich want to download.")
        await update.message.reply_text("Or send /cancel to restart.",
        reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    # Else try to retrieve keyword and offset (page) from resp. If Except set page = 1, 
    try:
        search = update.message.text.split('-')[1]
        offset = int(update.message.text.split('-')[2])
    except Exception:
        offset = 1

        # If user search a new keyword while is in wrong state
        if (search != globalvar[3]) & (globalvar[3] != ""):
            await update.message.reply_text("Finish this before start a new search.")
            await update.message.reply_text("OK? Write wich want to download or /cancel to stop",
            reply_markup=ReplyKeyboardRemove()
            )
            return CHOOSE

    # Send pirate command (keyword (str), page (int), category (int))
    foundtorrents, magnetlinks, urls = pirate.CustomizedSearch(search, offset, 104)
    # Store in global list the -torrents-magnet-url found, -sel blank.
    store_information(foundtorrents, magnetlinks, urls, search, "")

    # Check if no torrents found return KEYWORD state
    if (len(foundtorrents)) == 0:
        if offset == 1:
            logger.info("No torrents found :-(")
            await update.message.reply_text(
                "No torrents found :-(\nTry input a new keyword to search...",
                reply_markup=ReplyKeyboardRemove()
            )
            return KEYWORD
        return CHOOSE

    # Else print and store the info in globalvar
    logger.info("There were %s torrents found.", len(foundtorrents))
    await update.message.reply_text(
        "There were {0} torrents found:".format(len(foundtorrents))
    )
    # Reply to user all link found, 30 each step
    yesText = "Continue-{search}-{offset}".format(search=search,offset=str(offset+1))
    inline_button = [[
        InlineKeyboardButton(text="Continue", switch_inline_query_current_chat=yesText),
        InlineKeyboardButton(text="Stop", switch_inline_query_current_chat="Stop"),
    ]]
    reply = InlineKeyboardMarkup(inline_keyboard=inline_button)

    # Reply result (chunk_size = 30)
    for torrent in foundtorrents:
        await update.message.reply_text(torrent)

    # Check if found torrent are less than 30, so the search is finished
    if (len(foundtorrents)) < 30:
        await update.message.reply_text("OK! Write wich want to download.")
        await update.message.reply_text("Or send /cancel to restart.",
        reply_markup=ReplyKeyboardRemove()
        )
        return CHOOSE
    
    # Otherwise ask to continue (page+1) or stop the search (Continue / Stop inline button)
    await update.message.reply_text(text="Do you want to continue search?:\n", reply_markup=reply)

    return KEYWORD


async def choose(update: Update, context: ContextTypes.context) -> int:
    """Select wich torrent download and call canfirm action"""
    logger.info("CHOOSE state")
    user = update.message.from_user
    logger.info("User %s choose: %s", user.first_name, update.message.text)
    # print(update.message.text) #### < RISPOSTA DEL CLIENTE
    # Convert user response in numeric list
    res = re.findall(r'\d+', update.message.text)
    # Check the string if not valid return CHOOSE state
    if len(res) == 0:
        await update.message.reply_text("No! Input one or a list of numbers!")
        await update.message.reply_text("Write wich you want to download or /cancel to stop.",
            reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    # Reply all the result
    for i in res:
        try:
            print("{res} - {url}".format(res=globalvar[0][int(i)], url= globalvar[2][int(i)]))
            await update.message.reply_text(
                "{res} - {url}".format(res=globalvar[0][int(i)], url= globalvar[2][int(i)]),
            )
        except Exception as ex:
            await update.message.reply_text("No! " + str(ex))
            await update.message.reply_text("Write wich you want do download or /cancel to stop.",
                reply_markup=ReplyKeyboardRemove()
            )

            return CHOOSE

    # Else store the items to download in a list
    store_information("", "", "", "", res)

    inline_button = [[
        InlineKeyboardButton(text="Yes", switch_inline_query_current_chat="Yes"),
        InlineKeyboardButton(text="No", switch_inline_query_current_chat="No"),
    ]]
    reply = InlineKeyboardMarkup(inline_keyboard=inline_button)

    await update.message.reply_text(text="Please confirm the selected torrent:\n", reply_markup=reply)

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.context) -> int:
    """Ask confirm before start download."""
    logger.info("CONFIRM state")
    user = update.message.from_user
    logger.info("User %s selected: %s", user.first_name, update.message.text)
    #aggiungere controllo regex
    if update.message.text == "@noncapiscocosastasuccedendobot No":
        await update.message.reply_text("Ok! Let's start again!")
        await update.message.reply_text("Input a keyword to search...",
            reply_markup=ReplyKeyboardRemove(),
        )

        delete_information()

        return KEYWORD

    await update.message.reply_text("My job is done! I hope it was helpful.")
    await update.message.reply_text("Send /start to start over.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.context) -> int:
    """Cancels and ends the conversation."""
    delete_information()
    logger.info("CANCEL state")
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day."
        "Send /start to start over.\n\n ",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


# def test():
#     #categories = pirate.PrintCategories()
#     # print(categories[6])
#     # pirate.QuickSearch("pink floyd flac")
#     keyword = "nirvana"
#     foundtorrents = pirate.CustomizedSearch(keyword, 104)
#     return foundtorrents


def store_information(foundtorrents, magnetlinks, urls, search, select):
    """Store the conversation info as a global var list."""
    logger.info("Calling store_information()")
    global globalvar
    if (foundtorrents != "") & (magnetlinks != "") & (urls != "") & (search != ""):
        if (globalvar[0] == "") & (globalvar[0] == "") & (globalvar[0] == ""):
            globalvar[0] = foundtorrents
            globalvar[1] = magnetlinks
            globalvar[2] = urls
            globalvar[3] = search
        elif (globalvar[0] != "") &  (globalvar[0] != "") & (globalvar[0] != ""):
            globalvar[0] += foundtorrents
            globalvar[1] += magnetlinks
            globalvar[2] += urls
    else:
        globalvar[4] = select


def delete_information():
        logger.info("Calling delete_information()")
        global globalvar
        del globalvar
        globalvar = ["", "", "", "", ""]


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5792075504:AAHlzyBukL4HDqY5T8OIX1Y-bC4mPgq0pqo").build()    
    # Add conversation handler with the states CATEGORIES, PHOTO, LOCATION, KEYWORD
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORIES: [
                MessageHandler(filters.Regex("^(Music|Movie|Other)$"), categories),
                CommandHandler("skip", skip_categories),
            ],
            KEYWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, keyword)],
            CHOOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose)],
            CONFIRM: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    # main()
    pirate = ThePirateBay()
    main()


# from testThePirateBay import CATEGORIES
# pirate = ThePirateBay()
# CATGROUP = ["ALL","AUDIO","VIDEO","APPLICATIONS","GAMES","PORN","OTHER"]
# result = getattr(CATEGORIES, "AUDIO")
# print(result)
# result = (getattr(getattr(CATEGORIES, "AUDIO"), "ALL"))
# print(result)
# print(CATEGORIES.AUDIO.__dict__.keys())
# print(vars(CATEGORIES))