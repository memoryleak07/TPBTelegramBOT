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
from QBitTorrent import QBitTorrent
import time
import re
import logging
from turtle import forward
from telegram import ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
    CommandHandler,
    CallbackQueryHandler
)
from QBitTorrent import QBitTorrent
from StoreInformation import StoreInformation
from ThePirateBay import ThePirateBay

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CATEGORIES, SUBCATEGORIES, KEYWORD, CHOOSE, CONFIRM = range(5)

foundtorrents = []
magnetlinks = []
urls = []
#input_field_placeholder="e.g.  *artist* *album* *movie*" / e.g.  3 , 5, 12


async def start(update: Update, context: ContextTypes.context) -> int:
    """Starts the conversation and asks the user about categories."""
    id = update.message.chat_id
    logger.info("Chat %s enter START state", id)

    inline_button = pirate.GetInlineAllCategories()

    await update.effective_message.reply_text("Hi! I'm Bot.")
    await update.effective_message.reply_text("Select a category or /skip.")
    await update.effective_message.reply_text("Send /cancel /start to restart conversation.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_button, resize_keyboard=True)
    )

    return CATEGORIES


async def categories(update: Update, context: ContextTypes.context) -> int:
    """Stores the selected categories and asks for subcategory."""
    user = update.callback_query
    id = user.message.chat_id
    logger.info("Chat %s enter CATEGORIES state", id)
    logger.info("Chat %s category is: %s", id, user.data )

    store.store_id_information(id, "", "", "", "", user.data, "", "")

    if user.data == "ALL":
        await update.callback_query.message.reply_text("Ok!")
        await update.callback_query.message.reply_text("Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove()
        )

        return KEYWORD

    inline_button  = pirate.GetInlineSubCategories(user.data)

    await update.callback_query.message.reply_text("Select a subcategory or /skip: ",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_button, resize_keyboard=True)
    )

    return SUBCATEGORIES


async def skip_categories(update: Update, context: ContextTypes.context) -> int:
    """Skips the categories and asks for keyword."""
    id = update.message.chat_id

    store.store_id_information(id, "", "", "", "", "", "", "")

    logger.info("Chat %s did not set a category.", id)
    await update.effective_message.reply_text("Ok!")
    await update.effective_message.reply_text("Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove()
    )

    return KEYWORD


async def subcategories(update: Update, context: ContextTypes.context) -> int:
    """Stores the selected categories and asks for keyword."""
    user = update.callback_query
    id = user.message.chat_id

    logger.info("Chat %s enter SUBCATEGORIES state", id)
    logger.info("Chat %s subcategory is: %s", id, user.data )

    # print(getattr(getattr(CATEGORIES, "AUDIO"), user.data)
    store.store_id_information(id, "", "", "", "", "", user.data, "")

    await update.callback_query.message.reply_text("I see!")
    await update.callback_query.message.reply_text("Now, input a keyword to search..."
    )

    return KEYWORD


async def skip_subcategories(update: Update, context: ContextTypes.context) -> int:
    """Skips the categories and asks for keyword."""
    id = update.message.chat_id
    store.store_id_information(id, "", "", "", "", "", "", "")
    logger.info("Chat %s did not set a subcategory.", id)
    await update.effective_message.reply_text("Ok!")
    await update.effective_message.reply_text("Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove()
    )

    return KEYWORD


