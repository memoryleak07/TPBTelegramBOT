
import logging
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

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def configure(update: Update, context: ContextTypes.context) -> int:
    """Panel of configuration"""
    id = update.message.chat_id
    logger.info("Chat %s enter CONFIGURE state", id)
    await update.effective_message.reply_text("Panel of configuration")

    return ConversationHandler.END



async def configure(update: Update, context: ContextTypes.context) -> int:
    """Panel of configuration"""
    id = update.message.chat_id
    logger.info("Chat %s enter CONFIGURE state", id)
    await update.effective_message.reply_text("Panel of configuration")

    return ConversationHandler.END