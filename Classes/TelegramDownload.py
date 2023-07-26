# https://core.telegram.org/bots/api#botcommand

import asyncio
import json
import logging
import os
import shutil
from socket import timeout
from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext
)
from Classes.DataManage import DataManage
from Helpers.MemoryManage import memoryManage
from Helpers.PathManage import PathManage
from mimetypes import guess_extension

from Models.DownloadStatus import DownloadStatus
from Models.TelegramFile import TelegramFile

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
settings = json.load(open("settings.json"))
externalMemory = settings['extMemory']
localApi = settings['localApi']

dataManage = DataManage()
destinationPathKey = 'destinationPath'
chatIdKey = 'chat_id'
jobStatusKey = 'jobStatus'
last_dir_message = 'message_dir_id'
SPECIFY, DOC, SETNAME = range(3)
downloadListKey = 'download_list'


async def dw_telegram(update: Update, context: CallbackContext):
    """For run selection path"""
    await update.message.reply_text(
        # 'send /path for select path download'
        #f'send:\n/ls for show dir in {await get_path(context)}\n/space for disks spaces\n/next for send file\nor send the next directory name (for create or move)'
        f'Send:\n/space for disks spaces\n/next for send file'
    )
    await ls_command(update, context)
    await start_job(update, context)
    context.user_data[downloadListKey] = False
    return SPECIFY


async def space(update: Update, context: CallbackContext):
    """Get disks space"""
    internalSpace = memoryManage('/')
    extMemory = memoryManage(externalMemory)
    await update.message.reply_text(f'Internal memory:\nTotal: {internalSpace.total}GB\nUsed: {internalSpace.used}GB\nFree: {internalSpace.free}GB')
    await update.message.reply_text(f'External memory:\nTotal: {extMemory.total}GB\nUsed: {extMemory.used}GB\nFree: {extMemory.free}GB')

async def space_on_doc(update: Update, context: CallbackContext):
    """Get disks space on video handler"""
    await space(update, context)
    return DOC


async def space_on_specify(update: Update, context: CallbackContext):
    """Get disks space on specify handler"""
    await space(update, context)
    return SPECIFY


async def dir_specify(update: Update, context: CallbackContext):
    """Reply dir to save"""
    if update.callback_query:
        await set_path(context, update.callback_query.data)
        # controllo per cancellare l'ultimo messaggio
        if last_dir_message in context.user_data:
            await context.bot.deleteMessage(message_id=context.user_data[last_dir_message],
                                      chat_id=update.callback_query.message.chat_id)
    else:
        # controllo per cancellare l'ultimo messaggio
        if last_dir_message in context.user_data:
            await context.bot.deleteMessage(message_id=context.user_data[last_dir_message],
                                            chat_id=update.message.chat_id)
        await set_path(context, update.message.text)

    message = f'{await get_path(context)}\n/next to download or\n'
    await ls_command(update, context, message)
    return SPECIFY


async def ls_command(update: Update, context: CallbackContext, message=""):
    """Show list of directory"""
    message = f'{message}select or send the next directory name (for create or move)'
    directories = PathManage.GetInlineAllDirectories(await get_path(context))
    if update.callback_query:
        dir_message = await update.callback_query.message.reply_text(message, reply_markup=InlineKeyboardMarkup(
                                    inline_keyboard=directories, resize_keyboard=True)
                                    )
    else:
        dir_message = await update.message.reply_text(message, reply_markup=InlineKeyboardMarkup(
                                    inline_keyboard=directories, resize_keyboard=True)
                                    )
    context.user_data[last_dir_message] = dir_message.message_id


async def ls_dir_command(update: Update, context: CallbackContext):
    """Show list of directory in command status"""
    await ls_command(update, context)

    return SPECIFY


async def next_command(update: Update, context: CallbackContext):
    """Run for await download file"""
    await update.message.reply_text(f'Await for file download in: {await get_path(context)}')
    await update.message.reply_text(f'The commands available in this section are:\n/prev for select directory\n/space for disks spaces\n/dwList for show list of file and download status\n/end for exit from dw_telegram\n/setName for change file name')
    return DOC


async def end_telegram_download(update: Update, context: CallbackContext):
    """For end conversation handler"""
    await update.message.reply_text('Handler closed')

    return ConversationHandler.END


async def append_download(update: Update, context: CallbackContext):
    """Add file to download list"""
    if update.message.audio:
        doc = update.message.audio
    elif update.message.document:
        doc = update.message.document
    # elif update.message.photo:
    #     doc = update.message.photo
    elif update.message.video:
        doc = update.message.video
    else:
        await update.message.reply_text("Type not accepted")
        return DOC

    dest = await get_path(context)
    file = TelegramFile(
        file=doc,
        forward_from=update.message.forward_from_chat,
        destinationPath=dest,
        chat=update.message.chat)
    await dataManage.update_file(file)

    return DOC


