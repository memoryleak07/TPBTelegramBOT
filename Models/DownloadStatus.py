from enum import Enum

class DownloadStatus(Enum):
    NEW = 0
    DOWNLOADING = 1
    DOWNLOADED = 2
    ERROR = 99
