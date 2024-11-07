from Models.TelegramFile import TelegramFile
from mega import Mega

async def download_mega_file(data: TelegramFile):
    mega = Mega().login()

    # verbose information
    #mega = Mega({'verbose': True}).login()

    mega.download_url(data.file, data.destination_path)

    