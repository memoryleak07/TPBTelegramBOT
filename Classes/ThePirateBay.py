from tpblite import TPB
from tpblite import CATEGORIES, ORDERS
import logging
from telegram import InlineKeyboardButton

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
#

class ThePirateBay:

    def __init__(self) -> None:
        # Create a TPB object with a domain name: t = TPB('https://tpb.party')
        # Or create a TPB object with default domain
        self.t = TPB()
        

    def GetAllCategories(self):
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
        for row in categories:
            if i < 2:
                row_button.append(InlineKeyboardButton(text=row, callback_data=row))
                i += 1
            
            if (i >= 2) or (categories[-1] == row_button[-1].text):
                inline_button.append(row_button)
                row_button = []
                i = 0
            
        return inline_button


    def GetSubCategories(self, macro:str):
        y:str
        output = []
        categories = (getattr(CATEGORIES, macro)).__dict__.keys()
        for y in categories:
            if not (y.startswith("__")):
                output.append(y)

        return output


    def GetInlineSubCategories(self, macro:str):
        inline_button = []
        row_button = []
        i = 0
        categories = self.GetSubCategories(macro)
        #reply = InlineKeyboardMarkup(inline_keyboard=inline_button)
        if len(categories) == "":
            return 

        for row in categories:
            if i < 3:
                row_button.append(InlineKeyboardButton(text=row, callback_data=row))
                i += 1
            
            if (i >= 3) or (categories[-1] == row_button[-1].text):
                inline_button.append(row_button)
                row_button = []
                i = 0
            
        return inline_button


    def CustomizedSearch(self, keyword:str, page:int, categories:str, subcategories:str):
        ## Customize your search
        #self.torrents = self.t.search(keyword, page=page, order=ORDERS.NAME.DES, category=categories)        
        foundtorrents = []
        magnetlinks = []
        url = []
        i = 0

        # Retrieve the category (int)
        if (categories == "") & (subcategories == ""):
            cat = 0
            
        elif (categories == "ALL") & (subcategories == ""):
            cat = getattr(CATEGORIES, "ALL")

        elif (categories != "") & (subcategories == ""):
            cat = getattr(getattr(CATEGORIES, categories), "ALL")   

        elif (categories != "") & (subcategories != ""):
            cat = getattr(getattr(CATEGORIES, categories), subcategories)
        
        # Search:
        self.torrents = self.t.search(keyword, page=page, order=ORDERS.NAME.DES, category=cat)

        if len(self.torrents) == 0:
            return foundtorrents, magnetlinks, url
        
        # Var i is the index for user to allow select wich to download
        if page != 1:
            i = (page - 1) * 30

        for torrent in self.torrents:
            #print("[{i}]".format(i=i), torrent)
            line = "[#{i}] - {torrent}".format(i=i, torrent=torrent)
            foundtorrents.append(line)
            magnetlinks.append(torrent.magnetlink)
            url.append(torrent.url)
            i = i+1
        
        return foundtorrents, magnetlinks, url
