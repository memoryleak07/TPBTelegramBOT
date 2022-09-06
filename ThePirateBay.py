from tpblite import TPB
from tpblite import CATEGORIES, ORDERS
from io import StringIO 
import sys
import logging
from telegram import InlineKeyboardButton,InlineKeyboardMarkup

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
#


class ThePirateBay:
    # To capture the print output
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
        # Create a TPB object with a domain name
        # t = TPB('https://tpb.party')

        # Or create a TPB object with default domain
        self.t = TPB()
        

    def GetAllCategories(self):
        ## To print all available categories, use the classmethod printOptions
        # with self.Capturing() as output:
        #     CATEGORIES.printOptions()
        # return output
        output = []
        for y in CATEGORIES.__dict__.keys():
            if not (y.startswith("__")):
                output.append(y)
        return output

    def GetInlineAllCategories(self):
        inline_button = []
        row_button = []
        i = 0
        categories = self.GetAllCategories()
        #reply = InlineKeyboardMarkup(inline_keyboard=inline_button)
        for row in categories:
            if i < 2:
                row_button.append(InlineKeyboardButton(text=row, callback_data=row))
                i += 1
            
            if (i >= 2) or (categories[-1] == row_button[-1]):
                inline_button.append(row_button)
                row_button = []
                i = 0
            
        return inline_button


    def GetSubCategories(self, macro:str):
        y:str
        output = []
        for y in (getattr(getattr(CATEGORIES, macro), "__dict__").keys()):
            if not (y.startswith("__")):
                output.append(y)
        return output



    # def GetSubCategories(self):
    #     pass
        ## Or just a subset of categories, like VIDEO
        #CATEGORIES.VIDEO.printOptions()
        # category = 200
        
        # with self.Capturing() as output:
        #     CATEGORIES.category.printOptions()
        # return output


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
        #self.torrents = self.t.search(keyword, page=page, order=ORDERS.NAME.DES, category=categories)        
        foundtorrents = []
        magnetlinks = []
        url = []
        i = 0

        self.torrents = self.t.search(
            keyword, page=page, order=ORDERS.NAME.DES, category=categories)
        if len(self.torrents) == 0:
            return foundtorrents, magnetlinks, url
        
        if page != 1:
            i = (page - 1) * 30

        for torrent in self.torrents:
            #print("[{i}]".format(i=i), torrent)
            line = "[{i}] - {torrent}".format(i=i, torrent=torrent)
            foundtorrents.append(line)
            magnetlinks.append(torrent.magnetlink)
            url.append(torrent.url)
            i = i+1
        
        return foundtorrents, magnetlinks, url


    def FilterTorrent(self):
        # Get the most seeded torrent based on a filter
        self.torrent = self.torrents.getBestTorrent(
        min_seeds=30, min_filesize='500 MiB', max_filesize='20 GiB')


    def SelectTorrent(self, num: int):
        # Or select a particular torrent by indexing
        torrent = self.torrents[num]
