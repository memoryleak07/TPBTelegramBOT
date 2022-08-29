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
import re
import logging
from telegram import __version__ as TG_VER
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
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

# Import my class from TPB
from testThePirateBay import ThePirateBay 

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

CATEGORIES, KEYWORD, CHOOSE = range(3) 

foundtorrents = []
magnetlinks = []

async def start(update: Update, context: ContextTypes.context) -> int:
    """Starts the conversation and asks the user about categories."""
    reply_keyboard = [["Music", "Movie", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Bot.\n"
        "Send /cancel and /start to stop and restart conversation with me.\n"
        "Now please choose a category, or send /skip to go haead.\n\n",
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

#CHOOSE
async def keyword(update: Update, context: ContextTypes.context) -> int:
    """Stores the keyword to search and ends the conversation."""
    user = update.message.from_user
    logger.info("Keyword of %s is: %s", user.first_name, update.message.text)
    # Call function return list, iterate over list to printe single msg
    foundtorrents, magnetlinks = pirate.CustomizedSearch(update.message.text, 104)
    # Check if no torrents found
    if (len(foundtorrents)) == 0:
        await update.message.reply_text('No torrents found :(\nTry input a new keyword to search...')
        return KEYWORD

    await update.message.reply_text('There were {0} torrents found.'.format(len(foundtorrents)))
    for torrent in foundtorrents:
        await update.message.reply_text(torrent)


    await update.message.reply_text('Select which to download...', reply_markup=ReplyKeyboardRemove())

    return CHOOSE


#funzionava prima di aggiungere CHOOSE nel main!!!
# async def keyword(update: Update, context: ContextTypes.context) -> int:
#     """Stores the keyword to search and ends the conversation."""
#     user = update.message.from_user
#     logger.info("Keyword of %s: %s", user.first_name, update.message.text)
#     # Call function return list, iterate over list to printe single msg
#     foundtorrents = pirate.CustomizedSearch(update.message.text, 104)
#     # Display Message
#     await update.message.reply_text('There were {0} torrents found.'.format(len(foundtorrents)))

#     for torrent in foundtorrents:
#         await update.message.reply_text(torrent)

#     await update.message.reply_text("Thank you! I hope we can talk again some day.")
    
#     return ConversationHandler.END


async def choose(update: Update, context: ContextTypes.context) -> int:
    # def has_numbers(inputString):
    #     return [char for char in inputString if char.isdigit()]
    user = update.message.from_user
    logger.info("Choose of %s is: %s", user.first_name, update.message.text)
    # print(update.message.text) #### < RISPOSTA DEL CLIENTE  
    # Conver user response in numeric list
    res = re.findall(r'\d+', update.message.text)
    if len(res) == 0:
        await update.message.reply_text(
            "Error ! Insert a valid integer input! Es. 0, 1, 10 \n"
            "Select which to download...\n",
            reply_markup=ReplyKeyboardRemove()
        )

        return CHOOSE

    print(res)
    
    # for i in res: 
    #     print(foundtorrents[1])


    await update.message.reply_text(
        "Thank you! AAAAAAAAAAAAMMO I hope we can talk again some day."
        )
    return ConversationHandler.END



async def cancel(update: Update, context: ContextTypes.context) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def test():
    #categories = pirate.PrintCategories()
    # print(categories[6])
    # pirate.QuickSearch("pink floyd flac")
    keyword = "nirvana"
    foundtorrents = pirate.CustomizedSearch(keyword, 104)
    return foundtorrents


def test1(foundtorrents):
    #categories = pirate.PrintCategories()
    print("test1___________________")
    print(foundtorrents)
    # pirate.QuickSearch("pink floyd flac")
    # keyword = "nirvana"
    # foundtorrents = pirate.CustomizedSearch(keyword, 104)
    # return foundtorrents


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5792075504:AAHlzyBukL4HDqY5T8OIX1Y-bC4mPgq0pqo").build()

    # Add conversation handler with the states CATEGORIES, PHOTO, LOCATION, KEYWORD
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            CATEGORIES:[
                MessageHandler(filters.Regex("^(Music|Movie|Other)$"), categories),
                CommandHandler("skip", skip_categories),
                ],
            KEYWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, keyword)],
            CHOOSE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose)],
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