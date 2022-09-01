#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
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

from html.parser import HTMLParser
import re
import time
import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update, InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Import my class
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
globalvar = ["", "", "", ""]



async def start(update: Update, context: ContextTypes.context) -> int:
    """Starts the conversation and asks the user about categories."""
    reply_keyboard = [["Music", "Movie", "Other"]]
    await update.message.reply_text(
        "Hi! I'm Bot.\n"
        "Please select a category or /skip.\n"
        "Send /cancel /start to restart conversation.\n\n  ",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Send /skip to go haead."
        ),
    )

    return CATEGORIES


async def skip_categories(update: Update, context: ContextTypes.context) -> int:
    """Skips the categories and asks for keyword."""
    user = update.message.from_user
    logger.info("User %s did not set a category.", user.first_name)
    await update.message.reply_text(
        "Ok! Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove(),
    )

    return KEYWORD


async def categories(update: Update, context: ContextTypes.context) -> int:
    """Stores the selected categories and asks for keyword."""
    user = update.message.from_user
    logger.info("Category of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "I see! Now, input a keyword to search...",
        reply_markup=ReplyKeyboardRemove(),
    )

    return KEYWORD


async def keyword(update: Update, context: ContextTypes.context) -> int:
    """Stores the keyword to search and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s keyword is: %s", user.first_name, update.message.text)
    # Call function return list, iterate over list to printe single msg

    offset = 1
    search = update.message.text
    if search == '@noncapiscocosastasuccedendobot Stop':
        await update.message.reply_text('OK! Write wich want to download.', 
        reply_markup=ReplyKeyboardRemove()
        )
        return CHOOSE
    try:
        search = update.message.text.split('-')[1]
        offset = int(update.message.text.split('-')[2])
    except Exception as ex:
        offset = 1

    foundtorrents, magnetlinks, urls = pirate.CustomizedSearch(search, offset, 104)
    store_information(foundtorrents, magnetlinks, urls, "")

    # Check if no torrents found retunr KEYWORD state
    if (len(foundtorrents)) == 0:
        if offset == 1:
            logger.info("No torrents found :-(")
            await update.message.reply_text(
                'No torrents found :-(\nTry input a new keyword to search...'
            )
            return KEYWORD
        return CHOOSE
            
    # Else print and store the info in globalvar
    logger.info("There were %s torrents found.", len(foundtorrents))
    await update.message.reply_text(
        'There were {0} torrents found.'.format(len(foundtorrents))
    )
    # Reply to user all link found, 30 each step
    yesText = "Continue-{search}-{offset}".format(search=search,offset=str(offset+1))
    inline_button = [[
        InlineKeyboardButton(text="Continue", switch_inline_query_current_chat=yesText),
        InlineKeyboardButton(text="Stop", switch_inline_query_current_chat="Stop"),
    ]]
    reply = InlineKeyboardMarkup(inline_keyboard=inline_button)

    # chunk_size = 30
    # chunked_list = [globalvar[0][i:i+chunk_size] for i in range(0, len(globalvar[0]), chunk_size)]
    # Reply result
    for torrent in foundtorrents:
        await update.message.reply_text(torrent)

    if (len(foundtorrents)) < 30:
        await update.message.reply_text('OK! Write wich want to download.', 
        reply_markup=ReplyKeyboardRemove()
        )
        return CHOOSE
        # offset += 1
        # if offset == limit:
        #     await update.message.reply_text(text="Vuoi continuare????:\n", reply_markup=reply) 
        #     ask =  await stop_continue(update, context)
        #     if ask == "@noncapiscocosastasuccedendobot Stop":
        #         break
        #     elif ask == "@noncapiscocosastasuccedendobot Continue":
        #         print("continue")
        #         limit += 30

    # print(chunked_list)

    # for torrent in foundtorrents[:current, :current+limit]:
    # for index in range(current, current+limit):
    #     await update.message.reply_text(foundtorrents[index])
        # offset += 1
        # if offset < maxoffset:
        #     await update.message.reply_text(text="Continue?:\n", reply_markup=reply)
        #     ask = await stop_continue(update, context)
        #     if ask == "@noncapiscocosastasuccedendobot Stop":
        #         # return CHOOSE
        #         break
        #     elif ask == "@noncapiscocosastasuccedendobot Continue":
        #         limit += 5
        #         current = limit
        #     offset += 1
        # break
        # if offset == limit:
        #     await update.message.reply_text(text="Continue?:\n", reply_markup=reply)
        #     time.sleep(10)
        #     user = update.message.from_user
        #     logger.info("User %s selected: %s", user.first_name, update.message.text)
        #     #aggiungere controllo regex
        #     if update.message.text == "@noncapiscocosastasuccedendobot Stop":
        #         break
        #     limit += 30

    # for foundtorrents in range(1, limit):
    #     await update.message.reply_text(foundtorrents)



    # await update.message.reply_text('OK! Write wich want to download.', 
    #     reply_markup=ReplyKeyboardRemove()
    # )
    await update.message.reply_text(text="Vuoi continuare????:\n", reply_markup=reply) 

    # return CHOOSE
    return KEYWORD


async def stop_continue(update: Update, context: ContextTypes.context) -> int:
    """Ask confirm before start download."""
    user = update.message.from_user
    logger.info("User %s selected: %s", user.first_name, update.message.text)
    return update.message.text


async def choose(update: Update, context: ContextTypes.context) -> int:
    """Select wich torrent download and call canfirm action"""
    user = update.message.from_user
    logger.info("User %s choose: %s", user.first_name, update.message.text)
    # print(update.message.text) #### < RISPOSTA DEL CLIENTE
    # Conver user response in numeric list
    res = re.findall(r'\d+', update.message.text)
    # Check the string if not valid return in CHOOSSE state
    if len(res) == 0:
        await update.message.reply_text(
            "Error ! Insert a list of numbers! Es. 2 or 2, 9, 3...\n"
            "Write wich want to download.",
            reply_markup=ReplyKeyboardRemove()
        )
        
        return CHOOSE
    # Else store the item to download in a list
    store_information("", "", "", res)
    
    for i in res:
        try:
            print("{res} - {url}".format(res=globalvar[0][int(i)], url= globalvar[2][int(i)]))
            await update.message.reply_text(
                "{res} - {url}".format(res=globalvar[0][int(i)], url= globalvar[2][int(i)]),
            )
        except Exception as ex:
            await update.message.reply_text(str(ex))

    inline_button = [[
        InlineKeyboardButton(text="Yes", switch_inline_query_current_chat="Yes"),
        InlineKeyboardButton(text="No", switch_inline_query_current_chat="No"),
    ]]
    reply = InlineKeyboardMarkup(inline_keyboard=inline_button)
    #reply_keyboard = [["Yes", "No"]]
    # await update.message.reply_text(
    #     "Please confirm the selected torrent:\n",
    #     reply_markup=ReplyKeyboardMarkup(
    #     reply_keyboard, one_time_keyboard=True, input_field_placeholder="Yes or No"
    #     ),
    # )
    await update.message.reply_text(text="Please confirm the selected torrent:\n", reply_markup=reply)

    return CONFIRM


async def confirm(update: Update, context: ContextTypes.context) -> int:
    """Ask confirm before start download."""
    user = update.message.from_user
    logger.info("User %s selected: %s", user.first_name, update.message.text)
    #aggiungere controllo regex
    if update.message.text == "@noncapiscocosastasuccedendobot No":
        await update.message.reply_text(
            "Ok! Let's start again! Input a keyword to search...",
            reply_markup=ReplyKeyboardRemove(),
        )

        return KEYWORD
# async def confirm(update: Update, context: ContextTypes.context) -> int:
#     """Ask confirm before start download."""
#     user = update.message.from_user
#     logger.info("User %s selected: %s", user.first_name, update.message.text)
#     #aggiungere controllo regex
#     if update.message.text == "No":
#         await update.message.reply_text(
#             "Ok! Let's start again! Input a keyword to search...",
#             reply_markup=ReplyKeyboardRemove(),
#         )

#         return KEYWORD

    # for i in globalvar[3]:
    #     print(globalvar[0][int(i)], " - ", globalvar[2][int(i)])
    #     #await update.message.reply_text("{res}".format(res=globalvar[0][int(i)]))


    await update.message.reply_text(
        "My job is done! I hope it was helpful.\n"
        "Send /start to start over.\n\n ",
        reply_markup=ReplyKeyboardRemove(),
    )

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.context) -> int:
    """Cancels and ends the conversation."""
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


def store_information(foundtorrents, magnetlinks, urls, select):
    """Store the conversation info as a global var list."""
    global globalvar
    if (foundtorrents != "") & (magnetlinks != "") & (urls != ""):
        globalvar[0] = foundtorrents
        globalvar[1] = magnetlinks
        globalvar[2] = urls
    else:
        globalvar[3] = select



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
