# https://core.telegram.org/bots/api#botcommand

import asyncio
import logging
import os
import shutil
from socket import timeout
from telegram import InlineKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    CallbackContext
)
from Classes.DataManage import DataManage
from Helpers.MemoryManage import memoryManage
from Helpers.Converters import Converters
from Helpers.PathManage import PathManage
from Models.DownloadStatus import DownloadStatus
from Models.EnvKeysConsts import EnvKeysConsts
from Models.TelegramFile import TelegramFile

# Get logger
logger = logging.getLogger(__name__)
destination_path = os.getenv(EnvKeysConsts.DESTINATION_PATH)
is_local_api = Converters.string_to_bool(os.getenv(EnvKeysConsts.IS_LOCAL_API, EnvKeysConsts.IS_LOCAL_API_DEFAULT_VALUE))
bot_token = os.getenv(EnvKeysConsts.BOT_TOKEN)
base_file_url = os.getenv(EnvKeysConsts.BASE_FILE_URL, EnvKeysConsts.BASE_FILE_URL_DEFAULT_VALUE)
get_internal_usage = Converters.string_to_bool(os.getenv(EnvKeysConsts.GET_INTERNAL_USAGE, EnvKeysConsts.GET_INTERNAL_USAGE_DEFALUT_VALUE))
telegram_download_data_file_path = os.getenv(EnvKeysConsts.TELEGRAM_DOWNLOAD_DATA_FILE_PATH)

if not os.path.exists(telegram_download_data_file_path):
    raise Exception(f"The data file path '{telegram_download_data_file_path}' not exist")

if not os.path.exists(destination_path):
    raise Exception(f"The destination path '{destination_path}' not exist")

data_manage = DataManage()
destination_path_key = 'destination_path'
chatIdKey = 'chat_id'
job_status_key = 'job_status'
last_dir_message = 'message_dir_id'
SPECIFY, DOC, SETNAME = range(3)
download_list_key = 'download_list'
parse_mode='Markdown'


async def dw_telegram(update: Update, context: CallbackContext):
    """For run selection path"""
    await update.message.reply_text(
"""
Send:
/space for disks spaces
/next for send file
""")
    await ls_command(update, context)
    await start_job(update, context)
    context.user_data[download_list_key] = False
    return SPECIFY

async def reply_memory_response(update: Update, response: memoryManage, prefix_message: str):
    if response.total == response.error_message:
        await update.message.reply_text(
            f'{prefix_message}: {response.error_message}',
            parse_mode=parse_mode)
    else:
        await update.message.reply_text(
f"""
{prefix_message}:
Total: `{response.total}GB`
Used: `{response.used}GB`
Free: `{response.free}GB`
""", parse_mode=parse_mode)

async def space(update: Update, context: CallbackContext):
    """Get disks space"""
    destination_space = memoryManage(destination_path)
    if get_internal_usage:
        internal_space = memoryManage('/')
        await reply_memory_response(update, internal_space, "Internal memory")
    await reply_memory_response(update, destination_space, "Destinsyion memory")

async def space_on_doc(update: Update, context: CallbackContext):
    """Get disks space on video handler"""
    await space(update, context)
    return DOC


async def space_on_specify(update: Update, context: CallbackContext):
    """Get disks space on specify handler"""
    await space(update, context)
    return SPECIFY

async def delete_old_message_and_update_path(update: Update, context: CallbackContext, update_path: bool):
    """Delete old message and update path"""
    try:
        if update.callback_query:
            if update_path:
                await set_path(context, update.callback_query.data)
            # controllo per cancellare l'ultimo messaggio su callback query
            if last_dir_message in context.user_data:
                await context.bot.deleteMessage(message_id=context.user_data[last_dir_message],
                                            chat_id=update.callback_query.message.chat_id)
        else:
            if update_path:
                await set_path(context, update.message.text)
            # controllo per cancellare l'ultimo messaggio
            if last_dir_message in context.user_data:
                await context.bot.deleteMessage(message_id=context.user_data[last_dir_message],
                                                chat_id=update.message.chat_id)
    except:
        return

async def dir_specify(update: Update, context: CallbackContext):
    """Reply dir to save"""
    await delete_old_message_and_update_path(update, context, True)

    message = f'{await get_path(context)}\n/next to download or\n'
    await ls_command(update, context, message)
    return SPECIFY


