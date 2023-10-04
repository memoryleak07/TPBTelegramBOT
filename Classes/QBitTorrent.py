# ## Specifing save path for downloads:
# self.qb.download_from_link(magnet_link, savepath="path")

# # Applying labels to downloads:
# self.qb.download_from_link(magnet_link, category='anime')

# Raspberry installation: https://pimylifeup.com/raspberry-pi-qbittorrent/
import logging
from qbittorrent import Client

CLIENT = 'http://127.0.0.1:8980/'
USER = "admin"
PASSWORD = "adminadmin"

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


class QBitTorrent:

    def __init__(self) -> None:
        self.qb = Client(CLIENT)
        self.qb.login(USER, PASSWORD)
        # not required when 'Bypass from localhost' setting is active.
        # defaults to admin:admin.

    def PauseAll(self, id):
        """Pause all torrent."""
        logger.info("Chat %s PauseAll torrent", id)
        self.qb.pause_all()

    def ResumeAll(self, id):
        """Resume all torrent."""
        logger.info("Chat %s ResumeAll torrent", id)
        self.qb.resume_all()

    def ForceAll(self, id):
        """Force all torrent."""
        logger.info("Chat %s ForceAll torrent", id)
        self.qb.force_start(infohash_list="all", value=True)

    def FilterTorrent(self, key):
        """This will return all torrents which are currently downloading and are labeled as ``my category``."""
        return self.qb.torrents(filter=key, sort="progress")

    def DownloadTorrentFromLink(self, id, link_list:list):
        """"No matter the link is correct or not, method will always return empty JSON object."""
        logger.info("Chat %s DownloadTorrentFromLink", id)
        self.qb.download_from_link(link_list)

    def ReplyUserLocalsTorrentInformation(self, id, key):
        """Return a list of local torrent"""        
        def get_size_format(b, factor=1024, suffix="B"):
            """e.g: 1253656 => '1.20MB'- 1253656678 => '1.17GB'"""
            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                if b < factor:
                    return f"{b:.2f}{unit}{suffix}"
                b /= factor
            return f"{b:.2f}Y{suffix}"

        def format_line_to_print(t, s, fs, ds, st, p):
            """ Return string formatted for reply message to user"""
            return "[{t} \n*Seeds: {s} - FileSize: {fs}\n*Download speed: {ds}/s\n*State: {st}\n*Progress: {p}%".format(t=t, s=s, fs=fs, ds=ds, st=st, p=p)

        localdownloads = []
        for torrent in self.FilterTorrent(key):
            line = format_line_to_print(
                torrent["name"],
                torrent["num_seeds"],
                get_size_format(torrent["total_size"]),
                get_size_format(torrent["dlspeed"]),
                torrent["state"],
                str(round((torrent["progress"] * 100), 2))
            )
            localdownloads.append(line)

        return localdownloads

# qb = QBitTorrent()