async def keyword(update: Update, context: ContextTypes.context) -> int:
    """Stores the keyword to search and ends the conversation."""
    user = update.callback_query

    try:
        search = user.data
        id = user.message.chat_id
    except:
        search = update.message.text
        id = update.message.chat_id

    logger.info("Chat %s enter KEYWORD state", id)
    logger.info("Chat %s keyword is: %s", id, search)

    offset = 1
    # If user press "Stop":
    if search == 'Stop':
        await update.effective_message.reply_text("OK!")
        await update.effective_message.reply_text("Write wich you want to download.")
        await update.effective_message.reply_text("Or send /cancel to stop.")
        await update.effective_message.reply_text("e.g. 5 or 5, 3, 10...",
            reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    # Else try to retrieve keyword and offset (page) from resp. If Except set page = 1, 
    try:
        offset = int(search.split('-')[2])
        search = search.split('-')[1]
    except Exception:
        offset = 1
        previoussearch = store.get_id_information(id, 3, "")
        # If user search a new keyword while is in wrong state
        if (search != previoussearch) & (previoussearch != ""):
            logger.warning("Chat %s did not select a valid input (%s).", id, str(search))
            await update.effective_message.reply_text("Finish this before start a new search, ok? Or /cancel to stop.")
            await update.effective_message.reply_text("Write wich you want to download.")
            await update.effective_message.reply_text("e.g. 5 or 5, 3, 10...",
                reply_markup=ReplyKeyboardRemove()
            )
            return CHOOSE

    # Retrive the category
    category = store.get_id_information(id, 4, "")      #globalvar[id][4]
    subcategory = store.get_id_information(id, 5, "")   #globalvar[id][5]

    if (category != "") & (subcategory != ""):
        await update.effective_message.reply_text("Searching \"{search}\" in category \"{category} - {subcategory}\"...".format(search=search, category=category, subcategory=subcategory))
    elif (category != "") & (subcategory == ""):
        await update.effective_message.reply_text("Searching \"{search}\" in category \"{category}\"...".format(search=search, category=category))
    elif category == "":
        await update.effective_message.reply_text("Searching \"{search}\" in \"ALL\" categories...".format(search=search))

    # Send pirate search command (keyword (str), page (int), category (int))
    foundtorrents, magnetlinks, urls = pirate.CustomizedSearch(search, offset, category, subcategory)
    # Store in dict search and all results
    store.store_id_information(id, foundtorrents, magnetlinks, urls, search, "", "", "")

    # Check if no torrents found return KEYWORD state
    if (len(foundtorrents)) == 0:
        if offset == 1:
            logger.info("No torrents found :-(")
            await update.effective_message.reply_text("No torrents found :-(")
            await update.effective_message.reply_text("Try input a new keyword to search...",
                reply_markup=ReplyKeyboardRemove()
            )

            store.delete_id_information(id)
            store.create_id_information(id)
                       
            return KEYWORD
        return CHOOSE

    # Else print and store the info in globalvar
    logger.info("Chat %s founds %s torrents. (page=%s)", id, len(foundtorrents), offset)
    await update.effective_message.reply_text(
        "There were {0} torrents found:".format(len(foundtorrents))
    )

    # Reply result to user all link found, 30 each step
    i = 0
    for torrent in foundtorrents:
        # torrent = [i] - Name Of The Torrent
        try:
            line = "<b>{torrent}</b> - <a href=\"{url}\">[URL]</a>".format(torrent=torrent, url=urls[i])
            await update.effective_message.reply_text(line, parse_mode="HTML", disable_web_page_preview=True)
            i = i+1
        except:
            line = line.replace("<b>", "").replace("</b>", "").replace("<a href=\"", "").replace("\">[URL]</a>", "")
            await update.effective_message.reply_text(line, disable_web_page_preview=True)

    # Check if found torrent are less than 30, so the search is finished
    if (len(foundtorrents)) < 30:
        await update.effective_message.reply_text("OK! Write wich you want to download.")
        await update.effective_message.reply_text("Or send /cancel to stop.")
        await update.effective_message.reply_text("e.g. 5 or 5, 3, 10...",
        reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    # Otherwise ask to continue (offset+1) or stop the search (Continue / Stop inline button)
    yesText = "Continue-{search}-{offset}".format(search=search,offset=str(offset+1))
    inline_button = [[
        InlineKeyboardButton(text="Next Page >", callback_data=yesText),
        InlineKeyboardButton(text="Stop", callback_data="Stop"),
    ]]

    await update.effective_message.reply_text(text="Do you want to continue search?",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=inline_button)
    )

    return KEYWORD


async def choose(update: Update, context: ContextTypes.context) -> int:
    """Select wich torrent download and call canfirm action"""
    id = update.message.chat_id
    logger.info("Chat %s enter CHOOSE state", id)
    logger.info("Chat %s choose: %s", id, update.message.text)
    # Convert user response in numeric list
    res = re.findall(r'\d+', update.message.text)
    # Check the string if not valid return CHOOSE state
    if len(res) == 0:
        logger.warning("Chat %s did not select a valid input.", id)
        await update.effective_message.reply_text("No! Input one or a list of numbers!")
        await update.effective_message.reply_text("Write wich you want to download or /cancel to stop.")
        await update.effective_message.reply_text("e.g. 5 or 5, 3, 10...",
            reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    # Reply to user all the result
    for i in res:
        try:
            resp = str(store.get_id_information(id, 0, int(i)))
            url = str(store.get_id_information(id, 2, int(i)))
            line = "{resp} - {url}".format(resp=resp, url= url)
            await update.effective_message.reply_text(line)
        # Avoid user error:
        except Exception as ex:
            res.remove(i)
            logger.warning("Chat %s for input \"%s\": %s", id, str(i) , str(ex))
            await update.effective_message.reply_text("Warning! For input \"" + str(i) + "\": " + str(ex))

    # And store the items to download in the dictionary if lenght NOT zero
    if len(res) == 0:
        logger.warning("Chat %s did not select a valid input.", id)
        await update.effective_message.reply_text("Write wich you want do download or /cancel to stop.")
        await update.effective_message.reply_text("e.g. 5 or 5, 3, 10...",
            reply_markup=ReplyKeyboardRemove()
        )
        return CHOOSE
        
    store.store_id_information(id, "", "", "", "", "", "", res)

    inline_button = [[
        InlineKeyboardButton(text="Yes", callback_data="Yes"),
        InlineKeyboardButton(text="No", callback_data="No"),
    ]]
    
    await update.effective_message.reply_text(text="Please confirm the selected torrent:",
        reply_markup = InlineKeyboardMarkup(inline_keyboard=inline_button)
    )

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.context) -> int:
    """Ask confirm before start download."""
    user = update.callback_query

    try:
        id = user.message.chat_id
        search = user.data
    except:
        id = update.message.chat_id
        search = update.message.text

    logger.info("Chat %s enter CONFIRM state", id)

    if (search != "Yes") and (search != "No"):
        logger.warning("Chat %s did not select a valid input (%s): (Yes or No)", id, str(search))
        await update.effective_message.reply_text("Error! Just select \"Yes\" or \"No\""
        )

        return CONFIRM

    logger.info("Chat %s selected: %s", id, search)

    # If user press No return to KEYWORD
    if search == "No":
        await update.effective_message.reply_text("Ok! Let's start again!")
        await update.effective_message.reply_text("Send /cancel to stop.")
        await update.effective_message.reply_text("Or input a keyword to search in ALL categories:",
            reply_markup=ReplyKeyboardRemove(),
        )

        store.delete_id_information(id)
        store.create_id_information(id)

        return KEYWORD

    # Otherwise send magnet links to the downloader bot
    elif search == "Yes":
        sel = (store.get_id_information(id, 6, ""))
        magnetlinks = (store.get_id_information(id, 1, ""))
        todownload = []
        try:
            for i in sel:
                todownload.append(magnetlinks[int(i)])
        except Exception as ex:
            logger.warning("Chat %s for input \"%s\": %s", id, search, str(ex))
            await update.effective_message.reply_text("Warning! For input \"" + search + "\": "  + str(ex) 
            )
        
    qbit.DownloadTorrentLink(todownload)
    store.delete_id_information(id)

    await update.effective_message.reply_text("My job is done! I hope it was helpful.")
    await update.effective_message.reply_text("You can send /status to check current downloads information.",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END



async def status(update: Update, context: ContextTypes.context) -> int:
    """Starts the conversation and asks the user about categories."""
    id = update.message.chat_id
    logger.info("Chat %s enter STATUS state", id)
    localdownloads = qbit.GetTorrentInformation()
    for torrent in localdownloads:
        await update.effective_message.reply_text(torrent)

    return ConversationHandler.END





async def cancel(update: Update, context: ContextTypes.context) -> int:
    """Cancels and ends the conversation."""
    id = update.message.chat_id
    logger.info("Chat %s enter CANCEL state", id)
    store.delete_id_information(id)
    await update.effective_message.reply_text("Bye! I hope we can talk again some day.")
    await update.effective_message.reply_text("Send /start to start over.",
        reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5792075504:AAHlzyBukL4HDqY5T8OIX1Y-bC4mPgq0pqo").build()    
    # Add conversation handler with the states CATEGORIES, PHOTO, LOCATION, KEYWORD
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORIES:[
                CallbackQueryHandler(categories),
                CommandHandler("skip", skip_categories),
            ],
            SUBCATEGORIES:[
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
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("status", status))
    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    pirate = ThePirateBay()
    store = StoreInformation()
    qbit = QBitTorrent()
    main()