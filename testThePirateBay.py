from tpblite import TPB
from tpblite import CATEGORIES, ORDERS


class ThePirateBay:

    def __init__(self) -> None:
        # Create a TPB object with a domain name
        # t = TPB('https://tpb.party')

        # Or create a TPB object with default domain
        self.t = TPB()


    def PrintCategories(self):
        ## To print all available categories, use the classmethod printOptions
        #CATEGORIES.printOptions()
        return CATEGORIES.printOptions()

        ## Or just a subset of categories, like VIDEO
        #CATEGORIES.VIDEO.printOptions()
        ## Similarly for the sort order
        # ORDERS.printOptions()

    def PrintResults(self):
        ## See how many torrents were found
        print('There were {0} torrents found.'.format(len(self.torrents)))
        # Iterate through list of torrents and print info for Torrent object
        i = 0
        foundtorrent = []
        for torrent in self.torrents:
            print("[{i}]".format(i=i), torrent)
            foundtorrent.append(torrent)
            i = i +1
        return foundtorrent

    def QuickSearch(self, keyword:str):
        ## Quick search for torrents, returns a Torrents object
        self.torrents = self.t.search(keyword)
        self.PrintResults()


    def CustomizedSearch(self, keyword:str, categories:int):
        print("keyword is", keyword)
        ## Customize your search
        #self.torrents = self.t.search('flac pink floyd 24bit', page=0, order=ORDERS.NAME.DES, category=CATEGORIES.AUDIO.FLAC)
        self.torrents = self.t.search(keyword, page=0, order=ORDERS.NAME.DES, category=categories)
        ## See how many torrents were found
        print('There were {0} torrents found.'.format(len(self.torrents)))
        # Iterate through list of torrents and print info for Torrent object
        i = 0
        foundtorrents = []
        magnetlinks = []
        for torrent in self.torrents:
            print("[{i}]".format(i=i), torrent)
            line ="[{i}] - {torrent}".format(i=i, torrent=torrent) 
            foundtorrents.append(line)
            magnetlinks.append(torrent.magnetlink)
            i = i+1
        return foundtorrents, magnetlinks


    def FilterTorrent(self):
        # Get the most seeded torrent based on a filter
        torrent = self.torrents.getBestTorrent(min_seeds=30, min_filesize='500 MiB', max_filesize='20 GiB')


    def SelectTorrent(self, num:int):
        # Or select a particular torrent by indexing
        torrent = self.torrents[num]
    


    # # Get the magnet link for a torrent
    # print(torrent.magnetlink)

    # Get the url link for a torrent
    # print(torrent.url)


