# ## Specifing save path for downloads:
# self.qb.download_from_link(magnet_link, savepath="path")

# # Applying labels to downloads:
# self.qb.download_from_link(magnet_link, category='anime')

from qbittorrent import Client

CLIENT = 'http://127.0.0.1:8080/'
USER = "admin"
PASSWORD = "adminadmin"


class QBitTorrent:

    def __init__(self) -> None:
        self.qb = Client(CLIENT)
        self.qb.login(USER, PASSWORD)
        # not required when 'Bypass from localhost' setting is active.
        # defaults to admin:admin.

    def PauseAll(self):
        """Pause all torrent."""
        self.qb.pause_all()

    def ResumeAll(self):
        """Resume all torrent."""
        self.qb.resume_all()

    def ForceAll(self):
        """Resume all torrent."""
        self.qb.force_start(infohash_list="all", value=True)

    def FilterTorrent(self, key):
        """This will return all torrents which are currently downloading and are labeled as ``my category``."""
        return self.qb.torrents(filter=key, sort="progress")

    def DownloadTorrentFromLink(self, link_list: list):
        """"No matter the link is correct or not, method will always return empty JSON object."""
        self.qb.download_from_link(link_list)

    def ReplyUserLocalsTorrentInformation(self, key):
        """Return a list of local torrent"""

        def get_size_format(b, factor=1024, suffix="B"):
            """e.g: 1253656 => '1.20MB'- 1253656678 => '1.17GB'"""
            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                if b < factor:
                    return f"{b:.2f}{unit}{suffix}"
                b /= factor
            return f"{b:.2f}Y{suffix}"

        def format_line_to_print(t, s, fs, ds, p):
            """ Return string formatted for reply message to user"""
            return "[{t} \nSeeds: {s} - FileSize: {fs}\nDownload speed: {ds}/s\nProgress: {p}%".format(t=t, s=s, fs=fs, ds=ds, p=p)

        localdownloads = []
        for torrent in self.FilterTorrent(key):
            line = format_line_to_print(
                torrent["name"],
                torrent["num_seeds"],
                get_size_format(torrent["total_size"]),
                get_size_format(torrent["dlspeed"]),
                str(round((torrent["progress"] * 100), 2))
            )
            localdownloads.append(line)

        return localdownloads

# qb = QBitTorrent()
