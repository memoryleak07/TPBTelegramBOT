import logging
from QBitTorrent import QBitTorrent
from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


async def status(update: Update, context: ContextTypes.context) -> int:
    """Check the status of the local downloads"""
    id = update.message.chat_id
    logger.info("Chat %s enter STATUS state", id)

    try:
        qbit = QBitTorrent()
        downloading = qbit.ReplyUserLocalsTorrentInformation("downloading")
        if len(downloading) != 0:
            await update.effective_message.reply_text("In progress:")
            for torrent in downloading:
                await update.effective_message.reply_text(torrent)
        
        completed = qbit.ReplyUserLocalsTorrentInformation("completed")
        if len(completed) != 0:
            await update.effective_message.reply_text("Download completed:")
            for torrent in completed:
                await update.effective_message.reply_text(torrent)
        
        if (len(downloading) == 0) and (len(completed) == 0):
            await update.effective_message.reply_text("There are no torrent")

    except Exception as ex:
        logger.error("Chat %s: %s", id, (str(ex)))
        await update.effective_message.reply_text(str(ex))

    return ConversationHandler.END


async def pauseall(update: Update, context: ContextTypes.context) -> int:
    """Pause all local downloads"""
    id = update.message.chat_id
    logger.info("Chat %s enter PAUSE ALL state", id)
    try:
        qbit = QBitTorrent()
        qbit.PauseAll()
        await update.effective_message.reply_text("Ok job done!")
    except Exception as ex:
        logger.error("Chat %s: %s", id, (str(ex)))
        await update.effective_message.reply_text(str(ex))

    return ConversationHandler.END


async def resumeall(update: Update, context: ContextTypes.context) -> int:
    """Resume all local downloads"""
    id = update.message.chat_id
    logger.info("Chat %s enter RESUME ALL state", id)
    try:
        qbit = QBitTorrent()
        qbit.ResumeAll()
        await update.effective_message.reply_text("Ok job done!")
    except Exception as ex:
        logger.error("Chat %s: %s", id, (str(ex)))
        await update.effective_message.reply_text(str(ex))

    return ConversationHandler.END


async def forceall(update: Update, context: ContextTypes.context) -> int:
    """Pause all local downloads"""
    id = update.message.chat_id
    logger.info("Chat %s enter FORCE ALL state", id)
    try:
        qbit = QBitTorrent()
        qbit.ForceAll()
        await update.effective_message.reply_text("Ok job done!")
    except Exception as ex:
        logger.error("Chat %s: %s", id, (str(ex)))
        await update.effective_message.reply_text(str(ex))

    return ConversationHandler.END


async def configure(update: Update, context: ContextTypes.context) -> int:
    """Panel of configuration"""
    id = update.message.chat_id
    logger.info("Chat %s enter CONFIGURE state", id)
    await update.effective_message.reply_text("Panel of configuration")

    return ConversationHandler.END

