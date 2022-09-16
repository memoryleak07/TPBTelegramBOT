from qbittorrent import Client

CLIENT = 'http://127.0.0.1:8080'
USER = "admin"
PASSWORD = "adminadmin"

class QBitTorrent:

    def __init__(self) -> None:
        self.qb = Client(CLIENT)
        self.qb.login(USER, PASSWORD)
        # not required when 'Bypass from localhost' setting is active.
        # defaults to admin:admin.
        # to use defaults, just do qb.login()
        self.torrents = self.qb.torrents()

    def PauseAll(self):
        self.qb.pause_all()

    def ResumeAll(self):
        self.qb.resume_all()

    def FilterTorrent(self):
        # This will return all torrents which are currently downloading and are labeled as ``my category``.
        self.qb.torrents(filter='downloading', category='my category')
        # self.torrents(filter='paused', sort='ratio')

    def DownloadTorrentFromLink(self, link_list:list):
        self.qb.download_from_link(link_list)
        # No matter the link is correct or not, method will always return empty JSON object.


    def GetLocalsTorrentInformation(self):

        def get_size_format(b, factor=1024, suffix="B"):
            """
            Scale bytes to its proper byte format
            e.g:
                1253656 => '1.20MB'
                1253656678 => '1.17GB'
            """
            for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
                if b < factor:
                    return f"{b:.2f}{unit}{suffix}"
                b /= factor
            return f"{b:.2f}Y{suffix}"

        localdownloads = []
        for torrent in self.torrents:
            line = "{t} \nSeeds: {s} - FileSize: {fs}\nDownload speed: {ds}\nProgress: {p}".format(
                t = torrent["name"],
                s = torrent["num_seeds"],
                fs = get_size_format(torrent["total_size"]),
                ds = get_size_format(torrent["dlspeed"]) + "/s",
                p = str(round((torrent["progress"] *  100), 2)) + "%"
            )
            localdownloads.append(line)

        return localdownloads