async def get_path(context: CallbackContext):
    """Get path from user data if exist or set default"""
    if destinationPathKey not in context.user_data:
        context.user_data[destinationPathKey] = externalMemory
    return context.user_data[destinationPathKey]


async def set_path(context: CallbackContext, newDir):
    """Set path in user data"""
    dest = await get_path(context)
    dest = PathManage.merge_path(dest, newDir)
    context.user_data[destinationPathKey] = dest
    PathManage.create_dir(dest)


async def downloader_async(data: TelegramFile, context: CallbackContext):
    """Downloader"""
    logger.info(f"Run downloader {data.file}")

    path = data.destinationPath
    PathManage.create_dir(path)
    try:
        data.status = DownloadStatus.DOWNLOADING
        await dataManage.update_file(data)
        dw = await context.bot.get_file(data.file.file_id)
        if not localApi:
            # Scarica localmente il file
            await dw.download(custom_path=data.get_full_destination_path())
        else:
            # Muove il file scaricato dall'API nella directory desiderata
            # 'http://192.168.0.18:8880/file/bot<bottoken>//home/pi/Documents/telegram-bot-api/build/<token>/videos/file_7.mp4'
            file_location = f'{dw.file_path}'.replace(
                f'{settings["base_file_url"]}{settings["botToken"]}/', '')
            shutil.move(file_location, data.get_full_destination_path())
    except Exception as e:
        logger.exception(e)
        data.status = DownloadStatus.ERROR
        await dataManage.update_file(data)
        raise e

    context.user_data[downloadListKey] = False
    data.status = DownloadStatus.DOWNLOADED
    await dataManage.update_file(data)

    logger.info(f"End downloader, file saved {data.get_full_destination_path()}")
    await context.bot.send_message(chat_id=data.chat.id, text=f'File \"{data.file.file_name}\" downloaded successfully!')


async def check_and_download(context):
    """Job scheduled"""
    tasks = []
    for d in await dataManage.get_workable_list():
        tasks.append(asyncio.create_task(downloader_async(d, context)))

    if len(tasks) > 0:
        await asyncio.gather(*tasks)


async def start_job(update: Update, context: CallbackContext):
    """Schedule a new job if not exist"""
    if jobStatusKey not in context.user_data:
        if len(context.job_queue.get_jobs_by_name(update.message.from_user.id)) == 0:
            # Schedulo il job ogni 3 minuti
            context.job_queue.run_repeating(
                check_and_download, 180, first=10, context=update.message.chat.id, name=str(update.message.from_user.id))
        context.user_data[jobStatusKey] = True


async def dw_list(update: Update, context: CallbackContext):
    """Send list of download and status"""
    await execute_dw_list_command(update, context)
    return DOC

async def execute_dw_list_command(update: Update, context: CallbackContext):
    download_list = await dataManage.get_view_download_list()
    items_length = 20
    if len(download_list) > 0:
        for items in zip(*(iter(download_list),) * items_length):
            await update.message.reply_text("\n".join(items))
        # controllo per stampa degli ultimi items
        item_module = len(download_list) % items_length
        if item_module != 0:
            await update.message.reply_text("\n".join(download_list[-item_module:]))
        await update.message.reply_text(f"{len(download_list)} items in download list")
        await update.message.reply_text("Send /setsNew for set all download status \"ERROR\" in \"NEW\"")
    else:
        await update.message.reply_text("Download list is empty")
    context.user_data[downloadListKey] = True

async def set_to_new(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await dataManage.set_all_to_new()
    await update.message.reply_text("Update executed!")
    return DOC

async def run_set_name(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await update.message.reply_text("Send the new name by first indicating the number belonging to the download list file and then specifying the new name, separating them by a pipe. 1|name")
    return SETNAME

async def set_name_to_file(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    if context.user_data[downloadListKey]:
        if '|' in update.message.text and len(update.message.text.split('|')) > 0:
            message = update.message.text.split('|')
            await dataManage.update_file_name(int(message[0]) - 1, message[1])
            await update.message.reply_text(f"Name {message[1]} setted. Submit another name to change or send the '/nameEnd' command to return to the download")
            context.user_data[downloadListKey] = False
        else:
            await update.message.reply_text("The number must be indicated first and then the name and separated by pipe (1|name) or send the '/nameEnd' command to return to the download.")
    else:
        await update.message.reply_text("Send first download list command '/dwList'")
    return SETNAME

async def end_set_name(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await next_command(update, context)
    return DOC

async def dw_list_set_name(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await execute_dw_list_command(update, context)
    return SETNAME
