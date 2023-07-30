from mimetypes import guess_extension
import os
from Models.DownloadStatus import DownloadStatus


class TelegramFile:

    def __init__(self, file=None, status=DownloadStatus.NEW, forward_from=None, destinationPath=None, chat=None, fileNamedSetted = ''):
        self.file = file
        self.status = status
        self.forward_from = forward_from
        self.destinationPath = destinationPath
        self.chat = chat
        self.fileNameSetted = fileNamedSetted

    def set_file_name(self, file_name):
        self.fileNameSetted = file_name

    def get_full_destination_path(self):
        destination = self.get_file_name()
        extension = None
        if self.file.file_name:
            file_mame, extension = os.path.splitext(self.file.file_name)

        if self.file.mime_type and not extension:
            extension = guess_extension(self.file.mime_type)
        destination += extension
        return os.path.join(self.destinationPath, destination)
    
    def get_file_name(self):
        file_name = ''
        if self.fileNameSetted == '':
            if self.file.file_name:
                file_mame_not_extension, extension = os.path.splitext(self.file.file_name)
                file_name += file_mame_not_extension
            else:
                file_name += self.file.file_unique_id
        else:
            file_name += self.fileNameSetted
        return file_name
