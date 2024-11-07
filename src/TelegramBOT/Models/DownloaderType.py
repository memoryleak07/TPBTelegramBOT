from enum import Enum
import re

class DownloaderType(Enum):
    TELEGRAM = 0
    MEGA = 1

    def get_downloader_type_by_value(value):
        valid_urls = [
            "telegram",
            "https://mega.nz"
        ]
        try:
            url_pattern = r'https?://(?:www\.)?([a-zA-Z0-9-]+\.[a-zA-Z]{2,})'
            match = re.search(url_pattern, value)
            
            if match:
                found_url = match.group()
                # Cerchiamo se l'URL trovato è nella lista di URL validi
                for index, url in enumerate(valid_urls):
                    if found_url == url:
                        return DownloaderType(index)
            return None
        except ValueError:
            return None  
