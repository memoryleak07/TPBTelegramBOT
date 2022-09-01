from tpblite import TPB
from tpblite import CATEGORIES, ORDERS
from io import StringIO 
import sys


class ThePirateBay:

    class Capturing(list):

        def __enter__(self):
            self._stdout = sys.stdout
            sys.stdout = self._stringio = StringIO()
            return self
        def __exit__(self, *args):
            self.extend(self._stringio.getvalue().splitlines())
            del self._stringio    # free up some memory
            sys.stdout = self._stdout


    def __init__(self) -> None:
        self.capture = ThePirateBay.Capturing()
        # Create a TPB object with a domain name
        # t = TPB('https://tpb.party')

        # Or create a TPB object with default domain
        self.t = TPB()
        


    def GetCategories(self):
        ## To print all available categories, use the classmethod printOptions
        # with self.Capturing() as output:
        CATEGORIES.printOptions()

    def GetCategories1(self):
        ## To print all available categories, use the classmethod printOptions
        with self.Capturing() as output:
            CATEGORIES.printOptions()
        return output


    def GetSubCategories(self, category):
        ## Or just a subset of categories, like VIDEO
        #CATEGORIES.VIDEO.printOptions()
        pass

    def PrintResults(self):
        ## See how many torrents were found
        #print('There were {0} torrents found.'.format(len(self.torrents)))
        # Iterate through list of torrents and print info for Torrent object
        i = 0
        foundtorrent = []
        for torrent in self.torrents:
            print("[{i}]".format(i=i), torrent)
            foundtorrent.append(torrent)
            i = i + 1
        return foundtorrent


    def QuickSearch(self, keyword:str):
        ## Quick search for torrents, returns a Torrents object
        self.torrents = self.t.search(keyword)
        self.PrintResults()


    def CustomizedSearch(self, keyword:str, page:int, categories:int):
        ## Customize your search
        # Iterate through list of torrents and print info for Torrent object
        #self.torrents = self.t.search(keyword, page=page, order=ORDERS.NAME.DES, category=categories)
        ## See how many torrents were found
        #print('There were {0} torrents found.'.format(len(self.torrents)))
        
        foundtorrents = []
        magnetlinks = []
        url = []
        i = 0

        self.torrents = self.t.search(
            keyword, page=page, order=ORDERS.NAME.DES, category=categories)
        if len(self.torrents) == 0:
            return foundtorrents, magnetlinks, url
        
        for torrent in self.torrents:
            #print("[{i}]".format(i=i), torrent)
            line = "[{i}] - {torrent}".format(i=i, torrent=torrent)
            foundtorrents.append(line)
            magnetlinks.append(torrent.magnetlink)
            url.append(torrent.url)
            i = i+1            
        
        # while True:
        #     self.torrents = self.t.search(keyword, page=page, order=ORDERS.NAME.DES, category=categories)
        #     if len(self.torrents) == 0:
        #         break
        #     for torrent in self.torrents:
        #         #print("[{i}]".format(i=i), torrent)
        #         line = "[{i}] - {torrent}".format(i=i, torrent=torrent)
        #         foundtorrents.append(line)
        #         magnetlinks.append(torrent.magnetlink)
        #         url.append(torrent.url)
        #         i = i+1
        #     page = page + 1

        return foundtorrents, magnetlinks, url

    # def CustomizedSearch(self, keyword: str, categories: int):
    #     ## Customize your search
    #     # Iterate through list of torrents and print info for Torrent object
    #     self.torrents = self.t.search(keyword, page=0, order=ORDERS.NAME.DES, category=categories)
    #     ## See how many torrents were found
    #     #print('There were {0} torrents found.'.format(len(self.torrents)))
    #     i = 0
    #     foundtorrents = []
    #     magnetlinks = []
    #     url = []
    #     for torrent in self.torrents:
    #         #print("[{i}]".format(i=i), torrent)
    #         line = "[{i}] - {torrent}".format(i=i, torrent=torrent)
    #         foundtorrents.append(line)
    #         magnetlinks.append(torrent.magnetlink)
    #         url.append(torrent.url)
    #         i = i+1
    #     return foundtorrents, magnetlinks, url


    def FilterTorrent(self):
        # Get the most seeded torrent based on a filter
        self.torrent = self.torrents.getBestTorrent(
        min_seeds=30, min_filesize='500 MiB', max_filesize='20 GiB')


    def SelectTorrent(self, num: int):
        # Or select a particular torrent by indexing
        torrent = self.torrents[num]



    # # Get the magnet link for a torrent
    # print(torrent.magnetlink)

    # Get the url link for a torrent
    # print(torrent.url)

