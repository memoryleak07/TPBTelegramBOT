import pickle
import os
from Models.DownloadStatus import DownloadStatus
from Models.EnvKeysConsts import EnvKeysConsts
from Models.TelegramFile import TelegramFile


class DataManage:
    def __init__(self) -> None:
        self.file_name = os.getenv(EnvKeysConsts.TELEGRAM_DOWNLOAD_DATA_FILE_PATH)
        self.file_name = os.path.join(self.file_name, 'data.dict')
        self.Data = []
        self.load_data()

    def load_data(self) -> None:
        """Load self.Data from file on first run"""
        if os.path.exists(self.file_name):
            with open(self.file_name, 'rb') as f:
                self.Data = pickle.load(f)
            # Set to NEW status all file
            for d in self.Data:
                if d.status != DownloadStatus.NEW:
                    d.status = DownloadStatus.NEW
        self.write_data()

    def write_data(self) -> None:
        with open(self.file_name, 'wb') as f:
            pickle.dump(self.Data, f)

    async def update_file(self, file: TelegramFile):
        if file.status == DownloadStatus.NEW:
            self.Data.append(file)
        elif file.status == DownloadStatus.DOWNLOADED:
            self.Data.remove(file)
        elif file.status == DownloadStatus.ERROR:
            self.Data.remove(file)
            self.Data.append(file)
        else:
            return

        self.write_data()

    async def get_workable_list(self):
        forwarderList = {}
        workableList = []

        for d in self.Data:
            if d.forward_from and d.status != DownloadStatus.ERROR:
                if d.forward_from.id in forwarderList:
                    continue
                else:
                    forwarderList[d.forward_from.id] = False

            if d.status == DownloadStatus.NEW:
                workableList.append(d)

        return workableList
    
    async def update_file_name(self, index, file_name):
        self.Data[index].file_name_setted = file_name
        
        self.write_data()

    async def get_view_download_list(self):
        downloadList = []
        i = 0
        for d in self.Data:
            i += 1
            downloadList.append(f'[{i}]{d.get_file_name()}|{d.status}')

        return downloadList

    async def set_all_to_new(self):
        for f in self.Data:
            if f.status == DownloadStatus.ERROR:
                f.status = DownloadStatus.NEW

        self.write_data()
