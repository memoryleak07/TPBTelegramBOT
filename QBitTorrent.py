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
        # to use defaults, just do qb.login()

        self.torrents = self.qb.torrents()

        for torrent in self.torrents:
            print(torrent['name'])


    def PauseAll(self):
        self.qb.pause_all()

    def ResumeAll(self):
        self.qb.resume_all()
        

    def FilterTorrent(self):
        self.qb.torrents(filter='downloading', category='my category')
        # This will return all torrents which are currently
        # downloading and are labeled as ``my category``.

        # self.torrents(filter='paused', sort='ratio')
        # This will return all paused torrents sorted by their Leech:Seed ratio.


    def DownloadTorrentLink(self, magnet_link):
        # magnet_link = "magnet:?xt=urn:btih:e334ab9ddd91c10938a7....."
        self.qb.download_from_link(magnet_link)
        # No matter the link is correct or not,
        # method will always return empty JSON object.

        #Download multipe torrents by list of links:
        link_list = ["link1", "link2", "link3"]
        self.qb.download_from_link(link_list)

        ## Specifing save path for downloads:
        self.qb.download_from_link(magnet_link, savepath="path")

        # Applying labels to downloads:
        self.qb.download_from_link(magnet_link, category='anime')

    

qbit = QBitTorrent()

qbit.FilterTorrent()