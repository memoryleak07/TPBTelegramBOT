from mimetypes import guess_extension
import os
from Models.DownloadStatus import DownloadStatus
from Models.DownloaderType import DownloaderType
import re



class TelegramFile:

    def __init__(self, file=None, status=DownloadStatus.NEW, forward_from=None, destinationPath=None, chat=None, caption_message = '', fileNamedSetted = '', downloader_type=DownloaderType.TELEGRAM):
        self.file = file
        self.status = status
        self.forward_from = forward_from
        self.destination_path = destinationPath
        self.chat = chat
        self.cation_message = self.__get__caption_message__(caption_message)
        self.file_name_setted = fileNamedSetted
        self.downloader_type = downloader_type

    def __get__caption_message__(self, caption_message):
        if caption_message != None:
            caption_message = re.sub(r'[^\w\s-]', '', caption_message)
        else:
            caption_message = ''
        
        return caption_message

    def set_file_name(self, file_name):
        self.file_name_setted = file_name

    def get_full_destination_path(self):
        destination = self.get_file_name()
        extension = ''
        if self.file.file_name:
            file_mame, extension = os.path.splitext(self.file.file_name)

        if self.file.mime_type and not extension:
            extension = guess_extension(self.file.mime_type)
        destination += extension
        return os.path.join(self.destination_path, destination)
    
    def get_file_name(self):
        file_name = ''
        if self.file_name_setted == '':
            if self.file.file_name:
                file_mame_not_extension, extension = os.path.splitext(self.file.file_name)
                file_name += file_mame_not_extension
            elif self.cation_message != '':
                file_name += self.cation_message
            else:
                file_name += self.file.file_unique_id
        else:
            file_name += self.file_name_setted
        return file_name
