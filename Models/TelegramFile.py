from mimetypes import guess_extension
import os
from Models.DownloadStatus import DownloadStatus


class TelegramFile:

    def __init__(self, file=None, status=DownloadStatus.NEW, forward_from=None, destinationPath=None, chat=None):
        self.file = file
        self.status = status
        self.forward_from = forward_from
        self.destinationPath = destinationPath
        self.chat = chat
        self.full_destination_path = self.__get_full_destination_path__()

    def __get_full_destination_path__(self):
        destination = ''
        extension = None
        if self.file.file_name:
            destination += self.file.file_name
            file_mame, extension = os.path.splitext(self.file.file_name)
        else:
            destination += self.file.file_unique_id

        if self.file.mime_type and not extension:
            destination += guess_extension(self.file.mime_type)

        return os.path.join(self.destinationPath, destination)