async def ls_command(update: Update, context: CallbackContext, message=""):
    """Show list of directory"""
    message = f'{message}select or send the next directory name (for create or move)'
    try:
        directories = PathManage.GetInlineAllDirectories(await get_path(context))
    except:
        #se la directory viene cancellata esternamente riesce a restituire le directory
        logger.info(f'{await get_path(context)} not found, change on context with {destination_path}')
        context.user_data[destination_path_key] = destination_path
        directories = PathManage.GetInlineAllDirectories(destination_path)

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
    await delete_old_message_and_update_path(update, context, False)
    await update.message.reply_text(f'Send file for download in path: `{await get_path(context)}`', parse_mode=parse_mode)
    await update.message.reply_text(
"""
The commands available in this section are:
/prev for select directory
/space for disks spaces
/dwList for show list of file and download status
/end for exit from dw_telegram
/setName for change file name
""")
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
    if not update.message.forward_from_chat:
        forwoard_from = update.message.forward_from
    else:
        forwoard_from = update.message.forward_from_chat
    file = TelegramFile(
        file=doc,
        forward_from=forwoard_from,
        destinationPath=dest,
        chat=update.message.chat,
        caption_message=update.message.caption)
    await data_manage.update_file(file)

    return DOC


async def get_path(context: CallbackContext):
    """Get path from user data if exist or set default"""
    if destination_path_key not in context.user_data:
        context.user_data[destination_path_key] = destination_path
    return context.user_data[destination_path_key]


async def set_path(context: CallbackContext, newDir):
    """Set path in user data"""
    dest = await get_path(context)
    dest = PathManage.merge_path(dest, newDir)
    context.user_data[destination_path_key] = dest
    PathManage.create_dir(dest)


async def downloader_async(data: TelegramFile, context: CallbackContext):
    """Downloader"""
    logger.info(f"Run downloader {data.file}")

    path = data.destinationPath
    PathManage.create_dir(path)
    logger.info(f"Path '{path}' created")
    try:
        data.status = DownloadStatus.DOWNLOADING
        await data_manage.update_file(data)
        dw = await context.bot.get_file(data.file.file_id)
        logger.info(f"API download of '{data.get_file_name()}' executed\nSaved at '{dw.file_path}'")
        if not is_local_api:
            # Scarica localmente il file
            await dw.download(custom_path=data.get_full_destination_path())
        else:
            # Muove il file scaricato dall'API nella directory desiderata
            # 'http://192.168.0.18:8880/file/bot<bottoken>//home/pi/Documents/telegram-bot-api/build/<token>/videos/file_7.mp4'
            file_location = f'{dw.file_path}'.replace(
                f'{base_file_url}{bot_token}/', '')
            logger.info(f"file_location: {file_location}")
            logger.info(f"full destination path: {data.get_full_destination_path()}")
            destination_path = data.get_full_destination_path()
            shutil.move(file_location, destination_path)
    except Exception as e:
        logger.exception(e)
        data.status = DownloadStatus.ERROR
        await data_manage.update_file(data)
        raise e
    
    data.status = DownloadStatus.DOWNLOADED
    await data_manage.update_file(data)

    logger.info(f"End downloader, file saved {data.get_full_destination_path()}")
    await context.bot.send_message(chat_id=data.chat.id, text=f'File \"{data.get_file_name()}\" downloaded successfully!')


async def check_and_download(context):
    """Job scheduled"""
    tasks = []
    for d in await data_manage.get_workable_list():
        tasks.append(asyncio.create_task(downloader_async(d, context)))

    if len(tasks) > 0:
        await asyncio.gather(*tasks)


async def start_job(update: Update, context: CallbackContext):
    """Schedule a new job if not exist"""
    if job_status_key not in context.user_data:
        if len(context.job_queue.get_jobs_by_name(update.message.from_user.id)) == 0:
            # Schedulo il job ogni 3 minuti
            context.job_queue.run_repeating(
                check_and_download, 180, first=10, context=update.message.chat.id, name=str(update.message.from_user.id))
        context.user_data[job_status_key] = True


async def dw_list(update: Update, context: CallbackContext):
    """Send list of download and status"""
    await execute_dw_list_command(update, context)
    return DOC

async def execute_dw_list_command(update: Update, context: CallbackContext):
    download_list = await data_manage.get_view_download_list()
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
    context.user_data[download_list_key] = True

async def set_to_new(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await data_manage.set_all_to_new()
    await update.message.reply_text("Update executed!")
    return DOC

async def run_set_name(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    await update.message.reply_text("Send the new name by first indicating the number belonging to the download list file and then specifying the new name, separating them by a pipe. 1|name")
    return SETNAME

async def set_name_to_file(update: Update, context: CallbackContext):
    """Set to new all file in error state"""
    if context.user_data[download_list_key]:
        if '|' in update.message.text and len(update.message.text.split('|')) > 0:
            message = update.message.text.split('|')
            await data_manage.update_file_name(int(message[0]) - 1, message[1])
            await update.message.reply_text(f"Name {message[1]} setted. Submit another name to change or send the '/nameEnd' command to return to the download")
            context.user_data[download_list_key] = False
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
